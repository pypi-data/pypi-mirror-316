import argparse
import sys
from typing import Optional
from rich.panel import Panel
from rich.markdown import Markdown
from rich.console import Console
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from ra_aid.env import validate_environment
from ra_aid.tools.memory import _global_memory, get_related_files, get_memory_value
from ra_aid import print_agent_output, print_stage_header, print_task_header, print_error
from ra_aid.prompts import (
    RESEARCH_PROMPT,
    PLANNING_PROMPT,
    IMPLEMENTATION_PROMPT,
    EXPERT_PROMPT_SECTION_RESEARCH,
    EXPERT_PROMPT_SECTION_PLANNING,
    EXPERT_PROMPT_SECTION_IMPLEMENTATION,
    HUMAN_PROMPT_SECTION_RESEARCH,
    HUMAN_PROMPT_SECTION_PLANNING,
    HUMAN_PROMPT_SECTION_IMPLEMENTATION
)
import time
from anthropic import APIError, APITimeoutError, RateLimitError, InternalServerError
from ra_aid.llm import initialize_llm

from ra_aid.tool_configs import (
    get_read_only_tools,
    get_research_tools,
    get_planning_tools,
    get_implementation_tools
)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='RA.Aid - AI Agent for executing programming and research tasks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    ra-aid -m "Add error handling to the database module"
    ra-aid -m "Explain the authentication flow" --research-only
        '''
    )
    parser.add_argument(
        '-m', '--message',
        type=str,
        help='The task or query to be executed by the agent'
    )
    parser.add_argument(
        '--research-only',
        action='store_true',
        help='Only perform research without implementation'
    )
    parser.add_argument(
        '--provider',
        type=str,
        default='anthropic',
        choices=['anthropic', 'openai', 'openrouter', 'openai-compatible'],
        help='The LLM provider to use'
    )
    parser.add_argument(
        '--model',
        type=str,
        help='The model name to use (required for non-Anthropic providers)'
    )
    parser.add_argument(
        '--cowboy-mode',
        action='store_true',
        help='Skip interactive approval for shell commands'
    )
    parser.add_argument(
        '--expert-provider',
        type=str,
        default='openai',
        choices=['anthropic', 'openai', 'openrouter', 'openai-compatible'],
        help='The LLM provider to use for expert knowledge queries (default: openai)'
    )
    parser.add_argument(
        '--expert-model',
        type=str,
        help='The model name to use for expert knowledge queries (required for non-OpenAI providers)'
    )
    parser.add_argument(
        '--hil', '-H',
        action='store_true',
        help='Enable human-in-the-loop mode, where the agent can prompt the user for additional information.'
    )
    
    args = parser.parse_args()
    
    # Set default model for Anthropic, require model for other providers
    if args.provider == 'anthropic':
        if not args.model:
            args.model = 'claude-3-5-sonnet-20241022'
    elif not args.model:
        parser.error(f"--model is required when using provider '{args.provider}'")
    
    # Validate expert model requirement
    if args.expert_provider != 'openai' and not args.expert_model:
        parser.error(f"--expert-model is required when using expert provider '{args.expert_provider}'")
    
    return args

# Create console instance
console = Console()

# Create individual memory objects for each agent
research_memory = MemorySaver()
planning_memory = MemorySaver()
implementation_memory = MemorySaver()


def is_informational_query() -> bool:
    """Determine if the current query is informational based on implementation_requested state."""
    return _global_memory.get('config', {}).get('research_only', False) or not is_stage_requested('implementation')

def is_stage_requested(stage: str) -> bool:
    """Check if a stage has been requested to proceed."""
    if stage == 'implementation':
        return _global_memory.get('implementation_requested', False)
    return False

def run_agent_with_retry(agent, prompt: str, config: dict) -> Optional[str]:
    """Run an agent with retry logic for internal server errors and task completion handling.
    
    Args:
        agent: The agent to run
        prompt: The prompt to send to the agent
        config: Configuration dictionary for the agent
        
    Returns:
        Optional[str]: The completion message if task was completed, None otherwise
        
    Handles API errors with exponential backoff retry logic and checks for task
    completion after each chunk of output.
    """
    max_retries = 20
    base_delay = 1  # Initial delay in seconds
    
    for attempt in range(max_retries):
        try:
            for chunk in agent.stream(
                {"messages": [HumanMessage(content=prompt)]},
                config
            ):
                print_agent_output(chunk)
                
                # Check for task completion after each chunk
                if _global_memory.get('task_completed'):
                    completion_msg = _global_memory.get('completion_message', 'Task was completed successfully.')
                    console.print(Panel(
                        Markdown(completion_msg),
                        title="✅ Task Completed",
                        style="green"
                    ))
                    return completion_msg
            break
        except (InternalServerError, APITimeoutError, RateLimitError, APIError) as e:
            if attempt == max_retries - 1:
                raise RuntimeError(f"Max retries ({max_retries}) exceeded. Last error: {str(e)}")
            
            delay = base_delay * (2 ** attempt)  # Exponential backoff
            error_type = e.__class__.__name__
            print_error(f"Encountered {error_type}: {str(e)}. Retrying in {delay} seconds... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(delay)
            continue

def run_implementation_stage(base_task, tasks, plan, related_files, model, expert_enabled: bool):
    """Run implementation stage with a distinct agent for each task."""
    if not is_stage_requested('implementation'):
        print_stage_header("Implementation Stage Skipped")
        return
        
    print_stage_header("Implementation Stage")
    
    # Get tasks directly from memory, maintaining order by ID
    task_list = [task for _, task in sorted(_global_memory['tasks'].items())]
    
    print_task_header(f"Found {len(task_list)} tasks to implement")
    
    for i, task in enumerate(task_list, 1):
        print_task_header(task)
        
        # Create a unique memory instance for this task
        task_memory = MemorySaver()
        
        # Create a fresh agent for each task
        task_agent = create_react_agent(model, get_implementation_tools(expert_enabled=expert_enabled), checkpointer=task_memory)
        
        # Construct task-specific prompt
        expert_section = EXPERT_PROMPT_SECTION_IMPLEMENTATION if expert_enabled else ""
        human_section = HUMAN_PROMPT_SECTION_IMPLEMENTATION if _global_memory.get('config', {}).get('hil', False) else ""
        task_prompt = (IMPLEMENTATION_PROMPT).format(
            plan=plan,
            key_facts=get_memory_value('key_facts'),
            key_snippets=get_memory_value('key_snippets'),
            task=task,
            related_files="\n".join(related_files),
            base_task=base_task,
            expert_section=expert_section,
            human_section=human_section
        )
        
        # Run agent for this task
        run_agent_with_retry(task_agent, task_prompt, {"configurable": {"thread_id": "abc123"}, "recursion_limit": 100})


def run_research_subtasks(base_task: str, config: dict, model, expert_enabled: bool):
    """Run research subtasks with separate agents."""
    subtasks = _global_memory.get('research_subtasks', [])
    if not subtasks:
        return
        
    print_stage_header("Research Subtasks")
    
    # Get tools for subtask agents (excluding request_research_subtask and implementation)
    research_only = _global_memory.get('config', {}).get('research_only', False)
    subtask_tools = [
        t for t in get_research_tools(research_only=research_only, expert_enabled=expert_enabled)
        if t.name not in ['request_research_subtask']
    ]
    
    for i, subtask in enumerate(subtasks, 1):
        print_task_header(f"Research Subtask {i}/{len(subtasks)}")
        
        # Create fresh memory and agent for each subtask
        subtask_memory = MemorySaver()
        subtask_agent = create_react_agent(
            model,
            subtask_tools,
            checkpointer=subtask_memory
        )
        
        # Run the subtask agent
        expert_section = EXPERT_PROMPT_SECTION_RESEARCH if expert_enabled else ""
        human_section = HUMAN_PROMPT_SECTION_RESEARCH if config.get('hil', False) else ""
        subtask_prompt = f"Base Task: {base_task}\nResearch Subtask: {subtask}\n\n{RESEARCH_PROMPT.format(
            base_task=base_task,
            research_only_note='',
            expert_section=expert_section,
            human_section=human_section
        )}"
        run_agent_with_retry(subtask_agent, subtask_prompt, config)



def main():
    """Main entry point for the ra-aid command line tool."""
    try:
        args = parse_arguments()
        expert_enabled, expert_missing = validate_environment(args)  # Will exit if main env vars missing
        
        if expert_missing:
            console.print(Panel(
                f"[yellow]Expert tools disabled due to missing configuration:[/yellow]\n" + 
                "\n".join(f"- {m}" for m in expert_missing) +
                "\nSet the required environment variables or args to enable expert mode.",
                title="Expert Tools Disabled",
                style="yellow"
            ))
        
        # Create the base model after validation
        model = initialize_llm(args.provider, args.model)

        # Validate message is provided
        if not args.message:
            print_error("--message is required")
            sys.exit(1)
            
        base_task = args.message
        config = {
            "configurable": {
                "thread_id": "abc123"
            },
            "recursion_limit": 100,
            "research_only": args.research_only,
            "cowboy_mode": args.cowboy_mode
        }
    
        # Store config in global memory for access by is_informational_query
        _global_memory['config'] = config
    
        # Store expert provider and model in config
        _global_memory['config']['expert_provider'] = args.expert_provider
        _global_memory['config']['expert_model'] = args.expert_model
        
        # Run research stage
        print_stage_header("Research Stage")
        
        # Create research agent
        research_agent = create_react_agent(
            model,
            get_research_tools(
                research_only=_global_memory.get('config', {}).get('research_only', False),
                expert_enabled=expert_enabled,
                human_interaction=args.hil
            ),
            checkpointer=research_memory
        )
    
        expert_section = EXPERT_PROMPT_SECTION_RESEARCH if expert_enabled else ""
        human_section = HUMAN_PROMPT_SECTION_RESEARCH if args.hil else ""
        research_prompt = RESEARCH_PROMPT.format(
            expert_section=expert_section,
            human_section=human_section,
            base_task=base_task,
            research_only_note='' if args.research_only else ' Only request implementation if the user explicitly asked for changes to be made.'
        )

        # Run research agent
        run_agent_with_retry(research_agent, research_prompt, config)
        
        # Run any research subtasks
        run_research_subtasks(base_task, config, model, expert_enabled=expert_enabled)
        
        # Proceed with planning and implementation if not an informational query
        if not is_informational_query():
            print_stage_header("Planning Stage")
            
            # Create planning agent
            planning_agent = create_react_agent(model, get_planning_tools(expert_enabled=expert_enabled), checkpointer=planning_memory)
            
            expert_section = EXPERT_PROMPT_SECTION_PLANNING if expert_enabled else ""
            human_section = HUMAN_PROMPT_SECTION_PLANNING if args.hil else ""
            planning_prompt = PLANNING_PROMPT.format(
                expert_section=expert_section,
                human_section=human_section,
                base_task=base_task,
                research_notes=get_memory_value('research_notes'),
                related_files="\n".join(get_related_files()),
                key_facts=get_memory_value('key_facts'),
                key_snippets=get_memory_value('key_snippets'),
                research_only_note='' if args.research_only else ' Only request implementation if the user explicitly asked for changes to be made.'
            )

            # Run planning agent
            run_agent_with_retry(planning_agent, planning_prompt, config)

            # Run implementation stage with task-specific agents
            run_implementation_stage(
                base_task,
                get_memory_value('tasks'),
                get_memory_value('plan'),
                get_related_files(),
                model,
                expert_enabled=expert_enabled
            )

    except KeyboardInterrupt:
        console.print("\n[red]Operation cancelled by user[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()

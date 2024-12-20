from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.text import Text

from janito.agents import AIAgent, agent
from janito.workspace import workset
from janito.config import config
from janito.change.core import process_change_request
from janito.change.play import play_saved_changes
from janito.cli.history import save_to_history
from janito.qa import ask_question, display_answer
from janito.demo import DemoRunner
from janito.demo.data import get_demo_scenarios

console = Console()

def handle_ask(question: str):
    """Process a question about the codebase"""
    
    if config.tui:
        answer = ask_question(question)
        from janito.tui import TuiApp
        app = TuiApp(content=answer)
        app.run()
    else:
        answer = ask_question(question)
        display_answer(answer)

def handle_scan():
    """Preview files that would be analyzed"""
    workset.show()

def handle_play(filepath: Path):
    """Replay a saved changes or debug file"""
    play_saved_changes(filepath)

def is_dir_empty(path: Path) -> bool:
    """Check if directory is empty or only contains empty directories."""
    if not path.is_dir():
        return False

    for item in path.iterdir():
        if item.name.startswith(('.', '__pycache__')):
            continue
        if item.is_file():
            return False
        if item.is_dir() and not is_dir_empty(item):
            return False
    return True

def handle_request(request: str, preview_only: bool = False):
    """Process modification request"""
    is_empty = is_dir_empty(config.workspace_dir)
    if is_empty and not config.include:
        console.print("\n[bold blue]Empty directory - will create new files as needed[/bold blue]")

    success, history_file = process_change_request(request, preview_only)

    if success and history_file and config.verbose:
        try:
            rel_path = history_file.relative_to(config.workspace_dir)
            console.print(f"\nChanges saved to: ./{rel_path}")
        except ValueError:
            console.print(f"\nChanges saved to: {history_file}")
    elif not success:
        console.print("[red]Failed to process change request[/red]")

    # Save request and response to history
    if agent.last_response:
        save_to_history(request, agent.last_response)

def handle_demo():
    """Run demo scenarios"""
    runner = DemoRunner()

    # Add predefined scenarios
    for scenario in get_demo_scenarios():
        runner.add_scenario(scenario)

    # Preview and run scenarios
    console.print("\n[bold cyan]Demo Scenarios Preview:[/bold cyan]")
    runner.preview_changes()

    console.print("\n[bold cyan]Running Demo Scenarios:[/bold cyan]")
    runner.run_all()

    console.print("\n[green]Demo completed successfully![/green]")
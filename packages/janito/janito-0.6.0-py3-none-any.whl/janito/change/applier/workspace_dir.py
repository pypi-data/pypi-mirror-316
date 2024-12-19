from pathlib import Path
from typing import Set, List
import shutil
from rich.console import Console
from janito.config import config
from ..parser import FileChange, ChangeOperation

def verify_changes(changes: List[FileChange]) -> tuple[bool, str]:
    """Verify changes can be safely applied to workspace_dir.
    Returns (is_safe, error_message)."""
    for change in changes:
        source_path = config.workspace_dir / change.name
        
        if change.operation == ChangeOperation.CREATE_FILE:
            if source_path.exists():
                return False, f"Cannot create {change.name} - already exists"
                
        elif change.operation in (ChangeOperation.MOVE_FILE, ChangeOperation.RENAME_FILE):
            if not source_path.exists():
                return False, f"Cannot {change.operation.name.lower()} non-existent file {change.name}"
            target_path = config.workspace_dir / change.target
            if target_path.exists():
                return False, f"Cannot {change.operation.name.lower()} {change.name} to {change.target} - target already exists"

            
    return True, ""

def apply_changes(changes: List[FileChange], preview_dir: Path, console: Console) -> bool:
    """Apply all changes from preview to workspace_dir.
    Returns success status."""
    is_safe, error = verify_changes(changes)
    if not is_safe:
        console.print(f"[red]Error: {error}[/red]")
        return False

    console.print("\n[blue]Applying changes to working directory...[/blue]")

    for change in changes:
        if change.operation == ChangeOperation.REMOVE_FILE:
            remove_from_workspace_dir(change.name, console)
        else:
            filepath = change.target if change.operation == ChangeOperation.RENAME_FILE else change.name
            target_path = config.workspace_dir / filepath
            preview_path = preview_dir / filepath

            target_path.parent.mkdir(parents=True, exist_ok=True)
            if preview_path.exists():
                shutil.copy2(preview_path, target_path)
                console.print(f"[dim]Applied changes to {filepath}[/dim]")

    return True

def remove_from_workspace_dir(filepath: Path, console: Console) -> None:
    """Remove file from working directory"""
    target_path = config.workspace_dir / filepath
    if target_path.exists():
        target_path.unlink()
        console.print(f"[red]Removed {filepath}[/red]")
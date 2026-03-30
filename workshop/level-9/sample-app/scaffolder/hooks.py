"""Hook demonstration utilities for the Project Scaffolder.

This module shows how Copilot CLI hooks integrate with project workflows.
It's used in Level 9 exercises to understand hook concepts.
"""

import json
import os
from datetime import datetime, timezone


def save_context_summary(summary: str, output_dir: str = ".") -> str:
    """Save a context summary to a file (used by preCompact hook demo).

    Args:
        summary: The context summary text to save.
        output_dir: Directory to write the summary file.

    Returns:
        The path to the saved summary file.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"context_summary_{timestamp}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Context Summary — {timestamp}\n\n")
        f.write(summary)
        f.write("\n")

    return filepath


def generate_subagent_context(project_name: str = "scaffolder") -> str:
    """Generate context string for subagent injection (subagentStart hook demo).

    Args:
        project_name: Name of the current project.

    Returns:
        A context string suitable for injecting into subagent prompts.
    """
    context = {
        "project": project_name,
        "language": "python",
        "conventions": [
            "Python 3.8+ compatible",
            "Standard library only",
            "Type hints encouraged",
            "Docstrings on all public functions",
        ],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    return json.dumps(context, indent=2)


def log_hook_event(hook_name: str, details: str = "") -> None:
    """Log a hook event for debugging (used in exercises).

    Args:
        hook_name: Name of the hook (e.g., 'preCompact', 'subagentStart').
        details: Optional additional details about the event.
    """
    timestamp = datetime.now(timezone.utc).strftime("%H:%M:%S")
    message = f"[{timestamp}] Hook: {hook_name}"
    if details:
        message += f" — {details}"
    print(message)

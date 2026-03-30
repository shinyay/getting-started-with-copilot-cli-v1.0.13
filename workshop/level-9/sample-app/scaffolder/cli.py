"""CLI entry point for Project Scaffolder."""

import argparse
import os
import sys
from scaffolder.config import (
    TEMPLATES, OUTPUT_DIR, MAX_PROJECT_NAME_LENGTH, ALLOWED_CHARS, VERSION
)
from scaffolder.templates import (
    list_templates, get_template_description, render_template
)


def validate_project_name(name: str) -> bool:
    """Validate that a project name contains only allowed characters."""
    if not name or len(name) > MAX_PROJECT_NAME_LENGTH:
        return False
    return all(c in ALLOWED_CHARS for c in name)


def cmd_create(args):
    """Handle the 'create' subcommand."""
    name = args.name
    template = args.template

    if not validate_project_name(name):
        print(
            f"Error: Invalid project name '{name}'. "
            f"Use only lowercase letters, numbers, hyphens, and underscores.",
            file=sys.stderr,
        )
        sys.exit(1)

    if template not in TEMPLATES:
        print(
            f"Error: Unknown template '{template}'. "
            f"Available: {', '.join(TEMPLATES)}",
            file=sys.stderr,
        )
        sys.exit(1)

    output_path = os.path.join(OUTPUT_DIR, name)
    if os.path.exists(output_path):
        print(f"Error: Directory already exists: {output_path}", file=sys.stderr)
        sys.exit(1)

    try:
        files = render_template(template, name)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Create directories and write files
    for filepath, content in files.items():
        full_path = os.path.join(output_path, filepath)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"Created project '{name}' using '{template}' template at {output_path}")
    print(f"  Files: {len(files)}")
    for filepath in sorted(files.keys()):
        print(f"    {filepath}")


def cmd_list(args):
    """Handle the 'list' subcommand."""
    templates = list_templates()
    print("Available templates:\n")
    for name in templates:
        desc = get_template_description(name)
        print(f"  {name:12s}  {desc}")
    print(f"\nTotal: {len(templates)} templates")


def cmd_info(args):
    """Handle the 'info' subcommand."""
    name = args.template
    desc = get_template_description(name)
    if desc.startswith("Unknown"):
        print(f"Error: {desc}", file=sys.stderr)
        sys.exit(1)

    from scaffolder.templates import get_template
    template = get_template(name)
    print(f"Template: {name}")
    print(f"Description: {desc}")
    print(f"Files ({len(template['files'])}):")
    for filepath in sorted(template["files"].keys()):
        print(f"  {filepath}")


def main():
    """Main entry point for the scaffolder CLI."""
    parser = argparse.ArgumentParser(
        prog="scaffolder",
        description="Project Scaffolder — generate project templates",
    )
    parser.add_argument(
        "--version", action="version", version=f"scaffolder {VERSION}"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # create
    create_parser = subparsers.add_parser("create", help="Create a new project")
    create_parser.add_argument("--name", required=True, help="Project name")
    create_parser.add_argument(
        "--template",
        default="python",
        choices=TEMPLATES,
        help="Template to use (default: python)",
    )
    create_parser.set_defaults(func=cmd_create)

    # list
    list_parser = subparsers.add_parser("list", help="List available templates")
    list_parser.set_defaults(func=cmd_list)

    # info
    info_parser = subparsers.add_parser("info", help="Show template details")
    info_parser.add_argument("template", help="Template name")
    info_parser.set_defaults(func=cmd_info)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()

"""Template definitions and rendering for Project Scaffolder."""

from typing import Dict, List, Optional


# Template registry — each template defines its file structure
TEMPLATE_REGISTRY: Dict[str, dict] = {
    "python": {
        "description": "Python project with src layout, tests, and CI",
        "files": {
            "src/__init__.py": '"""Main package."""\n',
            "src/main.py": (
                '"""Entry point."""\n\n'
                'def main():\n'
                '    """Run the application."""\n'
                '    print("Hello from {name}!")\n\n\n'
                'if __name__ == "__main__":\n'
                '    main()\n'
            ),
            "tests/__init__.py": "",
            "tests/test_main.py": (
                '"""Tests for main module."""\n\n'
                'import unittest\n\n\n'
                'class TestMain(unittest.TestCase):\n'
                '    """Test cases for main."""\n\n'
                '    def test_placeholder(self):\n'
                '        """Placeholder test."""\n'
                '        self.assertTrue(True)\n\n\n'
                'if __name__ == "__main__":\n'
                '    unittest.main()\n'
            ),
            "README.md": "# {name}\n\nA Python project.\n",
            "requirements.txt": "# No external dependencies\n",
            ".gitignore": "__pycache__/\n*.pyc\n.venv/\n",
        },
    },
    "typescript": {
        "description": "TypeScript project with src layout and Jest",
        "files": {
            "src/index.ts": (
                'export function main(): void {{\n'
                '  console.log("Hello from {name}!");\n'
                '}}\n\n'
                'main();\n'
            ),
            "tests/index.test.ts": (
                'describe("{name}", () => {{\n'
                '  it("should work", () => {{\n'
                '    expect(true).toBe(true);\n'
                '  }});\n'
                '}});\n'
            ),
            "README.md": "# {name}\n\nA TypeScript project.\n",
            "tsconfig.json": (
                '{{\n'
                '  "compilerOptions": {{\n'
                '    "target": "ES2020",\n'
                '    "module": "commonjs",\n'
                '    "strict": true,\n'
                '    "outDir": "./dist"\n'
                '  }},\n'
                '  "include": ["src/"]\n'
                '}}\n'
            ),
            "package.json": (
                '{{\n'
                '  "name": "{name}",\n'
                '  "version": "1.0.0",\n'
                '  "scripts": {{\n'
                '    "build": "tsc",\n'
                '    "test": "jest"\n'
                '  }}\n'
                '}}\n'
            ),
            ".gitignore": "node_modules/\ndist/\n",
        },
    },
    "bash": {
        "description": "Bash script project with tests and CI",
        "files": {
            "bin/main.sh": (
                '#!/usr/bin/env bash\n'
                'set -euo pipefail\n\n'
                'echo "Hello from {name}!"\n'
            ),
            "tests/test_main.sh": (
                '#!/usr/bin/env bash\n'
                'set -euo pipefail\n\n'
                '# Simple test\n'
                'output=$(bash bin/main.sh)\n'
                'if [[ "$output" == *"Hello"* ]]; then\n'
                '    echo "PASS: main.sh outputs greeting"\n'
                'else\n'
                '    echo "FAIL: unexpected output"\n'
                '    exit 1\n'
                'fi\n'
            ),
            "README.md": "# {name}\n\nA Bash project.\n",
            ".gitignore": "*.log\n",
        },
    },
    "mixed": {
        "description": "Multi-language project (Python + TypeScript + Bash)",
        "files": {
            "services/api/index.ts": 'console.log("API service for {name}");\n',
            "services/worker/worker.py": '"""Worker service for {name}."""\n\nprint("Worker running")\n',
            "scripts/setup.sh": '#!/usr/bin/env bash\nset -euo pipefail\necho "Setting up {name}"\n',
            "README.md": "# {name}\n\nA multi-language project.\n",
            ".gitignore": "__pycache__/\nnode_modules/\n*.log\n",
        },
    },
}


def list_templates() -> List[str]:
    """Return sorted list of available template names."""
    return sorted(TEMPLATE_REGISTRY.keys())


def get_template(name: str) -> Optional[dict]:
    """Return template definition by name, or None if not found."""
    return TEMPLATE_REGISTRY.get(name)


def get_template_description(name: str) -> str:
    """Return human-readable description for a template."""
    template = get_template(name)
    if template is None:
        return f"Unknown template: {name}"
    return template["description"]


def render_template(template_name: str, project_name: str) -> Dict[str, str]:
    """Render a template with the given project name.

    Returns a dict of {filepath: content} with placeholders replaced.
    """
    template = get_template(template_name)
    if template is None:
        raise ValueError(f"Unknown template: {template_name}")

    rendered = {}
    for filepath, content in template["files"].items():
        rendered[filepath] = content.format(name=project_name)
    return rendered

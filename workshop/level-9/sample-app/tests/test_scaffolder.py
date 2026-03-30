"""Tests for the Project Scaffolder."""

import unittest
from scaffolder.templates import list_templates, get_template, render_template
from scaffolder.config import TEMPLATES
from scaffolder.cli import validate_project_name


class TestTemplates(unittest.TestCase):
    """Test template operations."""

    def test_list_templates(self):
        """List returns all registered templates."""
        templates = list_templates()
        self.assertEqual(len(templates), 4)
        self.assertIn("python", templates)
        self.assertIn("typescript", templates)

    def test_get_template_exists(self):
        """Get template returns definition for valid name."""
        template = get_template("python")
        self.assertIsNotNone(template)
        self.assertIn("files", template)
        self.assertIn("description", template)

    def test_get_template_not_found(self):
        """Get template returns None for invalid name."""
        self.assertIsNone(get_template("nonexistent"))

    def test_render_template(self):
        """Render replaces placeholders with project name."""
        files = render_template("python", "my-project")
        self.assertIn("README.md", files)
        self.assertIn("my-project", files["README.md"])

    def test_render_unknown_template(self):
        """Render raises ValueError for unknown template."""
        with self.assertRaises(ValueError):
            render_template("nonexistent", "test")


class TestValidation(unittest.TestCase):
    """Test project name validation."""

    def test_valid_name(self):
        """Valid names are accepted."""
        self.assertTrue(validate_project_name("my-project"))
        self.assertTrue(validate_project_name("test_app"))

    def test_empty_name(self):
        """Empty name is rejected."""
        self.assertFalse(validate_project_name(""))

    def test_invalid_chars(self):
        """Names with uppercase or special chars are rejected."""
        self.assertFalse(validate_project_name("MyProject"))
        self.assertFalse(validate_project_name("test project"))


class TestConfig(unittest.TestCase):
    """Test configuration."""

    def test_templates_list(self):
        """Config TEMPLATES matches template registry."""
        for name in TEMPLATES:
            self.assertIsNotNone(get_template(name))


if __name__ == "__main__":
    unittest.main()

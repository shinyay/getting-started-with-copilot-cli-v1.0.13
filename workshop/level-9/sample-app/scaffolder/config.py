"""Configuration for Project Scaffolder."""

import os

# Directories
OUTPUT_DIR = os.environ.get("SCAFFOLDER_OUTPUT_DIR", "./output")
TEMPLATE_DIR = os.environ.get("SCAFFOLDER_TEMPLATE_DIR", None)

# Defaults
DEFAULT_TEMPLATE = "python"
MAX_PROJECT_NAME_LENGTH = 64
ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789-_"

# Available templates
TEMPLATES = ["python", "typescript", "bash", "mixed"]

# Metadata
VERSION = "1.0.0"

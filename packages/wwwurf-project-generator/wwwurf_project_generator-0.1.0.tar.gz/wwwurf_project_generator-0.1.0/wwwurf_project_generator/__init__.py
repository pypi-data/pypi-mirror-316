"""WWWURF Project Generator - A tool for generating multi-package Python projects."""

__version__ = "0.1.0"
__author__ = "WorldWideWurf"
__email__ = "worldwidewurf@gmail.com"

from wwwurf_project_generator.project_manager import ProjectManager
from wwwurf_project_generator.cli import main

__all__ = ["ProjectManager", "main"]
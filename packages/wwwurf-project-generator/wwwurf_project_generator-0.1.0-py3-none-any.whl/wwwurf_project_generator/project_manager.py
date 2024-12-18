"""Module for managing multi-package Python project generation."""
import os
from pathlib import Path
import subprocess
import toml
from typing import List, Optional, Dict, Any

class ProjectManager:
    """Manages the creation and modification of multi-package Python projects."""
    
    def __init__(self, project_name: Optional[str] = None, packages: Optional[List[str]] = None):
        """
        Initialize ProjectManager.

        Args:
            project_name: Name of the project to create
            packages: List of package names to include
        """
        self.project_name = project_name
        self.packages = packages if packages else ["core"]
        self.root_dir = Path(project_name) if project_name else Path.cwd()

    def generate_file_content(self, file_type: str, package_name: Optional[str] = None) -> str:
        """
        Generate content for various project files.

        Args:
            file_type: Type of file to generate content for
            package_name: Name of the package (for package-specific files)

        Returns:
            Generated file content as string
        """
        if file_type == "package_pyproject" and not package_name:
            raise ValueError("package_name is required for package_pyproject")

        pkg_name = package_name if package_name else self.project_name
        pkg_desc = f"{pkg_name.title()} - Standalone functionality" if package_name else "Main application that combines all packages"

        contents: Dict[str, str] = {
            "root_pyproject": f'''[tool.poetry]
name = "{self.project_name}"
version = "0.1.0"
description = "Main application that combines all packages"
authors = ["WorldWideWurf <worldwidewurf@gmail.com>"]
readme = "README.md"
packages = [{{include = "main_app"}}]

[tool.poetry.dependencies]
python = "^3.9"
{self._generate_package_dependencies()}

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
black = "^23.7.0"
isort = "^5.12.0"
flake8 = "^6.1.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
''',
            "package_pyproject": f'''[tool.poetry]
name = "{pkg_name}"
version = "0.1.0"
description = "{pkg_desc}"
authors = ["WorldWideWurf <worldwidewurf@gmail.com>"]
readme = "README.md"
packages = [{{include = "{pkg_name}"}}]

[tool.poetry.dependencies]
python = "^3.9"

[tool.poetry.scripts]
{pkg_name} = "{pkg_name}.main:main"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
''',
            "main_app": '''"""Main application entry point that combines all packages."""

def main():
    """Run the complete application."""
    try:
        print("Running main application...")
        # Import packages dynamically
        package_names = []  # This will be populated during project creation
        
        for package_name in package_names:
            try:
                package = __import__(f"{package_name}.main", fromlist=['main'])
                print(f"Initializing {package_name}...")
                package.main()
            except ImportError as e:
                print(f"Failed to import {package_name}: {e}")
            except Exception as e:
                print(f"Error running {package_name}: {e}")
                
    except Exception as e:
        print(f"Error in main application: {e}")

if __name__ == "__main__":
    main()
''',
            "package_main": '''"""Standalone package entry point."""
def main():
    """Run this package as a standalone application."""
    print(f"Running {__package__}")

if __name__ == "__main__":
    main()
''',
            "package_init": '''"""Package initialization."""
__version__ = "0.1.0"
''',
            "root_readme": f'''# {self.project_name}

Multi-package application using Poetry.

## Structure

This project consists of multiple packages:
{self._generate_package_list()}

## Installation

### Complete Application
```bash
poetry install
```

### Individual Packages
```bash
cd packages/[package_name]
poetry install
```

## Usage

### Running Complete Application
```bash
poetry run python -m main_app.main
```

### Running Individual Packages
```bash
cd packages/[package_name]
poetry run [package-name]
```

### Adding New Packages
```bash
./manage.py add-package new_package_name
```
''',
            "package_readme": f'''# {pkg_name}

A standalone package that can also be part of {self.project_name}.

## Installation

```bash
poetry install
```

## Usage

```bash
poetry run {pkg_name}
```
''',
            "gitignore": '''__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.pytest_cache/
.coverage
htmlcov/
.env
.venv
venv/
ENV/
''',
            "test": '''"""Basic test template."""
def test_example():
    """Example test function."""
    assert True
'''
        }
        return contents.get(file_type, "")

    def _generate_package_dependencies(self) -> str:
        """Generate package dependencies for root pyproject.toml."""
        return "\n".join(f'{pkg} = {{path = "packages/{pkg}", develop = true}}' 
                        for pkg in self.packages)

    def _generate_package_list(self) -> str:
        """Generate package list for README."""
        return "\n".join(f"- {pkg}" for pkg in self.packages)

    def create_package(self, package_name: str) -> bool:
        """
        Create a new package in an existing project.

        Args:
            package_name: Name of the package to create

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            packages_dir = self.root_dir / "packages"
            if not packages_dir.exists():
                print("Error: This doesn't appear to be a valid project directory.")
                return False

            package_dir = packages_dir / package_name
            if package_dir.exists():
                print(f"Error: Package {package_name} already exists.")
                return False

            # Create package structure
            package_dir.mkdir(parents=True, exist_ok=True)
            
            src_dir = package_dir / package_name
            src_dir.mkdir(parents=True, exist_ok=True)
            (src_dir / "__init__.py").write_text(self.generate_file_content("package_init"))
            (src_dir / "main.py").write_text(self.generate_file_content("package_main"))
            
            utils_dir = src_dir / "utils"
            utils_dir.mkdir(parents=True, exist_ok=True)
            (utils_dir / "__init__.py").touch()
            
            tests_dir = package_dir / "tests"
            tests_dir.mkdir(parents=True, exist_ok=True)
            (tests_dir / "__init__.py").touch()
            (tests_dir / f"test_{package_name}.py").write_text(self.generate_file_content("test"))
            
            (package_dir / "pyproject.toml").write_text(
                self.generate_file_content("package_pyproject", package_name)
            )
            (package_dir / "README.md").write_text(
                self.generate_file_content("package_readme", package_name)
            )

            # Update root pyproject.toml
            root_pyproject = self.root_dir / "pyproject.toml"
            if root_pyproject.exists():
                try:
                    config = toml.load(root_pyproject)
                    config["tool"]["poetry"]["dependencies"][package_name] = {
                        "path": f"packages/{package_name}",
                        "develop": True
                    }
                    root_pyproject.write_text(toml.dumps(config))
                    print(f"Added {package_name} to root pyproject.toml")
                except Exception as e:
                    print(f"Error updating pyproject.toml: {e}")
                    return False

            return True
        except Exception as e:
            print(f"Error creating package {package_name}: {e}")
            return False

    def create_project(self) -> bool:
        """
        Create a new project with initial packages.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create root directory
            self.root_dir.mkdir(exist_ok=True)
            
            # Create main application structure
            main_app_dir = self.root_dir / "main_app"
            main_app_dir.mkdir(exist_ok=True)
            (main_app_dir / "__init__.py").write_text(self.generate_file_content("package_init"))
            (main_app_dir / "main.py").write_text(self.generate_file_content("main_app"))
            
            # Create packages directory
            packages_dir = self.root_dir / "packages"
            packages_dir.mkdir(exist_ok=True)
            
            # Create root configuration files
            (self.root_dir / "pyproject.toml").write_text(self.generate_file_content("root_pyproject"))
            (self.root_dir / "README.md").write_text(self.generate_file_content("root_readme"))
            (self.root_dir / ".gitignore").write_text(self.generate_file_content("gitignore"))
            
            # Create management script
            self.create_management_script()
            
            # Create each package
            for package in self.packages:
                if not self.create_package(package):
                    print(f"Failed to create package: {package}")
                    return False
            return True
        except Exception as e:
            print(f"Error creating project: {e}")
            return False

    def create_management_script(self) -> None:
        """Create a management script for the project."""
        script_content = '''#!/usr/bin/env python3
import sys
from pathlib import Path
from wwwurf_project_generator.project_manager import ProjectManager

def main():
    if len(sys.argv) < 2:
        print("Usage: ./manage.py <command> [args]")
        print("\\nAvailable commands:")
        print("  add-package <package_name>  - Add a new package to the project")
        return

    command = sys.argv[1]
    if command == "add-package":
        if len(sys.argv) < 3:
            print("Usage: ./manage.py add-package <package_name>")
            return
            
        package_name = sys.argv[2]
        manager = ProjectManager()
        if manager.create_package(package_name):
            print(f"Successfully created package: {package_name}")
            print("\\nTo install the new package:")
            print(f"1. cd packages/{package_name}")
            print("2. poetry install")
            print("\\nThen update the main project:")
            print("3. cd ../..")
            print("4. poetry install")
    else:
        print(f"Unknown command: {command}")
'''
        manage_script = self.root_dir / "manage.py"
        manage_script.write_text(script_content)
        manage_script.chmod(0o755)

    def initialize_git(self) -> bool:
        """
        Initialize git repository for the project.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            os.chdir(self.root_dir)
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
            return True
        except Exception as e:
            print(f"Error initializing git: {e}")
            return False
"""Command-line interface for the WWWURF project generator."""
import argparse
import sys
from typing import Optional
from wwwurf_project_generator.project_manager import ProjectManager

def main() -> Optional[int]:
    """
    Main entry point for the CLI.

    Returns:
        Optional[int]: Exit code (1 for error, None for success)
    """
    parser = argparse.ArgumentParser(
        description="Generate or modify a multi-package Python project",
        prog="wwwurf-gen"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Create project command
    create_parser = subparsers.add_parser("create", help="Create a new project")
    create_parser.add_argument("project_name", help="Name of the main project")
    create_parser.add_argument(
        "--packages", 
        nargs="+", 
        help="List of package names", 
        default=["core"]
    )

    # Add package command
    add_parser = subparsers.add_parser(
        "add-package", 
        help="Add a new package to existing project"
    )
    add_parser.add_argument("package_name", help="Name of the new package")

    args = parser.parse_args()

    if args.command == "create":
        manager = ProjectManager(args.project_name, args.packages)
        if manager.create_project():
            if manager.initialize_git():
                print(f"\nInitialized git repository in {manager.root_dir}")
            
            print(f"\nProject {args.project_name} created successfully!")
            print("\nTo get started:")
            print(f"cd {args.project_name}")
            print("poetry install")
            print("\nTo add new packages later:")
            print("./manage.py add-package <package_name>")
        else:
            return 1

    elif args.command == "add-package":
        manager = ProjectManager()
        if manager.create_package(args.package_name):
            print(f"\nPackage {args.package_name} created successfully!")
            print("\nTo install the new package:")
            print(f"1. cd packages/{args.package_name}")
            print("2. poetry install")
            print("\nThen update the main project:")
            print("3. cd ../..")
            print("4. poetry install")
        else:
            return 1
    else:
        parser.print_help()
        return 1

    return None

if __name__ == "__main__":
    sys.exit(main())
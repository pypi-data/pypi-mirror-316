import argparse
from sqliteorm_py.makemigrations import run_migrations
import os
import shutil


def create_project(project_name):
    """
    Create a new project structure with default files.
    """
    try:
        # Define the structure for the new project
        project_structure = {
            project_name: [
                "manage.py",
                "settings.py",
                "models.py",
            ]
        }

        # Create the root project directory
        os.makedirs(project_name, exist_ok=True)

        # Copy default templates
        templates_dir = os.path.join(os.path.dirname(__file__), "templates")

        for filename in project_structure[project_name]:
            src_file = os.path.join(templates_dir, filename)
            dest_file = os.path.join(project_name, filename)
            shutil.copyfile(src_file, dest_file)

        print(f"Project '{project_name}' created successfully!")
    except Exception as e:
        print(f"Error creating project '{project_name}': {e}")


def main():
    """
    Main function to parse and execute CLI commands.
    """
    parser = argparse.ArgumentParser(
        description="CLI tool for managing projects with sqliteorm."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subcommand: createproject
    create_project_parser = subparsers.add_parser(
        "createproject", help="Create a new ORM project."
    )
    create_project_parser.add_argument(
        "name", type=str, help="Name of the new project to be created"
    )

    # Subcommand: makemigrations
    # subparsers.add_parser(
    #     "makemigrations", help="Run migrations for the database."
    # )

    # Parse the arguments
    args = parser.parse_args()

    # Execute the appropriate function based on the command
    if args.command == "createproject":
        create_project(args.name)
    # elif args.command == "makemigrations":
    #     run_migrations()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

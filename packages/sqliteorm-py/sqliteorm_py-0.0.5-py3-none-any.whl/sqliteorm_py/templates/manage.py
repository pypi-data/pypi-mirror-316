from sqliteorm_py.makemigrations import run_migrations
import argparse


def manage():
    parser = argparse.ArgumentParser(description="Database migrations for models.")

    # Define the 'migrations' command
    parser.add_argument('command', choices=['migrations'], help="Run migrations")

    # Parse command line arguments
    args = parser.parse_args()

    try:
        # If the 'migrations' command is entered, run migrations
        if args.command == 'migrations':
            print("Running migrations...")
            run_migrations()  # Call the run_migrations method to synchronize models and tables
    except Exception as e:
        print(f"An error occurred during migrations: {e}")


if __name__ == "__main__":
    try:
        manage()
    except Exception as e:
        print(f"Unexpected error: {e}")


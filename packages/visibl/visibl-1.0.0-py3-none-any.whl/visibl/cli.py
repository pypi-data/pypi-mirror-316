# python/visibl/cli.py

import click
import os
import json
from pathlib import Path
import sys
from functools import update_wrapper

# Suppose we also want to call some backend logic:
from .backend import generate_docs, auto_generate_docs  # We'll define these

CONFIG_DIR = Path.home() / ".visibl"
CONFIG_FILE = CONFIG_DIR / "config.json"

MOCK_AUTH = False  # For testing: set to True to simulate being authenticated

def load_config():
    """Load local config with user credentials/token."""
    global MOCK_AUTH
    if MOCK_AUTH:  # For testing
        return {"token": "test_token"}
    if not CONFIG_FILE.exists():
        return {}
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(data):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f)

@click.group()
def cli():
    """Visibl CLI tool."""
    pass

def auth_required(f):
    """Decorator to require authentication for commands."""
    def wrapper(*args, **kwargs):
        # Skip auth check for login and logout commands
        if f.__name__ in ['login', 'logout']:
            return f(*args, **kwargs)
        
        # Check authentication for all other commands
        conf = load_config()
        if 'token' not in conf:
            click.secho("⚠️  Authentication required!", fg='yellow', bold=True)
            click.echo("Please run 'visibl login' first to authenticate.")
            sys.exit(1)
        return f(*args, **kwargs)
    
    return update_wrapper(wrapper, f)

@cli.command()
@auth_required
def gen():
    """Generate some documentation."""
    try:
        docs_path = generate_docs()
        click.secho(f"✨ Docs generated successfully at {docs_path}", fg='green')
    except FileNotFoundError as e:
        click.secho("❌ Error: Required directories not found", fg='red')
        click.echo(f"Details: {str(e)}")
        click.echo("Please ensure you're running this command from the correct directory.")
        sys.exit(1)

@cli.command()
@auth_required
def autogen():
    """Auto-generate docs."""
    try:
        docs_path = auto_generate_docs()
        click.secho(f"✨ Docs auto-generated successfully at {docs_path}", fg='green')
    except FileNotFoundError as e:
        click.secho("❌ Error: Required directories not found", fg='red')
        click.echo(f"Details: {str(e)}")
        click.echo("Please ensure you're running this command from the correct directory.")
        sys.exit(1)

@cli.command()
@auth_required
def view():
    """View docs or open the Electron UI."""
    # Update the electron_path based on your OS
    if sys.platform == 'darwin':  # macOS
        electron_path = "path/to/your/app.app"
    elif sys.platform.startswith('win'):  # Windows
        electron_path = "path/to/your/app.exe"
    else:  # Linux
        electron_path = "path/to/your/app"

    try:
        if sys.platform.startswith('win'):
            os.startfile(electron_path)
        else:
            import subprocess
            subprocess.Popen([electron_path])
        click.echo("Launching Visibl desktop app...")
    except FileNotFoundError:
        click.secho("❌ Error: Could not find the Visibl desktop app", fg='red')
        click.echo("Please ensure the application is properly installed.")
        sys.exit(1)

@cli.command()
def login():
    """Log in to Visibl"""
    global MOCK_AUTH
    if load_config().get('token'):
        click.secho("✓ Already logged in!", fg='green')
        return
    
    username = click.prompt("Enter your username", type=str)
    password = click.prompt("Enter your password", hide_input=True)

    # For testing purposes:
    MOCK_AUTH = True
    save_config({"username": username, "token": "test_token"})
    click.secho("✓ Login successful! You can now use visibl commands.", fg='green')

@cli.command()
def logout():
    """Logout from Visibl."""
    global MOCK_AUTH
    MOCK_AUTH = False
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
    click.secho("✓ You have been logged out.", fg='green')

def main():
    """Entry point for the CLI"""
    cli()

if __name__ == "__main__":
    main()
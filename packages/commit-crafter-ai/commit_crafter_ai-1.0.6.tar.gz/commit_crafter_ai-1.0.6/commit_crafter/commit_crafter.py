import os
import subprocess
import sys
import typer
from openai import OpenAI


app = typer.Typer(help="AI-powered commit message generator")

# Instead, get it from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set the OpenAI API key

client = OpenAI()


def get_git_diff() -> str:
    """Get the git diff output for staged changes"""
    try:
        diff_output = subprocess.check_output(
            ["git", "diff", "--staged"], stderr=subprocess.STDOUT
        ).decode("utf-8")

        if not diff_output:
            # If no staged changes, get unstaged changes
            diff_output = subprocess.check_output(
                ["git", "diff"], stderr=subprocess.STDOUT
            ).decode("utf-8")

        return diff_output
    except subprocess.CalledProcessError as e:
        print(f"Error getting git diff: {e}")
        sys.exit(1)


def generate_commit_message(diff: str) -> str:
    """Generate a commit message and detailed description using OpenAI"""
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY environment variable is not set")
        sys.exit(1)

    # Create a prompt that asks for both a commit message and a detailed description
    prompt = f"""You are a helpful assistant that generates clear and concise git commit messages.
    Follow these rules:
    1. Use the conventional commits format (type: description)
    2. Keep the message under 72 characters
    3. Use present tense
    4. Be specific but concise
    5. Focus on the "what" and "why" rather than "how"
    6. Provide a detailed description of the changes step by step.
    7. Do not use title, subtitle and markdown for the commit message. Example:
    **commit message**
    **detailed description**
    8. When writing the detailed description, write it item by item. You can use markdown to make it more readable at the start of item.
    
    Generate a commit message and detailed description for the following git diff:
    {diff}
    """

    # Call OpenAI API to get the response
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    # Correctly access the content of the response
    return response.choices[0].message.content


def create_commit(message: str):
    """Create a git commit with the generated message"""
    try:
        # Add all changes if nothing is staged
        diff_staged = subprocess.check_output(
            ["git", "diff", "--staged"], stderr=subprocess.STDOUT
        ).decode("utf-8")

        if not diff_staged:
            subprocess.run(["git", "add", "."], check=True)

        # Use the message directly for the commit
        subprocess.run(["git", "commit", "-m", message], check=True)
        print(f"Successfully committed with message: {message}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating commit: {e}")
        sys.exit(1)


@app.callback()
def callback():
    """
    Craft commit messages using AI
    """
    pass


@app.command()
def craft():
    """Craft a commit message and create a commit"""
    diff = get_git_diff()

    if not diff:
        print("No changes to commit!")
        sys.exit(0)

    commit_message = generate_commit_message(diff)
    create_commit(commit_message)


if __name__ == "__main__":
    app()

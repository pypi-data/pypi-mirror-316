# commit-crafter-ai

Ai tool to craft commit from terminal.

## Installation

```bash
pip install commit-crafter-ai
```

## Usage

```bash
commit-crafter-ai craft
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Features

- Generates clear and concise commit messages
- Follows conventional commit format
- Provides detailed descriptions of changes
- Easy to use command-line interface

## Requirements

- Python 3.7+
- OpenAI API key

## Upload to PyPI

```bash
python -m twine upload dist/*
```

## Setup

1. Export your OpenAI API key:

```bash
# Linux/macOS
export OPENAI_API_KEY="your-api-key-here"

# Windows (Command Prompt)
set OPENAI_API_KEY=your-api-key-here

# Windows (PowerShell)
$env:OPENAI_API_KEY="your-api-key-here"
```

2. The API key can also be added to your shell configuration file (~/.bashrc, ~/.zshrc, etc.) for persistence:

```bash
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bashrc  # or ~/.zshrc
```

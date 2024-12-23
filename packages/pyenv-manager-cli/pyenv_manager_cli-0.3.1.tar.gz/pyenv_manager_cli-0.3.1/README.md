# Pyenv Manager CLI

A command-line tool for managing Python virtual environments with pyenv.

## Features

- Detect and validate pyenv environments
- Manage `.python-version` files
- Switch between environments
- Create new environments
- Validate environment states
- Interactive environment management
- Non-interactive mode for scripting
- Comprehensive test suite

## Installation

### Using pipx (Recommended)

The recommended way to install `pyenv-manager-cli` is using `pipx`, which installs the tool in an isolated environment:

```bash
# Install pipx if you haven't already
python -m pip install --user pipx
python -m pipx ensurepath

# Install pyenv-manager-cli
pipx install pyenv-manager-cli
```

### Using pip

You can also install using pip directly:

```bash
pip install pyenv-manager-cli
```

## Usage

### Interactive Mode (Default)

Simply run:

```bash
pyenv-manager
```

The tool will:
1. Check your current Python environment
2. Detect any `.python-version` files
3. Validate environment consistency
4. Provide interactive options for managing your environment

### Non-Interactive Mode

For scripting or status checks:

```bash
pyenv-manager --non-interactive
```

### Version Information

```bash
pyenv-manager --version
```

### Help

```bash
pyenv-manager --help
```

### Common Operations

- **Switch Environments**: The tool will detect mismatches between your current environment and `.python-version` file
- **Create New Environments**: Easily create new pyenv environments with specific Python versions
- **Manage Local Settings**: Update `.python-version` files to persist your environment choices
- **Environment Validation**: Check if your environments are properly configured

## Requirements

- Python 3.8 or higher
- pyenv installed and configured
- pyenv-virtualenv plugin (recommended)

## Version History

- **0.3.0**
  - Added comprehensive test suite
  - Added non-interactive mode
  - Improved error handling
  - Added Click CLI interface

- **0.2.0**
  - Added Click CLI integration
  - Added version information
  - Improved command-line interface

- **0.1.0**
  - Initial release
  - Basic environment management
  - Interactive mode

## Development

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/terrylica/pyenv-manager-cli.git
cd pyenv-manager-cli

# Install in editable mode with test dependencies
pip install -e ".[test]"
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=pyenv_manager_cli
```

## Updating

### With pipx

```bash
pipx upgrade pyenv-manager-cli
```

### With pip

```bash
pip install --upgrade pyenv-manager-cli
```

## Uninstalling

### With pipx

```bash
pipx uninstall pyenv-manager-cli
```

### With pip

```bash
pip uninstall pyenv-manager-cli
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License 
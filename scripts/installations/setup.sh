#!/bin/bash

# Directory to install Poetry
POETRY_HOME="$(pwd)/.poetry"

# Python version, default to 3.9 unless otherwise specified
PYTHON_VERSION=${1:-3.9}

# Check if a given Python version is installed
is_python_installed() {
    command -v python$1 &> /dev/null
}

# Install the given Python version using Homebrew
install_python() {
    if brew list python@$1 &> /dev/null; then
        echo "Python $1 is already installed via Homebrew. Linking..."
        brew link --overwrite python@$1
    else
        echo "Installing Python $1..."
        brew install python@$1
        echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zshrc
        source ~/.zshrc
    fi
}

# Install an isolated Poetry environment
install_poetry() {
    echo "Installing Poetry..."

    # Check and install Python if necessary
    if ! is_python_installed $PYTHON_VERSION; then
        install_python $PYTHON_VERSION
    else 
        echo "Python $1 is already installed"
    fi

    # Use the specified Python version to create a new virtual environment for Poetry
    python$PYTHON_VERSION -m venv $POETRY_HOME

    # Activate the virtual environment
    source $POETRY_HOME/bin/activate

    # Install Poetry in the virtual environment
    curl -sSL https://install.python-poetry.org | sed 's/symlinks=False/symlinks=True/' | POETRY_HOME="$(pwd)/.poetry" python3 - 

    # Configure Poetry
    $POETRY_HOME/bin/poetry config virtualenvs.in-project true
    $POETRY_HOME/bin/poetry env use python$PYTHON_VERSION
    $POETRY_HOME/bin/poetry install

    deactivate
    echo "Poetry installed successfully using Python $PYTHON_VERSION."
}

# Clean up function
cleanup() {
    echo "Cleaning up..."
    rm -rf $POETRY_HOME
    echo "Cleanup done."
}

# Check arguments
if [[ "$2" == "install" ]]; then
    install_poetry
elif [[ "$2" == "clean" ]]; then
    cleanup
else
    echo "Usage: ./setup.sh PYTHON_VERSION [install|clean]"
fi

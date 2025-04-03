#!/bin/bash

# Define color codes
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
RED='\033[0;31m'
RESET='\033[0m' # No Color

# Function to print success messages in green
function print_success {
    echo -e "${GREEN}Success: $1${RESET}"
}

# Function to print warning messages in orange
function print_warning {
    echo -e "${ORANGE}Warning: $1${RESET}"
}

# Function to print error messages in red
function print_error {
    echo -e "${RED}Error: $1${RESET}"
}

# Step 0: Check required packages
# - check if git
if command -v git &> /dev/null -ne 0; then
    print_error "Git is not install. Please install it before retrying the installation."
    exit 1
fi
# - check if pip is install
if command -v pip &> /dev/null -ne 0; then
    print_error "Pip is not install. Please install it before retrying the installation."
    exit 1
fi

# Step 1: Install Python requirements
echo "Installing Python requirements..."
# Attempt to install Python requirements
pip install -r requirements.txt

# Check the return status of the pip install command
if $? -eq 0; then
    print_success "Python requirements installed successfully."
else
    print_warning "Failed to install Python requirements. Please check the requirements.txt file and try again.\n
    pip install -r requirements.txt"
    exit 1
fi

# Step 2: Clone the cvelistV5 repository
echo "Cloning of the official cve.org github repository..."
# Attempt to clone the repository
git clone git@github.com:CVEProject/cvelistV5.git

# Check the return status of the git clone command
if $? -eq 0; then
    print_success "Repository cloned successfully."
else
    print_warning "Failed to clone the repository. Please check the repository URL and your network connection.\n
    git clone git@github.com:CVEProject/cvelistV5.git"
    exit 1
fi

print_success "Installation and setup complete!"

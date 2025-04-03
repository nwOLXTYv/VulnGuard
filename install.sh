#! /bin/bash

# Define color codes
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
RESET='\033[0m' # No Color

# Function to print info message in white
function print_info {
    echo -e "${BLUE}$1${RESET}"
}

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
print_info "Check required packages..."
  # Check Git version
git --version &> /dev/null || { print_error "Git is not installed. Please install it before retrying the installation.\nSee https://git-scm.com/downloads/linux"; exit 1; }
  # Check Pip version
pipx --version &> /dev/null || { print_error "Pipx is not install. Please install it before retrying the installation.\n See https://pipx.pypa.io/latest/installation/"; exit 1; }
  # Print step 0 success
print_success "All required packages are installed."


# Step 1: Install Pipenv
print_info "Install pipenv package..."
  # Attempt to install pipenv package
pipx install pipenv || { print_warning "Failed to install pipenv package.\n See https://docs.pipenv.org/install/"; exit 1; }
  # Print step 1 success
print_success "Pipenv package installed successfully."


# Step 2: Install Python requirements
print_info "Installing project's requirements..."
# Attempt to install Python requirements
(pipenv upgrade && pipenv sync) || { print_warning "Failed to install project's requirements. Please check the Pipfile and Pipfile.lock file and try again.\n See https://pipenv.pypa.io/en/latest/commands.html"; exit 1; }


# Step 3: Clone the cvelistV5 repository
print_info "Cloning of the official cve.org github repository..."
# Attempt to clone the repository
git clone https://github.com/CVEProject/cvelistV5.git || { print_warning "Failed to clone the repository. Please check the repository URL and your network connection.\n git clone https://github.com/CVEProject/cvelistV5.git"; exit 1; }
# Print step 3 success
print_success "Repository cloned successfully."
print_success "Installation and setup complete!"

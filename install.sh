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
  # Check Python3 version
python3 --version &> /dev/null || { print_error "Python3 is not installed. Please install it before retrying the installation."; exit 1; }
  # Print step 0 success
print_success "All required packages are installed."

# Step 1: Set up virtual environment
print_info "Setting up virtual environment..."
  # Create a virtual environment
python3 -m venv .venv || { print_warning "Failed to create virtual environment."; exit 1; }
  # Activate the virtual environment
source .venv/bin/activate || { print_warning "Failed to activate virtual environment."; exit 1; }
  # Upgrade pip
python3 -m pip install --upgrade pip || { print_warning "Failed to upgrade pip."; exit 1; }
  # Print step 1 success
print_success "Virtual environment set up successfully."

# Step 2: Install Python requirements
print_info "Installing project's requirements..."
  # Attempt to install Python requirements
pip install -r requirements.txt || { print_warning "Failed to install project's requirements. Please check the requirements.txt file and try again."; exit 1; }
  # Print step 2 success
print_success "Project's requirements installed successfully."

# Step 3: Clone the cvelistV5 repository
print_info "Cloning the official cve.org GitHub repository..."
  # Attempt to clone the repository
git clone git@github.com:CVEProject/cvelistV5.git || { print_warning "Failed to clone the repository. Please check the repository URL and your network connection.\n git clone https://github.com/CVEProject/cvelistV5.git"; exit 1; }
  # Print step 3 success
print_success "Repository cloned successfully."
print_success "Installation and setup complete!"

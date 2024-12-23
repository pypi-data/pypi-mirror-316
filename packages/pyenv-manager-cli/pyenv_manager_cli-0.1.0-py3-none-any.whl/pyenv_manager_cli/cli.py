#!/usr/bin/env python3
import sys
import os
import subprocess
from pathlib import Path
import time

def get_pyenv_local_version():
    try:
        # Walk up the directory tree looking for .python-version
        current_dir = Path.cwd()
        while current_dir != current_dir.parent:
            version_file = current_dir / '.python-version'
            if version_file.exists():
                return version_file.read_text().strip(), str(version_file)
            current_dir = current_dir.parent
        return None, None
    except Exception as e:
        return None, f"Error reading .python-version: {e}"

def get_pyenv_root():
    try:
        # Try to get PYENV_ROOT from environment, fallback to default
        pyenv_root = os.environ.get('PYENV_ROOT', os.path.expanduser('~/.pyenv'))
        return pyenv_root if os.path.exists(pyenv_root) else None
    except Exception as e:
        return f"Error getting PYENV_ROOT: {e}"

def verify_pyenv_environment(version_name):
    """Verify if a pyenv version/environment exists and is valid"""
    pyenv_root = get_pyenv_root()
    if not pyenv_root:
        return False, None
    
    # Check both direct version path and envs subdirectory
    version_paths = [
        os.path.join(pyenv_root, 'versions', version_name),
        os.path.join(pyenv_root, 'versions', version_name.split('/')[0], 'envs', version_name.split('/')[-1])
    ]
    
    for venv_path in version_paths:
        if os.path.exists(venv_path) and os.path.exists(os.path.join(venv_path, 'bin', 'python')):
            return True, venv_path
    return False, None

def run_command(cmd):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, check=True, text=True, 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def get_available_environments():
    """Get list of available pyenv environments"""
    pyenv_root = get_pyenv_root()
    if not pyenv_root:
        return []
    
    try:
        result = subprocess.run(['pyenv', 'versions'], capture_output=True, text=True)
        versions = []
        for line in result.stdout.splitlines():
            if '*' in line:  # Currently active version
                version = line.split()[1]
            else:
                version = line.strip()
            if version != 'system':
                versions.append(version)
        return versions
    except:
        return []

def validate_environment_state():
    """Validate and display the current state of the environment"""
    print("\nValidating current state:")
    print("-" * 50)
    
    # Get current state
    current_venv = os.environ.get('VIRTUAL_ENV')
    pyenv_version, version_file = get_pyenv_local_version()
    
    # Display Python info
    print(f"Python Version: {sys.version.split()[0]}")
    print(f"Python Executable: {sys.executable}")
    
    # Display virtual environment info
    if current_venv:
        print(f"Active Virtual Environment: {os.path.basename(current_venv)}")
        print(f"Full Path: {current_venv}")
    else:
        print("No active virtual environment")
    
    # Display .python-version info
    if pyenv_version:
        print(f"\nPyenv Local Setup:")
        print(f"- .python-version location: {version_file}")
        print(f"- Specified version/environment: {pyenv_version}")
        
        # Verify if specified environment exists
        is_valid, venv_path = verify_pyenv_environment(pyenv_version)
        if is_valid:
            print(f"- Environment exists at: {venv_path}")
            if current_venv == venv_path:
                print("✓ Current environment matches .python-version specification")
            else:
                print("✗ Warning: Current environment does not match .python-version specification")
        else:
            print("✗ Warning: Specified environment does not exist")
    else:
        print("\nNo .python-version file found in current directory or parent directories")
    
    print("-" * 50)
    return current_venv, pyenv_version

def handle_environment_mismatch(current_venv, target_version, venv_path):
    """Handle environment mismatch with interactive choices"""
    print("\nEnvironment Mismatch Detected!")
    print(f"Current: {current_venv or 'No environment'}")
    print(f"Should be: {venv_path}")
    
    print("\nOptions:")
    print("1. Switch to the environment specified in .python-version")
    print("2. Update .python-version to use current environment")
    print("3. Do nothing (abandon)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == '1':
        if current_venv:
            success, msg = run_command('pyenv deactivate')
            if not success:
                print(f"Error deactivating current environment: {msg}")
                return
        
        success, msg = run_command(f'pyenv activate {target_version}')
        if success:
            print(f"Successfully switched to {target_version}")
            print("\nValidating changes...")
            time.sleep(1)  # Give system time to update environment
            validate_environment_state()
        else:
            print(f"Error activating environment: {msg}")
            
    elif choice == '2':
        if current_venv:
            current_name = os.path.basename(current_venv)
            success, msg = run_command(f'pyenv local {current_name}')
            if success:
                print(f"Successfully updated .python-version to use {current_name}")
                print("\nValidating changes...")
                time.sleep(1)  # Give system time to update environment
                validate_environment_state()
            else:
                print(f"Error updating .python-version: {msg}")
        else:
            print("No current environment to set as local")
    
    elif choice == '3':
        print("No changes made")
        validate_environment_state()
    
    else:
        print("Invalid choice")

def handle_missing_environment(version_name):
    """Handle missing environment with interactive choices"""
    print(f"\nWarning: Environment '{version_name}' specified in .python-version does not exist!")
    
    available_versions = get_available_environments()
    if available_versions:
        print("\nAvailable environments:")
        for i, version in enumerate(available_versions, 1):
            print(f"{i}. {version}")
    
    print("\nOptions:")
    print("1. Create this environment")
    if available_versions:
        print("2. Choose an existing environment")
    print(f"{'3' if available_versions else '2'}. Do nothing (abandon)")
    
    choice = input("\nEnter your choice: ").strip()
    
    if choice == '1':
        python_version = input("Enter Python version to use (e.g., 3.11.0): ").strip()
        success, msg = run_command(f'pyenv virtualenv {python_version} {version_name}')
        if success:
            print(f"Successfully created environment {version_name}")
            success, msg = run_command(f'pyenv activate {version_name}')
            if success:
                print(f"Activated environment {version_name}")
                print("\nValidating changes...")
                time.sleep(1)  # Give system time to update environment
                validate_environment_state()
            else:
                print(f"Error activating environment: {msg}")
        else:
            print(f"Error creating environment: {msg}")
            
    elif choice == '2' and available_versions:
        try:
            idx = int(input(f"Enter number (1-{len(available_versions)}): ").strip()) - 1
            if 0 <= idx < len(available_versions):
                chosen_version = available_versions[idx]
                success, msg = run_command(f'pyenv local {chosen_version}')
                if success:
                    print(f"Successfully set local version to {chosen_version}")
                    print("\nValidating changes...")
                    time.sleep(1)  # Give system time to update environment
                    validate_environment_state()
                else:
                    print(f"Error setting local version: {msg}")
            else:
                print("Invalid selection")
        except ValueError:
            print("Invalid input")
    
    else:
        print("No changes made")
        validate_environment_state()

def handle_no_local_setup(current_venv):
    """Handle case when there's no .python-version but there is a current environment"""
    print("\nNo .python-version file found, but virtual environment is active.")
    print("\nOptions:")
    print("1. Make current environment persistent (create .python-version)")
    print("2. Do nothing (abandon)")
    
    choice = input("\nEnter your choice (1-2): ").strip()
    
    if choice == '1':
        venv_name = os.path.basename(current_venv)
        success, msg = run_command(f'pyenv local {venv_name}')
        if success:
            print(f"Successfully created .python-version with {venv_name}")
            print("\nValidating changes...")
            time.sleep(1)  # Give system time to update environment
            validate_environment_state()
        else:
            print(f"Error creating .python-version: {msg}")
    else:
        print("No changes made")
        validate_environment_state()

def manage_virtual_environment():
    """Main function to manage virtual environments"""
    current_venv = os.environ.get('VIRTUAL_ENV')
    pyenv_version, version_file = get_pyenv_local_version()
    
    print("Initial Environment State:")
    print("-" * 50)
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Current Virtual Environment: {current_venv or 'Not in a virtual environment'}")
    
    if pyenv_version:
        print(f"\nPyenv Local Setup:")
        print(f"- Found .python-version file at: {version_file}")
        print(f"- Local version/environment: {pyenv_version}")
        
        # Verify the environment in .python-version exists
        is_valid, venv_path = verify_pyenv_environment(pyenv_version)
        if is_valid:
            print(f"- Target environment exists at: {venv_path}")
            
            if current_venv != venv_path:
                handle_environment_mismatch(current_venv, pyenv_version, venv_path)
        else:
            handle_missing_environment(pyenv_version)
    
    elif current_venv:
        handle_no_local_setup(current_venv)
    
    else:
        print("\nNo virtual environment active and no .python-version file found.")
        validate_environment_state()

def main():
    """Entry point for the CLI tool"""
    try:
        manage_virtual_environment()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
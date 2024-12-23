#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import shutil
import click
from click.testing import CliRunner
from pyenv_manager_cli.cli import main, get_pyenv_local_version, verify_pyenv_environment
from pyenv_manager_cli import __version__

class TestPyenvManager(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        # Create a temporary directory for tests
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
        
        # Mock PYENV_ROOT
        self.mock_pyenv_root = os.path.join(self.test_dir, '.pyenv')
        os.makedirs(os.path.join(self.mock_pyenv_root, 'versions'), exist_ok=True)
        self.old_pyenv_root = os.environ.get('PYENV_ROOT')
        os.environ['PYENV_ROOT'] = self.mock_pyenv_root
        
        # Set up CLI runner
        self.runner = CliRunner()

    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)
        if self.old_pyenv_root:
            os.environ['PYENV_ROOT'] = self.old_pyenv_root
        else:
            os.environ.pop('PYENV_ROOT', None)

    def create_mock_environment(self, env_name, python_version='3.11.0'):
        """Create a mock pyenv environment structure"""
        env_path = os.path.join(self.mock_pyenv_root, 'versions', env_name)
        os.makedirs(os.path.join(env_path, 'bin'), exist_ok=True)
        # Create dummy python executable
        with open(os.path.join(env_path, 'bin', 'python'), 'w') as f:
            f.write('#!/bin/sh\necho "Python ' + python_version + '"')
        os.chmod(os.path.join(env_path, 'bin', 'python'), 0o755)

    def create_python_version_file(self, version):
        """Create a .python-version file"""
        with open('.python-version', 'w') as f:
            f.write(version)

    def test_version_command(self):
        """Test --version flag"""
        result = self.runner.invoke(main, ['--version'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.strip(), f"pyenv-manager-cli version {__version__}")

    def test_non_interactive_mode(self):
        """Test --non-interactive flag"""
        # Setup a test environment
        self.create_mock_environment('test-env', '3.11.0')
        self.create_python_version_file('test-env')
        
        result = self.runner.invoke(main, ['--non-interactive'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Validating current state:", result.output)
        self.assertIn("Python Version:", result.output)

    @patch('pyenv_manager_cli.cli.run_command')
    def test_environment_mismatch(self, mock_run_command):
        """Test environment mismatch handling"""
        # Setup
        self.create_mock_environment('env-a', '3.11.0')
        self.create_mock_environment('env-b', '3.11.0')
        self.create_python_version_file('env-a')
        
        # Mock current environment
        os.environ['VIRTUAL_ENV'] = os.path.join(self.mock_pyenv_root, 'versions', 'env-b')
        
        # Mock command execution
        mock_run_command.return_value = (True, '')
        
        # Simulate user input choosing to switch environments
        result = self.runner.invoke(main, input='1\n')
        
        # Verify
        self.assertEqual(result.exit_code, 0)
        mock_run_command.assert_any_call('pyenv deactivate')
        mock_run_command.assert_any_call('pyenv activate env-a')

    @patch('pyenv_manager_cli.cli.run_command')
    def test_missing_environment(self, mock_run_command):
        """Test missing environment handling"""
        # Setup
        self.create_python_version_file('non-existent-env')
        
        # Mock command execution
        mock_run_command.return_value = (True, '')
        
        # Simulate user input choosing to create new environment
        result = self.runner.invoke(main, input='1\n3.11.0\n')
        
        # Verify
        self.assertEqual(result.exit_code, 0)
        mock_run_command.assert_any_call('pyenv virtualenv 3.11.0 non-existent-env')

    def test_get_pyenv_local_version(self):
        """Test .python-version file detection"""
        # Test with no .python-version file
        version, path = get_pyenv_local_version()
        self.assertIsNone(version)
        self.assertIsNone(path)
        
        # Test with .python-version file
        self.create_python_version_file('test-env')
        version, path = get_pyenv_local_version()
        self.assertEqual(version, 'test-env')
        self.assertTrue(str(path).endswith('.python-version'))

    def test_verify_pyenv_environment(self):
        """Test environment verification"""
        # Test non-existent environment
        is_valid, path = verify_pyenv_environment('non-existent-env')
        self.assertFalse(is_valid)
        self.assertIsNone(path)
        
        # Test existing environment
        self.create_mock_environment('test-env')
        is_valid, path = verify_pyenv_environment('test-env')
        self.assertTrue(is_valid)
        self.assertTrue(str(path).endswith('test-env'))

if __name__ == '__main__':
    unittest.main(verbosity=2) 
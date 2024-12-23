import unittest
from unittest.mock import patch, mock_open
import json
from runmd.config import ConfigLoader, CONFIG_DIR_NAME, CONFIG_FILE_NAME
import configparser
from pathlib import Path
import pytest
import tempfile
from configparser import ConfigParser
import os

@pytest.fixture
def temp_config_dir():
    """Creates a temporary directory for testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_dir = Path(temp_dir) / CONFIG_DIR_NAME
        config_dir.mkdir()
        config_file = config_dir / CONFIG_FILE_NAME
        config_file.touch()
        yield temp_dir

@pytest.fixture
def config_loader(temp_config_dir):
    config_loader = ConfigLoader()
    config_loader.default_config_path = Path(temp_config_dir) / CONFIG_DIR_NAME / CONFIG_FILE_NAME
    return config_loader

def test_get_config(temp_config_dir):
    config_loader = ConfigLoader()
    config_loader.default_config_path = Path(temp_config_dir) / CONFIG_DIR_NAME / CONFIG_FILE_NAME
    config = config_loader._get_config()
    assert isinstance(config, ConfigParser)

def test_get_config_file_not_found(temp_config_dir):
    config_loader = ConfigLoader()
    config_loader.default_config_path = Path(temp_config_dir) / CONFIG_DIR_NAME / CONFIG_FILE_NAME
    with patch.object(config_loader, '_copy_config') as mock_copy_config:
        config_loader._get_config()

def test_copy_config(temp_config_dir):
    config_loader = ConfigLoader()
    config_loader.default_config_path = Path(temp_config_dir) / CONFIG_DIR_NAME / CONFIG_FILE_NAME
    config_loader._copy_config()
    assert os.path.exists(config_loader.default_config_path)

def test_load_config(temp_config_dir):
    config_loader = ConfigLoader()
    config_loader.default_config_path = Path(temp_config_dir) / CONFIG_DIR_NAME / CONFIG_FILE_NAME
    with open(config_loader.default_config_path, 'w') as f:
        f.write('[lang.python]\naliases = py, python\ncommand = python\noptions =')

    config_loader = ConfigLoader()  # Reload the class
    assert isinstance(config_loader.config, ConfigParser)

def test_load_config_file_not_found(temp_config_dir):
    config_loader = ConfigLoader()
    config_loader.default_config_path = Path(temp_config_dir) / "SOMEDIR"
    with pytest.raises(FileNotFoundError):
        config_loader._load_config()

def test_get_all_aliases(config_loader):
    with open(config_loader.default_config_path, 'w') as f:
        f.write('[lang.python]\naliases = py, python\ncommand = python\noptions =')
    aliases = config_loader.get_all_aliases()
    assert aliases == ['py', 'python']

def test_find_language(config_loader):
    with open(config_loader.default_config_path, 'w') as f:
        f.write('[lang.python]\naliases = py, python\ncommand = python\noptions =')
    language = config_loader.find_language('py')
    assert language == 'python'

def test_get_language_options(config_loader):
    with open(config_loader.default_config_path, 'w') as f:
        f.write('[lang.python]\naliases = py, python\ncommand = python\noptions = -v')
    options = config_loader.get_language_options('python')
    assert options == ['-v']

def test_validate_lang_section(config_loader):
    with open(config_loader.default_config_path, 'w') as f:
        f.write('[lang.python]\naliases = py, python\ncommand = python\noptions =')
    config_loader._validate_lang_section(config_loader.config['lang.python'])

def test_validate_lang_section_missing_aliases(config_loader):
    with open(config_loader.default_config_path, 'w') as f:
        f.write('[lang.python]\ncommand = python\noptions =')
    with pytest.raises(ValueError):
        config_loader._validate_lang_section(config_loader.config['lang.python'])

def test_validate_lang_section_invalid_aliases(config_loader):
    with open(config_loader.default_config_path, 'w') as f:
        f.write('[lang.python]\naliases = \ncommand = python\noptions =')
    with pytest.raises(ValueError):
        config_loader._validate_lang_section(config_loader.config['lang.python'])

def test_validate_lang_section_missing_command(config_loader):
    with open(config_loader.default_config_path, 'w') as f:
        f.write('[lang.python]\naliases = py, python\noptions =')
    with pytest.raises(ValueError):
        config_loader._validate_lang_section(config_loader.config['lang.python'])

def test_validate_lang_section_invalid_command(config_loader):
    with open(config_loader.default_config_path, 'w') as f:
        f.write('[lang.python]\naliases = py, python\ncommand = \noptions =')
    with pytest.raises(ValueError):
        config_loader._validate_lang_section(config_loader.config['lang.python'])

def test_validate_lang_section_missing_options(config_loader):
    with open(config_loader.default_config_path, 'w') as f:
        f.write('[lang.python]\naliases = py, python\ncommand = python')
    with pytest.raises(ValueError):
        config_loader._validate_lang_section('lang.python')

def test_validate_lang_section_invalid_options(config_loader):
    with open(config_loader.default_config_path, 'w') as f:
        f.write('[lang.python]\naliases = py, python\ncommand = python\noptions = \n')
    with pytest.raises(ValueError):
        config_loader._validate_lang_section('lang.python')

#
# class TestRunmdConfig(unittest.TestCase):
#
#     def setUp(self):
#         self.config = configparser.ConfigParser()
#
#     # --------------------------------------------------
#     # >> COPY_CONFIG
#     # --------------------------------------------------
#
#     @patch('importlib.resources.files')
#     @patch("runmd.config.get_default_config_path")
#     @patch('shutil.copy')
#     @patch('pathlib.Path.exists')
#     @patch('pathlib.Path.mkdir')
#     def test_copy_config_success(self, mock_mkdir, mock_exists, mock_copy, mock_default_config_path, mock_files):
#         # Setup mocks
#         mock_exists.return_value = False
#         mock_files.return_value = Path('/mock/source/config.ini')
#         mock_default_config_path.return_value = Path('/mock/source/config.ini')
#
#         # Mock the path object directly
#         mock_source_path = Path('/mock/source') #/config.ini')
#
#         # Ensure that mock_files returns this path
#         mock_files.return_value = mock_source_path
#
#         # Call the function
#         copy_config()
#
#         # Assert mkdir was called to create directories
#         mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
#
#         # Assert copy was called with the correct source and destination
#         expected_dest = Path('/mock/source/config.ini')
#         mock_copy.assert_called_once_with(Path(mock_source_path) /"config.ini", expected_dest)
#
#     @patch('importlib.resources.files')
#     @patch("runmd.config.get_default_config_path")
#     @patch('shutil.copy')
#     @patch('pathlib.Path.exists')
#     @patch('pathlib.Path.mkdir')
#     @patch('builtins.print')
#     def test_copy_config_file_not_exist(self, mock_print, mock_mkdir, mock_exists, mock_copy, mock_default_config_path, mock_files):
#         # Setup mocks
#         mock_files.return_value = "/mock/source/config.ini"
#         mock_exists.side_effect = [False]  # Destination file does not exist
#         mock_default_config_path.return_value = Path('/mock/source/config.ini')
#
#         # Mock the path object directly
#         mock_source_path = Path('/mock/source') #/config.ini')
#
#         # Ensure that mock_files returns this path
#         mock_files.return_value = mock_source_path
#
#         # Call the function
#         copy_config()
#
#         # Verify behavior
#         mock_files.assert_called_once_with("runmd")
#         mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
#         expected_dest = Path('/mock/source/config.ini')
#         mock_copy.assert_called_once_with(Path(mock_source_path) /"config.ini", expected_dest)
#         mock_print.assert_called_once_with(f"Configuration file copied to /mock/source/config.ini.")
#
#     @patch('importlib.resources.files')
#     @patch("runmd.config.get_default_config_path")
#     @patch('shutil.copy')
#     @patch('pathlib.Path.exists')
#     @patch('pathlib.Path.mkdir')
#     @patch('builtins.print')
#     def test_copy_config_file_exists(self, mock_print, mock_mkdir, mock_exists, mock_copy, mock_default_config_path, mock_files):
#         # Setup mocks
#         mock_files.return_value = "/mock/source/config.ini"
#         mock_exists.side_effect = [True]  # Destination file already exists
#         mock_default_config_path.return_value = Path('/mock/source/config.ini')
#
#         # Mock the path object directly
#         mock_source_path = Path('/mock/source') #/config.ini')
#
#         # Ensure that mock_files returns this path
#         mock_files.return_value = mock_source_path
#
#         # Call the function
#         copy_config()
#
#         # Verify behavior
#         mock_files.assert_called_once_with("runmd")
#         mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
#         mock_copy.assert_not_called()  # Should not copy the file
#         mock_print.assert_called_once_with(f"Configuration file already exists at /mock/source/config.ini.")
#
#     @patch('importlib.resources.files', side_effect=Exception("Error locating the config file"))
#     @patch('builtins.print')
#     def test_copy_config_error_locating_file(self, mock_print, mock_resource_filename):
#         #mock_print.assert_called_once_with("Error locating the config file: Error locating the config file")
#         with self.assertRaises(FileNotFoundError):
#             copy_config()
#
#     # --------------------------------------------------
#     # >> LOAD_CONFIG
#     # --------------------------------------------------
#
#     @patch('runmd.config.get_default_config_path')
#     @patch('pathlib.Path.exists')
#     @patch('configparser.ConfigParser.read')
#     def test_load_config_success(self, mock_read, mock_exists, mock_get_default_config_path):
#         # Simulate config file exists
#         mock_exists.return_value = True
#         mock_get_default_config_path.return_value = Path("/mock/path/config.ini")
#         mock_read.return_value = True  # Simulate successful read
#
#         # Call the function
#         config = load_config()
#
#         # Verify the configuration was read successfully
#         mock_exists.assert_called_once()
#         self.assertIsInstance(config, configparser.ConfigParser)
#
#     @patch('runmd.config.get_default_config_path')
#     @patch('pathlib.Path.exists')
#     def test_load_config_file_not_found(self, mock_exists, mock_get_default_config_path):
#         # Simulate config file does not exist
#         mock_exists.return_value = False
#         mock_get_default_config_path.return_value = Path("/mock/path/config.ini")
#
#         # Expect FileNotFoundError to be raised
#         with self.assertRaises(FileNotFoundError):
#             load_config()
#
#         mock_exists.assert_called_once()
#
#     @patch('runmd.config.get_default_config_path')
#     @patch('pathlib.Path.exists')
#     @patch('configparser.ConfigParser.read')
#     def test_load_config_invalid_file(self, mock_read, mock_exists, mock_get_default_config_path):
#         # Simulate config file exists
#         mock_exists.return_value = True
#         mock_get_default_config_path.return_value = Path("/mock/path/config.ini")
#
#         # Simulate an error when reading the config file
#         mock_read.side_effect = configparser.Error("Mock parsing error")
#
#         # Expect ValueError to be raised
#         with self.assertRaises(ValueError):
#             load_config()
#
#         mock_exists.assert_called_once()
#
#     # --------------------------------------------------
#     # >> VALIDATE_LANG_SECTION
#     # --------------------------------------------------
#
#     def test_validate_lang_section_success(self):
#         # Valid section
#         section = {
#             'aliases': 'python, py',
#             'command': 'python3',
#             'options': '-c'
#         }
#
#         # No exception should be raised for a valid section
#         try:
#             _validate_lang_section(section)
#         except ValueError as e:
#             self.fail(f"Unexpected ValueError raised: {e}")
#
#     def test_validate_lang_section_missing_keys(self):
#         # Missing 'aliases'
#         section = {
#             'command': 'python3',
#             'options': '-c'
#         }
#         with self.assertRaises(ValueError) as cm:
#             _validate_lang_section(section)
#         self.assertIn("missing the 'aliases' field", str(cm.exception))
#
#         # Missing 'command'
#         section = {
#             'aliases': 'python, py',
#             'options': '-c'
#         }
#         with self.assertRaises(ValueError) as cm:
#             _validate_lang_section(section)
#         self.assertIn("missing the 'command' field", str(cm.exception))
#
#         # Missing 'options'
#         section = {
#             'aliases': 'python, py',
#             'command': 'python3'
#         }
#         with self.assertRaises(ValueError) as cm:
#             _validate_lang_section(section)
#         self.assertIn("missing the 'options' field", str(cm.exception))
#
#     def test_validate_lang_section_invalid_aliases(self):
#         # Invalid 'aliases': not a string
#         section = {
#             'aliases': None,
#             'command': 'python3',
#             'options': '-c'
#         }
#         with self.assertRaises(ValueError) as cm:
#             _validate_lang_section(section)
#         self.assertIn("invalid 'aliases' field", str(cm.exception))
#
#         # Invalid 'aliases': empty string
#         section = {
#             'aliases': '',
#             'command': 'python3',
#             'options': '-c'
#         }
#         with self.assertRaises(ValueError) as cm:
#             _validate_lang_section(section)
#         self.assertIn("invalid 'aliases' field", str(cm.exception))
#
#     def test_validate_lang_section_invalid_command(self):
#         # Invalid 'command': not a string
#         section = {
#             'aliases': 'python, py',
#             'command': None,
#             'options': '-c'
#         }
#         with self.assertRaises(ValueError) as cm:
#             _validate_lang_section(section)
#         self.assertIn("invalid 'command' field", str(cm.exception))
#
#         # Invalid 'command': empty string
#         section = {
#             'aliases': 'python, py',
#             'command': '',
#             'options': '-c'
#         }
#         with self.assertRaises(ValueError) as cm:
#             _validate_lang_section(section)
#         self.assertIn("invalid 'command' field", str(cm.exception))
#
#     def test_validate_lang_section_invalid_options(self):
#         # Invalid 'options': not a string
#         section = {
#             'aliases': 'python, py',
#             'command': 'python3',
#             'options': None
#         }
#         with self.assertRaises(ValueError) as cm:
#             _validate_lang_section(section)
#         self.assertIn("invalid 'options' field", str(cm.exception))
#
#     # --------------------------------------------------
#     # >> GET_ALL_ALIASES
#     # --------------------------------------------------
#
#     def test_get_all_aliases_single_section(self):
#         # Setup a config with a single section
#         self.config.add_section('lang.python')
#         self.config.set('lang.python', 'aliases', 'py, python')
#
#         # Call the function and check the result
#         result = get_all_aliases(self.config)
#         expected = ['py', 'python']
#         self.assertEqual(result, expected)
#
#     def test_get_all_aliases_multiple_sections(self):
#         # Setup a config with multiple sections
#         self.config.add_section('lang.python')
#         self.config.set('lang.python', 'aliases', 'py, python')
#
#         self.config.add_section('lang.bash')
#         self.config.set('lang.bash', 'aliases', 'bash')
#
#         self.config.add_section('lang.javascript')
#         self.config.set('lang.javascript', 'aliases', 'js, javascript, node')
#
#         # Call the function and check the result
#         result = get_all_aliases(self.config)
#         expected = ['py', 'python', 'bash', 'js', 'javascript', 'node']
#         self.assertEqual(result, expected)
#
#     def test_get_all_aliases_empty_aliases(self):
#         # Setup a config with a section but no aliases
#         self.config.add_section('lang.python')
#         self.config.set('lang.python', 'aliases', '')
#
#         # Call the function and check the result
#         result = get_all_aliases(self.config)
#         expected = []
#         self.assertEqual(result, expected)
#
#     def test_get_all_aliases_no_lang_sections(self):
#         # Setup a config with no 'lang.' sections
#         self.config.add_section('other_section')
#         self.config.set('other_section', 'aliases', 'something')
#
#         # Call the function and check the result
#         result = get_all_aliases(self.config)
#         expected = []  # No aliases should be returned since there are no 'lang.' sections
#         self.assertEqual(result, expected)

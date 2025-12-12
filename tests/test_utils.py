"""Comprehensive tests for bot utility functions."""
import pytest
from unittest.mock import Mock, patch, mock_open
from bot.utils import load_config


class TestLoadConfig:
    """Test configuration loading functionality."""

    def test_load_config_success(self):
        """Test successful configuration loading."""
        mock_config_content = """
[constants]
zoom_steps = 5

[coordinates]
compass_position = (100, 200)
inventory_slot_1 = (300, 400)
"""
        with patch('builtins.open', mock_open(read_data=mock_config_content)):
            config = load_config('test_config.ini')
            
            assert config['zoom_steps'] == 5
            assert config['compass_coordinates'] == (100, 200)
            assert config['thieve_coordinates'] == (300, 400)

    def test_load_config_missing_section(self):
        """Test error when required section is missing."""
        mock_config_content = """
[constants]
zoom_steps = 5
"""
        with patch('builtins.open', mock_open(read_data=mock_config_content)):
            with pytest.raises(KeyError, match="Missing required sections"):
                load_config('test_config.ini')

    def test_load_config_missing_constants_section(self):
        """Test error when constants section is missing."""
        mock_config_content = """
[coordinates]
compass_position = (100, 200)
inventory_slot_1 = (300, 400)
"""
        with patch('builtins.open', mock_open(read_data=mock_config_content)):
            with pytest.raises(KeyError, match="Missing required sections"):
                load_config('test_config.ini')

    def test_load_config_missing_key(self):
        """Test error when required key is missing."""
        mock_config_content = """
[constants]
zoom_steps = 5

[coordinates]
compass_position = (100, 200)
"""
        with patch('builtins.open', mock_open(read_data=mock_config_content)):
            with pytest.raises(KeyError, match="Missing key"):
                load_config('test_config.ini')

    def test_load_config_invalid_integer(self):
        """Test error when integer value is invalid."""
        mock_config_content = """
[constants]
zoom_steps = invalid

[coordinates]
compass_position = (100, 200)
inventory_slot_1 = (300, 400)
"""
        with patch('builtins.open', mock_open(read_data=mock_config_content)):
            with pytest.raises(ValueError, match="Invalid value"):
                load_config('test_config.ini')

    def test_load_config_invalid_tuple_format(self):
        """Test error when tuple format is invalid."""
        mock_config_content = """
[constants]
zoom_steps = 5

[coordinates]
compass_position = (100, abc)
inventory_slot_1 = (300, 400)
"""
        with patch('builtins.open', mock_open(read_data=mock_config_content)):
            with pytest.raises(ValueError, match="Invalid value"):
                load_config('test_config.ini')

    def test_load_config_coordinate_parsing(self):
        """Test correct parsing of coordinate tuples."""
        mock_config_content = """
[constants]
zoom_steps = 3

[coordinates]
compass_position = (150, 250)
inventory_slot_1 = (350, 450)
"""
        with patch('builtins.open', mock_open(read_data=mock_config_content)):
            config = load_config('test_config.ini')
            
            assert isinstance(config['compass_coordinates'], tuple)
            assert len(config['compass_coordinates']) == 2
            assert config['compass_coordinates'][0] == 150
            assert config['compass_coordinates'][1] == 250

    def test_load_config_different_zoom_values(self):
        """Test loading different zoom step values."""
        for zoom_value in [1, 5, 10, 20]:
            mock_config_content = f"""
[constants]
zoom_steps = {zoom_value}

[coordinates]
compass_position = (100, 200)
inventory_slot_1 = (300, 400)
"""
            with patch('builtins.open', mock_open(read_data=mock_config_content)):
                config = load_config('test_config.ini')
                assert config['zoom_steps'] == zoom_value

    def test_load_config_with_spaces_in_tuples(self):
        """Test parsing tuples with extra spaces."""
        mock_config_content = """
[constants]
zoom_steps = 5

[coordinates]
compass_position = ( 100 , 200 )
inventory_slot_1 = (  300  ,  400  )
"""
        with patch('builtins.open', mock_open(read_data=mock_config_content)):
            config = load_config('test_config.ini')
            
            assert config['compass_coordinates'] == (100, 200)
            assert config['thieve_coordinates'] == (300, 400)

    def test_load_config_returns_dict(self):
        """Test that load_config returns a dictionary."""
        mock_config_content = """
[constants]
zoom_steps = 5

[coordinates]
compass_position = (100, 200)
inventory_slot_1 = (300, 400)
"""
        with patch('builtins.open', mock_open(read_data=mock_config_content)):
            config = load_config('test_config.ini')
            
            assert isinstance(config, dict)
            assert set(config.keys()) == {'zoom_steps', 'compass_coordinates', 'thieve_coordinates'}

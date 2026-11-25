import pytest
from bot import config as bot_config


def test_shipped_config_has_expected_sections():
    assert "coordinates" in bot_config.config
    assert "constants" in bot_config.config
    assert "logger" in bot_config.config
    assert "tesseract" in bot_config.config


def test_zoom_steps_is_50():
    assert bot_config.config["constants"].getint("zoom_steps") == 50


def test_coordinate_points_split_into_two_ints():
    point_keys = [
        "inventory_icon",
        "inventory_slot_1",
        "stall_position",
        "compass_position",
    ]
    for key in point_keys:
        value = bot_config.config["coordinates"][key]
        parts = [p.strip() for p in value.split(",")]
        assert len(parts) == 2, f"{key} should have 2 parts, got {parts}"
        assert all(p.isdigit() for p in parts), f"{key} parts should be integers, got {parts}"


def test_chat_region_splits_into_four_ints():
    value = bot_config.config["coordinates"]["chat_region"]
    parts = [p.strip() for p in value.split(",")]
    assert len(parts) == 4, f"chat_region should have 4 parts, got {parts}"
    assert all(p.isdigit() for p in parts), f"chat_region parts should be integers, got {parts}"


def test_load_config_missing_file_returns_empty_parser():
    parser = bot_config.load_config("does_not_exist.ini")
    assert parser.sections() == []


def test_load_config_reads_relative_to_bot_folder(tmp_path, monkeypatch):
    monkeypatch.setattr(bot_config, "__file__", str(tmp_path / "config.py"))
    custom_ini = tmp_path / "custom.ini"
    custom_ini.write_text("[x]\nkey = value\n")
    parser = bot_config.load_config("custom.ini")
    assert parser["x"]["key"] == "value"
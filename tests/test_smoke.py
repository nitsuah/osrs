def test_imports():
    import importlib
    # Import modules that do not require a GUI/display
    assert importlib.import_module('bot.utils')

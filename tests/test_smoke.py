def test_imports():
    import importlib
    assert importlib.import_module('bot.utils')
    assert importlib.import_module('bot.core')

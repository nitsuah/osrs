# GitHub Copilot Instructions

This file provides custom instructions to GitHub Copilot when working in this repository.

## Project Context

**Project Name:** osrs
**Description:** A lazy old school runescape bot.
**Tech Stack:** Python

## Code Style & Conventions

### General Guidelines

- Follow PEP 8 style guidelines for Python.
- Use descriptive variable and function names.
- Add comments to explain complex logic.
- Keep functions short and focused.

### Python-Specific Guidelines

- Use type hints for function arguments and return values.
- Use docstrings to document functions and classes.
- Handle exceptions gracefully.
- Prefer list comprehensions and generators where appropriate.

### File Organization

- Group related bot functionality into separate modules (e.g., `fishing.py`, `mining.py`).
- Create a `utils.py` module for utility functions used across multiple modules.
- Organize images and data files in a dedicated `data/` directory.
- Place configuration files in a dedicated `config/` directory.

## Architecture Patterns

### Bot Logic

- Implement bot tasks as state machines.
- Use a main loop to orchestrate the bot's actions.
- Implement error handling and retry mechanisms.
- Allow for user configuration of bot parameters (e.g., location, items).

### Example: Good vs. Bad

**Good:**

```python
def fish(location: str = "Barbarian Village") -> bool:
    """Fishes at the specified location.

    Args:
        location: The location to fish at. Defaults to "Barbarian Village".

    Returns:
        True if fishing was successful, False otherwise.
    """
    try:
        # Logic to move to the fishing spot
        move_to(location)
        # Logic to start fishing
        start_fishing()
        return True
    except Exception as e:
        print(f"Error fishing at {location}: {e}")
        return False
```

**Bad:**

```python
def fish(location):
    #go fish
    #error?
    return True
```

## Testing Strategy

- Write unit tests for core bot functions.
- Use mocks to simulate game interactions.
- Focus tests on critical logic and error handling.
- Aim for high test coverage.

## Security Considerations

- Do not hardcode credentials or API keys.
- Use environment variables for sensitive information.
- Be aware of the game's anti-botting measures.
- Avoid actions that could lead to account bans.

## Performance Guidelines

- Optimize image recognition algorithms.
- Minimize CPU usage.
- Avoid unnecessary API calls.
- Use efficient data structures.

## Documentation Requirements

- Document all bot functions and modules.
- Provide instructions on how to configure and run the bot.
- Keep the README.md file up-to-date.

## Common Pitfalls to Avoid

- Hardcoding coordinates or item IDs.
- Ignoring game updates that break the bot.
- Overly aggressive botting behavior.
- Committing sensitive information to the repository.
- Using sleep() instead of event-driven programming.

## Preferred Libraries & Tools

- OpenCV for image recognition.
- PyAutoGUI for mouse and keyboard automation.
- NumPy for numerical operations.
- [TODO: Specific library for OSRS API, if applicable]
- pytest for testing.

## Additional Context

- [TODO: Link to OSRS Wiki for game information]
- [TODO: Information on specific botting techniques to avoid]
- [TODO: Team conventions regarding bot behavior and ethics]

### Commit Conventions

- Use conventional commits (e.g., `feat: Add fishing functionality`, `fix: Handle error when no fish are caught`).
- Keep commit messages concise and descriptive.
- Separate subject from body with a blank line.
- Limit subject line to 50 characters.

---

**Note:** These instructions help GitHub Copilot provide more relevant and consistent suggestions. Update this file as project conventions evolve.
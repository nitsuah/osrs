# Contributing to osrs

Thank you for your interest in contributing! We welcome contributions from everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Issues](#issues)
- [Pull Requests](#pull-requests)
- [Branching](#branching)
- [Commit Messages](#commit-messages)
- [Testing](#testing)
- [Linting](#linting)
- [Releases](#releases)

## 🤝 Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [maintainer@email.com]. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/osrs.git
   cd osrs
   ```
3. **Add the upstream repository**:
   ```bash
   git remote add upstream https://github.com/nitsuah/osrs.git
   ```
4. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 💡 How to Contribute

### Types of Contributions

- **Bug fixes**: Fix issues or problems in the codebase
- **New features**: Add new functionality or capabilities
- **Documentation**: Improve or add to project documentation
- **Tests**: Add or improve test coverage
- **Performance**: Optimize existing code
- **Refactoring**: Improve code quality without changing functionality

### Before You Start

- Check existing [issues](../../issues) and [pull requests](../../pulls) to avoid duplicate work
- For major changes, please open an issue first to discuss what you would like to change
- Make sure your code follows the project's coding standards

## 🛠️ Development Setup

### Prerequisites

- Python 3.7+

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Running the Bot

```bash
python main.py
```

## 🔄 Pull Request Process

1. **Update your branch** with the latest upstream changes:

   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Make your changes** following the coding standards

3. **Test your changes** thoroughly:
   - Run all existing tests
   - Add new tests for new features
   - Ensure all tests pass

4. **Commit your changes** with clear, descriptive messages:

   ```bash
   git commit -m "feat: add new feature description"
   ```

   Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `test:` for adding or updating tests
   - `refactor:` for code refactoring
   - `chore:` for maintenance tasks

5. **Push to your fork**:

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** on GitHub:
   - Provide a clear title and description
   - Reference any related issues
   - Ensure CI checks pass

7. **Respond to feedback** from maintainers and update as needed

## 📝 Coding Standards

### General Guidelines

- Write clean, readable, and maintainable code
- Follow the existing code style and conventions
- Add comments for complex logic
- Keep functions small and focused
- Use meaningful variable and function names

### Python Specific Standards

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions and classes

### Testing

- Write unit tests for new functions
- Aim for reasonable code coverage
- Test edge cases and error conditions

### Documentation

- Update README.md for new features
- Add docstring comments for public APIs
- Include inline comments for complex logic

## 🐛 Reporting Bugs

When reporting bugs, please include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Screenshots or error messages** if applicable
- **Environment details**: OS, Python version, etc.

Use the [bug report template](../../issues/new?template=bug_report.md) if available.

## 💡 Suggesting Features

When suggesting features, please include:

- **Clear title and description**
- **Use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternatives considered**: Other approaches you've thought about

Use the [feature request template](../../issues/new?template=feature_request.md) if available.

## Issues

- Use [GitHub Issues](../../issues) to report bugs, suggest enhancements, or ask questions.
- Search existing issues before creating a new one to avoid duplicates.
- Provide as much detail as possible when creating a new issue.

## Pull Requests

- Pull requests are the primary mechanism for contributing code.
- Ensure your code adheres to the coding standards.
- Include tests for new features and bug fixes.
- Address any feedback provided during the review process.

## Branching

- Use descriptive branch names, such as `feature/new-feature` or `fix/bug-description`.
- Base your branch off the `main` branch.
- Keep your branch up-to-date with `main` by rebasing.

## Commit Messages

- Write clear and concise commit messages.
- Use the imperative mood (e.g., "Add feature" instead of "Added feature").
- Include a brief summary of the changes in the first line.
- Optionally, include a more detailed explanation in the body of the commit message.

## Testing

- Write unit tests using `unittest` or `pytest`.
- Ensure all tests pass before submitting a pull request.
- Aim for high code coverage.

## Linting

- Use a linter like `pylint` or `flake8` to ensure code quality.
  ```bash
  # Example using flake8
  pip install flake8
  flake8 .
  ```
- Address any linting errors before submitting a pull request.

## Releases

- Releases are managed by the maintainers.
- New features and bug fixes will be included in upcoming releases.
- Release notes will be published with each release.

## 🙏 Recognition

Contributors will be recognized in:

- The project README
- Release notes for significant contributions
- The [CONTRIBUTORS](CONTRIBUTORS.md) file (if applicable)

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## 📧 Questions?

If you have questions, feel free to:

- Open an issue with the `question` label
- Contact the maintainers at [TODO: CONTACT_EMAIL]

Thank you for contributing! 🎉
# Contributing to SerialTalk

Thank you for your interest in contributing to SerialTalk!

## How to Contribute

### Reporting Issues

- Check if the issue already exists in [GitHub Issues](https://github.com/antonvh/SerialTalk/issues)
- Use the issue template if provided
- Include:
  - Clear description of the problem
  - Steps to reproduce
  - Expected vs actual behavior
  - Platform/device information
  - Python/MicroPython version

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test your changes thoroughly
5. Update documentation if needed
6. Commit with clear messages: `git commit -m "Add feature: description"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Open a Pull Request

### Development Setup

See [DEVELOPER.md](DEVELOPER.md) for detailed setup instructions.

Quick start:

```bash
git clone https://github.com/antonvh/SerialTalk.git
cd SerialTalk
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### Code Style

- Follow PEP 8 guidelines
- Use Black for formatting: `black serialtalk/`
- Check with flake8: `flake8 serialtalk/`
- Maximum line length: 100 characters

### Testing

- Write tests for new features
- Ensure existing tests pass
- Test on multiple platforms if possible (MicroPython, Python 3.x)
- Run tests: `pytest`

### Documentation

- Update README.md for user-facing changes
- Update docstrings for code changes
- Follow Google-style docstrings
- Build docs locally: `cd docs && make html`

### Commit Messages

Use clear, descriptive commit messages:

- `Add: New feature description`
- `Fix: Bug fix description`
- `Update: Documentation/dependency updates`
- `Refactor: Code improvements`
- `Test: Test additions/changes`

### Platform Support

SerialTalk supports multiple platforms:

- MicroPython (ESP32, ESP8266, PyBoard, OpenMV, K210)
- Python 3.7+
- Pybricks
- LEGO SPIKE Prime

When adding features, consider compatibility across platforms.

### Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on the best solution, not ego
- Help others learn and grow

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to:

- Open a discussion in GitHub Discussions
- Contact the maintainers
- Ask in the pull request/issue

Thank you for contributing to SerialTalk! 🚀

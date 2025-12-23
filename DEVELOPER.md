# Developer Guide

## Building and Publishing SerialTalk

This guide covers how to build and publish the SerialTalk package to PyPI.

## Prerequisites

- Python 3.7 or higher
- Git

## Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/antonvh/SerialTalk.git
   cd SerialTalk
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install in development mode:

   ```bash
   pip install -e ".[dev]"
   ```

## Building the Package

### Using the build script (Recommended)

```bash
chmod +x build.sh
./build.sh
```

### Manual build

1. Install build tools:

   ```bash
   pip install build twine
   ```

2. Clean previous builds:

   ```bash
   rm -rf dist/ build/ *.egg-info
   ```

3. Build the package:

   ```bash
   python -m build
   ```

This creates both source distribution (.tar.gz) and wheel (.whl) files in the `dist/` directory.

## Testing the Package Locally

Install the built package locally:

```bash
pip install dist/serialtalk-1.0.0-py3-none-any.whl
```

## Publishing to PyPI

### First time setup

1. Create accounts on:
   - Test PyPI: <https://test.pypi.org/account/register/>
   - PyPI: <https://pypi.org/account/register/>

2. Create API tokens:
   - Test PyPI: <https://test.pypi.org/manage/account/token/>
   - PyPI: <https://pypi.org/manage/account/token/>

3. Configure credentials in `~/.pypirc`:

   ```ini
   [distutils]
   index-servers =
       pypi
       testpypi

   [pypi]
   username = __token__
   password = pypi-YOUR-API-TOKEN-HERE

   [testpypi]
   repository = https://test.pypi.org/legacy/
   username = __token__
   password = pypi-YOUR-TEST-API-TOKEN-HERE
   ```

### Upload to Test PyPI (Recommended first)

```bash
python -m twine upload --repository testpypi dist/*
```

Test the installation:

```bash
pip install --index-url https://test.pypi.org/simple/ serialtalk
```

### Upload to Production PyPI

```bash
python -m twine upload dist/*
```

## Version Management

The version is defined in three places and must be kept in sync:

- `pyproject.toml` - Main version for PyPI
- `serialtalk/__init__.py` - `__version__` variable
- `package.json` - Version for mip (MicroPython)

To release a new version:

1. Update the version number in all three files
2. Commit the changes:

   ```bash
   git add pyproject.toml serialtalk/__init__.py package.json
   git commit -m "Bump version to X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

3. Build and publish as described above

## Package Structure

``` text
SerialTalk/
├── serialtalk/          # Main package directory
│   ├── __init__.py      # Package initialization with version info
│   ├── serialtalk.py    # Core SerialTalk class
│   ├── auto.py          # Auto-detection for platforms
│   ├── sockets.py       # Socket communication
│   └── ...              # Platform-specific modules
├── pyproject.toml       # Modern Python package metadata
├── setup.py             # Backwards compatibility setup
├── package.json         # MicroPython mip metadata
├── MANIFEST.in          # Additional files to include
├── LICENSE              # MIT License
├── README.md            # User documentation
└── docs/                # Sphinx documentation
```

## Running Tests

```bash
pytest
```

## Code Formatting

Format code with Black:

```bash
black serialtalk/
```

Check code style:

```bash
flake8 serialtalk/
```

## Building Documentation

```bash
cd docs
make html
```

Documentation will be in `docs/_build/html/`.

## Continuous Integration

Consider setting up GitHub Actions for:

- Automated testing on multiple Python versions
- Automated publishing on tagged releases
- Documentation building and deployment

## Support

For issues and questions:

- GitHub Issues: <https://github.com/antonvh/SerialTalk/issues>
- Email: <anton@antonsmindstorms.com>

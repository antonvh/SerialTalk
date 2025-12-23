#!/bin/bash
# Build and test the package locally
# Usage: ./build.sh

set -e

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists, skipping creation..."
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing build dependencies..."
pip install build twine

echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info

echo "Building package..."
python -m build

echo ""
echo "Build complete! Distribution files:"
ls -lh dist/

echo ""
echo "To upload to PyPI:"
echo "  python -m twine upload dist/*"
echo ""
echo "To upload to Test PyPI first:"
echo "  python -m twine upload --repository testpypi dist/*"
echo ""
echo "To install locally:"
echo "  pip install dist/serialtalk-1.0.0-py3-none-any.whl"

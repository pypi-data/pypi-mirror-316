# Anyparser Deployment on PyPI

## Prerequisites

### Github Repository
Optional

### Sign Up Link
https://pypi.org/account/register/

## How to Deploy Anyparser on PyPI

1. Install build tools:
   ```bash
   python -m pip install --upgrade pip
   python -m pip install --upgrade build twine
   ```

2. Build the distribution:
   ```bash
   python -m build
   ```
   This will create both wheel and source distribution in the `dist/` directory

3. Test your package on TestPyPI (optional but recommended):
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```

4. Upload to PyPI:
   ```bash
   python -m twine upload dist/*
   ```

## Project Structure
```
anyparser/
├── pyproject.toml
├── README.md
├── anyparser_core/
│   └── __init__.py
└── deployment.md
```

## Notes
- Before uploading, make sure you have a PyPI account and verify your email
- Store your PyPI API token securely
- Consider using GitHub Actions for automated deployment
 
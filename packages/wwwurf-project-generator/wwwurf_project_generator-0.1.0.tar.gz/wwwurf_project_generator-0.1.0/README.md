# WWWURF Project Generator

A command-line tool for generating structured multi-package Python projects using Poetry.

## Features

- Creates a structured multi-package Python project
- Generates package scaffolding with Poetry configuration
- Includes testing setup with pytest
- Automatic Git initialization
- Management script for adding new packages

## Installation

```bash
pip install wwwurf-project-generator
```

## Usage

### Creating a new project

```bash
wwwurf-gen create my-project --packages core api database
```

### Adding a new package to an existing project

```bash
wwwurf-gen add-package new-package-name
```

## Project Structure

The generated project will have the following structure:

```
my-project/
├── main_app/
│   ├── __init__.py
│   └── main.py
├── packages/
│   ├── core/
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── main.py
│   │   ├── tests/
│   │   ├── pyproject.toml
│   │   └── README.md
│   └── [other-packages]/
├── pyproject.toml
├── README.md
├── .gitignore
└── manage.py
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

WorldWideWurf (worldwidewurf@gmail.com)
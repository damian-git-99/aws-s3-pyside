# Bucket Browser

A PySide6 desktop application for browsing S3 bucket contents with a modern, intuitive interface.

## Features

- Browse bucket objects with a clean, modern UI
- View files and folders with appropriate icons by file type
- Sortable columns: Name, Size, Last Modified, Storage Class
- Mock data for development and testing
- Follows MVP (Model-View-Presenter) architecture pattern

## Architecture

This project uses the **Model-View-Presenter (MVP)** pattern for clean separation of concerns:

- **Models**: Handle data and business logic
- **Views**: Display data and capture user events (passive)
- **Presenters**: Coordinate between Models and Views

See [AGENTS.md](AGENTS.md) for detailed MVP documentation.

## Requirements

- Python 3.8+
- PySide6
- uv (for package management)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd pyside-crud
```

2. Install dependencies with uv:
```bash
uv pip install -r requirements.txt
# or
uv add PySide6
```

## Running the Application

```bash
# Desde el directorio raíz del proyecto
uv run python -m src.main
```

## Running Tests

```bash
# Run all tests
uv run python -m unittest discover src/tests/

# Run specific test file
uv run python -m unittest src.tests.test_bucket_browser_presenter
uv run python -m unittest src.tests.test_data_loading
uv run python -m unittest src.tests.test_file_icons
```

## Project Structure

```
pyside-crud/
├── src/                    # Source code
│   ├── mvp/               # MVP framework classes
│   ├── models/            # Data models
│   ├── views/             # UI views
│   ├── presenters/        # Presenters
│   ├── utils/             # Utilities
│   ├── tests/             # Test files
│   └── main.py            # Entry point
├── README.md
└── AGENTS.md              # MVP documentation
```

## Development

### Adding New Features

When adding new features, follow the MVP pattern:

1. Create or update the Model in `src/models/`
2. Create or update the View in `src/views/`
3. Create or update the Presenter in `src/presenters/`
4. Write tests in `src/tests/`

**Important**: All imports must use the `src.` prefix (e.g., `from src.mvp.base_model import BaseModel`).

See [AGENTS.md](AGENTS.md) for detailed guidelines and examples.

## License

MIT License

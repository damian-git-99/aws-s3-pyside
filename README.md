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

## Configuration

The application uses SQLite for persistent configuration storage. Settings are stored in your user data directory:
- **Linux/macOS**: `~/.config/BucketBrowser/config.db`
- **Windows**: `%APPDATA%/BucketBrowser/config.db`

### First-Time Setup

On first launch, the application will show a setup wizard to configure your AWS credentials:

1. Enter your AWS credentials in the setup wizard
2. Click "Finish" to save the configuration
3. The settings are persisted and will be remembered on subsequent launches

### Changing Settings

You can modify settings at any time:
- Click the **Settings** button in the toolbar
- Update your AWS credentials in the settings panel
- Click **Save** to persist changes

### Configuration Details

The following settings are stored:
- `AWS_ACCESS_KEY_ID`: Your AWS access key ID
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key  
- `AWS_DEFAULT_REGION`: AWS region (e.g., `us-east-1`)
- `AWS_S3_BUCKET_NAME`: Your S3 bucket name

**Security Warning**: Credentials are stored locally in a SQLite database. Ensure your user data directory is secure and not shared.

## Running the Application

```bash
# Desde el directorio raíz del proyecto
uv run python -m src.main
```

## Building the Executable

To create a standalone executable for distribution:

```bash
# Install dev dependencies (includes PyInstaller)
uv pip install -r requirements.txt

# Build the executable
uv run python build.py

# Or with optional output directory
uv run python build.py --distpath ./release
```

The executable will be created in `dist/s3-bucket-browser` (or your custom `--distpath`).

### Build Output

- **Windows**: `dist/s3-bucket-browser.exe`
- **Linux**: `dist/s3-bucket-browser`
- **macOS**: `dist/s3-bucket-browser.app`

The executable is a single file (~91MB) that includes Python and all dependencies.

### Troubleshooting

**Platform plugin not found**
If you get an error about missing Qt platform plugins, ensure PySide6 plugins are properly bundled. The spec file includes hooks to collect these automatically.

**Antivirus false positives**
Some antivirus software may flag PyInstaller executables. This is a known issue - code signing can help reduce false positives.

**Large file size**
The executable bundles Python and PySide6, resulting in ~91MB. Use UPX compression to reduce size if needed (enabled by default).

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

## Automated Releases

This project uses **semantic-release** and **GitHub Actions** for automated versioning and cross-platform builds.

### Release Process

1. Ensure your commits follow the [Conventional Commits](https://www.conventionalcommits.org/) format:
   - `feat:` - New features (minor version bump)
   - `fix:` - Bug fixes (patch version bump)
   - `BREAKING CHANGE:` or `!` - Breaking changes (major version bump)

2. To create a release:
   - Go to the **Actions** tab in GitHub
   - Select the **Release** workflow
   - Click **Run workflow**
   - The workflow will:
     - Calculate the next version based on commits
     - Create a GitHub release with auto-generated notes
     - Build executables for Windows and Linux
     - Attach executables to the release

3. Download the executables from the GitHub release page:
   - `pyside-crud-vX.X.X-windows.exe` - Windows executable
   - `pyside-crud-vX.X.X-linux` - Linux binary

### Manual Testing

Before triggering a release, you can test the build locally:

```bash
# Install PyInstaller
uv pip install pyinstaller

# Build executable
pyinstaller pyside-crud.spec

# Test the executable
dist/pyside-crud
```

## License

MIT License

## Why

Currently, the application can only be run from source with Python installed, which creates friction for end users. Creating a standalone executable with PyInstaller will allow users to run the application without installing Python or dependencies, significantly improving distribution and user experience.

## What Changes

- Add PyInstaller as a development dependency
- Create a `.spec` file configured for single-file executable generation with PySide6 support
- Add build scripts for easy executable generation
- Configure hidden imports and data files for proper bundling
- Add documentation for building and distributing the executable

## Capabilities

### New Capabilities
- `pyinstaller-build`: Single-file executable generation with PyInstaller including PySide6 GUI bundling and proper resource handling

### Modified Capabilities
- None - this is a build tooling addition that doesn't change runtime behavior

## Impact

- **Dependencies**: Add `pyinstaller` to dev dependencies
- **Build Process**: New build scripts and spec file configuration
- **Distribution**: Users can receive a single `.exe` (Windows) or binary (Linux/Mac) file
- **File Structure**: New `build/` directory added to `.gitignore`

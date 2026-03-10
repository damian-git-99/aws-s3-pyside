## Context

This is a PySide6 MVP application (S3 bucket browser) that currently requires Python and all dependencies to be installed to run. The project uses `uv` for package management and follows a Model-View-Presenter architecture pattern.

Current runtime command: `uv run python -m src.main`

PyInstaller will bundle Python interpreter, dependencies, and application code into a single executable that can run without Python installed on the target system.

## Goals / Non-Goals

**Goals:**
- Generate a single-file executable for Windows, Linux, and macOS
- Properly bundle PySide6 GUI dependencies including Qt plugins
- Include all necessary hidden imports for the MVP architecture
- Provide simple build scripts for developers
- Ensure the executable works identically to running from source

**Non-Goals:**
- Code signing (out of scope for this change)
- Auto-updater functionality
- Custom installer creation (the executable itself is sufficient)
- Obfuscation or anti-tampering measures

## Decisions

### 1. Use pyi-makespec for initial spec generation
**Rationale**: Using `pyi-makespec` generates a proper `.spec` file template that can be customized rather than using complex command-line options. The spec file allows:
- Precise control over hidden imports
- Data file bundling configuration
- Custom hooks for PySide6 plugins

**Alternative considered**: Command-line only approach with `--onefile` flag. Rejected because it's harder to maintain complex configurations.

### 2. Single-file executable (--onefile)
**Rationale**: Simpler distribution - users get one file to run. PyInstaller extracts to temp on first run.

**Alternative considered**: One-directory mode (--onedir). Rejected because it requires distributing a folder which is less user-friendly.

### 3. Include PySide6 plugins via Analysis datas
**Rationale**: PySide6 requires platform plugins (qwindows.dll on Windows, etc.) to be available. These need explicit inclusion in the spec file via the `datas` parameter of the Analysis object.

### 4. Use uv for dependency management during build
**Rationale**: Project already uses `uv`. The build script will use `uv run pyinstaller` to ensure consistent environment.

## Risks / Trade-offs

**Longer startup time** → PyInstaller onefile executables extract to a temp directory on first run. This adds ~1-2 seconds to initial startup. **Mitigation**: Acceptable trade-off for distribution simplicity.

**Larger file size** → Single executable will be ~50-100MB due to bundling Python + PySide6. **Mitigation**: This is expected for Python GUI applications; consider UPX compression.

**Antivirus false positives** → Some antivirus software may flag PyInstaller executables. **Mitigation**: Document this possibility; code signing in future would help.

**Qt platform plugin issues** → PySide6 executables sometimes fail with "platform plugin not found". **Mitigation**: Properly configure datas in spec file to include qwindows/qxcb plugins.

**Hidden import misses** → Dynamic imports in Python may not be detected automatically. **Mitigation**: Test thoroughly and add any missing imports to hiddenimports in spec.

## Context

This is a new PySide6 desktop application project for managing files in AWS S3. The initial phase focuses on setting up the project structure and creating a working main window.

## Goals / Non-Goals

**Goals:**
- Set up Python project with PySide6 dependency
- Create minimal project structure (src/, tests/)
- Implement main window that opens successfully
- Verify dependencies install correctly

**Non-Goals:**
- S3 integration (future phase)
- Advanced UI components (future phase)
- Authentication handling (future phase)
- Production build/packaging (future phase)

## Decisions

- **PySide6 over PyQt5**: More modern, better maintained, commercial-friendly license (LGPL)
- **Python 3.10+ minimum**: Ensures modern Python features and type hints
- **src/ layout**: Follows modern Python packaging best practices
- **pyproject.toml**: Standard Python project configuration (PEP 517/518)
- **uv for environment management**: Fast package manager, creates isolated .venv, no global installs

## Risks / Trade-offs

- **Risk**: PySide6 installation issues on some systems → **Mitigation**: Use official wheel distribution, specify platform-specific requirements if needed
- **Risk**: GUI testing is complex → **Mitigation**: Keep initial window simple for easy manual verification

## 1. Setup and Dependencies

- [x] 1.1 Add pyinstaller to dev dependencies in requirements.txt or pyproject.toml
- [x] 1.2 Add build/ and dist/ directories to .gitignore
- [x] 1.3 Install pyinstaller in the development environment

## 2. PyInstaller Configuration

- [x] 2.1 Create initial spec file using pyi-makespec for src/main.py
- [x] 2.2 Configure Analysis object with hidden imports for src.models, src.views, src.presenters
- [x] 2.3 Add PySide6 platform plugins to datas parameter (qwindows, qxcb, qcocoa)
- [x] 2.4 Configure EXE object for single-file output (--onefile)
- [x] 2.5 Set console=False for GUI application

## 3. Build Scripts

- [x] 3.1 Create build.py script that invokes pyinstaller with the spec file
- [x] 3.2 Add support for uv run in build script
- [x] 3.3 Add command-line argument for output directory (optional)

## 4. Testing and Validation

- [x] 4.1 Test executable builds successfully without errors
- [x] 4.2 Verify executable runs without Python installed (test in clean environment)
- [x] 4.3 Test all application functionality works in executable (file browser, navigation, uploads, etc.)
- [x] 4.4 Verify executable size is reasonable (< 150MB)

## 5. Documentation

- [x] 5.1 Add build instructions to README.md
- [x] 5.2 Document any platform-specific requirements
- [x] 5.3 Add troubleshooting section for common PyInstaller issues

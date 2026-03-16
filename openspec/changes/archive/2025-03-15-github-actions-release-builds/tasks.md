## 1. Semantic Release Configuration

- [x] 1.1 Create `.releaserc.json` with semantic-release configuration for GitHub
- [x] 1.2 Create `package.json` with semantic-release and @semantic-release/github dependencies
- [x] 1.3 Add package-lock.json (run npm install locally to generate)

## 2. GitHub Actions Workflow

- [x] 2.1 Create `.github/workflows/release.yml` with manual trigger (workflow_dispatch)
- [x] 2.2 Configure workflow permissions (contents: write, issues: write, pull-requests: write)
- [x] 2.3 Add Node.js 20 setup step
- [x] 2.4 Add semantic-release execution step with GITHUB_TOKEN
- [x] 2.5 Add version extraction step using git describe

## 3. Cross-Platform Build Jobs

- [x] 2.6 Add Python setup step for both platforms
- [x] 2.7 Add uv installation step
- [x] 2.8 Install Python dependencies with uv
- [x] 2.9 Install PyInstaller
- [x] 2.10 Create Windows build job with PyInstaller
- [x] 2.11 Create Linux build job with PyInstaller
- [x] 2.12 Configure build matrix for parallel execution

## 4. PyInstaller Configuration

- [x] 3.1 Create `pyside-crud.spec` file for PyInstaller configuration
- [x] 3.2 Configure entry point to `src/main.py`
- [x] 3.3 Include all necessary data files and hidden imports
- [x] 3.4 Set up one-file mode for distributable executables

## 5. Artifact Upload

- [x] 3.5 Configure artifact naming with version and platform (pyside-crud-{version}-{platform})
- [x] 3.6 Add artifact upload to GitHub release using semantic-release assets
- [x] 3.7 Ensure Windows executable has .exe extension
- [x] 3.8 Ensure Linux binary has executable permissions

## 6. Testing and Verification

- [x] 4.1 Test workflow in dry-run mode (local or branch)
- [x] 4.2 Verify semantic-release configuration is valid
- [x] 4.3 Test PyInstaller builds locally on development machine
- [x] 4.4 Document release process in README.md

## 7. Final Integration

- [x] 5.1 Commit all configuration files
- [x] 5.2 Create PR for review
- [x] 5.3 Merge to main branch
- [x] 5.4 Trigger first release manually to verify end-to-end workflow

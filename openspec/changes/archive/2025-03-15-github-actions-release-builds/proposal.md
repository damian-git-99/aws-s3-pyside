## Why

Currently, the PySide6 CRUD application requires manual builds and versioning, which is error-prone and time-consuming. We need an automated CI/CD pipeline that handles semantic versioning, creates GitHub releases, and generates cross-platform executables (Windows and Linux) on every release. This will ensure consistent versioning, reduce manual effort, and provide users with easy-to-install binaries.

## What Changes

- Add semantic-release configuration for automated semantic versioning based on conventional commits
- Create GitHub Actions workflow for release automation triggered manually via `workflow_dispatch`
- Implement cross-platform build pipeline generating Windows and Linux executables
- Configure PyInstaller spec files for both platforms to create standalone applications
- Add package.json with semantic-release plugins for GitHub releases
- Update project structure to support CI/CD artifacts and versioning
- Generate release notes automatically from commit messages

## Capabilities

### New Capabilities
- `semantic-release`: Automated semantic versioning and GitHub releases based on conventional commits
- `github-actions-ci`: GitHub Actions workflows for automated builds and releases
- `cross-platform-builds`: Cross-platform executable generation for Windows and Linux using PyInstaller
- `release-artifacts`: Management and attachment of build artifacts to GitHub releases

### Modified Capabilities
- None - this change introduces new infrastructure without modifying existing application behavior

## Impact

- **Dependencies**: New dev dependency on Node.js/npm for semantic-release
- **Project Structure**: New `.github/workflows/` directory, `package.json`, PyInstaller spec files
- **Build Process**: PyInstaller will bundle the application into standalone executables
- **Release Process**: Manual workflow dispatch triggers automated version bump, tag creation, and release
- **Artifacts**: Windows (.exe) and Linux binaries attached to each GitHub release
- **Versioning**: Follows semantic versioning (MAJOR.MINOR.PATCH) based on commit messages

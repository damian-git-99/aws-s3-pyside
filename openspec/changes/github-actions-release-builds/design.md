## Context

This PySide6 CRUD application currently has no automated CI/CD pipeline. Manual versioning and building is error-prone and doesn't provide users with easy access to pre-built executables. We need to implement a complete release automation system using GitHub Actions with semantic-release for versioning and PyInstaller for cross-platform builds.

The project uses:
- PySide6 for the GUI framework
- uv for Python package management
- MVP (Model-View-Presenter) architecture
- AWS S3 integration for storage

## Goals / Non-Goals

**Goals:**
- Automate semantic versioning based on conventional commits
- Create GitHub releases with auto-generated release notes
- Build standalone executables for Windows and Linux
- Attach executables to GitHub releases automatically
- Provide manual workflow trigger for releases

**Non-Goals:**
- macOS builds (not requested, can be added later)
- Docker image builds (user explicitly excluded this)
- Automatic releases on every push (manual trigger only)
- Code signing of executables
- Auto-update functionality in the application

## Decisions

### Decision 1: Use semantic-release with Node.js/npm
**Rationale**: semantic-release is the industry standard for semantic versioning automation. It has excellent GitHub integration and handles the entire release lifecycle (version calculation, tag creation, release notes, asset upload).

**Alternative Considered**: Python-based tools like `python-semantic-release` - rejected because semantic-release has better GitHub Actions integration and more mature plugins.

### Decision 2: Manual workflow_dispatch trigger
**Rationale**: Automatic releases on every push can create too many versions and noise. Manual trigger gives control over when to release and allows batching multiple changes into a single release.

**Alternative Considered**: Automatic releases on merge to main - rejected to avoid version proliferation.

### Decision 3: PyInstaller for executable generation
**Rationale**: PyInstaller is the most mature and widely-used tool for bundling Python applications. It handles PySide6 dependencies well and creates true standalone executables.

**Alternative Considered**: 
- cx_Freeze - less mature PySide6 support
- py2app - macOS only
- Nuitka - more complex, longer build times

### Decision 4: Parallel builds with build matrix
**Rationale**: GitHub Actions matrix strategy allows running Windows and Linux builds concurrently, reducing total release time.

### Decision 5: Separate version extraction step
**Rationale**: After semantic-release creates the tag, we need to extract that version to name our artifacts correctly. Using `git describe` is reliable.

## Risks / Trade-offs

**Risk**: PyInstaller executables may be flagged by antivirus software → Mitigation: This is a known issue with PyInstaller; consider code signing in future if needed

**Risk**: Build times may be long for complex dependencies → Mitigation: Use caching for pip dependencies in GitHub Actions

**Risk**: Windows builds require Windows runner which has limitations → Mitigation: GitHub-hosted Windows runners are sufficient for PyInstaller builds

**Trade-off**: Manual releases mean users don't get immediate access to every fix → Benefit is controlled release cadence and less version noise

## Migration Plan

1. Create `.releaserc.json` with semantic-release configuration
2. Add `package.json` with semantic-release plugins as dev dependencies
3. Create `.github/workflows/release.yml` with the complete workflow
4. Create PyInstaller spec files for Windows and Linux
5. Test workflow in a feature branch (dry-run mode)
6. Merge to main and trigger first release manually

## Open Questions

- Should we include a CHANGELOG.md file or rely solely on GitHub release notes?
- Do we want to support 32-bit Windows builds or only 64-bit?
- Should we include the Python version in the artifact name?

## ADDED Requirements

### Requirement: Automated semantic versioning
The system SHALL automatically determine the next version number based on conventional commit messages following the semantic versioning specification.

#### Scenario: Patch version bump
- **WHEN** a commit with type "fix" is pushed to the main branch
- **THEN** the patch version number SHALL be incremented (e.g., 1.0.0 → 1.0.1)

#### Scenario: Minor version bump
- **WHEN** a commit with type "feat" is pushed to the main branch
- **THEN** the minor version number SHALL be incremented (e.g., 1.0.0 → 1.1.0)

#### Scenario: Major version bump
- **WHEN** a commit with type "BREAKING CHANGE" or "breaking" footer is pushed to the main branch
- **THEN** the major version number SHALL be incremented (e.g., 1.0.0 → 2.0.0)

### Requirement: GitHub release creation
The system SHALL automatically create a GitHub release with release notes when a new version is determined.

#### Scenario: Release creation on version bump
- **WHEN** semantic-release determines a new version is needed
- **THEN** a Git tag SHALL be created with the new version
- **AND** a GitHub release SHALL be created with auto-generated release notes

### Requirement: Conventional commits enforcement
The system SHALL enforce or guide the use of conventional commit format for consistent versioning.

#### Scenario: Commit message format
- **WHEN** developers make commits
- **THEN** commit messages SHALL follow the conventional commits specification (type(scope): subject)

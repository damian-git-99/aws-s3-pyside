# context-menu-file-actions Specification

## Purpose
Right-click context menu for file actions on single file selection.

## ADDED Requirements

### Requirement: Context menu appears on right-click over file
The system SHALL display a context menu when the user right-clicks on a selected file in the table.

#### Scenario: Context menu appears on right-click
- **WHEN** user right-clicks on a table row containing a file
- **THEN** a context menu appears with available file actions
- **AND** the menu is positioned near the cursor

#### Scenario: Context menu shows for selected file
- **WHEN** user has selected a file row and right-clicks anywhere on that row
- **THEN** the context menu appears with actions applicable to that file

### Requirement: Preview action for image files
The system SHALL show a "Preview" option in the context menu only for image files.

#### Scenario: Preview shown for image file
- **WHEN** user right-clicks on a selected image file
- **THEN** "Preview" option appears in the context menu

#### Scenario: Preview hidden for non-image file
- **WHEN** user right-clicks on a selected non-image file
- **THEN** "Preview" option does not appear in the context menu

#### Scenario: Preview hidden for folders
- **WHEN** user right-clicks on a selected folder
- **THEN** "Preview" option does not appear in the context menu

### Requirement: Download action for files
The system SHALL show a "Download" option in the context menu for all files (not folders).

#### Scenario: Download shown for file
- **WHEN** user right-clicks on a selected file
- **THEN** "Download" option appears in the context menu

#### Scenario: Download hidden for folder
- **WHEN** user right-clicks on a selected folder
- **THEN** "Download" option does not appear in the context menu

### Requirement: Generate Link action for files
The system SHALL show a "Generate Link" option in the context menu for all files (not folders).

#### Scenario: Generate Link shown for file
- **WHEN** user right-clicks on a selected file
- **THEN** "Generate Link" option appears in the context menu

#### Scenario: Generate Link hidden for folder
- **WHEN** user right-clicks on a selected folder
- **THEN** "Generate Link" option does not appear in the context menu

### Requirement: Delete action for files
The system SHALL show a "Delete" option in the context menu for all files (not folders).

#### Scenario: Delete shown for file
- **WHEN** user right-clicks on a selected file
- **THEN** "Delete" option appears in the context menu at the bottom (after separator)

#### Scenario: Delete hidden for folder
- **WHEN** user right-clicks on a selected folder
- **THEN** "Delete" option does not appear in the context menu

### Requirement: Delete requires confirmation
The system SHALL require user confirmation before deleting a file.

#### Scenario: Delete shows confirmation dialog
- **WHEN** user clicks "Delete" in the context menu
- **THEN** a confirmation dialog appears asking "Are you sure you want to delete <filename>?"
- **AND** deletion only proceeds if user confirms

### Requirement: Visual hint for context menu availability
The system SHALL show a hint in the status bar when a file is selected.

#### Scenario: Status bar shows hint when file selected
- **WHEN** user selects a file in the table
- **THEN** status bar displays "Right-click for more actions"

#### Scenario: Hint cleared when selection cleared
- **WHEN** user clears the file selection
- **THEN** status bar returns to showing object count

## ADDED Requirements

### Requirement: User can create S3 folder via button
The system SHALL provide a "Create Folder" button in the bucket browser toolbar that opens a dialog for folder name input.

#### Scenario: Button click opens dialog
- **WHEN** user clicks "Create Folder" button
- **THEN** dialog appears with text input field for folder name and Cancel/Create buttons

### Requirement: Folder created in current S3 prefix location
The system SHALL create the S3 folder (prefix) in the currently selected location in the tree (root or selected folder prefix).

#### Scenario: Create folder at root
- **WHEN** user is at root level and enters "data" and clicks Create
- **THEN** folder "data" is created as S3 prefix "data/" in bucket

#### Scenario: Create folder in selected prefix
- **WHEN** user has "uploads/" prefix selected and enters "images" and clicks Create
- **THEN** folder "images" is created as S3 prefix "uploads/images/" in bucket

#### Scenario: Create nested folder
- **WHEN** user has "projects/archive/" selected and enters "2024" and clicks Create
- **THEN** folder "2024" is created as S3 prefix "projects/archive/2024/" in bucket

### Requirement: Folder name validation
The system SHALL validate folder names before creating in S3, rejecting empty names and S3-invalid characters.

#### Scenario: Empty name rejected
- **WHEN** user tries to create folder with empty name
- **THEN** validation error shows and no S3 operation occurs

#### Scenario: Invalid S3 characters rejected
- **WHEN** user enters name with invalid characters (empty string)
- **THEN** validation error shows

#### Scenario: Valid S3 name accepted
- **WHEN** user enters valid folder name (alphanumeric, hyphens, underscores, dots)
- **THEN** folder prefix is created in S3

### Requirement: Tree updates after folder creation
The system SHALL update the bucket browser tree immediately after folder is successfully created in S3.

#### Scenario: New folder appears in tree
- **WHEN** folder is successfully created in S3
- **THEN** new folder immediately appears in tree at correct prefix location

### Requirement: Error handling for folder creation
The system SHALL handle S3 errors (permission denied, connection issues) and display user-friendly error messages.

#### Scenario: Permission denied error
- **WHEN** user attempts to create folder without S3 write permission
- **THEN** error dialog displays indicating permission issues

#### Scenario: Connection error
- **WHEN** AWS connection fails during folder creation
- **THEN** error dialog displays connection error message

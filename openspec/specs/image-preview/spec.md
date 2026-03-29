## Purpose

Image preview functionality for the bucket browser, allowing users to view images stored in S3 without downloading them to the local filesystem.

## Requirements

### Requirement: Preview button visibility
The system SHALL display a "Preview" button in the toolbar when a supported image file is selected.

#### Scenario: Preview button enabled for image file
- **WHEN** user selects a file with extension jpg, jpeg, png, gif, bmp, svg, or webp
- **THEN** the Preview button is enabled

#### Scenario: Preview button disabled for non-image file
- **WHEN** user selects a file that is not an image (e.g., pdf, txt, folder)
- **THEN** the Preview button is disabled

#### Scenario: Preview button disabled when nothing selected
- **WHEN** no file is selected in the table
- **THEN** the Preview button is disabled

### Requirement: Image preview dialog display
The system SHALL open a modal dialog displaying the selected image when the Preview button is clicked.

#### Scenario: Preview dialog opens with image
- **WHEN** user clicks the Preview button with an image file selected
- **THEN** a modal dialog opens displaying the image

#### Scenario: Dialog shows filename
- **WHEN** the preview dialog is open
- **THEN** the dialog title includes the filename

#### Scenario: Dialog is closable
- **WHEN** the preview dialog is open
- **THEN** user can close it via close button, escape key, or clicking outside

### Requirement: Image loading from S3
The system SHALL download the image from S3 to memory and display it in the preview dialog.

#### Scenario: Image loads successfully
- **WHEN** user opens preview for a valid image file
- **THEN** the image is downloaded from S3 and displayed

#### Scenario: Loading state shown
- **WHEN** image is being downloaded from S3
- **THEN** a loading indicator is shown

#### Scenario: Error on failed load
- **WHEN** image download fails (network error, access denied, etc.)
- **THEN** an error message is displayed

### Requirement: Supported image formats
The system SHALL support previewing images with the following extensions: jpg, jpeg, png, gif, bmp, svg, webp.

#### Scenario: JPEG preview
- **WHEN** user previews a file with .jpg or .jpeg extension
- **THEN** the image is displayed correctly

#### Scenario: PNG preview
- **WHEN** user previews a file with .png extension
- **THEN** the image is displayed correctly

#### Scenario: GIF preview
- **WHEN** user previews a file with .gif extension
- **THEN** the image is displayed correctly (first frame for animated GIFs)

### Requirement: Image display handling
The system SHALL handle large images gracefully with scrolling and resizing capabilities.

#### Scenario: Large image scrollable
- **WHEN** the image is larger than the dialog viewport
- **THEN** scrollbars are available to view the entire image

#### Scenario: Dialog resizable
- **WHEN** user resizes the preview dialog
- **THEN** the image view adjusts accordingly

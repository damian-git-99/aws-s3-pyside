## ADDED Requirements

### Requirement: Folders always appear before files in listings
The system SHALL ensure folders are always displayed before files in the bucket browser table, regardless of user sorting actions.

#### Scenario: Default view shows folders first
- **WHEN** the bucket browser loads and displays objects
- **THEN** all folders appear at the top of the list, followed by files
- **AND** both groups are sorted alphabetically within their section

#### Scenario: Sorting by name maintains folders-first order
- **WHEN** user clicks the Name column header to sort
- **THEN** folders remain at the top of the list
- **AND** folders are sorted alphabetically among themselves
- **AND** files are sorted alphabetically among themselves below all folders

#### Scenario: Sorting by other columns maintains folders-first order
- **WHEN** user clicks the Size, Last Modified, or Storage Class column header
- **THEN** folders remain at the top of the list
- **AND** folders are sorted by the selected column within the folder group
- **AND** files are sorted by the selected column within the file group

#### Scenario: Reverse sorting maintains folders-first order
- **WHEN** user clicks a column header twice to reverse sort order
- **THEN** folders remain at the top of the list (not moved to bottom)
- **AND** the sort direction is applied within each group (folders and files separately)

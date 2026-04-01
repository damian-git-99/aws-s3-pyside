## ADDED Requirements

### Requirement: Local search filter with debounce
The bucket browser SHALL provide a search input field that filters displayed objects by name using in-memory data.

#### Scenario: Filter objects by partial name match
- **WHEN** user types text in the search field and waits 300ms
- **THEN** the displayed objects are filtered to show only those whose names contain the search text (case-insensitive)

#### Scenario: Empty search shows all objects
- **WHEN** user clears the search field or leaves it empty
- **THEN** all objects in the current folder are displayed

#### Scenario: Case-insensitive search
- **WHEN** user searches for "readme"
- **THEN** objects with names "README.txt", "readme.md", and "ReadMe.pdf" are all shown

#### Scenario: Partial match works
- **WHEN** user searches for "image"
- **THEN** objects named "image.png", "my-image.jpg", and "images/" are all shown

### Requirement: Debounce prevents excessive filtering
The search filter SHALL wait 300ms after the user stops typing before applying the filter.

#### Scenario: Rapid typing only triggers one filter
- **WHEN** user types "test" quickly (each character < 100ms apart)
- **THEN** the filter is applied only once, after the final character is typed and 300ms pass

#### Scenario: Slow typing triggers filter after each pause
- **WHEN** user types "test" with pauses of 400ms between characters
- **THEN** the filter is applied after the 4th character (first pause triggers filter)

### Requirement: Search only affects currently loaded data
The search filter SHALL only filter objects currently loaded in memory, not make additional S3 API calls.

#### Scenario: Search respects pagination
- **WHEN** user is viewing page 1 of paginated results and searches
- **THEN** only objects on page 1 are searched

#### Scenario: Loading more pages before search
- **WHEN** user clicks "Load More" to load additional pages, then searches
- **THEN** all loaded objects across pages are included in search results
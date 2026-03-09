## Why

The current pagination limit of 1000 objects per page is too large for a desktop UI application. Loading 1000 rows in a Qt table causes performance issues and provides poor user experience. A smaller page size (50 objects) offers better performance, faster initial load times, and more manageable navigation for users browsing S3 bucket contents.

## What Changes

- **Modify** `src/services/s3_service.py`: Change `MaxKeys` from `1000` to `50` in the `list_objects` method
- **Update** `src/tests/test_s3_service.py`: Update test assertions that expect `MaxKeys=1000` to use `MaxKeys=50`
- No breaking changes to the API or public interface - internal implementation detail only

## Capabilities

### New Capabilities
- *(none - this is a configuration change to existing pagination capability)*

### Modified Capabilities
- *(none - requirements remain the same, only implementation constants change)*

## Impact

- **S3 Service**: Single constant change in pagination logic
- **Tests**: 3 test cases need updated assertions
- **User Experience**: Faster initial page loads, more responsive UI
- **Network**: More frequent but smaller S3 API calls when paginating through large buckets

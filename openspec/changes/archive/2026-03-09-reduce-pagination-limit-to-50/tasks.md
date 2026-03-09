## 1. Update S3 Service Pagination Limit

- [x] 1.1 Change `MaxKeys` from `1000` to `50` in `src/services/s3_service.py` (line 74)
- [x] 1.2 Verify the change is correct by reviewing the `list_objects` method

## 2. Update Test Assertions

- [x] 2.1 Update test in `src/tests/test_s3_service.py` line 63: change `MaxKeys=1000` to `MaxKeys=50`
- [x] 2.2 Update test in `src/tests/test_s3_service.py` line 104: change `MaxKeys=1000` to `MaxKeys=50`
- [x] 2.3 Update test in `src/tests/test_s3_service.py` line 141: change `MaxKeys=1000` to `MaxKeys=50`

## 3. Verify Implementation

- [x] 3.1 Run tests to ensure all assertions pass: `uv run python -m unittest discover src/tests/`
- [x] 3.2 Verify no other files reference `MaxKeys=1000`
- [x] 3.3 Confirm pagination still works correctly with smaller page size

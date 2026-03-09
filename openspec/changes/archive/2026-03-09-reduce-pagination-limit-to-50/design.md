## Context

The current implementation in `src/services/s3_service.py` uses `MaxKeys: 1000` when calling S3's `list_objects_v2` API. While 1000 is S3's maximum allowed value, it's too large for a responsive desktop UI.

Current behavior:
- Loads up to 1000 objects per page
- Causes UI lag when displaying large tables in Qt
- Provides poor user experience with overwhelming data

Target behavior:
- Load 50 objects per page  
- Maintain existing pagination logic (continuation tokens, Load More button)
- Better performance and UX

## Goals / Non-Goals

**Goals:**
- Change the S3 pagination limit from 1000 to 50 objects per request
- Update all test assertions that validate the MaxKeys parameter
- Maintain backward compatibility with existing pagination flow

**Non-Goals:**
- No changes to the pagination UI or user-facing behavior
- No changes to the Load More button logic
- No changes to continuation token handling
- No new features or capabilities

## Decisions

**Decision: Hardcode 50 vs Make Configurable**
- **Chosen:** Hardcode to 50
- **Rationale:** This is a desktop UI app with consistent needs. 50 is the sweet spot for Qt table performance. Making it configurable adds complexity without clear benefit.
- **Alternative considered:** Environment variable or config file - rejected as overkill for this use case.

**Decision: Update Tests vs Parameterize**
- **Chosen:** Update test assertions to expect 50
- **Rationale:** Tests should verify actual behavior. The constant 50 is the expected behavior.
- **Alternative considered:** Mock the constant - rejected as it hides the actual integration behavior.

## Risks / Trade-offs

**[Risk]** More frequent S3 API calls when browsing large buckets
→ **Mitigation:** This is acceptable for a desktop UI. Users typically browse folders with <1000 items. If needed, can be optimized later with prefetching.

**[Risk]** Tests break if constant changes again  
→ **Mitigation:** Tests explicitly validate the MaxKeys value, so they'll fail loudly if changed - this is desired behavior.

**[Risk]** Some users might prefer different page sizes
→ **Mitigation:** Not in scope. Can add user preference later if requested.

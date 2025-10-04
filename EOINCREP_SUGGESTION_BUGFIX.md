# EOINCREP AI Suggestion Bug Fix

## Issue

When trying to generate AI suggestions for EOINCREP, the system returned an error:

```
Failed to get AI suggestions: 'str' object has no attribute 'get'
```

## Root Cause

The bug was in the error handling fallback code in both `/eoincrep/suggest` and `/casevac/suggest` endpoints.

### Problem Code Pattern:

```python
# This code assumed structured_json is always a dict
casualty_reports[0].get("structured_json", {}).get("location", "")
```

### Why It Failed:

1. In the database, `structured_json` is stored as a **JSON string**, not a dictionary
2. When retrieved from the database: `report.get("structured_json")` returns a **string**
3. Calling `.get("location", "")` on a **string** fails with: `'str' object has no attribute 'get'`

## Files Fixed

- `backend.py` - `/eoincrep/suggest` endpoint (lines ~1183-1201)
- `backend.py` - `/casevac/suggest` endpoint (lines ~907-925)

## Solution Applied

### Before (Broken):

```python
except json.JSONDecodeError as e:
    logger.error(f"Failed to parse Gemini response as JSON: {response_text}")
    return {"suggested_fields": {
        "location": relevant_reports[0].get("structured_json", {}).get("location", ""),
        # ... more fields
    }}
```

### After (Fixed):

```python
except json.JSONDecodeError as e:
    logger.error(f"Failed to parse Gemini response as JSON: {response_text}")

    # Safely parse structured_json from first report
    first_report_data = {}
    if relevant_reports:
        structured = relevant_reports[0].get("structured_json", {})
        if isinstance(structured, str):
            try:
                first_report_data = json.loads(structured)
            except:
                first_report_data = {}
        elif isinstance(structured, dict):
            first_report_data = structured

    return {"suggested_fields": {
        "location": first_report_data.get("location", ""),
        # ... more fields
    }}
```

## What Changed

### EOINCREP Suggest Endpoint:

- Added safe parsing of `structured_json` field
- Checks if it's a string and parses JSON
- Checks if it's already a dict and uses it directly
- Falls back to empty dict if parsing fails
- Prevents the `'str' object has no attribute 'get'` error

### CASEVAC Suggest Endpoint:

- Applied the same fix for consistency
- Prevents the same error from occurring in CASEVAC suggestions

## Testing

### To Test EOINCREP Suggestions:

1. Select a unit that has CONTACT, INTELLIGENCE, or SITREP reports
2. Switch to EOINCREP builder tab
3. Click "AI Suggest" button
4. Should now work without errors

### To Test CASEVAC Suggestions:

1. Select a unit that has CASUALTY reports
2. Switch to CASEVAC builder tab
3. Click "AI Suggest" button
4. Should now work without errors

## Error Handling Flow

### Happy Path:

1. User clicks "AI Suggest"
2. Backend calls Gemini AI with report context
3. Gemini returns valid JSON response
4. Fields are populated with AI suggestions ✅

### Fallback Path (AI fails):

1. User clicks "AI Suggest"
2. Backend calls Gemini AI
3. Gemini returns invalid/unparseable response
4. `json.JSONDecodeError` is caught
5. **NEW FIX:** Safely parse first report's structured_json
6. Return default values with location from first report ✅
7. User can still use the form with defaults

### Error Path (No reports):

1. User clicks "AI Suggest" with no relevant reports
2. Backend returns empty default fields immediately
3. User sees empty form to fill manually ✅

## Additional Notes

### Similar Issues Fixed Earlier:

The main EOINCREP and CASEVAC suggest endpoints already had proper handling of `structured_json` strings in the main code path (lines ~1119-1125 for EOINCREP, lines ~847-853 for CASEVAC).

The bug only existed in the **error handling fallback code** that triggers when Gemini AI fails to return valid JSON.

### Prevention:

This type of bug was already prevented in the normal code flow but was missed in the error handling. Going forward, all `structured_json` access should use this pattern:

```python
structured = report.get("structured_json", {})
if isinstance(structured, str):
    try:
        structured = json.loads(structured)
    except:
        structured = {}
```

## Status

✅ **FIXED** - Both EOINCREP and CASEVAC AI suggestion endpoints now handle string `structured_json` fields correctly in all code paths.

# CASEVAC and EOINCREP Issues - Troubleshooting Guide

## Issues Reported

1. ❌ **AI Suggestion not working for CASEVAC**
2. ❌ **No download button visible for CASEVAC or EOINCREP**

## Root Causes Identified

### Issue 1: AI Suggestion Errors (FIXED ✅)

**Problem:** Backend error when AI suggestion fails and tries to access fallback data

```
'str' object has no attribute 'get'
```

**Fix Applied:**

- Updated `/casevac/suggest` endpoint with safe JSON parsing
- Updated `/eoincrep/suggest` endpoint with safe JSON parsing
- Added detailed logging to track issues

### Issue 2: Download Button Not Visible (INVESTIGATION NEEDED ⚠️)

**Root Cause:** Download button only appears AFTER successfully generating a document

The download buttons are coded correctly but only show when:

```typescript
{
  generatedDoc && (
    <Button onClick={handleDownload}>
      <Download /> Download
    </Button>
  );
}
```

**Possible Reasons:**

1. **Generate button not being clicked** - User must click "Generate" first
2. **Generation failing silently** - Check browser console for errors
3. **No reports available** - Need CASUALTY reports for CASEVAC, CONTACT/INTELLIGENCE/SITREP for EOINCREP
4. **Backend not returning formatted_document** - Check backend logs

## How to Test and Verify

### Step 1: Check if Reports Exist

```bash
# Check for CASUALTY reports in database
sqlite3 military_hierarchy.db "SELECT COUNT(*) FROM reports WHERE report_type = 'CASUALTY';"

# Check for CONTACT/INTELLIGENCE/SITREP reports
sqlite3 military_hierarchy.db "SELECT COUNT(*) FROM reports WHERE report_type IN ('CONTACT', 'INTELLIGENCE', 'SITREP');"
```

If counts are 0, you need to generate test data first:

```bash
python populate_reports.py
```

### Step 2: Test CASEVAC Builder

1. Start backend: `.\.venv\Scripts\python.exe backend.py`
2. Start frontend: `cd mil_dashboard; npm run dev`
3. Open browser: `http://localhost:3000`
4. Select a unit that has soldiers with CASUALTY reports
5. Click "CASEVAC" tab
6. Click "AI Suggest" button
   - ✅ Should populate fields with AI suggestions
   - ❌ If error, check browser console AND backend terminal logs
7. Review/edit the suggested fields
8. Click "Generate 9-Line CASEVAC Request" button
   - ✅ Should show preview section below
   - ✅ Download button should appear in preview
9. Click "Download" button
   - ✅ Should download `CASEVAC_####_Unit_Name.txt`

### Step 3: Test EOINCREP Builder

Same steps as CASEVAC but:

- Click "EOINCREP" tab instead
- Need CONTACT, INTELLIGENCE, or SITREP reports
- Download will be `EOINCREP_####_Unit_Name.txt`

### Step 4: Check Browser Console

1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for errors when clicking:
   - "AI Suggest" button
   - "Generate" button
4. Common errors to check:
   ```
   Error getting AI suggestions: ...
   Error generating CASEVAC: ...
   Failed to fetch
   Network error
   ```

### Step 5: Check Backend Logs

The backend now has detailed logging. Look for:

```
INFO: CASEVAC suggest - Received 5 reports for 2nd Battalion
INFO: CASEVAC suggest - Found 2 CASUALTY reports
INFO: CASEVAC suggest - Gemini response received, length: 487
INFO: CASEVAC suggest - Successfully parsed AI suggestions
```

Or for errors:

```
ERROR: Failed to parse Gemini response as JSON: ...
ERROR: Error in suggest_casevac: ...
```

## Backend Code Changes Summary

### File: `backend.py`

#### 1. Added Safe JSON Parsing in CASEVAC Fallback (lines ~907-928)

```python
except json.JSONDecodeError as e:
    logger.error(f"Failed to parse Gemini response as JSON: {response_text}")
    # Safely parse structured_json from first report
    first_casualty_data = {}
    if casualty_reports:
        structured = casualty_reports[0].get("structured_json", {})
        if isinstance(structured, str):
            try:
                first_casualty_data = json.loads(structured)
            except:
                first_casualty_data = {}
        elif isinstance(structured, dict):
            first_casualty_data = structured

    return {"suggested_fields": {
        "location": first_casualty_data.get("location", ""),
        # ... other fields
    }}
```

#### 2. Added Safe JSON Parsing in EOINCREP Fallback (lines ~1195-1215)

Same pattern as CASEVAC

#### 3. Added Detailed Logging

- Log number of reports received
- Log number of relevant reports found
- Log Gemini response length
- Log parsing success/failure

## Download Button Location in UI

### CASEVAC Builder:

```
┌──────────────────────────────────────────┐
│ Form fields...                           │
│ [Generate 9-Line CASEVAC Request]       │
│                                          │
│ ┌────────────────────────────────────┐  │
│ │ CASEVAC 0001 - PREVIEW  [Download]│  │ ← Download button here
│ │ ---------------------------------- │  │
│ │ CASEVAC REQUEST 0001               │  │
│ │ DTG: 041200Z OCT 2025              │  │
│ │ ...                                │  │
│ └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
```

### EOINCREP Builder:

Same layout pattern

## Common Issues and Solutions

### Issue: "No reports available"

**Cause:** Selected unit has no soldiers or soldiers have no reports of correct type
**Solution:**

1. Check if soldiers exist: `sqlite3 military_hierarchy.db "SELECT COUNT(*) FROM soldiers;"`
2. Generate test data: `python populate_reports.py`
3. Select a different unit with reports

### Issue: "AI Suggest button disabled"

**Cause:** No reports available for the selected unit
**Solution:** Generate test data or select unit with reports

### Issue: "Generate button disabled"

**Cause:** Required fields not filled
**Solution:**

- CASEVAC: Must have `location` and `patients` fields filled
- EOINCREP: Must have `location` field filled

### Issue: "Failed to get AI suggestions: Network error"

**Cause:** Backend not running
**Solution:** Start backend: `.\.venv\Scripts\python.exe backend.py`

### Issue: "Failed to get AI suggestions: <error message>"

**Cause:** Various - check exact error message
**Solution:**

1. Check backend logs for detailed error
2. Verify Gemini API key is valid
3. Check if reports have proper structure

## Next Steps for User

1. **Restart Backend** (to apply logging changes):

   ```bash
   # Stop current backend (Ctrl+C in terminal)
   .\.venv\Scripts\python.exe backend.py
   ```

2. **Open Frontend**:

   ```bash
   cd mil_dashboard
   npm run dev
   ```

3. **Test CASEVAC**:

   - Select a unit
   - Switch to CASEVAC tab
   - Click "AI Suggest"
   - Watch backend terminal for logs
   - Watch browser console for errors
   - Fill fields if needed
   - Click "Generate"
   - Look for download button in preview section

4. **Report Back**:
   - What do backend logs show?
   - What do browser console logs show?
   - Does the generate button work?
   - Does preview section appear?
   - Does download button appear in preview?

## Files Modified

- ✅ `backend.py` - Added logging and fixed JSON parsing
- ✅ `EOINCREP_SUGGESTION_BUGFIX.md` - Documentation of initial fix
- ✅ `DOWNLOAD_FEATURE_STATUS.md` - Documentation of download feature
- ✅ This file - Comprehensive troubleshooting guide

## Status

- ✅ **Backend bug fixed** - Safe JSON parsing in fallback code
- ✅ **Logging added** - Better visibility into what's happening
- ⚠️ **Download buttons** - Code is correct, needs testing to verify visibility
- 🔄 **Awaiting user testing** - Need to see actual logs and error messages

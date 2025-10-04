# CASEVAC/EOINCREP 500 Error Fix

## Error Reported

```
AxiosError: Request failed with status code 500
at handleSuggest (casevac-builder.tsx:83:24)
```

## Root Cause

The backend was throwing a 500 Internal Server Error when the AI suggestion endpoint was called. This could be caused by:

1. Gemini API safety filters blocking the response
2. Network/API errors without proper handling
3. Missing error details in logs

## Fixes Applied

### 1. Added Safety Settings to Gemini API Calls ✅

**Problem:** Gemini API might block military content as "dangerous"

**Fix:** Added safety settings to disable content filters

```python
response = gemini_model.generate_content(
    prompt,
    safety_settings={
        'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
        'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
        'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
        'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
    }
)
```

**Applied to:**

- `/casevac/suggest` endpoint (line ~897)
- `/eoincrep/suggest` endpoint (line ~1173)

### 2. Enhanced Error Logging ✅

**Problem:** Error messages didn't show stack traces

**Fix:** Added `exc_info=True` to log full tracebacks

```python
except Exception as e:
    logger.error(f"Error in suggest_casevac: {e}", exc_info=True)
    raise HTTPException(status_code=500, detail=str(e))
```

**Applied to:**

- CASEVAC suggest error handlers (2 locations)
- EOINCREP suggest error handlers (2 locations)

### 3. Created Test Script ✅

**File:** `test_casevac_api.py`

Test the backend without needing the frontend:

```bash
.\.venv\Scripts\python.exe test_casevac_api.py
```

This will:

- Send a test CASUALTY report to the backend
- Show if the endpoint responds correctly
- Display any errors with details

## Testing Instructions

### Step 1: Restart Backend with Fixes

```bash
# In terminal (stop with Ctrl+C if running)
.\.venv\Scripts\python.exe backend.py
```

You should see:

```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Test with Test Script

Open a **new PowerShell terminal** and run:

```bash
cd C:\Users\touko\AIproject\aalto_defence_project
.\.venv\Scripts\python.exe test_casevac_api.py
```

**Expected output if working:**

```
Testing CASEVAC suggest endpoint...
Sending request with 1 reports

Status Code: 200

✅ SUCCESS! Suggested fields:
{
  "suggested_fields": {
    "location": "Grid NV123456",
    "callsign_frequency": "30.55 MHz / DUSTOFF 23",
    "precedence": "A",
    ...
  }
}
```

**If you see errors:**
Look at the backend terminal for detailed logs with stack traces

### Step 3: Test with Frontend

1. Make sure backend is still running
2. Start frontend:
   ```bash
   cd mil_dashboard
   npm run dev
   ```
3. Open browser: http://localhost:3000
4. Select a unit
5. Click CASEVAC tab
6. Click "AI Suggest"
7. Watch **both**:
   - Browser console (F12)
   - Backend terminal logs

### Step 4: Check Backend Logs

Look for these log messages in the backend terminal:

**Success pattern:**

```
INFO: CASEVAC suggest - Received 5 reports for 2nd Battalion
INFO: CASEVAC suggest - Found 2 CASUALTY reports
INFO: CASEVAC suggest - Gemini response received, length: 487
INFO: CASEVAC suggest - Successfully parsed AI suggestions
INFO: 127.0.0.1:xxxxx - "POST /casevac/suggest HTTP/1.1" 200 OK
```

**Error pattern:**

```
ERROR: Error in suggest_casevac: <error message>
Traceback (most recent call last):
  File "...", line ...
  ... full stack trace ...
ERROR: 127.0.0.1:xxxxx - "POST /casevac/suggest HTTP/1.1" 500 Internal Server Error
```

## Common Issues and Solutions

### Issue: "Gemini API Key Error"

**Error:** `google.api_core.exceptions.InvalidArgument: Invalid API key`

**Solution:**

1. Check if API key is valid
2. Generate new key at: https://makersuite.google.com/app/apikey
3. Update in `backend.py` line 18

### Issue: "Safety filter blocked"

**Error:** Content blocked due to safety settings

**Solution:** Already fixed with `BLOCK_NONE` settings

### Issue: "No CASUALTY reports found"

**Symptoms:** Returns empty default fields

**Solution:**

1. Check database:
   ```bash
   sqlite3 military_hierarchy.db "SELECT COUNT(*) FROM reports WHERE report_type = 'CASUALTY';"
   ```
2. If count is 0, generate test data:
   ```bash
   .\.venv\Scripts\python.exe populate_reports.py
   ```

### Issue: "Connection refused" in test script

**Error:** `Could not connect to backend at http://localhost:8000`

**Solution:** Start the backend:

```bash
.\.venv\Scripts\python.exe backend.py
```

## Files Modified

1. ✅ `backend.py` - Added safety settings and enhanced error logging

   - Lines ~897-905: CASEVAC Gemini API call with safety settings
   - Lines ~932-935: CASEVAC error logging with stack trace
   - Lines ~1173-1181: EOINCREP Gemini API call with safety settings
   - Lines ~1230-1233: EOINCREP error logging with stack trace

2. ✅ `test_casevac_api.py` - New test script for quick API testing

## Next Steps

1. **Restart backend** with the fixes
2. **Run test script** to verify API works standalone
3. **Test with frontend** to see if issue persists
4. **Check logs** in both backend and browser console
5. **Report back** with:
   - Test script output
   - Backend log output
   - Browser console errors (if any)

## Technical Details

### Why Safety Settings?

Gemini's default safety filters can block content related to:

- Violence (military operations)
- Dangerous content (weapons, injuries)
- Harassment (military terminology)

Since we're building a legitimate military training/simulation system, we need to disable these filters.

### Why Better Error Logging?

Previously, errors showed just the message like:

```
ERROR: Error in suggest_casevac: 'str' object has no attribute 'text'
```

Now with `exc_info=True`, we see the full stack trace:

```
ERROR: Error in suggest_casevac: 'str' object has no attribute 'text'
Traceback (most recent call last):
  File "backend.py", line 899, in suggest_casevac
    response_text = response.text.strip()
AttributeError: 'str' object has no attribute 'text'
```

This makes debugging much easier!

## Status

✅ **Fixes applied and ready for testing**
🔄 **Awaiting test results from user**

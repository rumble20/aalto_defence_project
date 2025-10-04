# Quick Start Guide - Smart Notifications System

## 🚀 Steps to Run

### 1. **Stop the old backend** (if running)

Press `Ctrl+C` in the terminal where backend is running

### 2. **Restart the backend**

```powershell
.\.venv\Scripts\python.exe backend.py
```

### 3. **Run the test script**

Open a new PowerShell terminal:

```powershell
.\.venv\Scripts\python.exe test_smart_notifications.py
```

### 4. **Expected Output**

You should see:

```
✅ Report created: <report_id>
Found 5 pending suggestions:

1. CASEVAC - URGENT
   Reason: URGENT: Critical casualties detected
   Confidence: 95%

2. CASEVAC - HIGH
   Reason: 1 casualties reported
   Confidence: 90%

3. EOINCREP - HIGH
   Reason: Significant enemy force: 15 personnel, 3 vehicles
   Confidence: 90%

4. EOINCREP - MEDIUM
   Reason: Enemy contact: 6 hostiles
   Confidence: 85%

5. EOINCREP_EOD - HIGH
   Reason: Explosive ordnance/device detected
   Confidence: 85%
```

### 5. **View in Dashboard**

1. Start the frontend (if not running):
   ```powershell
   cd mil_dashboard
   npm run dev
   ```
2. Open http://localhost:3000
3. Look for the **bell icon (🔔)** in the header
4. It should show a **red badge with "5"**
5. Click it to see the suggestions panel

---

## 🐛 If You Still See Errors:

### Check Backend Logs

Look for errors in the terminal where backend is running. Common issues:

1. **"table suggestions has no column..."** → Database not migrated

   ```powershell
   Get-Content add_suggestions_table.sql | sqlite3 military_hierarchy.db
   ```

2. **"Port 8000 already in use"** → Old backend still running

   - Find and kill the process
   - Or use a different port

3. **Import errors** → Missing dependencies
   ```powershell
   .\.venv\Scripts\pip install fastapi uvicorn paho-mqtt google-generativeai
   ```

---

## ✅ What's Fixed:

- ✅ Made `analyze_report_triggers()` synchronous (was async)
- ✅ Made `create_suggestions()` synchronous (was async)
- ✅ Removed `await` calls from sync endpoint
- ✅ Database schema applied
- ✅ API endpoints added

The 500 errors were caused by calling async functions from a non-async endpoint. Now fixed!

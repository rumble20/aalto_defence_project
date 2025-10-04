# EOINCREP & CASEVAC Implementation Plan

**Tactical Operations Dashboard - Report Generation Features**

---

## 🎯 Executive Summary

Implement AI-assisted **EOINCREP** (Explosive Ordnance/Enemy Observation Incident Report) and **CASEVAC** (Casualty Evacuation) report generation features, similar to the FRAGO builder, but with standardized military formats and real-time urgency indicators.

---

## 📋 Current State Analysis

### ✅ What We Already Have:

1. **Backend Support**:

   - Report types defined: `EOINCREP`, `CASEVAC` in schema
   - `improved_military_report_formatter.py` with proper formats
   - Database table storing structured reports
   - Existing report display in `NodeReports` component

2. **Standards Implemented**:

   - **CASEVAC**: Nine-line MEDEVAC format (FM 4-02.2)
   - **EOINCREP**: DA Form 3265 EOD incident format + enemy observation
   - Color coding: Red for CASEVAC, Amber for EOINCREP

3. **UI Components**:
   - Report drawer (needs updating for these types)
   - Report list with filtering
   - AI chat for analysis

### ❌ What's Missing:

1. Dedicated builder UI for EOINCREP/CASEVAC
2. AI-assisted field completion
3. Priority/urgency workflows
4. Template-based generation
5. Quick-create buttons for emergencies

---

## 🏗️ Architecture Design

### **Option 1: Unified Report Builder (Recommended)**

Create a single `ReportBuilder` component that adapts to different report types.

**Pros**:

- Code reuse and consistency
- Single UI pattern to learn
- Easier to add new report types (SITREP, SPOTREP, etc.)
- Centralized AI suggestion logic

**Cons**:

- More complex component logic
- Might be overkill for simple reports

### **Option 2: Dedicated Builders**

Separate `CASEVACBuilder` and `EOINCREPBuilder` components.

**Pros**:

- Simpler, focused components
- Specialized workflows per type
- Better for very different forms

**Cons**:

- Code duplication
- More components to maintain

**💡 Recommendation**: Start with **Option 1**, create a flexible `ReportBuilder` with type-specific templates.

---

## 📝 Report Structure Specifications

### **CASEVAC - Nine-Line Format**

Based on FM 4-02.2 Medical Evacuation (MEDEVAC) procedures:

```
LINE 1: Location of pick-up site (Grid coordinates)
LINE 2: Radio frequency, call sign, suffix
LINE 3: Number of patients by precedence:
        - A = Urgent (life, limb, or eyesight threatening)
        - B = Priority (should be evacuated within 4 hours)
        - C = Routine (should be evacuated within 24 hours)
        - D = Convenience
LINE 4: Special equipment required:
        - A = None
        - B = Hoist
        - C = Extraction equipment
        - D = Ventilator
LINE 5: Number of patients by type:
        - L = Litter
        - A = Ambulatory
LINE 6: Security at pick-up site:
        - N = No enemy troops in area
        - P = Possible enemy troops (approach with caution)
        - E = Enemy troops in area (armed escort required)
        - X = Enemy troops in area (armed escort required, hospital threatened)
LINE 7: Method of marking pick-up site:
        - A = Panels
        - B = Pyrotechnic signal
        - C = Smoke signal
        - D = None
        - E = Other
LINE 8: Patient nationality and status:
        - A = US Military
        - B = US Civilian
        - C = Non-US Military
        - D = Non-US Civilian
        - E = EPW (Enemy Prisoner of War)
LINE 9: NBC Contamination (if applicable):
        - N = Nuclear
        - B = Biological
        - C = Chemical
```

**Example JSON Structure**:

```json
{
  "report_type": "CASEVAC",
  "structured_json": {
    "line1_location": "Grid NK 123 456",
    "line2_frequency": "30.150 MHz / DUSTOFF 23",
    "line3_precedence": "2A (2 Urgent)",
    "line4_equipment": "A (None)",
    "line5_patients": "2L (2 Litter)",
    "line6_security": "P (Possible enemy)",
    "line7_marking": "C (Smoke - purple)",
    "line8_nationality": "A (US Military)",
    "line9_nbc": "None",
    "casualties_count": 2,
    "injury_description": "Gunshot wounds, chest and abdomen",
    "evac_requested": true,
    "priority": "URGENT"
  },
  "confidence": 0.95,
  "timestamp": "2025-10-04T14:30:00Z"
}
```

---

### **EOINCREP - Explosive Ordnance/Enemy Observation**

Two variants:

#### **Variant A: Enemy Observation Report**

Used for spotting enemy forces, vehicles, equipment.

```
DATE-TIME GROUP (DTG):
LOCATION: Grid coordinates
OBSERVER: Unit/Callsign
ENEMY DESCRIPTION:
  - Type: Infantry / Mechanized / Armor / Mixed
  - Size: Count of personnel/vehicles
  - Activity: Moving / Stationary / Digging in / Attacking
  - Direction: Bearing and direction of movement
  - Equipment: Weapons, vehicles observed
  - Uniform/Markings: Identification features
ASSESSMENT:
  - Threat level: Low / Medium / High / Critical
  - Estimated intent
  - Recommended action
```

#### **Variant B: EOD Incident Report (DA Form 3265)**

Used for unexploded ordnance, IEDs, suspicious items.

```
CONTROL NUMBER:
CATEGORY: Routine / Unusual
DATE/TIME REPORTED:
REPORTED BY: Name, unit, phone
LOCATION: Address/grid coordinates
INCIDENT DESCRIPTION:
  - Type of ordnance/device
  - Quantity
  - Condition
  - Description
ACTION TAKEN:
  - Personnel dispatched
  - Time of arrival
  - Confirmation/identification
  - Disposition (destroyed, removed, false alarm)
AUTHENTICATION:
  - Commander name/phone
  - Date
```

**Example JSON Structure (Enemy Observation)**:

```json
{
  "report_type": "EOINCREP",
  "structured_json": {
    "dtg": "041430ZOCT25",
    "location": "Grid NK 234 567",
    "observer": "Alpha 2-3",
    "enemy_type": "Mechanized infantry",
    "enemy_count": 6,
    "vehicle_count": 2,
    "activity": "Moving north",
    "direction": "Bearing 015",
    "equipment": ["BTR-80 APCs", "PKM machine guns"],
    "threat_level": "HIGH",
    "estimated_intent": "Flanking maneuver",
    "recommended_action": "Prepare defensive positions"
  },
  "confidence": 0.88,
  "timestamp": "2025-10-04T14:30:00Z"
}
```

---

## 🎨 UI/UX Design

### **Layout Concept**

```
┌─────────────────────────────────────────────────────────┐
│  REPORT BUILDER - [CASEVAC/EOINCREP/FRAGO]             │
│  [Tab: FRAGO] [Tab: CASEVAC ⚠️] [Tab: EOINCREP 👁️]    │
└─────────────────────────────────────────────────────────┘
│                                                          │
│  📊 Selected: Battalion Alpha (45 reports)              │
│                                                          │
│  ┌──────────────────────────────────────────────┐      │
│  │ [🤖 AI Suggest from Reports]  [📋 Template]  │      │
│  └──────────────────────────────────────────────┘      │
│                                                          │
│  ┌── CASEVAC Nine-Line ─────────────────────────┐      │
│  │ 1. LOCATION                                   │      │
│  │ [Auto-expanding textarea]                     │      │
│  │ 2. RADIO FREQ                                 │      │
│  │ [Auto-expanding textarea]                     │      │
│  │ 3. PRECEDENCE                                 │      │
│  │ [Dropdown: Urgent/Priority/Routine]           │      │
│  │ 4. EQUIPMENT                                  │      │
│  │ [Dropdown: None/Hoist/Extraction/Ventilator]  │      │
│  │ ... (9 lines total)                           │      │
│  └───────────────────────────────────────────────┘      │
│                                                          │
│  [Generate Report] [Save Draft] [Send ⚡]              │
│                                                          │
│  ┌── Generated Report Preview ───────────────────┐      │
│  │ CASEVAC REQUEST 0042                          │      │
│  │ 041430ZOCT25                                  │      │
│  │                                                │      │
│  │ 1. Location: Grid NK 123 456                  │      │
│  │ 2. Freq: 30.150 / DUSTOFF 23                  │      │
│  │ 3. Patients: 2A (Urgent)                      │      │
│  │ ...                                            │      │
│  └────────────────────────────────────────────────┘      │
└──────────────────────────────────────────────────────────┘
```

### **Quick Actions Panel**

Add emergency quick-create buttons to the header:

```tsx
<Button variant="destructive" size="sm">
  <AlertTriangle className="mr-1 h-3 w-3" />
  URGENT CASEVAC
</Button>
<Button variant="warning" size="sm">
  <Eye className="mr-1 h-3 w-3" />
  ENEMY CONTACT
</Button>
```

---

## 🔧 Implementation Plan

### **Phase 1: Unified Report Builder Component** (4-6 hours)

**File**: `mil_dashboard/src/app/components/report-builder.tsx`

```tsx
interface ReportBuilderProps {
  reportType: "CASEVAC" | "EOINCREP" | "FRAGO";
  unitId: string;
  unitName: string;
  soldierIds: string[];
  reports: any[];
}

interface ReportTemplate {
  fields: FieldDefinition[];
  aiPrompt: string;
  formatFunction: (fields: any) => string;
}

const REPORT_TEMPLATES: Record<string, ReportTemplate> = {
  CASEVAC: {
    fields: [
      {
        name: "line1_location",
        label: "1. LOCATION",
        type: "text",
        required: true,
      },
      {
        name: "line2_frequency",
        label: "2. FREQ/CALLSIGN",
        type: "text",
        required: true,
      },
      {
        name: "line3_precedence",
        label: "3. PRECEDENCE",
        type: "select",
        options: ["A (Urgent)", "B (Priority)", "C (Routine)"],
        required: true,
      },
      // ... 9 lines total
    ],
    aiPrompt: "Analyze casualty reports and suggest CASEVAC nine-line...",
    formatFunction: formatCASEVAC,
  },
  EOINCREP: {
    /* ... */
  },
};
```

**Key Features**:

- Tab-based interface for switching report types
- Dynamic form generation based on templates
- AI suggestion for each report type
- Auto-expanding textareas (like FRAGO)
- Validation for required fields
- Preview panel with live formatting

### **Phase 2: Backend Endpoints** (2-3 hours)

**File**: `backend.py`

Add new endpoints similar to FRAGO:

```python
@app.post("/report/suggest")
async def suggest_report(request: ReportSuggestRequest):
    """
    Analyze reports and suggest CASEVAC/EOINCREP fields using AI.
    """
    # Similar to /frago/suggest but with report-type-specific prompts
    # CASEVAC: Focus on casualty info, location, urgency
    # EOINCREP: Focus on enemy activity, threat assessment

@app.post("/report/generate")
async def generate_report(request: ReportGenerateRequest):
    """
    Generate formatted report document and save to database.
    """
    # Auto-increment report numbers per type
    # Format according to military standards
    # Save to reports table
```

**Database Extension**:

```sql
-- Add report number sequences
CREATE TABLE IF NOT EXISTS report_sequences (
    report_type TEXT PRIMARY KEY,
    next_number INTEGER NOT NULL DEFAULT 1
);

INSERT INTO report_sequences (report_type, next_number) VALUES
    ('CASEVAC', 1),
    ('EOINCREP', 1);
```

### **Phase 3: Template System** (2 hours)

**File**: `mil_dashboard/src/lib/report-templates.ts`

```typescript
export interface ReportField {
  name: string;
  label: string;
  type: "text" | "textarea" | "select" | "number" | "datetime";
  required?: boolean;
  options?: string[];
  placeholder?: string;
  helpText?: string;
}

export const CASEVAC_TEMPLATE: ReportField[] = [
  {
    name: "line1_location",
    label: "1. LOCATION",
    type: "text",
    required: true,
    placeholder: "Grid NK 123 456",
    helpText: "Grid coordinates of pick-up site",
  },
  // ... all 9 lines
];

export const EOINCREP_ENEMY_TEMPLATE: ReportField[] = [
  {
    name: "dtg",
    label: "DTG",
    type: "datetime",
    required: true,
    helpText: "Date-Time Group (auto-filled)",
  },
  {
    name: "enemy_type",
    label: "ENEMY TYPE",
    type: "select",
    options: ["Infantry", "Mechanized", "Armor", "Artillery", "Mixed"],
    required: true,
  },
  // ... more fields
];
```

### **Phase 4: UI Integration** (3 hours)

**Update**: `mil_dashboard/src/app/page.tsx`

```tsx
// Add state for report type
const [activeReportType, setActiveReportType] = useState<
  "FRAGO" | "CASEVAC" | "EOINCREP"
>("FRAGO");

// Add tabs to header
<div className="flex gap-1">
  <Button onClick={() => setActiveReportType("FRAGO")}>FRAGO</Button>
  <Button onClick={() => setActiveReportType("CASEVAC")} variant="destructive">
    CASEVAC ⚠️
  </Button>
  <Button onClick={() => setActiveReportType("EOINCREP")} variant="warning">
    EOINCREP 👁️
  </Button>
</div>;

// Render appropriate builder
{
  activeReportType === "FRAGO" && <FRAGOBuilder {...props} />;
}
{
  activeReportType === "CASEVAC" && <ReportBuilder type="CASEVAC" {...props} />;
}
{
  activeReportType === "EOINCREP" && (
    <ReportBuilder type="EOINCREP" {...props} />
  );
}
```

### **Phase 5: Advanced Features** (Optional, 4-6 hours)

1. **Quick Templates**:

   - Pre-filled common scenarios
   - "Mass Casualty", "Single Urgent", "EOD Find", "Enemy Patrol"

2. **Voice Input** (Future):

   - Record audio description
   - AI transcription → field extraction
   - One-click CASEVAC from voice

3. **Map Integration**:

   - Click map to set location
   - Visual distance/direction indicators
   - Route planning for MEDEVAC

4. **Alert System**:

   - Auto-notify higher command on URGENT CASEVAC
   - Sound alerts for critical reports
   - Push notifications

5. **Historical Analysis**:
   - Track CASEVAC response times
   - Enemy pattern recognition from EOINCREP
   - Heatmaps of incidents

---

## 🎯 AI Prompting Strategy

### **CASEVAC AI Prompt**:

```
You are a military medical operations AI. Analyze these casualty and injury reports
from {unit_name} and suggest a CASEVAC nine-line request.

CASUALTY REPORTS ({count} total):
{report_list}

Based on these reports, suggest:
1. Best pick-up location (central to casualties)
2. Recommended frequency/callsign
3. Precedence (A=Urgent, B=Priority, C=Routine) - use MOST URGENT patient
4. Special equipment needed (ventilator, hoist, etc.)
5. Total patients by type (litter vs ambulatory)
6. Security assessment (enemy threat level)
7. Marking method recommendation
8. Patient nationality (infer from unit)
9. NBC contamination status

Return JSON with these fields. Be conservative - prioritize life-saving speed.
```

### **EOINCREP AI Prompt**:

```
You are a military intelligence analyst AI. Analyze these contact and observation
reports from {unit_name} and suggest an EOINCREP.

CONTACT/INTELLIGENCE REPORTS ({count} total):
{report_list}

Based on these reports, suggest:
- DTG (current time)
- Location (most recent/accurate)
- Enemy type and size (aggregate counts)
- Activity and movement direction
- Equipment observed
- Threat level assessment
- Estimated enemy intent
- Recommended action

Return JSON. Prioritize accuracy and tactical relevance.
```

---

## 📊 Success Metrics

### **User Experience**:

- ✅ Generate CASEVAC in < 30 seconds
- ✅ Generate EOINCREP in < 45 seconds
- ✅ AI suggestion accuracy > 85%
- ✅ Zero required manual field entry for urgent cases

### **Technical**:

- ✅ Report numbering: auto-increment, no collisions
- ✅ Database: all reports saved with full audit trail
- ✅ Format compliance: 100% adherence to FM standards
- ✅ Mobile responsive: works on tablets in field

---

## 🚀 Quick Start Implementation

### **Minimum Viable Product (MVP)** - 8 hours:

1. **Create `ReportBuilder` component** (3 hours)

   - Copy FRAGO builder structure
   - Add CASEVAC template (9 lines)
   - Add EOINCREP template (enemy observation variant)
   - Tab switching UI

2. **Add backend endpoints** (2 hours)

   - `/report/suggest` - AI analysis
   - `/report/generate` - format and save
   - Report sequences table

3. **Integration** (2 hours)

   - Add tabs to main page
   - Connect to existing report system
   - Test with real data

4. **Polish** (1 hour)
   - Color coding (red for CASEVAC, amber for EOINCREP)
   - Urgency indicators
   - Preview formatting

### **What to Build First**:

1. ✅ CASEVAC Builder (highest priority - life-saving)
2. ✅ EOINCREP Enemy Observation (tactical awareness)
3. Later: EOINCREP EOD variant (less common)

---

## 💡 Key Design Decisions

### **1. Separate vs Unified Builder?**

**Decision**: **Unified** with templates

- Reuse 90% of FRAGO code
- Easy to add SITREP, SPOTREP later
- Consistent UX across all report types

### **2. Dropdown vs Text for Coded Fields?**

**Decision**: **Dropdowns** for Line 3-9 (CASEVAC)

- Prevent errors (must use A/B/C/D codes)
- Faster input
- Mobile-friendly
- But allow "Other" text option for flexibility

### **3. Auto-generate vs User-initiated?**

**Decision**: **User-initiated with quick actions**

- Button in header: "URGENT CASEVAC"
- Auto-pre-fill from AI suggestions
- User reviews and sends
- Avoids false alarms

### **4. Real-time vs Batch Processing?**

**Decision**: **Real-time** AI suggestions

- Immediate feedback
- Can refine and regenerate
- Better UX for urgent situations

---

## 🔒 Security & Validation

### **Input Validation**:

```typescript
const validateCASEVAC = (fields: CASEVACFields) => {
  const errors: string[] = [];

  // Location must be valid grid
  if (!isValidGrid(fields.line1_location)) {
    errors.push("Invalid grid coordinates");
  }

  // Precedence must be A/B/C/D
  if (!["A", "B", "C", "D"].includes(fields.line3_precedence[0])) {
    errors.push("Invalid precedence code");
  }

  // At least 1 patient
  if (fields.casualties_count < 1) {
    errors.push("Must have at least 1 casualty");
  }

  return errors;
};
```

### **Permission Checks**:

- Only authorized users can generate reports
- CASEVAC requires medical or command role
- Audit log: who created, when, from what data

---

## 📚 References

### **Military Standards**:

- **FM 4-02.2**: Medical Evacuation (MEDEVAC)
- **DA Form 3265**: EOD Incident/Accident Report
- **FM 9-15**: Explosive Ordnance Disposal
- **ATP 2-01.3**: Intelligence Preparation of the Battlefield

### **Implementation Files**:

- `improved_military_report_formatter.py` - Already has formatters
- `send_test_report.py` - Test data examples
- `schema_definition.py` - Database schema
- `frago-builder.tsx` - Template to copy

---

## 🎬 Next Steps

1. **Review & Approve** this design document
2. **Create `ReportBuilder` component** based on FRAGO
3. **Add CASEVAC template** (9 lines)
4. **Add EOINCREP template** (enemy observation)
5. **Backend endpoints** for AI + generation
6. **Test with real casualty scenarios**
7. **Polish & deploy**

**Estimated Time**: 10-12 hours for MVP
**Priority**: HIGH (CASEVAC is life-saving)

---

## ✨ Future Enhancements

- **SITREP Builder**: Situation reports
- **SPOTREP Builder**: Spot reports (immediate threats)
- **INTREP Builder**: Intelligence reports
- **Voice-to-Report**: Speak report, AI generates
- **Map Integration**: Click location, auto-fill grid
- **Response Tracking**: Track MEDEVAC arrival times
- **Pattern Analysis**: Enemy activity heatmaps from EOINCREP

---

**Ready to implement? Let's start with CASEVAC - it's the most critical! 🚑**

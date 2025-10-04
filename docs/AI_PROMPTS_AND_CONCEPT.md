# AI Prompts and Project Concept

## Project Concept

### Problem Statement (Finnish)

Nykyiselta sotakentältä ei saada informaatiota järkevästi: radion kautta puhuminen, kirjoittaminen vanhentuneilla laitteilla on vaivailloista ja usein jää toteuttamatta. Tiedon lähetys eteenpäin tulee olla muodollista sekä sitä on vaivalloista.

### Solution (Finnish)

Jokaisella sotilaalla tai ryhmänjohtajalla tai muutaman sotilaan johtajalla tulee olemaan älykäs radio joka on aina päällä ja kuuntelee passiivisesti tai napin painalluksella sotiaan puhetta ja raportointia. Täten kukin sotilas kykenee monimuotoisesti, vapaasti ja suurella tarkkuudella kuvailemaan tilannetta ja radio lähettää tiedon eteenpäin. Tämä puheen ja tiedon hälinä kasataan ja jalostetaan tekoälymallin avulla tukiasemalla.

Nyt voidaan saada realiaikainen ja kattava tilannekuva koko taistelutilanteesta. Tämä aijemmin olisi mahdotonta, sillä tiedon hälinän prosenssointi manuaalisesti vaatisi yhtä monta kuuntelijaa ja analysoijaa kuin itse lähettävää sotilasta. Ja se tiedon rakennus yhtenäiseksi raportiksi olisi mahdotonta.

Toinen asia on se, että basessa oleva tekoälymalli kykenee muodostamaan siitä vaatimusten mukaisia raportteja: "OPORD/FRAGO and standard reports (EOINCREP, CASEVAC) with citations and confidence flags, then translates them between NATO, national, and machine-readable schemas so people and robots share"

### Problem Statement (English)

Current battlefield information gathering is inefficient: radio communication and writing on outdated devices is cumbersome and often not executed. Information transmission must be formal, making it laborious.

### Solution (English)

Each soldier, squad leader, or small team leader will have a smart radio that is always on and passively listens or activates with a button press to capture soldier speech and reporting. This allows each soldier to describe the situation in a multifaceted, free, and highly accurate manner, with the radio transmitting the information forward. This speech and information noise is collected and refined by an AI model at the base station.

This enables real-time and comprehensive situational awareness of the entire battle situation. Previously impossible, as manually processing this information noise would require as many listeners and analysts as there are reporting soldiers, and building coherent reports from this data would be impossible.

Additionally, the AI model at the base can generate compliant reports: "OPORD/FRAGO and standard reports (EOINCREP, CASEVAC) with citations and confidence flags, then translates them between NATO, national, and machine-readable schemas so people and robots share."

---

## AI Prompts Used in the System

### 1. AI Chat Analysis Prompt

**Location**: `backend/backend.py` (~line 850)

**Purpose**: Analyzes battlefield reports and answers tactical questions

**Template**:

```
You are a military intelligence analyst AI. Analyze these battlefield reports and answer the user's question.

Node: {node_name}
User Question: {user_message}

Reports ({report_count} total):
{formatted_reports}

Provide a direct, clear answer using military terminology. Be concise and actionable.
```

**Features**:

- Processes up to 50 reports
- Extracts structured data from reports
- Provides tactical insights
- Uses military terminology

---

### 2. FRAGO (Fragmentary Order) Suggestion Prompt

**Location**: `backend/backend.py` (~line 945)

**Purpose**: Generates tactical order suggestions based on battlefield reports

**Template**:

```
You are a military AI assistant. Based on the following reports from {unit_name}, suggest appropriate fields for a Fragmentary Order (FRAGO).

Recent Reports ({report_count}):
{formatted_reports}

Analyze the reports and suggest content for these FRAGO fields in JSON format:
{
  "situation": "Brief enemy and friendly situation update",
  "mission": "Clear mission statement with task and purpose",
  "execution": "Concept of operations and key tasks",
  "service_support": "Logistics and support requirements",
  "command_signal": "Command post locations and communication plan"
}

Provide ONLY the JSON object, no additional text.
```

**Guidelines**:

- 5-paragraph order structure
- Based on current tactical situation
- Clear, actionable mission statements

---

### 3. CASEVAC (Casualty Evacuation) Suggestion Prompt

**Location**: `backend/backend.py` (~line 1180)

**Purpose**: Generates CASEVAC report fields from casualty information

**Template**:

```
You are a military medical AI assistant. Based on casualty reports from {unit_name}, suggest appropriate CASEVAC request fields.

Casualty Reports ({report_count}):
{formatted_reports}

Generate a CASEVAC request in JSON format:
{
  "location": "9-line MGRS grid or description",
  "call_sign": "Unit call sign",
  "precedence": "A (URGENT), B (URGENT SURGICAL), C (PRIORITY), D (ROUTINE), E (CONVENIENCE)",
  "special_equipment": "Required special equipment",
  "patients_by_type": "Number and type: L (litter) or A (ambulatory)",
  "security": "N (no enemy), P (possible enemy), E (enemy in area), X (armed escort required)",
  "marking_method": "How LZ will be marked",
  "nationality": "Nationality and status",
  "nbc": "N (none), B (biological), C (chemical), R (radiological)"
}

Guidelines:
- Set precedence to A (URGENT) for life-threatening injuries, B for surgical needs, C for stable but needs care
- Estimate litter vs ambulatory based on injury severity
- Consider security situation from reports
- Default to US Military nationality unless specified otherwise
- Default NBC to "N" unless reports mention chemical/biological/radiological hazards
```

**9-Line CASEVAC Format**:

1. Location of pickup site
2. Radio frequency, call sign
3. Number of patients by precedence
4. Special equipment required
5. Number of patients by type
6. Security at pickup site
7. Method of marking pickup site
8. Patient nationality and status
9. NBC contamination

---

### 4. EOINCREP (Enemy Observation) Suggestion Prompt

**Location**: `backend/backend.py` (~line 1505)

**Purpose**: Generates enemy observation reports from intelligence

**Template**:

```
You are a military intelligence AI assistant. Based on enemy observation reports from {unit_name}, suggest appropriate EOINCREP fields.

Enemy Reports ({report_count}):
{formatted_reports}

Generate an EOINCREP (Enemy Observation and Information Report) in JSON format:
{
  "location": "Enemy location (MGRS grid or description)",
  "activity": "Enemy activity description",
  "unit_composition": "Estimated enemy unit size and type",
  "equipment": "Enemy equipment observed",
  "assessment": "Threat assessment and recommended actions"
}

Guidelines:
- Extract enemy_type from reports (infantry, armor, artillery mentions)
- Set threat_level to CRITICAL for large forces (>20 personnel or >3 vehicles)
- Set threat_level to HIGH for significant forces (10-20 personnel or 2-3 vehicles)
- Set threat_level to MEDIUM for small patrols (5-10 personnel or 1 vehicle)
- Set threat_level to LOW for minimal presence (<5 personnel)
- Recommend "Monitor and report" for LOW, "Prepare to engage" for MEDIUM, "Engage with support" for HIGH, "Immediate support required" for CRITICAL
```

**Threat Levels**:

- **CRITICAL**: Large forces, immediate support required
- **HIGH**: Significant forces, engage with support
- **MEDIUM**: Small patrols, prepare to engage
- **LOW**: Minimal presence, monitor and report

---

## Technical Implementation

### AI Model

- **Model**: Google Gemini 2.5 Pro
- **API**: Google Generative AI
- **Safety Settings**: Disabled for military content

### Output Format

- **Schema Enforcement**: Pydantic (implied through JSON validation)
- **Format**: Structured JSON
- **Fallback**: Default values if AI fails

### Processing Pipeline

1. Collect relevant reports from database
2. Format reports with context
3. Generate AI prompt with guidelines
4. Call Gemini API with safety settings
5. Parse JSON response (handle markdown code blocks)
6. Return structured suggestions

---

## Hackathon Context

### Challenge: What The Warfighter?

**Path 1**: AI for Front and Rear

**Requirements**:

- Turn raw, unstructured battlefield inputs into clear decisions
- Ingest chat logs, sensor snippets, and doctrine
- Draft 5-paragraph OPORD/FRAGO and standard reports (EOINCREP, CASEVAC)
- Provide citations and confidence flags
- Translate between NATO, national, and machine-readable schemas
- Function when GPS is spoofed
- Operate with near-zero bandwidth
- Edge vision models (Segment Anything + lightweight classifiers)
- Speech recognition (VOSK)
- LLM + RAG pipelines

**Tech Stack**:

- **Edge Device**: Raspberry Pi with VOSK for speech-to-text
- **Backend**: FastAPI + Python
- **AI**: Google Gemini API (swappable with local Llama)
- **Frontend**: Next.js dashboard
- **Database**: SQLite
- **Communication**: MQTT
- **Validation**: Pydantic

**Winning Criteria**:

- Uniqueness: 70%
- Feasibility: 30%

---

## Future Enhancements

1. **RAG Pipeline**: Add doctrine.txt with military report formatting examples
2. **Confidence Scores**: Add confidence flags to AI-generated fields
3. **Citations**: Reference which reports contributed to each field
4. **Local LLM**: Option to run Llama locally for offline operation
5. **Vision AI**: Integrate Segment Anything for image analysis
6. **Bandwidth Optimization**: Compress reports for low-bandwidth transmission
7. **GPS-Denied Navigation**: Alternative positioning methods

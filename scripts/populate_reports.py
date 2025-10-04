"""
Script to populate the database with diverse military reports from different soldiers.
"""
import sqlite3
import json
import uuid
from datetime import datetime, timedelta
import random

DB_PATH = "military_hierarchy.db"

# Sample report templates for different types
REPORT_TEMPLATES = {
    "CONTACT": [
        {
            "enemy_type": "Infantry",
            "enemy_count": random.randint(5, 15),
            "location": "Grid 12345678",
            "engagement_status": "Engaged",
            "casualties_friendly": 0,
            "casualties_enemy": random.randint(0, 5),
            "weapons_observed": ["AK-47", "RPG"],
            "direction_of_travel": "North"
        },
        {
            "enemy_type": "Mechanized",
            "enemy_count": random.randint(2, 8),
            "location": "Grid 23456789",
            "engagement_status": "Observed",
            "casualties_friendly": 0,
            "casualties_enemy": 0,
            "weapons_observed": ["BTR-80", "PKM"],
            "direction_of_travel": "East"
        },
        {
            "enemy_type": "Sniper",
            "enemy_count": random.randint(1, 3),
            "location": "Grid 34567890",
            "engagement_status": "Taking Fire",
            "casualties_friendly": random.randint(0, 2),
            "casualties_enemy": 0,
            "weapons_observed": ["Sniper Rifle"],
            "direction_of_travel": "Unknown"
        }
    ],
    "SITREP": [
        {
            "personnel_status": "All accounted for",
            "equipment_status": "Fully operational",
            "ammunition_status": "75% remaining",
            "fuel_status": "50% remaining",
            "morale": "High",
            "weather": "Clear, visibility good",
            "next_planned_action": "Continue patrol route"
        },
        {
            "personnel_status": "1 minor injury",
            "equipment_status": "1 vehicle needs maintenance",
            "ammunition_status": "90% remaining",
            "fuel_status": "80% remaining",
            "morale": "Moderate",
            "weather": "Overcast, light rain",
            "next_planned_action": "Return to base"
        },
        {
            "personnel_status": "All healthy",
            "equipment_status": "Communications intermittent",
            "ammunition_status": "60% remaining",
            "fuel_status": "40% remaining",
            "morale": "High",
            "weather": "Fog, limited visibility",
            "next_planned_action": "Establish defensive position"
        }
    ],
    "CASUALTY": [
        {
            "casualty_type": "Wounded in Action",
            "count": 1,
            "status": "Stable, MEDEVAC requested",
            "injury_type": "Gunshot wound - leg",
            "treatment_given": "Tourniquet applied, morphine administered",
            "priority": "Priority 2"
        },
        {
            "casualty_type": "Non-combat injury",
            "count": 1,
            "status": "Stable, continuing mission",
            "injury_type": "Sprained ankle",
            "treatment_given": "Field dressing, pain medication",
            "priority": "Priority 3"
        }
    ],
    "SUPPLY": [
        {
            "supply_type": "Ammunition",
            "quantity": "200 rounds",
            "status": "Resupply needed within 24hrs",
            "location": "Forward Operating Base Alpha",
            "requested_items": ["5.56mm NATO", "40mm grenades"]
        },
        {
            "supply_type": "Water",
            "quantity": "50 liters",
            "status": "Adequate for 48hrs",
            "location": "Patrol Base Bravo",
            "requested_items": []
        },
        {
            "supply_type": "Medical",
            "quantity": "1 trauma kit",
            "status": "Critical - immediate resupply required",
            "location": "Checkpoint Charlie",
            "requested_items": ["Tourniquets", "Combat gauze", "IV fluids"]
        }
    ],
    "INTELLIGENCE": [
        {
            "observation": "Civilian reports increased enemy activity in sector",
            "reliability": "B - Usually Reliable",
            "credibility": "3 - Fairly credible",
            "details": "Local elder reports convoy movement at night",
            "recommended_action": "Increase patrols, establish observation post"
        },
        {
            "observation": "Enemy communications intercepted",
            "reliability": "A - Completely Reliable",
            "credibility": "1 - Confirmed",
            "details": "Radio chatter indicates planned attack in 48hrs",
            "recommended_action": "Immediate alert, reinforce defenses"
        }
    ],
    "LOGSTAT": [
        {
            "fuel": "60%",
            "ammunition": "75%",
            "water": "80%",
            "food": "90%",
            "medical_supplies": "70%",
            "vehicle_status": "All operational",
            "resupply_eta": "24 hours"
        },
        {
            "fuel": "30%",
            "ammunition": "50%",
            "water": "40%",
            "food": "60%",
            "medical_supplies": "85%",
            "vehicle_status": "1 vehicle down for maintenance",
            "resupply_eta": "12 hours"
        }
    ]
}

def get_soldiers():
    """Get all soldiers from database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT soldier_id, name, unit_id FROM soldiers")
    soldiers = c.fetchall()
    conn.close()
    return soldiers

def create_report(soldier_id, unit_id, report_type, structured_data):
    """Create a report in the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    report_id = str(uuid.uuid4())
    # Random timestamp within last 24 hours
    timestamp = (datetime.now() - timedelta(hours=random.randint(0, 24))).isoformat()
    confidence = round(random.uniform(0.75, 0.99), 2)
    
    c.execute("""
        INSERT INTO reports (report_id, soldier_id, unit_id, timestamp, report_type, structured_json, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        report_id,
        soldier_id,
        unit_id,
        timestamp,
        report_type,
        json.dumps(structured_data),
        confidence
    ))
    
    conn.commit()
    conn.close()
    return report_id

def populate_database():
    """Populate database with diverse reports."""
    soldiers = get_soldiers()
    
    if not soldiers:
        print("No soldiers found in database!")
        return
    
    print(f"Found {len(soldiers)} soldiers in database")
    print("\nGenerating diverse reports...\n")
    
    # Create 10 diverse reports across different soldiers
    reports_created = 0
    
    # Distribute reports across different soldiers
    for i in range(10):
        # Select a random soldier (but distribute evenly)
        soldier = soldiers[i % len(soldiers)]
        soldier_id, soldier_name, unit_id = soldier
        
        # Select a random report type
        report_type = random.choice(list(REPORT_TEMPLATES.keys()))
        
        # Get a random template for this type
        template = random.choice(REPORT_TEMPLATES[report_type])
        
        # Create the report with some randomization
        structured_data = template.copy()
        if report_type == "CONTACT":
            structured_data["enemy_count"] = random.randint(5, 20)
            structured_data["casualties_friendly"] = random.randint(0, 3)
            structured_data["casualties_enemy"] = random.randint(0, 10)
        elif report_type == "SITREP":
            structured_data["ammunition_status"] = f"{random.randint(50, 100)}% remaining"
            structured_data["fuel_status"] = f"{random.randint(30, 100)}% remaining"
        
        report_id = create_report(soldier_id, unit_id, report_type, structured_data)
        
        print(f"✓ Created {report_type} report from {soldier_name}")
        print(f"  ID: {report_id}")
        print(f"  Data: {json.dumps(structured_data, indent=2)[:100]}...")
        print()
        
        reports_created += 1
    
    print(f"\n✅ Successfully created {reports_created} diverse reports!")
    print(f"📊 Report types distributed across {len(set([s[0] for s in soldiers[:10]]))} soldiers")

if __name__ == "__main__":
    print("=" * 60)
    print("MILITARY REPORT DATABASE POPULATOR")
    print("=" * 60)
    print()
    populate_database()
    print()
    print("=" * 60)
    print("Done! Check your dashboard to see the new reports.")
    print("=" * 60)

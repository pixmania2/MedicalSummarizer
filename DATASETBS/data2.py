#!/usr/bin/env python3
"""
Generate 10 000 long-form synthetic consultation reports **plus**
a one-sentence abstractive summary for each report.  Output:
{
  "report_text": ...,
  "summary": ...,
  "annotation": {...}
}
(one JSON object per line in `synthetic_medical_reports.jsonl`)
"""

import random, json
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# ————————————————————————————————————————————————————————————————
# (1) helper to inflate base lists to ≥500 options
def expand_options(base_list, qualifiers, target=500):
    combos = [f"{q} {b}" for q in qualifiers for b in base_list]
    full   = list({*base_list, *combos})
    random.shuffle(full)
    while len(full) < target:
        full.append(fake.sentence(nb_words=3).rstrip("."))
    return full[:target]

# (2) base pools
base_symptoms = [
    "cough", "fever", "fatigue", "headache", "nausea", "vomiting", "dizziness",
    "rash", "pain", "swelling", "shortness of breath", "chest pain", "back pain",
    "diarrhea", "constipation", "insomnia", "anxiety", "depression", "tremors",
    "palpitations", "blurred vision", "itching", "joint pain", "edema", "dry mouth",
    "sore throat", "runny nose", "earache", "hearing loss", "tinnitus", "weight loss",
    "weight gain", "weakness", "tingling", "numbness", "chills", "sweating",
    "frequent urination", "burning urination", "menstrual cramps", "low libido"
]
base_histories = [
    "diabetes", "hypertension", "asthma", "allergies", "migraines", "thyroid disorder",
    "eczema", "anxiety", "depression", "COPD", "GERD", "IBS", "UTI", "tuberculosis",
    "pneumonia", "arthritis", "cataract surgery", "appendectomy", "hernia repair",
    "gallstones", "kidney stones", "stroke", "TIA", "leukemia", "cancer", "seizures",
    "fracture", "COVID-19", "hepatitis B", "HIV", "malaria", "chickenpox", "PTSD",
    "ADHD", "bipolar disorder", "PCOS", "sickle cell", "thalassemia", "anemia"
]
base_labs = [
    "WBC count", "RBC count", "hemoglobin", "platelet count", "cholesterol", "LDL",
    "HDL", "triglycerides", "blood sugar", "HbA1c", "TSH", "creatinine", "ALT", "AST",
    "CRP", "ESR", "D-dimer", "INR", "PT", "pH", "PaO2", "PaCO2", "bicarbonate",
    "ferritin", "vitamin B12", "vitamin D", "calcium", "potassium", "sodium", "magnesium"
]
base_meds = [
    "Paracetamol", "Ibuprofen", "Amoxicillin", "Azithromycin", "Metformin", "Lisinopril",
    "Atorvastatin", "Omeprazole", "Cetirizine", "Salbutamol", "Insulin", "Prednisone",
    "Warfarin", "Clopidogrel", "Ranitidine", "Diazepam", "Sertraline", "Escitalopram",
    "Fluconazole", "Doxycycline", "Hydrochlorothiazide", "Amlodipine", "Losartan",
    "Furosemide", "Metoprolol", "Clonazepam", "Tamsulosin", "Pantoprazole",
    "Sitagliptin", "Glimepiride"
]
base_exams = [
    "normal lung sounds", "wheezing", "crackles", "clear lungs", "normal heart sounds",
    "tachycardia", "bradycardia", "normal abdominal exam", "tenderness",
    "rebound tenderness", "normal neurological exam", "clonus", "Babinski reflex",
    "limp", "gait normal", "jaundiced sclera", "pale conjunctiva", "edema", "cyanosis",
    "ulceration", "rash", "erythema", "blisters", "lymphedema", "hepatomegaly",
    "splenomegaly"
]
base_treatment = [
    "antibiotics", "antivirals", "bronchodilators", "NSAIDs", "antidepressants",
    "antihypertensives", "insulin therapy", "physiotherapy", "CBT", "surgery referral",
    "imaging", "blood work", "dietary counseling", "smoking cessation", "CPAP trial",
    "wound care", "topical steroids", "multivitamins", "hydration", "rest",
    "analgesics", "anticoagulation", "vaccination", "allergy testing", "iron supplements"
]

# qualifiers
qualifiers_short = ["mild", "moderate", "severe", "acute", "chronic",
                    "intermittent", "persistent"]
qualifiers_long  = [
    "elevated", "low", "normal", "borderline high", "borderline low",
    "significantly elevated", "slightly low", "markedly elevated"
]

# ————————————————————————————————————————————————————————————————
# (3) expanded lists (≥ 500 options each)
symptoms_options        = expand_options(base_symptoms, qualifiers_short)
past_history_options    = expand_options(base_histories,
                                         ["history of", "family history of", "treated for"])
lab_results_options     = expand_options(base_labs, qualifiers_long)
medications_options     = expand_options(
    base_meds, [f"{d} mg" for d in [5, 10, 20, 50, 100, 250, 500]]
)
examination_options     = expand_options(base_exams, qualifiers_short)
treatment_plans_options = expand_options(
    base_treatment, ["recommend", "advise", "prescribe", "schedule"]
)

# look-ups
genders       = ["M", "F"]
locations     = ["Outpatient Clinic", "ER", "Telehealth", "Inpatient Ward"]
system_names  = ["Cardiac", "Respiratory", "GI", "GU", "Neuro", "MSK", "Derm"]
social_history_options = [
    "Non-smoker", "Smoker (5 pack-years)", "Occasional alcohol",
    "Recreational drug use", "Lives alone", "Lives with family",
]
imaging_options = [
    "Chest X-ray: clear lung fields",
    "Abdominal ultrasound: gallstones",
    "CT head: no acute intracranial abnormality",
    "MRI spine: degenerative changes",
    "EKG: normal sinus rhythm",
]
assessment_options = [
    "Acute bronchitis", "Community-acquired pneumonia", "Migraine headache",
    "Gastroenteritis", "Hypertensive urgency", "Anxiety disorder",
]

# ————————————————————————————————————————————————————————————————
# (4) master template
long_template = """
General Consultation Report
Patient ID: {patient_id}    Name: {patient_name}    Age/Gender: {age}/{gender}
Date: {appointment_date}    Location: {clinic_location}

CHIEF COMPLAINT:
- {chief_complaint}

HISTORY OF PRESENT ILLNESS:
{hpi}

PAST MEDICAL HISTORY:
- {past_history}

MEDICATIONS & ALLERGIES:
- Medications: {medications}
- Allergies: {allergies}

FAMILY & SOCIAL HISTORY:
- Family: {family_history}
- Social: {social_history}

REVIEW OF SYSTEMS (positive / negative):
{ros}

VITAL SIGNS:
  • Temperature: {temp} °C   • HR: {hr} bpm   • BP: {bp} mmHg
  • RR: {rr} /min            • SpO2: {spo2}%

SYSTEMS EXAM:
{systems_exam}

LAB RESULTS:
- {lab_results}

IMAGING:
- {imaging}

ASSESSMENT & PLAN:
Assessment:
- {assessment}
Plan:
{plan}

FOLLOW-UP:
- Return in {followup_days} days or sooner if symptoms worsen.

Physician: Dr. {provider_name}, {provider_title}
Signature: ________________________
""".strip()

# ————————————————————————————————————————————————————————————————
# (5) single-report generator
def generate_report():
    # demographics
    pid      = fake.bothify(text="??-####")
    name     = fake.name()
    age      = random.randint(18, 90)
    gender   = random.choice(genders)
    date     = fake.date(pattern="%d-%m-%Y", end_datetime=datetime.now() + timedelta(days=365))
    location = random.choice(locations)

    # CC & HPI
    cc       = random.choice(symptoms_options)
    hpi      = (
        f"{name} is a {age}-year-old {gender} presenting with {cc} for "
        f"{random.randint(1, 30)} days. Symptoms are "
        f"{random.choice(['intermittent', 'constant'])} and "
        f"{random.choice(['worsen with activity', 'relieved by rest'])}."
    )

    # ROS
    ros_lines = [
        f"- {sys}: {random.choice(['Denies', 'No'])} {random.choice(symptoms_options)}"
        for sys in system_names
    ]
    ros = "\n".join(ros_lines)

    # vitals
    temp = round(random.uniform(36.0, 39.0), 1)
    hr   = random.randint(60, 110)
    bp   = f"{random.randint(110, 140)}/{random.randint(70, 90)}"
    rr   = random.randint(12, 24)
    spo2 = random.randint(92, 100)

    # exams, labs, imaging
    exam_findings = random.sample(examination_options, k=4)
    labs          = random.sample(lab_results_options, k=2)
    imaging       = random.choice(imaging_options)

    # assessment & plan
    assess  = random.choice(assessment_options)
    meds    = random.choice(medications_options)
    plan_steps = [
        f"- Prescribe {meds}",
        f"- Advise {random.choice(['hydration', 'rest', 'dietary modifications'])}",
        f"- Recommend follow-up labs in {random.randint(3, 7)} days",
        f"- Refer to {random.choice(['pulmonology', 'neurology', 'GI', 'cardiology'])}",
    ]
    plan = "\n".join(plan_steps)

    # misc
    past_hist     = "; ".join(random.sample(past_history_options, k=2))
    allergies     = random.choice(["None", random.choice(["Penicillin", "Peanuts", "Sulfa drugs"])])
    fam_hist      = random.choice(past_history_options)
    soc_hist      = random.choice(social_history_options)
    followup_days = random.randint(7, 14)
    prov_name     = fake.last_name()
    prov_title    = random.choice(["MD", "DO", "PA-C", "NP"])

    # render template
    report_text = long_template.format(
        patient_id=pid,
        patient_name=name,
        age=age,
        gender=gender,
        appointment_date=date,
        clinic_location=location,
        chief_complaint=cc,
        hpi=hpi,
        past_history=past_hist,
        medications=meds,
        allergies=allergies,
        family_history=fam_hist,
        social_history=soc_hist,
        ros=ros,
        temp=temp,
        hr=hr,
        bp=bp,
        rr=rr,
        spo2=spo2,
        systems_exam="\n".join(f"- {f}" for f in exam_findings),
        lab_results="; ".join(labs),
        imaging=imaging,
        assessment=assess,
        plan=plan,
        followup_days=followup_days,
        provider_name=prov_name,
        provider_title=prov_title,
    )

    # --- ★ NEW: abstractive summary -----------------------------------------
    summary = (
        f"{name}, {age}{gender}, presented with {cc}. "
        f"Assessment: {assess}. Key plan: {meds.lower()}; "
        f"follow-up in {followup_days} days."
    )
    # ------------------------------------------------------------------------

    # annotation (ground-truth for NER or eval)
    annotation = {
        "patient_id": pid,
        "patient_name": name,
        "age": age,
        "gender": gender,
        "chief_complaint": cc,
        "hpi": hpi,
        "past_history": past_hist,
        "medications": meds,
        "allergies": allergies,
        "family_history": fam_hist,
        "social_history": soc_hist,
        "ros": ros_lines,
        "vitals": {"temp": temp, "hr": hr, "bp": bp, "rr": rr, "spo2": spo2},
        "systems_exam": exam_findings,
        "lab_results": labs,
        "imaging": imaging,
        "assessment": assess,
        "plan": plan_steps,
        "followup_days": followup_days,
    }

    # top-level record
    return {
        "report_text": report_text,
        "summary": summary,          # ★ NEW
        "annotation": annotation,
    }

# ————————————————————————————————————————————————————————————————
# (6) main loop
if __name__ == "__main__":
    num_reports = 10_000
    with open("synthetic_medical_reports.jsonl", "w", encoding="utf-8") as f:
        for _ in range(num_reports):
            json.dump(generate_report(), f, ensure_ascii=False)
            f.write("\n")
    print(f"Generated {num_reports:,} synthetic reports with summaries ✔")

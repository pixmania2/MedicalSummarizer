import random
import json
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# Data pools
patient_names = [fake.name() for _ in range(100)]

symptoms_options = [
    "dry cough", "low-grade fever", "fatigue", "shortness of breath", "headache", "chills",
    "body ache", "loss of appetite", "nausea", "vomiting", "diarrhea", "abdominal pain",
    "dizziness", "blurred vision", "sore throat", "chest pain", "palpitations", "insomnia",
    "night sweats", "joint pain", "back pain", "muscle cramps", "nasal congestion", "runny nose",
    "wheezing", "difficulty swallowing", "frequent urination", "burning urination",
    "painful menstruation", "irregular periods", "sensitivity to light", "itchy skin",
    "skin rash", "swollen lymph nodes", "earache", "hearing loss", "tinnitus", "cold hands",
    "cold feet", "hair loss", "weight gain", "weight loss", "anxiety", "depression",
    "irritability", "memory loss", "tingling in limbs", "numbness", "slurred speech",
    "persistent cough", "productive cough", "heartburn", "acid reflux", "constipation",
    "bloating", "gas", "change in bowel habits", "rectal bleeding", "difficulty breathing at night",
    "snoring", "dry mouth", "mouth ulcers", "bad breath", "frequent headaches", "vision loss",
    "eye redness", "eye discharge", "itchy eyes", "excessive thirst", "increased hunger",
    "sensitivity to sound", "clumsiness", "tremors", "restlessness", "hot flashes",
    "cold intolerance", "heat intolerance", "pain during sex", "low libido", "bruising easily",
    "bleeding gums", "swollen joints", "slow healing", "sleepwalking", "confusion", "hallucinations",
    "panic attacks", "tightness in chest", "difficulty focusing", "frequent nosebleeds",
    "unexplained fatigue", "general discomfort", "low back pain", "pain radiating to leg",
    "clogged ears", "difficulty urinating", "urge incontinence", "dry eyes", "facial swelling"
]

past_history_options = [
    "seasonal allergies", "diabetes diagnosed in 2019", "hypertension diagnosed in 2018",
    "asthma diagnosed in 2015", "history of appendectomy in 2012", "smoker for 10 years",
    "alcohol use - moderate", "GERD diagnosed in 2020", "migraine since teenage years",
    "thyroid disorder diagnosed in 2017", "fractured arm in 2014", "childhood asthma",
    "eczema since 2016", "diagnosed with anxiety in 2021", "sleep apnea", "knee surgery in 2019",
    "kidney stones in 2015", "family history of heart disease", "allergic to penicillin",
    "allergic to peanuts", "breast cancer in remission since 2018", "high cholesterol since 2014",
    "chronic sinusitis", "recurrent UTIs", "depression diagnosed in college", "hepatitis B - recovered",
    "broken nose in 2013", "tonsillectomy in 2000", "malaria in 2016", "chickenpox in childhood",
    "anemia diagnosed in 2011", "IBS - diagnosed in 2020", "past history of tuberculosis (treated)",
    "hernia surgery in 2018", "varicose veins", "COPD diagnosed in 2022", "vitamin D deficiency",
    "low B12 levels", "family history of diabetes", "C-section delivery in 2020",
    "menstrual irregularities", "PCOS diagnosed in 2019", "cataract surgery in 2021",
    "lactose intolerance", "gluten sensitivity", "cervical dysplasia (treated)",
    "eczema since childhood", "dermatitis", "past smoker - quit in 2016", "H. pylori infection in 2021",
    "tuberculosis exposure", "mental health hospitalization in 2018", "bariatric surgery",
    "gallbladder removed in 2017", "past use of corticosteroids", "severe acne history",
    "history of seizures", "nephritis in 2015", "chemotherapy in 2020", "radiation therapy in 2020",
    "past STD (chlamydia)", "drug allergy: sulfa drugs", "mononucleosis in 2012", "ulcerative colitis",
    "Crohn’s disease", "family history of breast cancer", "migraines with aura", "asbestos exposure",
    "past blood transfusion", "organ donor", "organ recipient", "past cardiac catheterization",
    "pacemaker implant in 2022", "prosthetic knee", "postpartum depression", "borderline personality disorder",
    "PTSD diagnosis", "ADHD since childhood", "bipolar disorder", "childhood leukemia",
    "COVID-19 in 2021", "long COVID symptoms", "allergic rhinitis", "recurrent bronchitis",
    "past pneumonia", "HIV positive", "syphilis (treated)", "diabetes - insulin-dependent",
    "hyperparathyroidism", "hypoparathyroidism", "stroke in 2019", "TIA in 2016", "car accident in 2014",
    "traumatic brain injury", "burn injury in 2020", "pneumothorax in 2018", "acid attack survivor",
    "liver cirrhosis", "pancreatitis", "sickle cell disease", "thalassemia minor"
]

lab_results_options = [
    "normal cholesterol levels", "Oxygen saturation 96%", "BP 120/80", "blood sugar 110 mg/dL",
    "elevated WBC count", "low hemoglobin", "platelet count within normal range",
    "HbA1c 6.2%", "creatinine 0.9 mg/dL", "elevated liver enzymes", "normal liver function test",
    "mild anemia", "urinalysis: no abnormalities", "ECG: normal sinus rhythm", "X-ray: clear lungs",
    "MRI: no abnormalities", "ultrasound: gallstones", "thyroid levels normal",
    "TSH 3.1 mIU/L", "high LDL cholesterol", "low HDL cholesterol", "triglycerides 150 mg/dL",
    "blood group B+", "RBC count normal", "serum calcium: 9.5 mg/dL", "CRP elevated",
    "ESR 20 mm/hr", "COVID-19 test: negative", "COVID antibodies: positive", "HIV test: negative",
    "Hepatitis B surface antigen: negative", "ANA test: negative", "D-dimer: normal", "PT: 12s",
    "INR: 1.0", "Vitamin D: 22 ng/mL", "B12: 450 pg/mL", "Ferritin: low", "ALT: 45 U/L",
    "AST: 38 U/L", "uric acid: high", "cholesterol: 210 mg/dL", "LDL: 160 mg/dL",
    "HDL: 35 mg/dL", "Triglycerides: 250 mg/dL", "Echo: normal valves", "EEG: normal",
    "Chest CT: no consolidation", "blood culture: negative", "urine culture: E.coli detected",
    "Pap smear: normal", "mammogram: no masses", "PSA: 3.2 ng/mL", "sperm count: normal",
    "FSH: normal", "LH: normal", "Testosterone: low", "insulin levels: elevated",
    "GTT: impaired glucose tolerance", "coagulation profile: normal", "pH: 7.4",
    "PaO2: 95 mmHg", "PaCO2: 40 mmHg", "bicarbonate: 24 mEq/L", "anemia profile: microcytic",
    "blood smear: normal", "stool culture: negative", "clotting time: 3 min", "bleeding time: 2 min",
    "prolactin: normal", "serum cortisol: high", "ACTH: normal", "liver biopsy: fatty liver",
    "renal ultrasound: normal", "KFT: within normal limits", "LFT: mild elevation", 
    "CPK: normal", "H. pylori antigen: positive", "Malaria parasite: negative", "Dengue NS1: negative",
    "Widal test: negative", "Chikungunya IgM: negative", "ANA profile: negative", "rheumatoid factor: negative",
    "blood ammonia: elevated", "bilirubin: 1.1 mg/dL", "total protein: 6.5 g/dL"
]

medications_options = [
    "Bronchodilator: 2 puffs", "Antibiotic: 250mg for 5 days", "Antihistamine: 10mg",
    "Paracetamol: 500mg every 6 hours", "Ibuprofen: 400mg twice a day", "Metformin: 500mg daily",
    "Lisinopril: 10mg once a day", "Atorvastatin: 20mg at bedtime", "Amoxicillin: 500mg TID",
    "Doxycycline: 100mg BID", "Azithromycin: 500mg once daily", "Cough syrup: 10ml thrice daily",
    "Insulin: 10 units before meals", "Salbutamol inhaler: 2 puffs every 4 hours", "Cetirizine: 10mg at night",
    "Omeprazole: 20mg before breakfast", "Ranitidine: 150mg BID", "Prednisone: 5mg daily",
    "Multivitamin: one daily", "Vitamin D: 60,000 IU weekly", "Calcium supplement: 500mg",
    "Iron supplement: once daily", "Clopidogrel: 75mg", "Aspirin: 81mg", "Warfarin: 5mg",
    "Losartan: 50mg", "Hydrochlorothiazide: 25mg", "Levothyroxine: 50mcg", "Insulin glargine: 12 units",
    "Nasal spray: 2 sprays per nostril", "Eye drops: 2 drops every 8 hours", "Topical cream: apply twice",
    "Oral rehydration salts", "Fluconazole: 150mg", "Nystatin: swish and swallow", "Metronidazole: 400mg",
    "Probiotic: daily", "Loperamide: 2mg", "Domperidone: 10mg before meals", "Pantoprazole: 40mg",
    "Tamsulosin: 0.4mg at night", "Sildenafil: 50mg", "Sertraline: 50mg", "Escitalopram: 10mg",
    "Diazepam: 5mg", "Lorazepam: 1mg", "Clonazepam: 0.5mg", "Haloperidol: 2mg",
    "Insulin aspart: 4 units", "Glimepiride: 2mg", "Glyburide: 5mg", "Sitagliptin: 100mg",
    "Saxagliptin: 2.5mg", "Erythromycin: 250mg", "Nicotine patch: daily", "Saline nebulization",
    "Hydrocortisone: IV", "Adrenaline: IM", "Chlorpheniramine: 4mg", "Mupirocin ointment",
    "Zinc supplement", "Amlodipine: 5mg", "Bisoprolol: 2.5mg", "Diltiazem: 30mg",
    "Nifedipine: 10mg", "Enoxaparin: 40mg SC", "Gentamicin: 80mg IV", "Furosemide: 40mg"
]

examination_options = [
    "mild bilateral wheezing", "clear lung sounds", "stable oxygen saturation",
    "tachycardia observed", "bradycardia observed", "normal heart sounds",
    "no pedal edema", "swollen lymph nodes in neck", "red throat", "tonsils enlarged",
    "abdominal tenderness", "rigid abdomen", "no rebound tenderness",
    "decreased breath sounds", "coarse crackles", "fine rales", "skin warm and dry",
    "cyanosis of lips", "jaundiced sclera", "clubbing of fingers", "normal gait",
    "reduced reflexes", "muscle strength 5/5", "normal bowel sounds",
    "hypoactive bowel sounds", "spine curvature normal", "scoliosis present",
    "nystagmus noted", "positive Babinski reflex", "negative Romberg test",
    "normal range of motion", "limping observed", "pupils equal and reactive",
    "pale conjunctiva", "palmar erythema", "nail pitting", "erythematous rash",
    "urticarial rash", "blisters on lower limbs", "hepatomegaly", "splenomegaly",
    "inguinal swelling", "breath sounds equal bilaterally", "percussion dullness at base",
    "orthopnea observed", "diaphoresis", "tachypnea", "bruising on arms", "bleeding gums"
]

treatment_plans_options = [
    "recommended increased fluid intake and rest", "advised follow-up visit in 7 days",
    "prescribed a short course of antibiotics", "scheduled for imaging test",
    "referred to specialist", "started physiotherapy", "advised dietary changes",
    "prescribed anti-inflammatory drugs", "recommended stress reduction",
    "counseled for smoking cessation", "vaccination scheduled", "advised COVID test",
    "prescribed inhaler", "encouraged daily walking", "scheduled for blood work",
    "referred for colonoscopy", "prescribed antidepressants", "started insulin therapy",
    "follow-up in 1 month", "advised hydration and sleep", "applied topical ointment",
    "recommended surgery consultation", "advised to avoid allergens",
    "suggested mindfulness practice", "initiated CBT", "ordered MRI scan",
    "recommended glasses", "scheduled dental cleaning", "referral to dermatologist",
    "advised avoiding caffeine", "prescribed calcium supplements", "referred for counseling",
    "advised CPAP trial", "discussed medication adherence", "suggested pelvic exercises",
    "provided ergonomic advice", "adjusted medication dosage", "restarted previous medication",
    "prescribed anti-anxiety meds", "recommended bed rest", "prescribed multivitamins",
    "encouraged journaling", "guided breathing exercises", "gave wound care instructions",
    "advised avoiding NSAIDs", "started desensitization therapy", "initiated statin therapy"
]

# Define three templates for different report lengths
templates = {
    "short": (
        "General Consultation\nPatient: {patient_name}, Age: {age}\nDate: {appointment_date}\n\n"
        "{patient_name} presented with {symptom_summary}. Past history includes {past_history}. "
        "Examination revealed {examination}. Treatment: {treatment_plan}."
    ),
    "medium": (
        "General Consultation\nPatient {patient_name} (Age: {age}) visited on {appointment_date}.\n"
        "Symptoms: {symptom_details}.\nMedical History: {past_history}.\nLab Results: {lab_results}.\n"
        "Examination: {examination}.\nTreatment: {treatment_plan}."
    ),
    "long": (
        "General Consultation\nPatient: {patient_name} | Age: {age}\nAppointment Date: {appointment_date}\n\n"
        "Detailed Report:\n{patient_name} is a {age}-year-old patient presenting with {symptom_details}. "
        "The patient has a history including {past_history}. Lab analysis showed: {lab_results}, and "
        "examination revealed: {examination}. The treatment plan includes {medications} along with "
        "recommendations for follow-up in {followup}. Additional Notes: {additional_notes}."
    )
}

def generate_report():
    # Choose a random template type and get the corresponding template string
    template_type = random.choice(list(templates.keys()))
    template = templates[template_type]
    
    # Generate the fields once and store them in variables
    patient_name = random.choice(patient_names)
    age = random.randint(18, 90)
    appointment_date = fake.date(pattern="%d-%m-%Y", end_datetime=datetime.now() + timedelta(days=365))
    
    # Select symptoms consistently for both summary and detailed versions
    num_symptoms = random.randint(1, 3)
    selected_symptoms = random.sample(symptoms_options, num_symptoms)
    symptom_summary = ", ".join(selected_symptoms)
    symptom_details = ", ".join(selected_symptoms)  # Ensures consistency
    
    # Select past history (1 or 2 items)
    num_history = random.randint(1, 2)
    selected_history = random.sample(past_history_options, num_history)
    past_history = "; ".join(selected_history)
    
    # Select lab results (1 or 2 items)
    num_lab = random.randint(1, 2)
    selected_lab = random.sample(lab_results_options, num_lab)
    lab_results = "; ".join(selected_lab)
    
    # Other fields
    examination = random.choice(examination_options)
    treatment_plan = random.choice(treatment_plans_options)
    medications = random.choice(medications_options)
    followup = f"{random.randint(3, 14)} days"
    additional_notes = (
        "Patient advised to maintain a symptom diary." if random.random() > 0.5 
        else "No additional notes."
    )
    
    # Fill in the chosen template with the same variable values
    report_text = template.format(
        patient_name=patient_name,
        age=age,
        appointment_date=appointment_date,
        symptom_summary=symptom_summary,
        symptom_details=symptom_details,
        past_history=past_history,
        lab_results=lab_results,
        examination=examination,
        treatment_plan=treatment_plan,
        medications=medications,
        followup=followup,
        additional_notes=additional_notes
    )
    
    # Create a JSON annotation that mirrors the fields used in the report text
    annotation = {
        "patient_name": patient_name,
        "age": age,
        "appointment_date": appointment_date,
        "symptoms": symptom_details,
        "past_history": past_history,
        "lab_results": lab_results,
        "medications": medications,
        "examination": examination
    }
    
    return {"report_text": report_text, "annotation": annotation}

# Generate 1,000 reports and write to a JSON Lines file
num_reports = 1000
with open("synthetic_medical_reports.jsonl", "w") as outfile:
    for _ in range(num_reports):
        report_entry = generate_report()
        outfile.write(json.dumps(report_entry) + "\n")

print("Synthetic dataset of", num_reports, "reports generated successfully.")

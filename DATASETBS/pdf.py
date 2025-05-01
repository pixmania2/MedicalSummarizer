import os
import random
import json
from datetime import datetime, timedelta
from faker import Faker

# ReportLab imports for Platypus
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

fake = Faker()
# Base pools (keep these relatively small—~50 entries each)
patient_names = [fake.name() for _ in range(100)]
base_symptoms = [
    "cough", "fever", "fatigue", "headache", "nausea",
    "vomiting", "dizziness", "rash", "pain", "swelling",
    "shortness of breath", "chest pain", "back pain", "diarrhea",
    "constipation", "insomnia", "anxiety", "depression", "tremors",
    "palpitations", "blurred vision", "itching", "joint pain", "edema",
    "dry mouth", "sore throat", "runny nose", "earache", "hearing loss",
    "tinnitus", "weight loss", "weight gain", "weakness", "tingling",
    "numbness", "chills", "sweating", "frequent urination", "burning urination",
    "menstrual cramps", "low libido", "memory loss", "restlessness", "hallucinations"
]
base_histories = [
    "diabetes", "hypertension", "asthma", "allergies", "migraines",
    "thyroid disorder", "eczema", "anxiety", "depression", "COPD",
    "GERD", "IBS", "UTI", "tuberculosis", "pneumonia",
    "arthritis", "cataract surgery", "appendectomy", "hernia repair", "gallstones",
    "kidney stones", "stroke", "TIA", "leukemia", "cancer",
    "seizures", "fracture", "COVID-19", "hepatitis B", "HIV",
    "malaria", "chickenpox", "PTSD", "ADHD", "bipolar disorder",
    "PCOS", "sickle cell", "thalassemia", "vitamin D deficiency", "anemia"
]
base_labs = [
    "WBC count", "RBC count", "hemoglobin", "platelet count", "cholesterol",
    "LDL", "HDL", "triglycerides", "blood sugar", "HbA1c",
    "TSH", "creatinine", "ALT", "AST", "CRP",
    "ESR", "D-dimer", "INR", "PT", "pH",
    "PaO2", "PaCO2", "bicarbonate", "ferritin", "vitamin B12",
    "vitamin D", "calcium", "potassium", "sodium", "magnesium"
]
base_meds = [
    "Paracetamol", "Ibuprofen", "Amoxicillin", "Azithromycin",
    "Metformin", "Lisinopril", "Atorvastatin", "Omeprazole",
    "Cetirizine", "Salbutamol", "Insulin", "Prednisone",
    "Warfarin", "Clopidogrel", "Ranitidine", "Diazepam",
    "Sertraline", "Escitalopram", "Fluconazole", "Doxycycline",
    "Hydrochlorothiazide", "Amlodipine", "Losartan", "Furosemide",
    "Metoprolol", "Clonazepam", "Tamsulosin", "Pantoprazole",
    "Sitagliptin", "Glimepiride"
]
base_exams = [
    "normal lung sounds", "wheezing", "crackles", "clear lungs",
    "normal heart sounds", "tachycardia", "bradycardia",
    "normal abdominal exam", "tenderness", "rebound tenderness",
    "normal neurological exam", "clonus", "Babinski reflex",
    "limp", "gait normal", "jaundiced sclera", "pale conjunctiva",
    "edema", "cyanosis", "ulceration", "rash", "erythema",
    "blisters", "lymphedema", "hepatomegaly", "splenomegaly"
]
base_treatment = [
    "antibiotics", "antivirals", "bronchodilators", "NSAIDs",
    "antidepressants", "antihypertensives", "insulin therapy",
    "physiotherapy", "CBT", "surgery referral", "imaging",
    "blood work", "dietary counseling", "smoking cessation",
    "CPAP trial", "wound care", "topical steroids", "multivitamins",
    "hydration", "rest", "analgesics", "anticoagulation", "vaccination",
    "allergy testing", "immune therapy", "iron supplements"
]

# Qualifiers to combine
qualifiers_short = ["mild", "moderate", "severe", "acute", "chronic",
                    "intermittent", "persistent", "occasional", "sudden"]
qualifiers_long  = ["elevated", "low", "normal", "borderline high",
                    "borderline low", "significantly elevated", "slightly low",
                    "markedly elevated", "markedly low", "unremarkable"]

def expand_options(base_list, qualifiers, target=500):
    # create qualifier + base combinations
    combos = [f"{q} {b}" for q in qualifiers for b in base_list]
    full = list({*base_list, *combos})
    random.shuffle(full)
    # if still short, pad with faker-generated phrases
    while len(full) < target:
        full.append(fake.sentence(nb_words=3).rstrip('.'))
    return full[:target]

symptoms_options        = expand_options(base_symptoms, qualifiers_short)
past_history_options    = expand_options(base_histories, ["history of", "family history of", "treated for"])
lab_results_options     = expand_options(base_labs, qualifiers_long)
medications_options     = expand_options(base_meds, ["{} mg".format(d) for d in [5,10,20,50,100,250,500]], target=500)
examination_options     = expand_options(base_exams, qualifiers_short)
treatment_plans_options = expand_options(base_treatment, ["recommend", "advise", "prescribe", "schedule"], target=500)

# Templates unchanged…
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
    ttype = random.choice(list(templates))
    tpl   = templates[ttype]
    name  = random.choice(patient_names)
    age   = random.randint(18, 90)
    date  = fake.date(pattern="%d-%m-%Y", end_datetime=datetime.now() + timedelta(days=365))
    # pick details
    syms = random.sample(symptoms_options, random.randint(1,3))
    past = random.sample(past_history_options, random.randint(1,2))
    labs = random.sample(lab_results_options, random.randint(1,2))
    exam = random.choice(examination_options)
    treat= random.choice(treatment_plans_options)
    meds = random.choice(medications_options)
    foll = f"{random.randint(3,14)} days"
    addn = "Patient advised to maintain a symptom diary." if random.random()>0.5 else "No additional notes."
    rpt  = tpl.format(
        patient_name=name, age=age, appointment_date=date,
        symptom_summary=", ".join(syms),
        symptom_details=", ".join(syms),
        past_history="; ".join(past),
        lab_results="; ".join(labs),
        examination=exam, treatment_plan=treat,
        medications=meds, followup=foll, additional_notes=addn
    )
    ann  = {
        "patient_name": name, "age": age, "appointment_date": date,
        "symptoms": ", ".join(syms), "past_history": "; ".join(past),
        "lab_results": "; ".join(labs), "medications": meds, "examination": exam
    }
    return {"report_text": rpt, "annotation": ann}

# (2) PDF output directory
output_dir = "pdf_reports"
os.makedirs(output_dir, exist_ok=True)

# (3) Prepare styles
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="ReportTitle",
    parent=styles["Heading1"],
    fontSize=18,
    alignment=TA_CENTER,
    spaceAfter=12
))
styles.add(ParagraphStyle(
    name="BodyLabel",
    parent=styles["Heading2"],
    fontSize=12,
    alignment=TA_LEFT,
    spaceAfter=6
))
styles.add(ParagraphStyle(
    name="BodyTextWrap",
    parent=styles["BodyText"],
    fontSize=10,
    leading=12,
    alignment=TA_LEFT,
    spaceAfter=8
))

# (4) Generate 100 well-formatted PDFs
for i in range(1, 101):
    data = generate_report()
    text = data["report_text"]
    
    pdf_path = os.path.join(output_dir, f"report_{i:03d}.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    story = []
    # Title
    story.append(Paragraph(f"Medical Report #{i:03d}", styles["ReportTitle"]))
    story.append(Spacer(1, 0.2*inch))
    
    # Split into lines and label sections
    # Assuming your template starts with "General Consultation"
    lines = text.split("\n")
    for line in lines:
        if line.strip() == "":
            continue
        # Treat the first non-blank line as section header
        if line.startswith("General Consultation"):
            story.append(Paragraph(line, styles["BodyLabel"]))
        else:
            story.append(Paragraph(line, styles["BodyTextWrap"]))
    
    # Add a page break after each report (except last)
    if i < 100:
        story.append(PageBreak())
    
    doc.build(story)

print("100 formatted PDFs generated in:", output_dir)
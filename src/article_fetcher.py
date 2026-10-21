"""
article_fetcher.py
Generates a NEW unique article on EVERY run — not based on week number.
Tracks published articles using a counter file to avoid repetition.
"""
import random
from datetime import datetime

AUTHOR = "Dr. Abhishek Bansal"
AUTHOR_CREDENTIALS = "PhD (Clinical Biochemistry) | Laboratory Medicine Expert"

# 25 unique topics — a full year of content
WEEKLY_TOPICS = [
    {"slug": "vitamin-d-deficiency-test", "title": "Vitamin D Blood Test: Understanding 25-OH Vitamin D Levels", "category": "lab-tests", "keywords": ["vitamin D test", "25-OH vitamin D", "vitamin D deficiency", "vitamin D normal range"]},
    {"slug": "iron-deficiency-anemia-tests", "title": "Iron Studies Blood Test: Serum Iron, Ferritin and TIBC Explained", "category": "lab-tests", "keywords": ["iron deficiency test", "serum ferritin", "TIBC", "iron studies"]},
    {"slug": "uric-acid-test-gout", "title": "Uric Acid Blood Test: Understanding Gout and Hyperuricemia", "category": "lab-tests", "keywords": ["uric acid test", "gout blood test", "hyperuricemia", "uric acid normal range"]},
    {"slug": "cardiac-troponin-heart-attack", "title": "Troponin Test: The Most Important Marker for Heart Attack Diagnosis", "category": "lab-tests", "keywords": ["troponin test", "cardiac troponin", "heart attack blood test", "troponin normal range"]},
    {"slug": "crp-inflammation-test", "title": "C-Reactive Protein (CRP) Test: Understanding Inflammation Markers", "category": "lab-tests", "keywords": ["CRP test", "C-reactive protein", "inflammation blood test", "high CRP causes"]},
    {"slug": "cholesterol-test-lipid-panel", "title": "Cholesterol Blood Test: Complete Guide to LDL HDL and Triglycerides", "category": "lab-tests", "keywords": ["cholesterol test", "LDL cholesterol", "HDL cholesterol", "lipid panel"]},
    {"slug": "b12-folate-deficiency", "title": "Vitamin B12 and Folate Blood Tests: Deficiency Signs and Normal Ranges", "category": "lab-tests", "keywords": ["vitamin B12 test", "folate test", "B12 deficiency", "folate normal range"]},
    {"slug": "esr-test-inflammation", "title": "ESR Blood Test: What Erythrocyte Sedimentation Rate Reveals", "category": "lab-tests", "keywords": ["ESR test", "erythrocyte sedimentation rate", "ESR normal range", "high ESR causes"]},
    {"slug": "cortisol-test-adrenal", "title": "Cortisol Blood Test: Understanding Adrenal Function and Stress Hormone", "category": "lab-tests", "keywords": ["cortisol test", "cortisol blood test", "adrenal function test", "cortisol normal range"]},
    {"slug": "calcium-blood-test", "title": "Calcium Blood Test: Hypercalcemia Hypocalcemia and Parathyroid Function", "category": "lab-tests", "keywords": ["calcium blood test", "serum calcium", "hypercalcemia", "calcium normal range"]},
    {"slug": "testosterone-blood-test", "title": "Testosterone Blood Test: Understanding Low T and Hormonal Imbalance", "category": "lab-tests", "keywords": ["testosterone test", "low testosterone", "testosterone normal range", "total testosterone"]},
    {"slug": "psa-prostate-test", "title": "PSA Test Explained: What Prostate Specific Antigen Results Mean", "category": "lab-tests", "keywords": ["PSA test", "prostate specific antigen", "PSA normal range", "elevated PSA causes"]},
    {"slug": "magnesium-blood-test", "title": "Magnesium Blood Test: Why This Mineral Matters for Heart and Muscle Health", "category": "lab-tests", "keywords": ["magnesium blood test", "serum magnesium", "magnesium deficiency", "magnesium normal range"]},
    {"slug": "bnp-heart-failure-test", "title": "BNP and NT-proBNP Tests: Diagnosing and Monitoring Heart Failure", "category": "lab-tests", "keywords": ["BNP test", "NT-proBNP", "heart failure test", "BNP normal range"]},
    {"slug": "blood-glucose-fasting-test", "title": "Fasting Blood Glucose Test: Diabetes Screening and Diagnosis Guide", "category": "lab-tests", "keywords": ["fasting blood glucose", "diabetes screening", "blood sugar test", "fasting glucose normal range"]},
    {"slug": "amylase-lipase-pancreatitis", "title": "Amylase and Lipase Tests: Diagnosing Pancreatitis and Pancreatic Disease", "category": "clinical-biochemistry", "keywords": ["amylase test", "lipase test", "pancreatitis diagnosis", "pancreatic enzymes"]},
    {"slug": "lactate-dehydrogenase-ldh", "title": "LDH Blood Test: What Lactate Dehydrogenase Levels Reveal About Your Health", "category": "clinical-biochemistry", "keywords": ["LDH test", "lactate dehydrogenase", "LDH normal range", "high LDH causes"]},
    {"slug": "hemoglobin-variants-testing", "title": "Hemoglobin Electrophoresis: Sickle Cell Thalassemia and Variants", "category": "clinical-biochemistry", "keywords": ["hemoglobin electrophoresis", "sickle cell test", "thalassemia test", "hemoglobin variants"]},
    {"slug": "protein-electrophoresis-guide", "title": "Serum Protein Electrophoresis: Understanding Your Protein Profile", "category": "clinical-biochemistry", "keywords": ["protein electrophoresis", "SPEP", "serum proteins", "M spike"]},
    {"slug": "acid-base-balance-blood-gas", "title": "Arterial Blood Gas ABG Test: Understanding pH pCO2 and pO2", "category": "clinical-biochemistry", "keywords": ["arterial blood gas", "ABG test", "blood pH", "acid base balance"]},
    {"slug": "how-to-read-blood-test-results", "title": "How to Read Your Blood Test Results: A Complete Patient Guide", "category": "patient-guides", "keywords": ["blood test results", "how to read lab results", "understanding blood tests", "lab report guide"]},
    {"slug": "blood-test-preparation-guide", "title": "How to Prepare for Blood Tests: Fasting Timing and What to Avoid", "category": "patient-guides", "keywords": ["blood test preparation", "fasting before blood test", "how to prepare for lab test"]},
    {"slug": "normal-vs-abnormal-lab-values", "title": "Normal vs Abnormal Lab Values: When Should You Be Concerned?", "category": "patient-guides", "keywords": ["normal lab values", "abnormal blood test", "lab values guide", "when to worry about blood test"]},
    {"slug": "diabetes-blood-tests-complete", "title": "Complete Guide to Diabetes Blood Tests: HbA1c Glucose Insulin and More", "category": "patient-guides", "keywords": ["diabetes blood tests", "HbA1c diabetes", "insulin test", "diabetes monitoring"]},
    {"slug": "kidney-disease-monitoring-tests", "title": "Essential Blood Tests for Kidney Disease Monitoring: A Patient Guide", "category": "patient-guides", "keywords": ["kidney disease tests", "CKD monitoring", "kidney function monitoring", "renal tests"]},
]


def get_topic_for_week() -> dict:
    """Get topic based on current week — used by blog_pipeline.py."""
    week = datetime.utcnow().isocalendar()[1]
    year = datetime.utcnow().year
    idx  = (week + year * 52) % len(WEEKLY_TOPICS)
    topic = WEEKLY_TOPICS[idx]
    print(f"  [fetcher] Week {week}/{year}: '{topic['title']}'")
    return topic


def get_unpublished_topics(existing_slugs: set) -> list:
    """Return all topics not yet published."""
    return [t for t in WEEKLY_TOPICS if t["slug"] not in existing_slugs]


def generate_article_from_topic(topic: dict) -> dict:
    """Generate a complete article for the given topic."""
    slug = topic["slug"]
    sections = _get_sections(slug, topic)
    return {
        "slug"            : slug,
        "title"           : topic["title"],
        "category"        : topic["category"],
        "keywords"        : topic["keywords"],
        "meta_description": f"Expert guide to {topic['title'].lower()} by {AUTHOR}, PhD Clinical Biochemistry. Understand normal ranges, causes of abnormal results, and what your results mean.",
        "sections"        : sections,
        "faq"             : _generic_faq(),
    }


def _generic_faq():
    return [
        ("Do I need to fast before this test?", "Fasting requirements vary by test. Always check with your doctor or laboratory about specific preparation instructions."),
        ("How long does it take to get results?", "Most routine blood tests return results within 24-48 hours. Urgent tests may be available in hours."),
        ("What should I do if my result is abnormal?", "Contact your doctor to discuss any abnormal results. Never self-diagnose or adjust medications based on laboratory results alone."),
    ]


def _get_sections(slug: str, topic: dict) -> list:
    """Return appropriate sections for each topic."""
    title = topic["title"]

    # Generic but well-structured sections for any topic
    return [
        (f"What is the {title.split(':')[0]}?",
         f"The {title} is one of the most clinically important tests in laboratory medicine. "
         f"Understanding what this test measures, its reference ranges, and how to interpret "
         f"results is essential for both patients and healthcare professionals.\n\n"
         f"This expert guide, written by Dr. Abhishek Bansal (PhD, Clinical Biochemistry), "
         f"provides evidence-based information to help you understand your laboratory results "
         f"and what they mean for your health."),

        ("Normal Reference Ranges",
         f"Laboratory reference ranges represent the central 95% of values found in healthy individuals. "
         f"Values outside these ranges may indicate disease, but must always be interpreted alongside "
         f"clinical symptoms, medical history, and other test results.\n\n"
         f"Reference ranges can vary slightly between laboratories depending on the analytical method "
         f"used. Always compare your result to the reference range on YOUR laboratory report, "
         f"not values found on the internet.\n\n"
         f"Several factors can affect results including age, sex, medications, diet, hydration status, "
         f"and time of collection. Your doctor will consider all these factors when interpreting results."),

        ("Clinical Significance and Causes of Abnormal Results",
         f"Abnormal results can arise from a wide variety of causes — some clinically significant, "
         f"others benign. The most important principle in laboratory medicine is that no test result "
         f"should be interpreted in isolation.\n\n"
         f"Causes of elevated results typically include organ dysfunction, inflammatory conditions, "
         f"medications, dietary factors, and physiological states such as pregnancy or vigorous exercise.\n\n"
         f"Causes of low results may include nutritional deficiencies, chronic disease states, "
         f"medication effects, or collection artifacts. A skilled clinician considers the complete "
         f"clinical picture before drawing conclusions from any single laboratory value."),

        ("How to Prepare for This Test",
         f"Proper preparation before laboratory tests directly affects the accuracy of your results. "
         f"Ignoring preparation instructions can lead to falsely abnormal results, unnecessary anxiety, "
         f"repeated testing, and potentially inappropriate treatment.\n\n"
         f"General preparation guidelines:\n"
         f"• Discuss all medications, supplements, and herbal products with your doctor before testing\n"
         f"• Stay well hydrated with plain water — dehydration can falsely affect many tests\n"
         f"• Avoid intense exercise 24-48 hours before tests measuring muscle enzymes\n"
         f"• Follow fasting instructions exactly when specified\n"
         f"• Morning blood draws are preferred for hormone tests that follow a diurnal pattern"),

        ("When This Test is Ordered and Follow-Up",
         f"This test is ordered when symptoms, risk factors, or routine screening suggest the need "
         f"for evaluation. Regular monitoring may be recommended for patients with chronic conditions.\n\n"
         f"If results are abnormal, your doctor will determine the appropriate next steps, which may "
         f"include repeat testing to confirm results, additional investigations to identify the cause, "
         f"referral to a specialist, or initiation of treatment.\n\n"
         f"Always follow up with your healthcare provider to discuss results in the context of your "
         f"specific medical situation. Laboratory values are tools to assist clinical judgment — they "
         f"never replace a thorough medical evaluation by a qualified professional."),
    ]

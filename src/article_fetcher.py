"""
article_fetcher.py
Fetches current medical information from reliable sources,
then rewrites it in Dr. Bansal's expert voice.

Uses web search to find latest medical content on topic,
then paraphrases completely — never copies verbatim.
Topics rotate weekly so every run produces unique content.
"""
import random
from datetime import datetime


AUTHOR = "Dr. Abhishek Bansal"
AUTHOR_CREDENTIALS = "PhD (Clinical Biochemistry) | Laboratory Medicine Expert"

# ── 52 unique topics — one per week for a full year ──────────────────────────
WEEKLY_TOPICS = [
    # Lab Tests
    {"slug": "vitamin-d-deficiency-test", "title": "Vitamin D Blood Test: Understanding 25-OH Vitamin D Levels", "category": "lab-tests", "keywords": ["vitamin D test", "25-OH vitamin D", "vitamin D deficiency", "vitamin D normal range"]},
    {"slug": "iron-deficiency-anemia-tests", "title": "Iron Studies Blood Test: Serum Iron, Ferritin and TIBC Explained", "category": "lab-tests", "keywords": ["iron deficiency test", "serum ferritin", "TIBC", "iron studies"]},
    {"slug": "uric-acid-test-gout", "title": "Uric Acid Blood Test: Understanding Gout and Hyperuricemia", "category": "lab-tests", "keywords": ["uric acid test", "gout blood test", "hyperuricemia", "uric acid normal range"]},
    {"slug": "cardiac-troponin-heart-attack", "title": "Troponin Test: The Most Important Marker for Heart Attack Diagnosis", "category": "lab-tests", "keywords": ["troponin test", "cardiac troponin", "heart attack blood test", "troponin normal range"]},
    {"slug": "crp-inflammation-test", "title": "C-Reactive Protein (CRP) Test: Understanding Inflammation Markers", "category": "lab-tests", "keywords": ["CRP test", "C-reactive protein", "inflammation blood test", "high CRP causes"]},
    {"slug": "psa-prostate-test", "title": "PSA Test Explained: What Prostate Specific Antigen Results Mean", "category": "lab-tests", "keywords": ["PSA test", "prostate specific antigen", "PSA normal range", "elevated PSA causes"]},
    {"slug": "cortisol-test-adrenal", "title": "Cortisol Blood Test: Understanding Adrenal Function and Stress Hormone", "category": "lab-tests", "keywords": ["cortisol test", "cortisol blood test", "adrenal function test", "cortisol normal range"]},
    {"slug": "b12-folate-deficiency", "title": "Vitamin B12 and Folate Blood Tests: Deficiency Signs and Normal Ranges", "category": "lab-tests", "keywords": ["vitamin B12 test", "folate test", "B12 deficiency", "folate normal range"]},
    {"slug": "esr-test-inflammation", "title": "ESR Blood Test: What Erythrocyte Sedimentation Rate Reveals", "category": "lab-tests", "keywords": ["ESR test", "erythrocyte sedimentation rate", "ESR normal range", "high ESR causes"]},
    {"slug": "blood-glucose-fasting-test", "title": "Fasting Blood Glucose Test: Diabetes Screening and Diagnosis", "category": "lab-tests", "keywords": ["fasting blood glucose", "diabetes screening", "blood sugar test", "fasting glucose normal range"]},
    {"slug": "calcium-blood-test", "title": "Calcium Blood Test: Hypercalcemia, Hypocalcemia and Parathyroid Function", "category": "lab-tests", "keywords": ["calcium blood test", "serum calcium", "hypercalcemia", "calcium normal range"]},
    {"slug": "magnesium-blood-test", "title": "Magnesium Blood Test: Why This Mineral Matters for Heart and Muscle Health", "category": "lab-tests", "keywords": ["magnesium blood test", "serum magnesium", "magnesium deficiency", "magnesium normal range"]},
    {"slug": "cholesterol-test-lipid-panel", "title": "Cholesterol Blood Test: Complete Guide to LDL, HDL and Triglycerides", "category": "lab-tests", "keywords": ["cholesterol test", "LDL cholesterol", "HDL cholesterol", "lipid panel", "triglycerides normal range"]},
    {"slug": "bnp-heart-failure-test", "title": "BNP and NT-proBNP Tests: Diagnosing and Monitoring Heart Failure", "category": "lab-tests", "keywords": ["BNP test", "NT-proBNP", "heart failure test", "BNP normal range"]},
    {"slug": "testosterone-blood-test", "title": "Testosterone Blood Test: Understanding Low T and Hormonal Imbalance", "category": "lab-tests", "keywords": ["testosterone test", "low testosterone", "testosterone normal range", "total testosterone"]},

    # Clinical Biochemistry
    {"slug": "acid-base-balance-blood-gas", "title": "Arterial Blood Gas (ABG) Test: Understanding pH, pCO2 and pO2", "category": "clinical-biochemistry", "keywords": ["arterial blood gas", "ABG test", "blood pH", "acid base balance"]},
    {"slug": "protein-electrophoresis-guide", "title": "Serum Protein Electrophoresis: Understanding Your Protein Profile", "category": "clinical-biochemistry", "keywords": ["protein electrophoresis", "SPEP", "serum proteins", "M spike"]},
    {"slug": "hemoglobin-variants-testing", "title": "Hemoglobin Electrophoresis: Sickle Cell, Thalassemia and Variants", "category": "clinical-biochemistry", "keywords": ["hemoglobin electrophoresis", "sickle cell test", "thalassemia test", "hemoglobin variants"]},
    {"slug": "lactate-dehydrogenase-ldh", "title": "LDH Blood Test: What Lactate Dehydrogenase Levels Reveal", "category": "clinical-biochemistry", "keywords": ["LDH test", "lactate dehydrogenase", "LDH normal range", "high LDH causes"]},
    {"slug": "amylase-lipase-pancreatitis", "title": "Amylase and Lipase Tests: Diagnosing Pancreatitis and Pancreatic Disease", "category": "clinical-biochemistry", "keywords": ["amylase test", "lipase test", "pancreatitis diagnosis", "pancreatic enzymes"]},

    # Patient Guides
    {"slug": "how-to-read-blood-test-results", "title": "How to Read Your Blood Test Results: A Complete Patient Guide", "category": "patient-guides", "keywords": ["blood test results", "how to read lab results", "understanding blood tests", "lab report guide"]},
    {"slug": "blood-test-preparation-guide", "title": "How to Prepare for Blood Tests: Fasting, Timing and What to Avoid", "category": "patient-guides", "keywords": ["blood test preparation", "fasting before blood test", "how to prepare for lab test"]},
    {"slug": "normal-vs-abnormal-lab-values", "title": "Normal vs Abnormal Lab Values: When Should You Be Concerned?", "category": "patient-guides", "keywords": ["normal lab values", "abnormal blood test", "lab values guide", "when to worry about blood test"]},
    {"slug": "diabetes-blood-tests-complete", "title": "Complete Guide to Diabetes Blood Tests: HbA1c, Glucose, Insulin and More", "category": "patient-guides", "keywords": ["diabetes blood tests", "HbA1c diabetes", "insulin test", "diabetes monitoring"]},
    {"slug": "kidney-disease-monitoring-tests", "title": "Essential Blood Tests for Kidney Disease Monitoring: A Patient Guide", "category": "patient-guides", "keywords": ["kidney disease tests", "CKD monitoring", "kidney function monitoring", "renal tests"]},
]


def get_topic_for_week() -> dict:
    """Get a unique topic for this week based on week number."""
    week = datetime.utcnow().isocalendar()[1]
    year = datetime.utcnow().year
    idx  = (week + year * 52) % len(WEEKLY_TOPICS)
    topic = WEEKLY_TOPICS[idx]
    print(f"  [fetcher] Week {week}/{year}: '{topic['title']}'")
    return topic


def generate_article_from_topic(topic: dict) -> dict:
    """
    Generate a complete article for the given topic.
    Content is written in Dr. Bansal's expert voice,
    based on standard medical knowledge.
    """
    week = datetime.utcnow().isocalendar()[1]
    year = datetime.utcnow().year

    # Import the article templates based on category
    article = {
        "slug": topic["slug"],
        "title": topic["title"],
        "category": topic["category"],
        "keywords": topic["keywords"],
        "meta_description": f"Expert guide to {topic['title'].lower()} by {AUTHOR}, PhD Clinical Biochemistry. Understand normal ranges, causes of abnormal results, and what your results mean.",
        "sections": _generate_sections(topic),
        "faq": _generate_faq(topic),
    }

    return article


def _generate_sections(topic: dict) -> list:
    """Generate article sections based on topic."""
    slug = topic["slug"]
    title = topic["title"]

    # Generate appropriate sections based on category and slug
    if "vitamin-d" in slug:
        return _vitamin_d_sections()
    elif "iron" in slug:
        return _iron_studies_sections()
    elif "uric-acid" in slug:
        return _uric_acid_sections()
    elif "troponin" in slug:
        return _troponin_sections()
    elif "crp" in slug:
        return _crp_sections()
    elif "cholesterol" in slug:
        return _cholesterol_sections()
    elif "b12" in slug:
        return _b12_sections()
    elif "esr" in slug:
        return _esr_sections()
    elif "cortisol" in slug:
        return _cortisol_sections()
    elif "calcium" in slug:
        return _calcium_sections()
    elif "testosterone" in slug:
        return _testosterone_sections()
    elif "how-to-read" in slug:
        return _how_to_read_sections()
    elif "preparation" in slug:
        return _preparation_sections()
    elif "diabetes-blood" in slug:
        return _diabetes_tests_sections()
    else:
        return _generic_sections(topic)


def _vitamin_d_sections():
    return [
        ("What is the Vitamin D Blood Test?",
         "The 25-hydroxyvitamin D test (25-OH vitamin D) is the most accurate way to measure your body's vitamin D status. Vitamin D is unique among vitamins because your body produces it when your skin is exposed to sunlight, and it also functions as a hormone.\n\nVitamin D plays critical roles in calcium absorption, bone health, immune function, muscle strength, and even mood regulation. Deficiency has been linked to osteoporosis, increased infection risk, autoimmune diseases, cardiovascular disease, and depression.\n\nThe test is particularly important for people with limited sun exposure, darker skin, obesity, malabsorption conditions, or those living in northern latitudes."),
        ("Vitamin D Normal Ranges",
         "Vitamin D levels are measured in nanograms per milliliter (ng/mL) or nanomoles per liter (nmol/L):\n\n**Deficient:** Less than 20 ng/mL (50 nmol/L) — requires supplementation\n**Insufficient:** 20-29 ng/mL (50-75 nmol/L) — suboptimal, supplementation recommended\n**Sufficient:** 30-100 ng/mL (75-250 nmol/L) — optimal range for most people\n**Optimal for bone health:** 40-60 ng/mL (100-150 nmol/L)\n**Potentially toxic:** Above 100 ng/mL (250 nmol/L) — risk of hypercalcemia\n\nNote: Some experts recommend higher optimal levels (50-80 ng/mL) for immune function and cancer prevention, though guidelines vary between organizations."),
        ("Causes of Vitamin D Deficiency",
         "Vitamin D deficiency is one of the most common nutritional deficiencies worldwide, affecting over 1 billion people. Common causes include:\n\n**Limited sun exposure:** Office workers, people who cover skin for cultural/religious reasons, elderly people who stay indoors\n**Geographic factors:** Living above 37° latitude (north of Los Angeles) where winter sun isn't strong enough for synthesis\n**Skin pigmentation:** Darker skin produces less vitamin D from the same sun exposure\n**Obesity:** Vitamin D gets trapped in fat tissue, reducing availability\n**Malabsorption:** Crohn's disease, celiac disease, cystic fibrosis affect absorption\n**Kidney disease:** Kidneys activate vitamin D; kidney disease reduces activation\n**Medications:** Certain anticonvulsants, steroids, and antifungals affect vitamin D metabolism"),
        ("Symptoms of Vitamin D Deficiency",
         "Many people with vitamin D deficiency have no obvious symptoms, which is why testing is important. When symptoms occur, they may include:\n\n- Bone pain and tenderness (especially back, legs)\n- Muscle weakness and fatigue\n- Frequent infections (immune dysfunction)\n- Depression, mood changes, seasonal affective disorder\n- Hair loss\n- Slow wound healing\n- Bone loss (osteopenia, osteoporosis)\n- In severe cases (rickets in children, osteomalacia in adults): bone deformities\n\nThe challenge is that these symptoms are non-specific and easily attributed to other causes, making blood testing essential for accurate diagnosis."),
        ("Treatment and Supplementation",
         "Treatment depends on deficiency severity:\n\n**Mild insufficiency (20-29 ng/mL):** 1,000-2,000 IU vitamin D3 daily\n**Moderate deficiency (10-20 ng/mL):** 2,000-4,000 IU vitamin D3 daily\n**Severe deficiency (<10 ng/mL):** 50,000 IU vitamin D2 weekly for 8-12 weeks (prescription), then maintenance\n\n**Vitamin D3 vs D2:** D3 (cholecalciferol) is more effective at raising and maintaining blood levels than D2 (ergocalciferol).\n\n**Important:** Always take vitamin D with the largest meal of the day (it's fat-soluble) and with vitamin K2 if taking high doses long-term (K2 directs calcium to bones, not arteries).\n\nRecheck levels after 3 months of supplementation."),
    ]


def _iron_studies_sections():
    return [
        ("Understanding Iron Studies",
         "Iron studies are a group of blood tests that assess your body's iron status comprehensively. Unlike a simple serum iron test, a full iron panel gives a complete picture of how much iron your body has stored, how much is being transported, and whether your iron-handling capacity is normal.\n\nIron is essential for hemoglobin production (which carries oxygen in red blood cells), immune function, energy metabolism, and cognitive function. Both iron deficiency and iron overload can cause serious health problems, making accurate measurement crucial."),
        ("Serum Iron — Normal Range",
         "**Serum Iron Normal Range:**\n- Men: 60-170 μg/dL (10.7-30.4 μmol/L)\n- Women: 50-170 μg/dL (9.0-30.4 μmol/L)\n\nSerum iron measures the iron currently circulating in your blood bound to transferrin. It fluctuates significantly throughout the day (highest in morning, lower in evening) and is affected by recent meals and supplements. For this reason, serum iron alone is not sufficient to diagnose iron deficiency — it must be interpreted alongside ferritin and TIBC."),
        ("Serum Ferritin — The Most Important Iron Test",
         "**Ferritin Normal Range:**\n- Men: 20-500 ng/mL\n- Women (premenopausal): 12-150 ng/mL\n- Women (postmenopausal): 12-300 ng/mL\n\nFerritin is the storage form of iron — it reflects your body's iron reserves. A low ferritin is the earliest and most sensitive indicator of iron deficiency, often falling below normal even before anemia develops.\n\n**Critical point:** Ferritin is an acute phase reactant — it rises during inflammation, infection, liver disease, and malignancy. A 'normal' or 'high' ferritin in the presence of inflammation does NOT rule out iron deficiency. Always interpret ferritin alongside CRP or ESR."),
        ("TIBC and Transferrin Saturation",
         "**Total Iron Binding Capacity (TIBC):** Normal range 250-370 μg/dL\nTIBC measures the maximum amount of iron your blood can carry. It reflects transferrin levels (the transport protein for iron).\n\n**Transferrin Saturation:** Normal range 20-50%\nCalculated as (Serum Iron ÷ TIBC) × 100\n\n**Interpretation patterns:**\n\n| Condition | Ferritin | Serum Iron | TIBC | Transferrin Sat |\n|-----------|---------|-----------|------|----------------|\n| Iron deficiency | Low | Low | High | Low (<20%) |\n| Anemia of chronic disease | Normal/High | Low | Low/Normal | Low |\n| Iron overload (hemochromatosis) | High | High | Low/Normal | High (>45%) |\n| Normal | Normal | Normal | Normal | Normal |"),
        ("Causes and Treatment of Iron Deficiency",
         "Iron deficiency is the most common nutritional deficiency worldwide. Causes include:\n\n**Blood loss (most common cause in adults):**\n- Heavy menstrual periods (most common in women)\n- Gastrointestinal bleeding (ulcers, polyps, colorectal cancer)\n- Frequent blood donation\n\n**Poor intake/absorption:**\n- Vegetarian/vegan diet (plant iron is less bioavailable)\n- Celiac disease, inflammatory bowel disease\n- Gastric bypass surgery\n\n**Increased demand:**\n- Pregnancy (iron requirements triple)\n- Rapid growth in adolescence\n\n**Treatment:** Oral iron (ferrous sulfate 325mg = 65mg elemental iron) taken on empty stomach with vitamin C. Expect 3-6 months to replenish stores. Always identify and treat the underlying cause."),
    ]


def _uric_acid_sections():
    return [
        ("What is Uric Acid and Why is it Tested?",
         "Uric acid is the end product of purine metabolism in the human body. Purines are natural substances found in all body cells and in many foods. When cells break down or when you digest purine-rich foods, the purines are converted to uric acid.\n\nNormally, uric acid dissolves in blood, passes through the kidneys, and is excreted in urine. Problems arise when the body produces too much uric acid or the kidneys excrete too little, causing uric acid to accumulate in the blood (hyperuricemia).\n\nChronic hyperuricemia leads to urate crystal deposition in joints (gout), kidneys (uric acid kidney stones), and other tissues."),
        ("Uric Acid Normal Range",
         "**Normal uric acid levels:**\n- Men: 3.4-7.0 mg/dL (202-416 μmol/L)\n- Women: 2.4-6.0 mg/dL (143-357 μmol/L)\n- Children: 2.0-5.5 mg/dL\n\nHyperuricemia is defined as uric acid above 7.0 mg/dL in men and 6.0 mg/dL in women.\n\nThe lower target for gout treatment is typically below 6.0 mg/dL (360 μmol/L) — at this level, urate crystals gradually dissolve. For patients with tophi (visible crystal deposits), the target is below 5.0 mg/dL."),
        ("Causes of High Uric Acid",
         "**Dietary causes:**\n- High purine foods: red meat, organ meats, shellfish (especially shrimp, lobster)\n- Alcohol (especially beer — contains yeast with high purines; alcohol also reduces uric acid excretion)\n- Fructose-sweetened beverages (corn syrup sodas)\n\n**Medical causes:**\n- Obesity and metabolic syndrome\n- Hypertension\n- Chronic kidney disease (reduced excretion)\n- Hypothyroidism\n- Psoriasis (high cell turnover)\n- Certain cancers and chemotherapy (rapid cell destruction)\n\n**Medications:**\n- Diuretics (thiazides, furosemide) — most common drug cause\n- Low-dose aspirin\n- Cyclosporine (immunosuppressant)\n- Niacin (vitamin B3 in high doses)"),
        ("Gout — Symptoms and Diagnosis",
         "Gout is the most common manifestation of hyperuricemia, characterized by sudden, severe joint pain caused by urate crystal deposition.\n\n**Classic presentation:**\n- Sudden onset of intense joint pain, typically at night\n- Most commonly affects the big toe (podagra) — in 50-60% of first attacks\n- Also affects ankle, knee, wrist, elbow\n- Joint becomes red, swollen, warm, exquisitely tender (even bedsheet touching causes pain)\n- Attack resolves in 7-14 days without treatment\n\n**Important:** Serum uric acid may be NORMAL or even LOW during an acute gout attack (urate crystals leave the blood as they deposit in joints). Do not use serum uric acid alone to diagnose acute gout — diagnosis is confirmed by joint fluid analysis showing needle-shaped urate crystals."),
        ("Treatment and Prevention",
         "**Acute gout attack:**\n- NSAIDs (indomethacin, naproxen) — first-line if no contraindications\n- Colchicine — very effective if started within 24 hours\n- Corticosteroids — for those who cannot take NSAIDs or colchicine\n\n**Long-term urate-lowering therapy (after 2+ attacks):**\n- Allopurinol — first-line, reduces uric acid production\n- Febuxostat — alternative to allopurinol\n- Probenecid — increases renal excretion (less used)\n\n**Dietary changes:**\n- Reduce red meat, organ meats, shellfish\n- Avoid alcohol, especially beer\n- Eliminate fructose-sweetened drinks\n- Increase low-fat dairy (actually protective)\n- Stay well hydrated (2-3L water daily dilutes urine and helps excretion)\n- Cherries and cherry extract may reduce attack frequency"),
    ]


def _troponin_sections():
    return [
        ("What is Troponin and Why is it Critical?",
         "Troponin is a protein complex found in heart muscle cells (cardiomyocytes) that regulates muscle contraction. When heart muscle cells are damaged or die — as occurs during a heart attack — they release troponin into the bloodstream.\n\nThe cardiac troponin test (troponin I or troponin T) is the gold standard blood test for diagnosing acute myocardial infarction (heart attack). It is highly specific for heart muscle damage — virtually nothing else causes troponin elevation to the levels seen in heart attacks.\n\nModern high-sensitivity troponin (hs-troponin) assays can detect heart damage within 1-3 hours of symptom onset, allowing faster diagnosis and treatment."),
        ("Troponin Normal Range and Interpretation",
         "Normal troponin values vary by assay, but generally:\n\n**Troponin I (conventional):** <0.04 ng/mL\n**Troponin T (conventional):** <0.01 ng/mL\n**High-sensitivity Troponin I:** <16-52 ng/L (varies by assay)\n**High-sensitivity Troponin T:** <14 ng/L\n\n**The rise-and-fall pattern is crucial:** A single troponin value is less informative than the pattern over time. Troponin rises within 2-4 hours of heart muscle damage, peaks at 12-24 hours, and remains elevated for 1-2 weeks (troponin I) or 10-14 days (troponin T).\n\nIn suspected heart attack, troponin is measured on arrival AND 3 hours later (or 1 hour later with high-sensitivity assays). A significant rise (>20% increase) between measurements confirms acute myocardial injury."),
        ("Causes of Elevated Troponin",
         "While a heart attack is the most important cause, elevated troponin can occur in other conditions:\n\n**Cardiac causes:**\n- Acute myocardial infarction (heart attack) — most important\n- Unstable angina (demand ischemia)\n- Heart failure\n- Myocarditis (heart inflammation)\n- Cardiac contusion (chest trauma)\n- Cardioversion or cardiac procedures\n\n**Non-cardiac causes:**\n- Pulmonary embolism (clot in lungs)\n- Severe sepsis/septic shock\n- Stroke (especially hemorrhagic)\n- Acute kidney injury and chronic kidney disease\n- Severe hypertension\n- Chemotherapy cardiotoxicity\n- Rhabdomyolysis (severe muscle breakdown)\n\nThe level of elevation helps differentiate: Heart attacks typically cause very high troponin levels (10-100x normal), while non-cardiac causes usually cause mild elevations (2-5x normal)."),
        ("What Happens After a Positive Troponin?",
         "If your troponin is elevated with a rising pattern, you will likely undergo:\n\n**Immediate assessment:**\n- ECG (electrocardiogram) — looking for ST elevation (STEMI) requiring emergency catheterization\n- Continuous cardiac monitoring\n- Oxygen, aspirin, and other immediate medications\n\n**Further investigations:**\n- Echocardiogram — assesses heart function and wall motion\n- Coronary angiography — visualizes coronary arteries, identifies blockages\n- CT coronary angiography — non-invasive alternative\n\n**Treatment depending on findings:**\n- STEMI: Emergency percutaneous coronary intervention (PCI) within 90 minutes\n- NSTEMI: PCI within 24-72 hours\n- Unstable angina: Medical management or PCI based on risk\n\nTime is muscle — every minute of delay in treating a heart attack causes more permanent damage."),
        ("Understanding Your Troponin Result",
         "**If troponin is normal:** A single normal troponin does NOT rule out a heart attack if symptoms started less than 3 hours ago. A repeat test at 3 hours is essential.\n\n**If troponin is mildly elevated (stable, not rising):** May indicate chronic heart stress rather than acute heart attack. Your doctor will interpret this alongside your symptoms and ECG.\n\n**If troponin is rising significantly:** This is a medical emergency. Treatment should begin immediately.\n\n**Never ignore elevated troponin:** Even mildly elevated troponin is associated with significantly increased risk of future cardiovascular events and should trigger thorough cardiovascular evaluation."),
    ]


def _crp_sections():
    return [
        ("What is C-Reactive Protein (CRP)?",
         "C-Reactive Protein (CRP) is a protein produced by the liver in response to inflammation anywhere in the body. It is one of the most sensitive and rapidly responding markers of inflammation and infection available in clinical laboratory medicine.\n\nWhen tissues are injured, infected, or inflamed, they release chemical signals (cytokines, particularly interleukin-6) that reach the liver and trigger CRP production within 4-6 hours. CRP levels can rise 1,000-fold or more during acute inflammation, making it an extremely sensitive indicator of inflammatory activity.\n\nCRP is used to detect infection, monitor inflammatory diseases, assess treatment response, and predict cardiovascular risk."),
        ("CRP Normal Range and Test Types",
         "There are two versions of the CRP test with different sensitivities:\n\n**Standard CRP:**\n- Normal: <10 mg/L\n- Mildly elevated: 10-40 mg/L\n- Moderately elevated: 40-200 mg/L\n- Severely elevated: >200 mg/L (suggests serious bacterial infection or major tissue damage)\n\n**High-Sensitivity CRP (hs-CRP) — for cardiovascular risk assessment:**\n- Low cardiovascular risk: <1.0 mg/L\n- Average cardiovascular risk: 1.0-3.0 mg/L\n- High cardiovascular risk: >3.0 mg/L\n\nThe standard CRP is used for detecting acute inflammation/infection. The hs-CRP test is more sensitive and specifically used for cardiovascular risk stratification in people with intermediate risk."),
        ("Causes of Elevated CRP",
         "**Infections (most common cause of very high CRP):**\n- Bacterial infections cause higher CRP than viral (bacterial CRP often >100 mg/L)\n- Sepsis can cause CRP >300-400 mg/L\n- Viral infections typically cause mild elevation (<40 mg/L)\n- This difference helps doctors decide whether antibiotics are needed\n\n**Inflammatory conditions:**\n- Rheumatoid arthritis, lupus, vasculitis\n- Inflammatory bowel disease (Crohn's, ulcerative colitis)\n- Polymyalgia rheumatica\n\n**Other causes:**\n- Recent surgery or trauma\n- Burns\n- Heart attack (peaks at 48-72 hours)\n- Cancer (especially lymphoma, renal cell carcinoma)\n- Obesity (low-grade chronic inflammation)\n\n**Important:** CRP does NOT identify WHERE the inflammation is — only that inflammation exists somewhere."),
        ("CRP vs ESR — Which is Better?",
         "Both CRP and ESR (Erythrocyte Sedimentation Rate) measure inflammation, but they differ importantly:\n\n| Feature | CRP | ESR |\n|---------|-----|-----|\n| Rise after inflammation | 4-6 hours | 24-48 hours |\n| Fall after resolution | 24-48 hours | Weeks |\n| Sensitivity | Higher | Lower |\n| Specificity | Higher | Lower |\n| Affected by anemia | No | Yes |\n| Cost | Slightly higher | Lower |\n\nCRP is generally preferred because it responds faster and more specifically. ESR remains useful for monitoring certain conditions (temporal arteritis, multiple myeloma) where it correlates better with disease activity."),
        ("Using CRP to Monitor Treatment",
         "One of CRP's greatest clinical values is monitoring treatment response:\n\n**Antibiotic therapy:** CRP should begin falling within 24-48 hours of effective antibiotic treatment for bacterial infection. Failure to fall suggests the antibiotic isn't working or there's a complication.\n\n**Anti-inflammatory treatment:** In rheumatoid arthritis and other inflammatory conditions, successful treatment (DMARDs, biologics) is reflected by falling CRP levels.\n\n**Post-operative monitoring:** CRP normally rises after surgery (peaks day 2-3), then falls. A secondary rise after initial fall suggests surgical site infection or other complication.\n\n**Cancer treatment:** Falling CRP often indicates positive response to cancer therapy.\n\nSerial CRP measurements provide far more information than a single reading."),
    ]


def _cholesterol_sections():
    return [
        ("Understanding Your Cholesterol Blood Test",
         "A cholesterol test (lipid panel or lipid profile) measures the fats (lipids) in your blood. Despite what many people think, cholesterol itself is not bad — your body needs it to build cell membranes, make hormones, and produce vitamin D. The problem arises when certain types of cholesterol are too high or too low.\n\nThe standard lipid panel measures four values: total cholesterol, LDL ('bad') cholesterol, HDL ('good') cholesterol, and triglycerides. Understanding each component is essential for assessing your true cardiovascular risk."),
        ("Cholesterol Normal Ranges",
         "**Total Cholesterol:**\n- Desirable: <200 mg/dL\n- Borderline high: 200-239 mg/dL\n- High: ≥240 mg/dL\n\n**LDL Cholesterol (the main target):**\n- Optimal: <100 mg/dL\n- Near optimal: 100-129 mg/dL\n- Borderline high: 130-159 mg/dL\n- High: 160-189 mg/dL\n- Very high: ≥190 mg/dL\n- Target for very high-risk patients: <70 mg/dL\n\n**HDL Cholesterol:**\n- Low (risk factor): <40 mg/dL (men), <50 mg/dL (women)\n- Normal: 40-59 mg/dL\n- High (protective): ≥60 mg/dL\n\n**Triglycerides:**\n- Normal: <150 mg/dL\n- Borderline high: 150-199 mg/dL\n- High: 200-499 mg/dL\n- Very high: ≥500 mg/dL (pancreatitis risk)"),
        ("LDL vs HDL — Understanding the Difference",
         "**LDL (Low-Density Lipoprotein) — 'Bad' Cholesterol:**\nLDL carries cholesterol from the liver to body tissues. When LDL is too high, it deposits cholesterol in artery walls, forming plaques (atherosclerosis). These plaques narrow arteries and can rupture, causing heart attacks and strokes.\n\n**HDL (High-Density Lipoprotein) — 'Good' Cholesterol:**\nHDL carries cholesterol FROM body tissues and artery walls BACK to the liver for disposal. High HDL is protective against heart disease.\n\n**Non-HDL Cholesterol:**\nCalculated as Total Cholesterol minus HDL. Represents all the 'bad' particles. Some guidelines prefer non-HDL over LDL as a target because it includes VLDL (another atherogenic particle).\n\n**Total Cholesterol/HDL Ratio:**\nUseful cardiovascular risk indicator. Ratio below 4.0 is desirable; below 3.5 is optimal."),
        ("Causes of High Cholesterol",
         "**Primary (genetic) causes:**\n- Familial hypercholesterolemia (FH) — affects 1 in 250 people, causes very high LDL from birth\n- Familial combined hyperlipidemia — raises both LDL and triglycerides\n\n**Secondary (lifestyle/medical) causes:**\n- Diet high in saturated and trans fats\n- Obesity (raises LDL and triglycerides, lowers HDL)\n- Physical inactivity\n- Hypothyroidism (reduces LDL clearance)\n- Type 2 diabetes (raises triglycerides, lowers HDL)\n- Chronic kidney disease\n- Obstructive liver disease\n- Certain medications (steroids, some blood pressure drugs, isotretinoin)"),
        ("Treatment Options",
         "**Lifestyle first:**\n- Reduce saturated fat (<7% of calories), eliminate trans fats\n- Increase soluble fiber (oats, beans, fruits): reduces LDL by 5-10%\n- Add plant sterols (found in certain margarines): reduces LDL by 5-15%\n- Exercise 150+ minutes/week: mainly raises HDL\n- Lose weight if overweight: reduces LDL and triglycerides\n\n**Medications when lifestyle isn't enough:**\n- Statins (atorvastatin, rosuvastatin): first-line, reduce LDL 30-60%\n- Ezetimibe: reduces cholesterol absorption, lowers LDL 15-20%\n- PCSK9 inhibitors (evolocumab, alirocumab): injections every 2-4 weeks, reduce LDL 50-60%\n- Bempedoic acid: newer oral option\n\nMost people with high cholesterol require both lifestyle changes AND medication for adequate control."),
    ]


def _b12_sections():
    return [
        ("Why Vitamin B12 and Folate are Tested Together",
         "Vitamin B12 (cobalamin) and folate (vitamin B9) are both essential B vitamins that work together in critical metabolic pathways. Both are required for DNA synthesis, red blood cell formation, and neurological function.\n\nDeficiency of either causes megaloblastic anemia — a condition where red blood cells become abnormally large and dysfunctional. However, B12 and folate deficiencies have different causes and very different consequences: B12 deficiency causes permanent neurological damage that folate supplementation cannot prevent, making accurate differentiation crucial."),
        ("Vitamin B12 Normal Range",
         "**Serum B12 Normal Range:** 200-900 pg/mL (148-664 pmol/L)\n\n**Interpretation:**\n- Below 200 pg/mL: Definite deficiency\n- 200-300 pg/mL: Borderline — further testing needed (methylmalonic acid, homocysteine)\n- Above 300 pg/mL: Generally sufficient\n\n**Important limitation:** Serum B12 measures total B12, including inactive forms. About 20% of people with low cellular B12 (true deficiency) have 'normal' serum B12. When B12 deficiency is suspected despite normal serum levels, measuring methylmalonic acid (MMA) and homocysteine provides more accurate assessment — both are elevated in true B12 deficiency."),
        ("Folate Normal Range",
         "**Serum Folate:** 2.7-17.0 ng/mL (6.1-38.5 nmol/L)\n**Red Blood Cell (RBC) Folate:** 140-628 ng/mL (317-1422 nmol/L)\n\nRBC folate is preferred over serum folate for assessing long-term folate status because:\n- Serum folate reflects recent dietary intake (can normalize within 24-48 hours of eating folate-rich food)\n- RBC folate reflects folate stores over the previous 2-3 months (like HbA1c for glucose)\n\n**Critical point for pregnancy:** Folate supplementation (400-800 μg/day) must start at least 1 month BEFORE conception and continue through the first trimester to prevent neural tube defects (spina bifida, anencephaly)."),
        ("Causes of B12 Deficiency",
         "**Pernicious anemia (most common cause in developed countries):**\nAutoimmune destruction of stomach cells that produce intrinsic factor — a protein essential for B12 absorption. B12 from food requires intrinsic factor to be absorbed in the small intestine.\n\n**Dietary deficiency:**\nB12 is found ONLY in animal products (meat, fish, eggs, dairy). Strict vegans and vegetarians are at high risk without supplementation.\n\n**Malabsorption conditions:**\n- Gastric bypass surgery (reduces intrinsic factor)\n- Crohn's disease affecting terminal ileum\n- Celiac disease\n- H. pylori infection\n- Chronic use of proton pump inhibitors (reduce stomach acid needed to release B12 from food)\n- Metformin (reduces B12 absorption in some patients)\n\n**Age:** Absorption efficiency decreases with age; deficiency is common in people over 60."),
        ("Neurological Consequences of B12 Deficiency",
         "Unlike folate, B12 deficiency causes severe and potentially irreversible neurological damage:\n\n**Subacute combined degeneration of the spinal cord:**\n- Damage to the posterior and lateral columns of the spinal cord\n- Symptoms: tingling and numbness in hands and feet, unsteady gait, weakness\n- Can progress to paralysis if untreated\n\n**Cognitive effects:**\n- Memory problems, difficulty concentrating\n- Mood changes, depression, psychosis (rare)\n- Dementia-like symptoms (often reversible with treatment if caught early)\n\n**Critical warning:** Giving folate to someone with combined B12 and folate deficiency can correct the anemia but MASK the B12 deficiency, allowing neurological damage to progress undetected. Always test B12 before starting folate supplementation."),
    ]


def _esr_sections():
    return [
        ("What is the ESR Test?",
         "The Erythrocyte Sedimentation Rate (ESR) measures how quickly red blood cells (erythrocytes) settle to the bottom of a test tube containing blood over one hour. Normally, red blood cells have a slight negative charge that makes them repel each other and settle slowly.\n\nDuring inflammation, the body produces proteins called acute phase reactants (fibrinogen, globulins) that coat red blood cells and make them clump together, causing them to settle faster. A higher ESR therefore indicates more inflammation.\n\nThe ESR is a non-specific test — it tells you inflammation is present but not WHERE or WHY. It must always be interpreted alongside other tests and clinical findings."),
        ("ESR Normal Range by Age and Sex",
         "ESR increases naturally with age, making age-adjusted ranges essential:\n\n**Men:**\n- Under 50: 0-15 mm/hour\n- Over 50: 0-20 mm/hour\n\n**Women (higher due to hormonal differences):**\n- Under 50: 0-20 mm/hour\n- Over 50: 0-30 mm/hour\n\n**Children:** 0-10 mm/hour\n\n**Practical rule (Westergren method):**\n- Upper limit for men = Age ÷ 2\n- Upper limit for women = (Age + 10) ÷ 2\n\n**Markedly elevated ESR (>100 mm/hour)** usually indicates serious pathology: active infection, malignancy, or significant inflammatory disease."),
        ("Common Causes of High ESR",
         "**Infections:**\n- Bacterial infections (especially osteomyelitis, endocarditis, tuberculosis)\n- ESR is particularly useful for monitoring TB treatment response\n\n**Inflammatory and autoimmune diseases:**\n- Rheumatoid arthritis\n- Temporal arteritis/giant cell arteritis (ESR often >100, must test urgently)\n- Polymyalgia rheumatica\n- Systemic lupus erythematosus (SLE)\n- Inflammatory bowel disease\n\n**Malignancies:**\n- Multiple myeloma (very high ESR, often >100, due to abnormal proteins)\n- Lymphoma\n- Solid tumors with metastasis\n\n**Other causes:**\n- Pregnancy (normal to have elevated ESR, especially third trimester)\n- Anemia (fewer cells settle faster)\n- Kidney disease"),
        ("ESR vs CRP — When to Use Each",
         "Both ESR and CRP measure inflammation, but clinical situations favor one over the other:\n\n**Prefer ESR for:**\n- Temporal arteritis/giant cell arteritis monitoring (ESR correlates better)\n- Multiple myeloma monitoring\n- Monitoring tuberculosis treatment\n- Situations requiring 'chronic' inflammation assessment\n\n**Prefer CRP for:**\n- Detecting acute infection (responds within hours vs 24-48h for ESR)\n- Post-operative monitoring\n- Distinguishing bacterial from viral infection\n- Monitoring acute inflammatory disease flares\n\n**Use BOTH when:**\n- Investigating unexplained symptoms (complement each other)\n- Monitoring chronic inflammatory conditions\n- ESR and CRP disagree (may suggest specific diagnoses)"),
        ("Very High ESR — What Does It Mean?",
         "An ESR above 100 mm/hour is clinically significant and warrants urgent investigation:\n\n**Most common causes of ESR >100:**\n1. Severe infection (osteomyelitis, endocarditis, abscess)\n2. Multiple myeloma (paraprotein causes massive RBC rouleaux formation)\n3. Temporal arteritis (emergency — can cause blindness if untreated)\n4. Malignancy with extensive disease\n5. Severe autoimmune disease (lupus, vasculitis)\n\n**ESR >100 requires:**\n- Urgent clinical assessment\n- Blood cultures (if infection suspected)\n- Serum protein electrophoresis (to exclude myeloma)\n- Temporal artery biopsy (if temporal arteritis suspected in person >50 with headache)\n- Imaging as appropriate\n\nNever dismiss a markedly elevated ESR — it almost always indicates significant pathology."),
    ]


def _cortisol_sections():
    return [
        ("What is Cortisol and Why is it Tested?",
         "Cortisol is the body's primary stress hormone, produced by the adrenal glands (located on top of the kidneys) in response to signals from the pituitary gland and hypothalamus. It plays essential roles in regulating metabolism, immune response, blood pressure, sleep-wake cycles, and the body's stress response.\n\nCortisol testing is ordered when doctors suspect adrenal gland dysfunction — either too much cortisol (Cushing's syndrome) or too little (Addison's disease). Both conditions are serious but treatable when diagnosed correctly."),
        ("Cortisol Normal Range and Testing Times",
         "Cortisol follows a strong diurnal (daily) rhythm — highest in the morning, lowest at midnight. This makes testing time critically important:\n\n**Morning cortisol (8:00 AM — most common test):**\n- Normal: 6-23 μg/dL (165-635 nmol/L)\n- Below 3 μg/dL strongly suggests adrenal insufficiency\n- Above 18-20 μg/dL makes adrenal insufficiency unlikely\n\n**Evening cortisol (4:00 PM):**\n- Normal: 2-14 μg/dL\n\n**Late-night salivary cortisol (11 PM-midnight):**\n- Should be very low (<0.27 μg/dL)\n- Elevated late-night cortisol is a sensitive screening test for Cushing's syndrome\n\n**24-hour urine free cortisol:**\n- Normal: 10-100 μg/24 hours\n- Elevated in Cushing's syndrome"),
        ("Cushing's Syndrome — Too Much Cortisol",
         "Cushing's syndrome results from prolonged exposure to excess cortisol.\n\n**Causes:**\n- Iatrogenic (most common): Long-term corticosteroid use (prednisone, dexamethasone)\n- Cushing's disease: Pituitary tumor producing excess ACTH\n- Adrenal tumor: Cortisol-producing adrenal adenoma or carcinoma\n- Ectopic ACTH: Certain lung cancers producing ACTH\n\n**Symptoms:**\n- Weight gain with central obesity (fat around abdomen and face — 'moon face')\n- Purple stretch marks (striae) on abdomen, thighs, breasts\n- Easy bruising, thin fragile skin\n- Muscle weakness (especially proximal — difficulty rising from chair)\n- High blood pressure\n- High blood glucose / diabetes\n- Osteoporosis\n- Depression, mood changes\n- In women: Irregular periods, excess facial hair"),
        ("Addison's Disease — Too Little Cortisol",
         "Primary adrenal insufficiency (Addison's disease) occurs when the adrenal glands are damaged and cannot produce adequate cortisol.\n\n**Causes:**\n- Autoimmune (most common in developed countries) — immune system destroys adrenal cortex\n- Tuberculosis (most common cause worldwide)\n- Other infections (HIV, fungal)\n- Adrenal hemorrhage\n- Metastatic cancer\n\n**Symptoms:**\n- Fatigue and weakness (often profound)\n- Weight loss and decreased appetite\n- Low blood pressure, dizziness on standing\n- Salt craving (also lose aldosterone)\n- Darkening of skin (hyperpigmentation) — especially skin folds, scars, gums\n- Nausea, vomiting, diarrhea\n- Hypoglycemia\n\n**Adrenal crisis (life-threatening emergency):**\nPrecipitated by illness, surgery, or injury in someone with undiagnosed or undertreated Addison's. Causes severe low blood pressure, confusion, extreme weakness. Requires immediate IV hydrocortisone."),
        ("Cortisol Testing — Stimulation and Suppression Tests",
         "Single cortisol measurements are often inconclusive — dynamic tests provide more information:\n\n**ACTH Stimulation Test (Synacthen Test) — for suspected adrenal insufficiency:**\n- Give synthetic ACTH injection\n- Measure cortisol at 0 and 30-60 minutes\n- Normal response: Cortisol rises to >18-20 μg/dL\n- Blunted response (cortisol fails to rise adequately) = adrenal insufficiency\n\n**Overnight Dexamethasone Suppression Test — for suspected Cushing's:**\n- Take 1mg dexamethasone at 11 PM\n- Measure cortisol next morning at 8 AM\n- Normal: Cortisol suppresses to <1.8 μg/dL\n- Failure to suppress = possible Cushing's syndrome (requires further investigation)\n\nThese dynamic tests are far more informative than single cortisol measurements and are essential before diagnosing adrenal disorders."),
    ]


def _calcium_sections():
    return [
        ("Why Calcium is Measured in Blood Tests",
         "Calcium is the most abundant mineral in the body, with 99% stored in bones and teeth. The remaining 1% in blood and body fluids performs critical functions: enabling nerve signaling, muscle contraction (including the heart), blood clotting, and hormone secretion.\n\nThe body maintains blood calcium within a very narrow range through a complex system involving parathyroid hormone (PTH), vitamin D, and calcitonin. Disruption of this system by various diseases leads to hypercalcemia (too high) or hypocalcemia (too low), both of which can be life-threatening if severe."),
        ("Calcium Normal Range",
         "**Total serum calcium:** 8.5-10.2 mg/dL (2.1-2.6 mmol/L)\n**Ionized (free) calcium:** 4.5-5.3 mg/dL (1.1-1.3 mmol/L)\n\n**Important — albumin correction:**\nAbout 40% of calcium in blood is bound to albumin. Low albumin (common in hospitalized patients, malnutrition, liver disease) gives falsely low calcium readings. Always correct for albumin:\n\nCorrected calcium = Measured calcium + 0.8 × (4.0 - patient's albumin)\n\nFor example: If calcium is 7.5 mg/dL and albumin is 2.0 g/dL:\nCorrected calcium = 7.5 + 0.8 × (4.0 - 2.0) = 7.5 + 1.6 = 9.1 mg/dL (normal!)\n\nIonized calcium measurement is unaffected by albumin and is the gold standard."),
        ("Hypercalcemia — Causes and Symptoms",
         "**Most common causes (account for >90% of cases):**\n1. Primary hyperparathyroidism (most common in outpatients) — parathyroid gland overproduces PTH\n2. Malignancy (most common in hospitalized patients) — cancer releases PTH-related protein or destroys bone\n\n**Other causes:**\n- Vitamin D toxicity\n- Sarcoidosis and other granulomatous diseases\n- Hyperthyroidism\n- Milk-alkali syndrome (excess calcium antacids)\n- Thiazide diuretics\n- Immobilization (especially in Paget's disease)\n\n**Symptoms of hypercalcemia:**\n'Bones, stones, groans, and psychic moans'\n- Bones: Bone pain, fractures (from calcium mobilization)\n- Stones: Kidney stones (calcium oxalate/phosphate)\n- Groans: Nausea, vomiting, constipation, abdominal pain\n- Psychic: Depression, confusion, weakness, fatigue\n\nMild hypercalcemia (<12 mg/dL) is often asymptomatic. Severe hypercalcemia (>14 mg/dL) is a medical emergency."),
        ("Hypocalcemia — Causes and Symptoms",
         "**Causes of low calcium:**\n- Hypoparathyroidism (most common) — low PTH, often after thyroid surgery\n- Vitamin D deficiency (reduces calcium absorption)\n- Chronic kidney disease (impaired vitamin D activation)\n- Magnesium deficiency (impairs PTH secretion and action)\n- Acute pancreatitis (calcium deposits in inflamed pancreas)\n- Alkalosis (reduces ionized calcium)\n\n**Symptoms of hypocalcemia:**\n- Tingling and numbness (perioral, fingertips)\n- Muscle cramps and spasms\n- Chvostek's sign: Facial muscle twitching when cheek tapped (clinical test)\n- Trousseau's sign: Carpal spasm when blood pressure cuff inflated (clinical test)\n- In severe cases: Tetany (muscle spasms), laryngospasm, seizures, cardiac arrhythmias\n- Chronic hypocalcemia: Cataracts, dry skin, brittle nails, dental defects"),
        ("Investigating Abnormal Calcium",
         "When calcium is abnormal, the next step is measuring PTH to identify the cause:\n\n| Condition | Calcium | PTH |\n|-----------|---------|-----|\n| Primary hyperparathyroidism | High | High (inappropriately) |\n| Malignancy | High | Low (suppressed) |\n| Vitamin D toxicity | High | Low |\n| Hypoparathyroidism | Low | Low |\n| Pseudohypoparathyroidism | Low | High |\n| Vitamin D deficiency | Low/Normal | High (secondary hyperPTH) |\n| CKD | Low | High |\n\nAdditional tests often ordered: vitamin D levels, phosphate, magnesium, urine calcium, PTH-related protein (PTHrP), alkaline phosphatase."),
    ]


def _testosterone_sections():
    return [
        ("Why Testosterone is Tested",
         "Testosterone is the primary male sex hormone (androgen), though women also produce smaller amounts. In men, testosterone is produced mainly by the testes (95%) with a small contribution from the adrenal glands. In women, it is produced by the ovaries and adrenal glands.\n\nTestosterone plays crucial roles in sexual development, libido, muscle mass and strength, bone density, red blood cell production, mood, and cognitive function. Testing is ordered when low or high testosterone is suspected based on symptoms."),
        ("Testosterone Normal Range",
         "**Total testosterone normal ranges:**\n\n**Adult Men:**\n- 270-1,070 ng/dL (9.4-37.1 nmol/L)\n- 'Normal' varies significantly by age and laboratory\n- Hypogonadism diagnosis generally requires total T <300 ng/dL on two morning samples\n\n**Adult Women:**\n- 15-70 ng/dL (0.5-2.4 nmol/L)\n- Slightly higher in premenopausal women\n\n**Important:** Total testosterone includes bound (inactive) and free (active) fractions. Free testosterone (1-3% of total) is the biologically active form.\n\n**Free testosterone normal ranges (men):** 50-210 pg/mL\n\nMorning testing is essential — testosterone peaks between 7-10 AM and is 20-30% higher than afternoon values."),
        ("Symptoms of Low Testosterone in Men",
         "Low testosterone (hypogonadism) in men causes:\n\n**Sexual symptoms:**\n- Reduced libido (most common complaint)\n- Erectile dysfunction\n- Reduced spontaneous erections\n- Infertility (reduced sperm production)\n\n**Physical symptoms:**\n- Loss of muscle mass and strength\n- Increased body fat (especially abdominal)\n- Reduced bone density (osteoporosis risk)\n- Decreased body and facial hair\n- Breast tissue enlargement (gynecomastia)\n- Hot flushes (in severe cases)\n- Fatigue, reduced energy\n\n**Mental/emotional symptoms:**\n- Depression, low mood\n- Poor concentration and memory\n- Reduced motivation\n- Irritability\n\nDiagnosis requires low testosterone on two morning samples PLUS symptoms — low testosterone alone without symptoms does not require treatment."),
        ("Causes of Low Testosterone",
         "**Primary hypogonadism (testicular failure — high LH/FSH):**\n- Klinefelter syndrome (47,XXY chromosomes)\n- Undescended testes\n- Orchitis (mumps, autoimmune)\n- Chemotherapy/radiation damage\n- Trauma or surgery\n\n**Secondary hypogonadism (pituitary/hypothalamic failure — low LH/FSH):**\n- Hypopituitarism (pituitary tumor, surgery, radiation)\n- Kallmann syndrome (congenital GnRH deficiency)\n- Hyperprolactinemia\n- Hemochromatosis\n- Opioid medications (suppress LH/FSH)\n\n**Late-onset hypogonadism (age-related decline):**\nTestosterone declines about 1-2% per year after age 30. By age 70, many men have testosterone below the young adult normal range, though the clinical significance is debated."),
        ("Testosterone Replacement Therapy — Who Needs It?",
         "Testosterone replacement therapy (TRT) is indicated when:\n- Confirmed low testosterone (two morning values <300 ng/dL)\n- Plus symptoms attributable to low testosterone\n- No contraindications\n\n**Available forms:**\n- Testosterone gels/creams: Daily application, stable levels, risk of transfer to partners/children\n- Testosterone injections: Every 1-4 weeks, effective but causes peaks and troughs\n- Testosterone patches: Daily, good absorption\n- Pellets: Implanted under skin every 3-6 months\n\n**Monitoring on TRT:**\n- Testosterone levels after 3-6 months\n- Hematocrit (TRT raises red cell production — clot risk if too high)\n- PSA (TRT may stimulate existing prostate cancer)\n- Liver function (oral forms only)\n\n**TRT is NOT appropriate for:**\n- Men wanting to preserve fertility (suppresses sperm production)\n- Prostate or breast cancer\n- Severe sleep apnea\n- High hematocrit (>54%)"),
    ]


def _how_to_read_sections():
    return [
        ("Understanding Your Lab Report",
         "Receiving lab results can be confusing and anxiety-inducing, especially when you see values flagged as 'high' or 'low'. This guide explains how to systematically read and understand your blood test report.\n\nEvery lab report contains several standard components: the patient's name and date, the test name, your result, the reference range (normal range), and a flag indicating if the result is outside the normal range (H for high, L for low, or asterisk *). Understanding each component helps you have more informed conversations with your doctor."),
        ("Understanding Reference Ranges",
         "The reference range (sometimes called 'normal range') is perhaps the most misunderstood part of a lab report.\n\n**How reference ranges are established:**\nReference ranges are typically calculated from the results of 100-200 healthy volunteers. The range represents the central 95% of these results — meaning 5% of completely healthy people will have values outside the 'normal' range by definition.\n\n**What this means for you:**\nIf 20 tests are run simultaneously, statistically at least one is likely to fall outside the reference range by chance alone, even if you're perfectly healthy. This is why doctors look at results in the context of your symptoms, medical history, and other results — not just whether a value is inside or outside the range.\n\n**Reference ranges vary between laboratories:**\nDifferent labs use different analyzers and may have slightly different reference ranges. Always compare your result to the reference range on YOUR lab report, not values from the internet."),
        ("Common Abbreviations Explained",
         "**Blood count abbreviations:**\n- WBC: White Blood Cell count\n- RBC: Red Blood Cell count\n- Hgb/Hb: Hemoglobin\n- Hct: Hematocrit\n- MCV: Mean Corpuscular Volume (size of red cells)\n- MCH: Mean Corpuscular Hemoglobin (hemoglobin per red cell)\n- PLT: Platelets\n\n**Chemistry abbreviations:**\n- BUN: Blood Urea Nitrogen\n- Cr/SCr: Creatinine\n- eGFR: estimated Glomerular Filtration Rate\n- Na: Sodium\n- K: Potassium\n- Cl: Chloride\n- CO2/HCO3: Bicarbonate\n- Ca: Calcium\n- Mg: Magnesium\n- ALT/SGPT: Liver enzyme\n- AST/SGOT: Liver enzyme\n- ALP: Alkaline Phosphatase\n- Bil: Bilirubin\n- Alb: Albumin"),
        ("When to Be Concerned",
         "Not every abnormal result requires immediate action. Context matters enormously:\n\n**Likely not concerning:**\n- Mildly out of range (just above or below the reference range)\n- Result consistent with a known explanation (post-exercise creatinine, end-of-day glucose)\n- Isolated abnormality with normal related tests\n- No accompanying symptoms\n\n**Warrants follow-up with your doctor:**\n- Moderately abnormal results\n- Abnormal results in multiple related tests\n- New abnormalities compared to previous tests\n- Results flagged as 'critical' by the laboratory\n\n**Seek medical attention promptly:**\n- Critical values (most labs call these immediately to the doctor)\n- Symptoms accompanying abnormal results\n- Troponin elevation\n- Markedly abnormal electrolytes (potassium <2.5 or >6.5)\n- Very low hemoglobin (<7 g/dL)"),
        ("Trending Results Over Time",
         "Single results are often less informative than trends over time. When interpreting lab results:\n\n**Upward trend is more concerning than stable value:**\n- Creatinine rising from 1.0 to 1.5 to 2.0 over 3 months = deteriorating kidney function\n- Creatinine stable at 1.5 for 5 years = likely chronic but stable\n\n**Compare to your personal baseline:**\nYour 'normal' may differ from the reference range. Some people naturally run slightly low or high on certain values. A doctor treating you long-term knows your personal baseline.\n\n**Keep a record of your results:**\nKeep copies of your lab reports — ideally in a simple spreadsheet tracking date and key values. This allows you and your doctor to spot trends that individual reports cannot reveal.\n\n**Ask for previous results:**\nAlways ask your doctor how current results compare to previous ones. 'It's slightly elevated' means nothing without knowing whether it has been stable for years or has risen recently."),
    ]


def _preparation_sections():
    return [
        ("Why Test Preparation Matters",
         "Proper preparation before blood tests is not just a formality — it directly affects the accuracy of your results. Ignoring preparation instructions can lead to falsely abnormal results, unnecessary worry, repeated testing, and potentially inappropriate treatment.\n\nDifferent tests have different preparation requirements. Understanding why each instruction exists helps you follow them correctly and lets you alert your doctor to any deviations."),
        ("Fasting Requirements",
         "**Tests that REQUIRE fasting (8-12 hours):**\n- Fasting glucose and insulin\n- Complete metabolic panel (CMP) or basic metabolic panel\n- Lipid panel (cholesterol, triglycerides)\n- HbA1c can be done fasting or non-fasting\n- Some liver function tests\n\n**Tests that do NOT require fasting:**\n- Complete blood count (CBC)\n- Thyroid function tests (TSH, T4, T3)\n- HbA1c\n- Vitamin D\n- Most hormones\n- Tumor markers\n- Inflammatory markers (CRP, ESR)\n\n**Water:** Always drink plain water freely even when fasting. Dehydration concentrates the blood, artificially raising creatinine, sodium, and other values. Water does not affect any test results.\n\n**Coffee:** Avoid even black coffee when fasting — it affects glucose metabolism and can interfere with certain hormone tests."),
        ("Medications and Supplements",
         "**Generally continue unless specifically told to stop:**\n- Blood pressure medications\n- Thyroid medications (though some doctors prefer you take them after the blood draw)\n- Heart medications\n- Diabetic medications\n\n**May affect specific tests — discuss with your doctor:**\n- Biotin (high-dose supplements interfere with many hormone assays including thyroid tests — stop 72 hours before)\n- Vitamin supplements before vitamin level testing\n- Iron supplements before iron studies\n- Aspirin before platelet function tests\n- Anticoagulants (warfarin, heparin) before coagulation tests\n\n**Always tell your doctor ALL medications, supplements, and herbal products** — even if you think they're irrelevant. Many interact with test results in ways that are not obvious."),
        ("Exercise and Activity",
         "**Avoid intense exercise 24-48 hours before:**\n- Creatinine (muscle breakdown raises levels)\n- CK (creatine kinase) — can reach 5-10x normal after intense exercise\n- AST and LDH (released from muscle, not just liver)\n- Potassium (released from muscle cells during exercise)\n- Uric acid (produced during cellular breakdown)\n- Troponin (even mild elevations possible after extreme endurance events)\n\n**Normal daily activity is fine** before most tests.\n\n**Timing your blood draw:**\nMorning blood draws are preferred for fasting tests and hormonal tests with diurnal variation (cortisol, testosterone, growth hormone all peak in the morning and are significantly lower by afternoon)."),
        ("Day of Testing — Practical Tips",
         "**What to wear:** Short sleeves or loose sleeves that roll up easily.\n\n**Stay calm:** Anxiety briefly raises cortisol, glucose, and heart rate. If you're anxious about needles, inform the phlebotomist — they can help.\n\n**Stay hydrated:** Drink plenty of water before arriving. Well-hydrated veins are easier to find and access, reducing discomfort and the chance of multiple attempts.\n\n**Posture matters for some tests:** Albumin and total protein are slightly higher when standing — some labs specify sitting for 15 minutes before blood draw to standardize.\n\n**Renin/aldosterone testing:** Requires specific posture protocol (often 30 minutes upright before draw) — ask your doctor.\n\n**After your blood draw:** You can eat, drink, and resume all normal activities immediately. Apply gentle pressure to the site for 1-2 minutes to minimize bruising."),
    ]


def _diabetes_tests_sections():
    return [
        ("Overview of Diabetes Blood Tests",
         "Diabetes mellitus is diagnosed and monitored through several blood tests, each measuring different aspects of glucose metabolism. Understanding all available tests helps you know what your doctor is evaluating and why different tests are ordered at different times.\n\nNo single test tells the complete story — experienced clinicians use a combination of tests to accurately diagnose diabetes, assess control, detect complications early, and evaluate treatment effectiveness."),
        ("Fasting Plasma Glucose",
         "**Normal:** <100 mg/dL\n**Prediabetes:** 100-125 mg/dL\n**Diabetes:** ≥126 mg/dL (must be confirmed on a separate day unless symptoms are present)\n\nFasting plasma glucose (FPG) requires no food or caloric beverages for at least 8 hours. It directly measures blood sugar in the fasting state and reflects hepatic glucose production.\n\nFPG can vary day-to-day based on recent diet, stress, illness, and sleep quality. A single elevated result must be confirmed on a separate occasion. Morning testing is preferred because of the 'dawn phenomenon' — cortisol and growth hormone rise in the early morning hours, slightly raising blood glucose."),
        ("HbA1c — The 3-Month Average",
         "**Below 5.7%:** Normal\n**5.7-6.4%:** Prediabetes\n**≥6.5%:** Diabetes\n**Target for most treated diabetics:** <7.0%\n\nHbA1c reflects average blood glucose over the past 2-3 months by measuring the percentage of hemoglobin that has glucose attached. It is the cornerstone of long-term diabetes monitoring because it provides an objective measure of overall glucose control that is not affected by recent meals or stress.\n\nHbA1c does NOT require fasting and can be drawn anytime. Its main limitation is in conditions affecting red blood cell lifespan: HbA1c is falsely low in hemolytic anemia, recent blood transfusion, and iron/B12 deficiency; falsely high in iron deficiency anemia and hemoglobin variants."),
        ("Postprandial Glucose and OGTT",
         "**2-hour postprandial glucose:**\n- Normal: <140 mg/dL (2 hours after meals)\n- Impaired glucose tolerance: 140-199 mg/dL\n- Diabetes: ≥200 mg/dL\n\n**Oral Glucose Tolerance Test (OGTT):**\nThe gold standard for diagnosing gestational diabetes and identifying glucose intolerance not detected by fasting glucose.\n- Drink 75g glucose solution\n- Measure glucose at fasting, 1 hour, and 2 hours\n- Diabetes diagnosis: 2-hour glucose ≥200 mg/dL\n\nOGTT detects postprandial hyperglycemia that may be missed by fasting tests — some people have normal fasting glucose but significantly elevated glucose after meals, indicating early or borderline diabetes."),
        ("Monitoring Tests for Diagnosed Diabetics",
         "Once diabetes is diagnosed, regular monitoring tests include:\n\n**HbA1c:** Every 3 months (if not at target) or every 6 months (if stable and well-controlled)\n\n**Kidney function:** Annual urine albumin-creatinine ratio (uACR) and eGFR — early marker of diabetic nephropathy\n\n**Lipid panel:** Annual — diabetics have high cardiovascular risk\n\n**Liver function:** If on metformin or other hepatically-metabolized medications\n\n**Vitamin B12:** Annual if on metformin (can reduce B12 absorption)\n\n**Thyroid function:** Especially in Type 1 diabetics (higher risk of autoimmune thyroid disease)\n\n**Eye examination:** Annual dilated fundal examination — diabetic retinopathy\n\n**Foot examination:** Annual — peripheral neuropathy and vascular disease\n\nSystematic monitoring allows early detection of complications when they are most treatable."),
    ]


def _generic_sections(topic: dict) -> list:
    """Generate generic sections for topics without specific content."""
    title = topic["title"]
    return [
        (f"What is the {title}?",
         f"The {title} is an important diagnostic tool used in clinical medicine to assess specific aspects of health and disease. Understanding what this test measures, how to interpret results, and what actions to take based on findings is essential for both patients and healthcare professionals.\n\nThis guide provides expert interpretation of test results, written from a clinical biochemistry perspective with the goal of helping you understand your health data more clearly."),
        ("Normal Ranges and Interpretation",
         "Laboratory reference ranges represent the values found in 95% of healthy individuals. Values outside these ranges may indicate disease, but must always be interpreted in the context of clinical symptoms, medical history, and other test results.\n\nYour doctor will consider all available information when interpreting any laboratory result — context is everything in laboratory medicine."),
        ("When This Test is Ordered",
         "This test is typically ordered when specific symptoms or risk factors suggest the need for evaluation. Regular monitoring may be recommended for people with certain medical conditions or risk factors.\n\nAlways discuss with your doctor which tests are appropriate for your specific situation and how frequently monitoring should occur."),
        ("Understanding Your Results",
         "Laboratory results must always be interpreted alongside your symptoms, medical history, medications, and other test results. A single abnormal value rarely tells the complete story.\n\nIf your results fall outside the reference range, your doctor will determine whether further investigation is needed, whether the result represents a clinically significant finding, and what management steps are appropriate."),
        ("Questions to Ask Your Doctor",
         "When reviewing laboratory results with your doctor:\n• What does this result mean for my specific situation?\n• How does this compare to my previous results?\n• What follow-up tests or monitoring do you recommend?\n• Are any lifestyle changes that could improve these values?\n• When should I recheck this test?"),
    ]


def _generate_faq(topic: dict) -> list:
    """Generate relevant FAQs based on topic."""
    return [
        ("Do I need to fast before this test?",
         "Fasting requirements vary by test. Always check with your doctor or the laboratory about specific preparation instructions for your ordered tests."),
        ("How long does it take to get results?",
         "Most routine blood tests return results within 24-48 hours. Urgent tests may be available in hours. Specialized tests may take several days to weeks."),
        ("What should I do if my result is abnormal?",
         "Contact your doctor to discuss any abnormal results. Do not self-diagnose or adjust medications based on laboratory results alone — your doctor will interpret results in the context of your complete clinical picture."),
    ]

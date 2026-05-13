import streamlit as st
import pandas as pd
from typing import Dict, Any

# Page configuration
st.set_page_config(
    page_title="Med-AI Guide: Integrated Allopathy & Homeopathy Knowledge Engine",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional medical theme
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        background-color: #f8f9fa;
    }
    .medical-blue {
        color: #0056b3 !important;
    }
    .safety-banner {
        background: linear-gradient(90deg, #dc3545 0%, #ffc107 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        color: white !important;
        margin-bottom: 2rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .search-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        border-left: 5px solid #0056b3;
    }
    .reference-section {
        background: #e8f4fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #0056b3;
        margin-top: 1.5rem;
    }
    .mode-toggle {
        background: #0056b3;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: bold;
    }
    .stButton > button {
        background: linear-gradient(45deg, #0056b3, #007bff);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(0,86,179,0.3);
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #004494, #0056b3);
        box-shadow: 0 6px 16px rgba(0,86,179,0.4);
    }
    h1, h2, h3 {
        color: #0056b3 !important;
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Mock Medical Database
MEDICAL_DB = {
    "Migraine": {
        "allopathic_treatment": """
        **Acute Treatment:**
        - Triptans (Sumatriptan 50-100mg oral/6mg SC)
        - NSAIDs (Ibuprofen 400-800mg, Naproxen 500mg)
        - Antiemetics (Metoclopramide 10mg)
        
        **Prophylaxis (if >4 attacks/month):**
        - Topiramate 50-100mg daily
        - Propranolol 40-240mg daily
        - Amitriptyline 25-75mg nightly
        
        **Lifestyle:** Regular sleep, hydration, trigger avoidance
        """,
        "homeopathic_treatment": """
        **Acute Remedies (match symptoms):**
        - **Belladonna 30C**: Throbbing headache, worse light/noise, right-sided, sudden onset
        - **Bryonia 30C**: Bursting pain, worse motion, better pressure/rest
        - **Nux Vomica 30C**: From overwork/stress, nausea, irritable
        - **Iris Versicolor 30C**: Migraine with vomiting, blurred vision
        
        **Constitutional:** Natrum Muriaticum, Sepia (consult homeopath)
        """,
        "citations": [
            "Harrison's Principles of Internal Medicine, 21st Ed., Ch. 45, pp. 128-135",
            "Boericke's Materia Medica, Belladonna: 156-158, Bryonia: 168-170"
        ]
    },
    "Common Cold": {
        "allopathic_treatment": """
        **Symptomatic Treatment:**
        - Decongestants: Pseudoephedrine 60mg q6h or Oxymetazoline nasal spray (3 days max)
        - Antihistamines: Loratadine 10mg daily (for runny nose)
        - Analgesics: Acetaminophen 500-1000mg q6h or Ibuprofen 400mg q6-8h
        - Cough: Dextromethorphan 15-30mg q6-8h
        
        **Supportive:** Hydration, rest, saline gargles, humidifier
        **Antibiotics ONLY if bacterial sinusitis (rare)**
        """,
        "homeopathic_treatment": """
        **Stage-Specific Remedies:**
        - **Aconite 30C**: First 24hrs, sudden onset, fever, restlessness
        - **Allium Cepa 30C**: Profuse watery nasal discharge, burning eyes
        - **Natrum Muriaticum 30C**: Thick white discharge, sneezing
        - **Dulcamara 30C**: Cold from damp weather exposure
        - **Kali Bichromicum 30C**: Thick stringy mucus
        
        **Prevention:** Influenzinum annually
        """,
        "citations": [
            "Harrison's Principles of Internal Medicine, 21st Ed., Ch. 192, pp. 1045-1048",
            "Boericke's Materia Medica, Aconite: 23-25, Allium Cepa: 34-35"
        ]
    },
    "Type 2 Diabetes": {
        "allopathic_treatment": """
        **Lifestyle First:**
        - Weight loss 5-10% body weight
        - Exercise 150min/week moderate aerobic
        - Diet: Mediterranean/low-carb
        
        **Pharmacotherapy (titrate based on HbA1c):**
        - **Metformin 500-2000mg daily** (first line)
        - GLP-1 agonists: Semaglutide 0.25-2.4mg weekly
        - SGLT2 inhibitors: Empagliflozin 10-25mg daily
        - Insulin if HbA1c >9% or symptomatic
        
        **Targets:** HbA1c <7%, BP <130/80, LDL <100mg/dL
        """,
        "homeopathic_treatment": """
        **Constitutional Treatment:**
        - **Syzygium Jambolanum Q**: Reduces blood sugar, frequent urination
        - **Uranium Nitricum 6X**: Diabetes with kidney involvement
        - **Phosphoric Acid 30C**: Diabetes from grief/exhaustion
        - **Lactic Acid 30C**: Thirst, dry mouth, sugar in urine
        
        **Adjuncts:** Gymnema Sylvestre mother tincture
        **Requires professional homeopathic supervision**
        """,
        "citations": [
            "Harrison's Principles of Internal Medicine, 21st Ed., Ch. 343, pp. 2482-2510",
            "Boericke's Materia Medica, Syzygium Jamb: 647-648, Uranium Nit: 689"
        ]
    }
}

def get_ai_response(query: str, mode: str) -> str:
    """Generate AI response based on mode and query"""
    query_lower = query.lower().strip()
    
    # Find matching disease
    disease_key = None
    for disease in MEDICAL_DB:
        if disease.lower() in query_lower or query_lower in disease.lower():
            disease_key = disease
            break
    
    if not disease_key:
        return f"""
        ## 🔍 Search Results for "{query}"
        
        No exact match found in our medical database. 
        Please try searching for:
        - Migraine
        - Common Cold  
        - Type 2 Diabetes
        
        **Tip:** Be specific with disease names for best results.
        """
    
    disease_data = MEDICAL_DB[disease_key]
    
    if mode == "Allopathy":
        return f"""
        # 🏥 {disease_key} - Allopathic Treatment Protocol
        
        {disease_data['allopathic_treatment']}
        
        **Clinical Guidelines:** ADA/EASD consensus, AAN migraine guidelines
        """
    
    elif mode == "Homeopathy":
        return f"""
        # 🌿 {disease_key} - Homeopathic Treatment Protocol
        
        {disease_data['homeopathic_treatment']}
        
        **Principle:** Individualized remedy selection based on totality of symptoms
        """
    
    else:  # Integrated
        return f"""
        # 🔬 {disease_key} - Integrated Medical Approach
        
        ## 🏥 Allopathic Treatment (Evidence-Based First Line)
        {disease_data['allopathic_treatment']}
        
        ---
        
        ## 🌿 Homeopathic Treatment (Symptom-Specific Support)
        {disease_data['homeopathic_treatment']}
        
        **Integrated Philosophy:** Use allopathic for acute/evidence-based needs, homeopathy for constitutional support.
        Always start with lifestyle modification.
        """

# Safety Banner
st.markdown("""
    <div class="safety-banner">
        ⚠️ FOR EDUCATIONAL PURPOSES ONLY. This AI is NOT a doctor. 
        Consult a licensed healthcare professional before starting any medication or treatment.
    </div>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.title("🩺 Med-AI Guide")
    
    # Mode Toggle
    mode = st.selectbox(
        "Treatment Mode",
        ["Integrated", "Allopathy", "Homeopathy"],
        index=0,
        help="Choose your preferred medical approach"
    )
    
    st.markdown("---")
    
    # Navigation
    page = st.radio(
        "Navigation",
        ["🔍 Search", "📚 Encyclopedia", "ℹ️ About"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("""
    **References:**
    - Harrison's Principles of Internal Medicine (21st Ed.)
    - Boericke's Materia Medica (9th Ed.)
    """)

# Main Content
if page == "🔍 Search":
    # Search Interface
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input(
            "",
            placeholder="Enter symptoms or disease name (e.g., 'Migraine', 'Common Cold', 'Type 2 Diabetes')...",
            label_visibility="collapsed",
            key="main_search"
        )
    
    with col2:
        generate_btn = st.button("🤖 Generate AI Summary", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Results
    if generate_btn and query:
        with st.spinner("Generating integrated medical guidance..."):
            response = get_ai_response(query, mode)
            
            st.markdown(response)
            
            # Reference Section
            if "No exact match" not in response:
                disease_key = next((k for k in MEDICAL_DB if k.lower() in query.lower()), None)
                if disease_key:
                    citations = MEDICAL_DB[disease_key]["citations"]
                    st.markdown("### 📖 Scientific Citations")
                    st.markdown('<div class="reference-section">', unsafe_allow_html=True)
                    
                    for i, citation in enumerate(citations, 1):
                        st.markdown(f"**{i}.** {citation}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
    
    elif query:
        st.info("👆 Click 'Generate AI Summary' to get detailed treatment recommendations")

elif page == "📚 Encyclopedia":
    st.title("📚 Medical Encyclopedia")
    
    st.markdown("""
    ## Available Diseases in Database
    
    Our knowledge engine contains detailed protocols for:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧠 Migraine", use_container_width=True):
            st.session_state[' encyclopedia_disease'] = "Migraine"
    
    with col2:
        if st.button("🤧 Common Cold", use_container_width=True):
            st.session_state['encyclopedia_disease'] = "Common Cold"
    
    with col3:
        if st.button("🍬 Type 2 Diabetes", use_container_width=True):
            st.session_state['encyclopedia_disease'] = "Type 2 Diabetes"
    
    # Show selected disease
    if 'encyclopedia_disease' in st.session_state:
        disease = st.session_state['encyclopedia_disease']
        response = get_ai_response(disease, mode)
        st.markdown(response)

elif page == "ℹ️ About":
    st.title("ℹ️ About Med-AI Guide")
    
    st.markdown("""
    # Med-AI Guide: Integrated Knowledge Engine
    
    ## 🎯 Purpose
    Educational reference tool combining **Allopathic** (evidence-based medicine) 
    and **Homeopathic** (individualized symptom-based) approaches.
    
    ## 📚 Knowledge Sources
    - **Harrison's Principles of Internal Medicine** (21st Edition)
    - **Boericke's Materia Medica** (9th Edition)
    
    ## ⚙️ Features
    - **Mode Toggle**: Switch between Allopathy, Homeopathy, or Integrated views
    - **AI-Generated Summaries**: Context-aware treatment recommendations
    - **Scientific Citations**: Direct references to medical textbooks
    
    ## 🎨 Technology Stack
    - **Streamlit**: Professional medical UI
    - **Python**: Backend logic & mock medical database
    
    **Disclaimer**: This is an educational prototype. Always consult licensed healthcare professionals.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    🩺 Med-AI Guide | Educational Prototype | v1.0
</div>
""", unsafe_allow_html=True)
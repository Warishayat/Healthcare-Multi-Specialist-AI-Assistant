from Backend.Dental_Module import Dental_Specialist
from Backend.Dermotologist import Dermatologist_specialist, encode_image 
from Backend.Diet_Neutration import Diet_Neutration_planner, Download_Diet_plan
from Backend.Fitness_advisor import Fitness_advisor_Coach, Download_Fitness_advisor_plan
from Backend.Genral_Physican import General_physican
from Backend.Medical_Report_Analyzer import query_medical_report, rag_pipeline
from Backend.pharmacist import encode_image as encode_image_pharmacist, Pharmacist_specialist
from Backend.M_Health_Counselor import Mental_Health_counselor, Download_Mental_plan
import streamlit as st
import os
import tempfile
import base64
from fpdf import FPDF
from PIL import Image
import requests
from io import BytesIO

# --- Page Configuration ---
st.set_page_config(
    page_title="HealthHub AI - Multi-Specialist Healthcare Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Session State Initialization ---
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'dental': {'query': '', 'image': None},
        'dermatologist': {'query': '', 'image': None},
        'diet': {'age': 30, 'weight': 70.0, 'height': 170.0, 'activity': 'Beginner', 'goal': 'Weight loss', 'restrictions': 'None'},
        'fitness': {'level': 'Beginner', 'goal': 'Strength', 'equipment': 'None'},
        'physician': {'age': 30, 'gender': 'Male', 'weight': 70.0, 'height': 170.0, 'symptoms': ''},
        'mental_health': {'mood': '', 'sleep': 5, 'stress': 5},
        'pharmacist': {'query': '', 'image': None},
        'report': {'query': '', 'file': None}
    }

# --- Theme-Aware CSS ---
st.markdown("""
    <style>
    :root {
        --primary: #2563eb;
        --primary-dark: #1d4ed8;
        --secondary: #059669;
        --secondary-dark: #047857;
        --text: #1f2937;
        --text-light: #f9fafb;
        --bg: #f8fafc;
        --card-bg: #fcfcfd;
        --card-shadow: rgba(0,0,0,0.06);
        --input-bg: #fff;
        --input-border: #e2e8f0;
        --sidebar-bg: #f1f5f9;
        --sidebar-border: #e5e7eb;
        --sidebar-text: #334155;
        --radio-bg: rgba(0,0,0,0.03);
        --radio-selected: #e0e7ef;
    }
    
    @media (prefers-color-scheme: dark) {
        :root {
            --text: #f0f0f0;
            --bg: #121212;
            --card-bg: #1e1e1e;
            --card-shadow: rgba(0,0,0,0.3);
            --input-bg: #2d2d2d;
            --input-border: #444;
            --sidebar-bg: linear-gradient(180deg, #1a3d7a 0%, #0d2b5e 100%);
            --sidebar-text: #ffffff;
        }
    }
    
    body, .main {
        background-color: var(--bg);
        color: var(--text);
        font-size: 1.08rem;
        line-height: 1.7;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: var(--sidebar-bg);
        color: var(--sidebar-text);
        padding: 2rem 1.2rem 2rem 1.2rem;
        border-right: 1.5px solid var(--sidebar-border);
        box-shadow: 2px 0 8px 0 rgba(0,0,0,0.03);
    }
    
    /* Sidebar logo */
    .sidebar-logo {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Sidebar radio buttons */
    .st-eb {
        background-color: var(--radio-bg) !important;
        margin-bottom: 12px;
        border-radius: 14px !important;
        padding: 14px !important;
        transition: all 0.3s ease;
    }
    
    /* Selected radio button */
    .st-eb.st-c7 {
        background-color: var(--radio-selected) !important;
        font-weight: 600;
        border: 1.5px solid var(--primary);
    }
    
    /* Radio button label */
    .stRadio > label {
        color: var(--sidebar-text) !important;
        font-size: 1.08rem;
        padding: 10px 0;
    }
    
    /* Cards for sections */
    .card {
        background: var(--card-bg);
        border-radius: 18px;
        padding: 2.2rem 2rem 2.2rem 2rem;
        box-shadow: 0 4px 18px var(--card-shadow);
        margin-bottom: 2.2rem;
        color: var(--text);
        border: 1.5px solid var(--input-border);
    }
    
    /* Form elements */
    .stTextInput>div>div>input, 
    .stNumberInput>div>div>input, 
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        border-radius: 14px;
        padding: 1rem;
        border: 1.5px solid var(--input-border);
        background-color: var(--input-bg);
        color: var(--text);
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        font-size: 1.08rem;
    }
    
    .stTextArea>div>div>textarea {
        background-color: #fff;
        color: #1f2937;
        border-radius: 14px;
        padding: 1rem;
        border: 1.5px solid var(--input-border);
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        min-height: 120px;
    }
    @media (prefers-color-scheme: dark) {
        .stTextArea>div>div>textarea {
            background-color: #23272f;
            color: #f0f0f0;
        }
    }
    
    /* File uploader */
    .stFileUploader>div>div>div>button {
        border-radius: 14px;
        padding: 1rem 2rem;
    }
    
    /* Download buttons */
    .download-btn {
        background: linear-gradient(90deg, var(--secondary) 0%, var(--secondary-dark) 100%) !important;
        color: white !important;
        border-radius: 14px;
        padding: 1rem 2rem;
        margin: 1.5rem 0;
        text-align: center;
        display: inline-block;
        font-weight: 600;
        text-decoration: none;
        box-shadow: 0 2px 8px rgba(5, 150, 105, 0.13);
        transition: all 0.3s ease;
    }
    
    .download-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 14px rgba(5, 150, 105, 0.18);
        color: white !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white !important;
        border-radius: 14px;
        padding: 1rem 2rem;
        margin-top: 1.7rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.13);
        transition: all 0.3s ease;
        font-size: 1.08rem;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.18);
        opacity: 0.97;
    }
    
    /* Header image */
    .header-img {
        text-align: center;
        margin-bottom: 2.2rem;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: var(--text);
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    h1 {
        margin-top: 0.5rem;
        font-size: 2.7rem;
    }
    
    /* Spinner */
    .stSpinner > div {
        margin: 2rem auto;
    }
    
    /* Error messages */
    .stAlert {
        border-radius: 14px;
        padding: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
def create_download_link(content, filename, text):
    """Create a download link for text content."""
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}" class="download-btn">{text}</a>'
    return href

def create_pdf_download_link(pdf_bytes, filename, text):
    """Create a download link for PDF bytes."""
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}" class="download-btn">{text}</a>'
    return href

def generate_pdf_from_text(text):
    """Generate PDF from text using FPDF."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=text)
    return pdf.output(dest='S').encode('latin-1')

# --- Header Image ---
def load_header_image():
    hospital_img_url = "https://th.bing.com/th/id/OIP.-VH9JiaEYFtLCToj3rI8JgHaE7?cb=iwc2&rs=1&pid=ImgDetMain"
    response = requests.get(hospital_img_url)
    img = Image.open(BytesIO(response.content))
    return img

header_img = load_header_image()
buffered = BytesIO()
header_img.save(buffered, format="PNG")
img_str = base64.b64encode(buffered.getvalue()).decode()
st.markdown(
    f"""
    <div class="header-img">
        <img src='data:image/png;base64,{img_str}' 
             style='height: 200px; width: auto; max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'/>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Sidebar with Logo ---
st.sidebar.markdown("""
    <div class="sidebar-logo">
        <svg width="50" height="50" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 8V16" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M8 12H16" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h2 style="color: white; margin-top: 10px;">HealthHub AI</h2>
    </div>
    <div style="color: white; font-size: 0.95rem; margin-bottom: 2rem;">
    Your personal AI healthcare assistant providing expert advice across multiple specialties.
    </div>
""", unsafe_allow_html=True)

# --- Navigation ---
app_mode = st.sidebar.radio(
    "Choose a specialist:",
    ["🦷 Dental Specialist", 
     "🧴 Dermatologist", 
     "🍎 Diet & Nutrition", 
     "💪 Fitness Coach",
     "👨‍⚕️ General Physician", 
     "🧠 Mental Health", 
     "💊 Pharmacist", 
     "📄 Medical Report Analysis"],
    index=0
)

# --- Main Content ---
st.title("🏥 Healthcare Multi-Specialist AI Assistant")

# --- Specialist Sections with Session Management ---
if app_mode == "🦷 Dental Specialist":
    st.header("🦷 Dental Specialist")
    st.markdown("Upload an image of your teeth/gums and describe your symptoms")
    
    dental_image = st.file_uploader("Upload dental image", type=["jpg", "jpeg", "png"])
    dental_query = st.text_area("Describe your symptoms or concerns", 
                              value=st.session_state.user_data['dental']['query'])
    
    if st.button("Analyze Dental Issue"):
        if dental_image and dental_query:
            st.session_state.user_data['dental']['query'] = dental_query
            st.session_state.user_data['dental']['image'] = dental_image
            with st.spinner("Analyzing your dental issue..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                        tmp.write(dental_image.read())
                        img_path = tmp.name
                    
                    from Backend.Dental_Module import encode_image
                    encoded_img = encode_image(img_path)
                    response = Dental_Specialist(encoded_img, dental_query)
                    
                    st.subheader("Dental Diagnosis")
                    st.markdown(f"<div class='card'>{response}</div>", unsafe_allow_html=True)
                    st.markdown(create_download_link(response, "dental_diagnosis.txt", "📥 Download Diagnosis"), unsafe_allow_html=True)
                    
                    os.unlink(img_path)
                except Exception as e:
                    st.error(f"Error processing your request: {str(e)}")
        else:
            st.warning("Please upload an image and describe your symptoms")

elif app_mode == "🧴 Dermatologist":
    st.header("🧴 Dermatologist")
    st.markdown("Upload an image of your skin condition and describe your symptoms")
    
    derm_image = st.file_uploader("Upload skin image", type=["jpg", "jpeg", "png"])
    derm_query = st.text_area("Describe your symptoms or concerns",
                             value=st.session_state.user_data['dermatologist']['query'])
    
    if st.button("Analyze Skin Condition"):
        if derm_image and derm_query:
            st.session_state.user_data['dermatologist']['query'] = derm_query
            st.session_state.user_data['dermatologist']['image'] = derm_image
            with st.spinner("Analyzing your skin condition..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                        tmp.write(derm_image.read())
                        img_path = tmp.name
                    
                    encoded_img = encode_image(img_path)
                    response = Dermatologist_specialist(encoded_img, derm_query)
                    
                    st.subheader("Dermatological Assessment")
                    st.markdown(f"<div class='card'>{response}</div>", unsafe_allow_html=True)
                    st.markdown(create_download_link(response, "skin_assessment.txt", "📥 Download Assessment"), unsafe_allow_html=True)
                    
                    os.unlink(img_path)
                except Exception as e:
                    st.error(f"Error processing your request: {str(e)}")
        else:
            st.warning("Please upload an image and describe your symptoms")

elif app_mode == "🍎 Diet & Nutrition":
    st.header("🍎 Diet & Nutrition Planner")
    st.markdown("Get a personalized 7-day meal plan based on your profile")
    
    with st.form("diet_form"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=1, max_value=120, 
                                value=st.session_state.user_data['diet']['age'],
                                key='diet_age')
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, 
                                   value=st.session_state.user_data['diet']['weight'],
                                   key='diet_weight')
            height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, 
                                   value=st.session_state.user_data['diet']['height'],
                                   key='diet_height')
        with col2:
            activity_level = st.selectbox("Activity Level", ["Beginner", "Intermediate", "Advanced"],
                                        index=["Beginner", "Intermediate", "Advanced"].index(
                                            st.session_state.user_data['diet']['activity']),
                                        key='diet_activity')
            goal = st.selectbox("Goal", ["Weight loss", "Muscle gain", "Maintenance"],
                              index=["Weight loss", "Muscle gain", "Maintenance"].index(
                                  st.session_state.user_data['diet']['goal']),
                              key='diet_goal')
            dietary_restrictions = st.selectbox("Dietary Restrictions", 
                                             ["None", "Vegetarian", "Vegan", "Gluten-free", "Diabetic", "Keto"],
                                             index=["None", "Vegetarian", "Vegan", "Gluten-free", "Diabetic", "Keto"].index(
                                                 st.session_state.user_data['diet']['restrictions']),
                                             key='diet_restrictions')
        
        if st.form_submit_button("Generate Meal Plan"):
            # Update session state
            st.session_state.user_data['diet'] = {
                'age': age,
                'weight': weight,
                'height': height,
                'activity': activity_level,
                'goal': goal,
                'restrictions': dietary_restrictions
            }
            
            with st.spinner("Creating your personalized meal plan..."):
                try:
                    meal_plan_text = Diet_Neutration_planner(
                        age=age,
                        weight=weight,
                        height=height,
                        activity_level=activity_level,
                        goal=goal,
                        dietary_restrictions=dietary_restrictions
                    )
                    
                    st.subheader("Your Personalized Meal Plan")
                    st.markdown(f"<div class='card'>{meal_plan_text}</div>", unsafe_allow_html=True)
                    
                    # Generate PDF
                    try:
                        pdf_bytes = generate_pdf_from_text(meal_plan_text)
                        st.markdown(create_pdf_download_link(pdf_bytes, "meal_plan.pdf", "📥 Download as PDF"), unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"PDF generation failed: {str(e)}")
                        st.markdown(create_download_link(meal_plan_text, "meal_plan.txt", "📥 Download as Text"), unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Error generating meal plan: {str(e)}")

elif app_mode == "💪 Fitness Coach":
    st.header("💪 Fitness Coach")
    st.markdown("Get a personalized workout plan based on your fitness level and goals")
    
    with st.form("fitness_form"):
        col1, col2 = st.columns(2)
        with col1:
            fitness_level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"],
                                       index=["Beginner", "Intermediate", "Advanced"].index(
                                           st.session_state.user_data['fitness']['level']),
                                       key='fitness_level')
            goal = st.selectbox("Goal", ["Strength", "Weight Loss", "Flexibility", "Muscle Gain"],
                              index=["Strength", "Weight Loss", "Flexibility", "Muscle Gain"].index(
                                  st.session_state.user_data['fitness']['goal']),
                              key='fitness_goal')
        with col2:
            equipment_available = st.selectbox("Equipment Available", 
                                            ["None", "Home (basic)", "Gym (full equipment)"],
                                            index=["None", "Home (basic)", "Gym (full equipment)"].index(
                                                st.session_state.user_data['fitness']['equipment']),
                                            key='fitness_equipment')
        
        if st.form_submit_button("Generate Workout Plan"):
            # Update session state
            st.session_state.user_data['fitness'] = {
                'level': fitness_level,
                'goal': goal,
                'equipment': equipment_available
            }
            
            with st.spinner("Creating your personalized workout plan..."):
                try:
                    workout_plan = Fitness_advisor_Coach(
                        fitness_level=fitness_level,
                        equipment_available=equipment_available,
                        goal=goal
                    )
                    
                    st.subheader("Your Personalized Workout Plan")
                    st.markdown(f"<div class='card'>{workout_plan}</div>", unsafe_allow_html=True)
                    
                    # Generate PDF
                    try:
                        pdf_bytes = generate_pdf_from_text(workout_plan)
                        st.markdown(create_pdf_download_link(pdf_bytes, "workout_plan.pdf", "📥 Download as PDF"), unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"PDF generation failed: {str(e)}")
                        st.markdown(create_download_link(workout_plan, "workout_plan.txt", "📥 Download as Text"), unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error generating workout plan: {str(e)}")

elif app_mode == "👨‍⚕️ General Physician":
    st.header("👨‍⚕️ General Physician")
    st.markdown("Describe your symptoms for general health advice")
    
    with st.form("physician_form"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=1, max_value=120, 
                                value=st.session_state.user_data['physician']['age'],
                                key='physician_age')
            gender = st.selectbox("Gender", ["Male", "Female", "Other"],
                                index=["Male", "Female", "Other"].index(
                                    st.session_state.user_data['physician']['gender']),
                                key='physician_gender')
        with col2:
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, 
                                   value=st.session_state.user_data['physician']['weight'],
                                   key='physician_weight')
            height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, 
                                   value=st.session_state.user_data['physician']['height'],
                                   key='physician_height')
        
        symptoms = st.text_area("Describe your symptoms in detail",
                              value=st.session_state.user_data['physician']['symptoms'],
                              key='physician_symptoms')
        
        if st.form_submit_button("Get Medical Advice"):
            # Update session state
            st.session_state.user_data['physician'] = {
                'age': age,
                'gender': gender,
                'weight': weight,
                'height': height,
                'symptoms': symptoms
            }
            
            with st.spinner("Analyzing your symptoms..."):
                try:
                    advice = General_physican(
                        age=age,
                        gender=gender,
                        weight=weight,
                        height=height,
                        symptoms=symptoms
                    )
                    
                    st.subheader("Medical Advice")
                    st.markdown(f"<div class='card'>{advice}</div>", unsafe_allow_html=True)
                    st.markdown(create_download_link(advice, "medical_advice.txt", "📥 Download Advice"), unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error processing your request: {str(e)}")

elif app_mode == "🧠 Mental Health":
    st.header("🧠 Mental Health Counselor")
    st.markdown("Share how you're feeling for personalized mental health advice")
    
    with st.form("mental_health_form"):
        mood_desc = st.text_area("How are you feeling today? Describe your mood and thoughts",
                               value=st.session_state.user_data['mental_health']['mood'],
                               key='mental_health_mood')
        
        col1, col2 = st.columns(2)
        with col1:
            sleep_quality = st.slider("Sleep Quality (1-10)", 1, 10, 
                                    value=st.session_state.user_data['mental_health']['sleep'],
                                    key='mental_health_sleep')
        with col2:
            stress_level = st.slider("Stress Level (1-10)", 1, 10,
                                   value=st.session_state.user_data['mental_health']['stress'],
                                   key='mental_health_stress')
        
        if st.form_submit_button("Get Mental Health Advice"):
            # Update session state
            st.session_state.user_data['mental_health'] = {
                'mood': mood_desc,
                'sleep': sleep_quality,
                'stress': stress_level
            }
            
            with st.spinner("Analyzing your mental health..."):
                try:
                    advice = Mental_Health_counselor(
                        mood_desc=mood_desc,
                        sleep_quality=sleep_quality,
                        stress_level=stress_level
                    )
                    
                    st.subheader("Mental Health Assessment")
                    st.markdown(f"<div class='card'>{advice}</div>", unsafe_allow_html=True)
                    
                    # Generate PDF
                    try:
                        pdf_bytes = generate_pdf_from_text(advice)
                        st.markdown(create_pdf_download_link(pdf_bytes, "mental_health_advice.pdf", "📥 Download as PDF"), unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"PDF generation failed: {str(e)}")
                        st.markdown(create_download_link(advice, "mental_health_advice.txt", "📥 Download as Text"), unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error processing your request: {str(e)}")

elif app_mode == "💊 Pharmacist":
    st.header("💊 Pharmacist Specialist")
    st.markdown("Upload an image of your medicine for information about usage and side effects")
    
    pharma_image = st.file_uploader("Upload medicine image", type=["jpg", "jpeg", "png"])
    pharma_query = st.text_area("What would you like to know about this medicine?",
                              value=st.session_state.user_data['pharmacist']['query'])
    
    if st.button("Get Medicine Information"):
        if pharma_image and pharma_query:
            st.session_state.user_data['pharmacist']['query'] = pharma_query
            st.session_state.user_data['pharmacist']['image'] = pharma_image
            with st.spinner("Analyzing the medicine..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                        tmp.write(pharma_image.read())
                        img_path = tmp.name
                    
                    encoded_img = encode_image_pharmacist(img_path)
                    response = Pharmacist_specialist(encoded_img, pharma_query)
                    
                    st.subheader("Medicine Information")
                    st.markdown(f"<div class='card'>{response}</div>", unsafe_allow_html=True)
                    st.markdown(create_download_link(response, "medicine_info.txt", "📥 Download Information"), unsafe_allow_html=True)
                    
                    os.unlink(img_path)
                except Exception as e:
                    st.error(f"Error processing your request: {str(e)}")
        else:
            st.warning("Please upload an image of the medicine and ask your question")

elif app_mode == "📄 Medical Report Analysis":
    st.header("📄 Medical Report Analysis")
    st.markdown("Upload your medical report (PDF) and ask questions about it")
    
    report_file = st.file_uploader("Upload medical report (PDF)", type=["pdf"])
    report_query = st.text_area("What would you like to know about your report?",
                              value=st.session_state.user_data['report']['query'])
    
    if st.button("Analyze Report"):
        if report_file and report_query:
            st.session_state.user_data['report']['query'] = report_query
            st.session_state.user_data['report']['file'] = report_file
            with st.spinner("Analyzing your medical report..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(report_file.read())
                        report_path = tmp.name
                    
                    vector_store, model = rag_pipeline(report_path, 'pdf')
                    analysis = query_medical_report(vector_store, model, report_query)
                    
                    st.subheader("Report Analysis")
                    st.markdown(f"<div class='card'>{analysis}</div>", unsafe_allow_html=True)
                    st.markdown(create_download_link(analysis, "report_analysis.txt", "📥 Download Analysis"), unsafe_allow_html=True)
                    
                    os.unlink(report_path)
                except Exception as e:
                    st.error(f"Error processing your request: {str(e)}")
        else:
            st.warning("Please upload your medical report and ask your question")

# Add footer
st.markdown("""
    <div style="margin-top: 5rem; padding: 1.5rem; background: var(--primary); color: white; border-radius: 8px; text-align: center;">
    <p style="margin: 0; font-weight: 600;">© 2023 HealthHub AI</p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem;">Disclaimer: This AI assistant provides general health information and should not replace professional medical advice.</p>
    </div>
""", unsafe_allow_html=True)
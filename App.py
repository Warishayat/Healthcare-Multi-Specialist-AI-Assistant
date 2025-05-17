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
import io

st.set_page_config(
    page_title="Healthcare Multi-Specialist AI Assistant",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS for better appearance
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #4a8fe7;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        margin-top: 1rem;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 5px;
        padding: 0.5rem;
    }
    .stFileUploader>div>div>div>button {
        border-radius: 5px;
    }
    .download-btn {
        background-color: #28a745 !important;
        color: white !important;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        margin-top: 1rem;
        text-align: center;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

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

# Sidebar navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose a specialist:",
    ["🦷 Dental Specialist", 
     "🧴 Dermatologist", 
     "🍎 Diet & Nutrition", 
     "💪 Fitness Coach",
     "👨‍⚕️ General Physician", 
     "🧠 Mental Health", 
     "💊 Pharmacist", 
     "📄 Medical Report Analysis"])

# Main content area
st.title("🏥 Healthcare Multi-Specialist AI Assistant")

if app_mode == "🦷 Dental Specialist":
    st.header("🦷 Dental Specialist")
    st.markdown("Upload an image of your teeth/gums and describe your symptoms")
    
    dental_image = st.file_uploader("Upload dental image", type=["jpg", "jpeg", "png"])
    dental_query = st.text_area("Describe your symptoms or concerns")
    
    if st.button("Analyze Dental Issue"):
        if dental_image and dental_query:
            with st.spinner("Analyzing your dental issue..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                        tmp.write(dental_image.read())
                        img_path = tmp.name
                    
                    from Backend.Dental_Module import encode_image
                    encoded_img = encode_image(img_path)
                    response = Dental_Specialist(encoded_img, dental_query)
                    
                    st.subheader("Dental Diagnosis")
                    st.markdown(response)
                    st.markdown(create_download_link(response, "dental_diagnosis.txt", "Download Diagnosis"), unsafe_allow_html=True)
                    
                    os.unlink(img_path)
                except Exception as e:
                    st.error(f"Error processing your request: {str(e)}")
        else:
            st.warning("Please upload an image and describe your symptoms")

elif app_mode == "🧴 Dermatologist":
    st.header("🧴 Dermatologist")
    st.markdown("Upload an image of your skin condition and describe your symptoms")
    
    derm_image = st.file_uploader("Upload skin image", type=["jpg", "jpeg", "png"])
    derm_query = st.text_area("Describe your symptoms or concerns")
    
    if st.button("Analyze Skin Condition"):
        if derm_image and derm_query:
            with st.spinner("Analyzing your skin condition..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                        tmp.write(derm_image.read())
                        img_path = tmp.name
                    
                    encoded_img = encode_image(img_path)
                    response = Dermatologist_specialist(encoded_img, derm_query)
                    
                    st.subheader("Dermatological Assessment")
                    st.markdown(response)
                    st.markdown(create_download_link(response, "skin_assessment.txt", "Download Assessment"), unsafe_allow_html=True)
                    
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
            age = st.number_input("Age", min_value=1, max_value=120, value=30)
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
            height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0)
        with col2:
            activity_level = st.selectbox("Activity Level", ["Beginner", "Intermediate", "Advanced"])
            goal = st.selectbox("Goal", ["Weight loss", "Muscle gain", "Maintenance"])
            dietary_restrictions = st.selectbox("Dietary Restrictions", 
                                            ["None", "Vegetarian", "Vegan", "Gluten-free", "Diabetic", "Keto"])
        
        if st.form_submit_button("Generate Meal Plan"):
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
                    st.markdown(meal_plan_text)
                    
                    # Generate PDF
                    try:
                        pdf_bytes = generate_pdf_from_text(meal_plan_text)
                        st.markdown(create_pdf_download_link(pdf_bytes, "meal_plan.pdf", "Download as PDF"), unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"PDF generation failed: {str(e)}")
                        st.markdown(create_download_link(meal_plan_text, "meal_plan.txt", "Download as Text"), unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Error generating meal plan: {str(e)}")

elif app_mode == "💪 Fitness Coach":
    st.header("💪 Fitness Coach")
    st.markdown("Get a personalized workout plan based on your fitness level and goals")
    
    with st.form("fitness_form"):
        col1, col2 = st.columns(2)
        with col1:
            fitness_level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"])
            goal = st.selectbox("Goal", ["Strength", "Weight Loss", "Flexibility", "Muscle Gain"])
        with col2:
            equipment_available = st.selectbox("Equipment Available", 
                                            ["None", "Home (basic)", "Gym (full equipment)"])
        
        if st.form_submit_button("Generate Workout Plan"):
            with st.spinner("Creating your personalized workout plan..."):
                try:
                    workout_plan = Fitness_advisor_Coach(
                        fitness_level=fitness_level,
                        equipment_available=equipment_available,
                        goal=goal
                    )
                    
                    st.subheader("Your Personalized Workout Plan")
                    st.markdown(workout_plan)
                    
                    # Generate PDF
                    try:
                        pdf_bytes = generate_pdf_from_text(workout_plan)
                        st.markdown(create_pdf_download_link(pdf_bytes, "workout_plan.pdf", "Download as PDF"), unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"PDF generation failed: {str(e)}")
                        st.markdown(create_download_link(workout_plan, "workout_plan.txt", "Download as Text"), unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error generating workout plan: {str(e)}")

elif app_mode == "👨‍⚕️ General Physician":
    st.header("👨‍⚕️ General Physician")
    st.markdown("Describe your symptoms for general health advice")
    
    with st.form("physician_form"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=1, max_value=120, value=30)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        with col2:
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
            height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0)
        
        symptoms = st.text_area("Describe your symptoms in detail")
        
        if st.form_submit_button("Get Medical Advice"):
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
                    st.markdown(advice)
                    st.markdown(create_download_link(advice, "medical_advice.txt", "Download Advice"), unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error processing your request: {str(e)}")

elif app_mode == "🧠 Mental Health":
    st.header("🧠 Mental Health Counselor")
    st.markdown("Share how you're feeling for personalized mental health advice")
    
    with st.form("mental_health_form"):
        mood_desc = st.text_area("How are you feeling today? Describe your mood and thoughts")
        
        col1, col2 = st.columns(2)
        with col1:
            sleep_quality = st.slider("Sleep Quality (1-10)", 1, 10, 5)
        with col2:
            stress_level = st.slider("Stress Level (1-10)", 1, 10, 5)
        
        if st.form_submit_button("Get Mental Health Advice"):
            with st.spinner("Analyzing your mental health..."):
                try:
                    advice = Mental_Health_counselor(
                        mood_desc=mood_desc,
                        sleep_quality=sleep_quality,
                        stress_level=stress_level
                    )
                    
                    st.subheader("Mental Health Assessment")
                    st.markdown(advice)
                    
                    # Generate PDF
                    try:
                        pdf_bytes = generate_pdf_from_text(advice)
                        st.markdown(create_pdf_download_link(pdf_bytes, "mental_health_advice.pdf", "Download as PDF"), unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"PDF generation failed: {str(e)}")
                        st.markdown(create_download_link(advice, "mental_health_advice.txt", "Download as Text"), unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error processing your request: {str(e)}")

elif app_mode == "💊 Pharmacist":
    st.header("💊 Pharmacist Specialist")
    st.markdown("Upload an image of your medicine for information about usage and side effects")
    
    pharma_image = st.file_uploader("Upload medicine image", type=["jpg", "jpeg", "png"])
    pharma_query = st.text_area("What would you like to know about this medicine?")
    
    if st.button("Get Medicine Information"):
        if pharma_image and pharma_query:
            with st.spinner("Analyzing the medicine..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                        tmp.write(pharma_image.read())
                        img_path = tmp.name
                    
                    encoded_img = encode_image_pharmacist(img_path)
                    response = Pharmacist_specialist(encoded_img, pharma_query)
                    
                    st.subheader("Medicine Information")
                    st.markdown(response)
                    st.markdown(create_download_link(response, "medicine_info.txt", "Download Information"), unsafe_allow_html=True)
                    
                    os.unlink(img_path)
                except Exception as e:
                    st.error(f"Error processing your request: {str(e)}")
        else:
            st.warning("Please upload an image of the medicine and ask your question")

elif app_mode == "📄 Medical Report Analysis":
    st.header("📄 Medical Report Analysis")
    st.markdown("Upload your medical report (PDF) and ask questions about it")
    
    report_file = st.file_uploader("Upload medical report (PDF)", type=["pdf"])
    report_query = st.text_area("What would you like to know about your report?")
    
    if st.button("Analyze Report"):
        if report_file and report_query:
            with st.spinner("Analyzing your medical report..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(report_file.read())
                        report_path = tmp.name
                    
                    vector_store, model = rag_pipeline(report_path, 'pdf')
                    analysis = query_medical_report(vector_store, model, report_query)
                    
                    st.subheader("Report Analysis")
                    st.markdown(analysis)
                    st.markdown(create_download_link(analysis, "report_analysis.txt", "Download Analysis"), unsafe_allow_html=True)
                    
                    os.unlink(report_path)
                except Exception as e:
                    st.error(f"Error processing your request: {str(e)}")
        else:
            st.warning("Please upload your medical report and ask your question")

# Add some spacing at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)
# 🏥 HealthHub AI - Multi-Specialist Healthcare Assistant

**HealthHub AI** is an advanced, multi-agent healthcare assistant powered by state-of-the-art language models and AI pipelines. It provides personalized support across various medical domains, allowing users to interact with specialized agents like Dental Experts, Dermatologists, Diet Planners, Fitness Coaches, Mental Health Counselors, General Physicians, Pharmacists, and Medical Report Analyzers — all in one place.

![HealthHub AI Screenshot](https://th.bing.com/th/id/OIP.-VH9JiaEYFtLCToj3rI8JgHaE7?cb=iwc2\&rs=1\&pid=ImgDetMain)

---

## 🔍 Features

* 🦷 **Dental Specialist**: Analyze dental queries and x-rays (image input supported).
* 🧴 **Dermatologist**: Provide skin care advice based on image and text queries.
* 🥗 **Diet & Nutrition Planner**: Generate a fully personalized diet plan based on user profile and fitness goals.
* 🏋️ **Fitness Advisor Coach**: Create custom fitness plans for beginners to advanced levels.
* 👨‍⚕️ **General Physician**: Basic health assessment using age, gender, symptoms, and vitals.
* 🧠 **Mental Health Counselor**: Get emotional well-being recommendations with downloadable therapy plans.
* 💊 **Pharmacist**: Ask medication-related queries or upload images of prescriptions.
* 📄 **Medical Report Analyzer**: Upload medical PDFs and query using RAG (Retrieval-Augmented Generation) pipeline.

---

## 🛠️ Tech Stack

* **Frontend**: Streamlit + Custom CSS
* **Backend**: Python modules for each agent
* **LLM Integration**: [Groq API](https://groq.com/), Gemini Pro (if enabled)
* **RAG Pipeline**: FAISS + LangChain + Custom PDF parsing
* **Image Processing**: `PIL`, `base64`, and `encode_image` functions for visual input
* **PDF Report Generation**: `FPDF` library for downloading diet, fitness, and therapy plans

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone [https://github.com/Warishayat/Healthcare-Multi-Specialist-AI-Assistant]
cd Healthcare-Multi-Specialist-AI-Assistant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Make sure your API keys (e.g., Groq, Gemini, etc.) are properly configured in an `.env` file or directly in your backend modules.

### 4. Run the Streamlit App

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```bash
healthhub-ai/
│
├── Backend/
│   ├── Dental_Module.py
│   ├── Dermotologist.py
│   ├── Diet_Neutration.py
│   ├── Fitness_advisor.py
│   ├── Genral_Physican.py
│   ├── Medical_Report_Analyzer.py
│   ├── pharmacist.py
│   └── M_Health_Counselor.py
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 📸 Screenshots

| Dashboard                                                                                     | Specialist Tabs                              |
| --------------------------------------------------------------------------------------------- | -------------------------------------------- |
| ![UI](https://th.bing.com/th/id/OIP.-VH9JiaEYFtLCToj3rI8JgHaE7?cb=iwc2\&rs=1\&pid=ImgDetMain) | ![Features](https://your-screenshot-url.png) |

---

## 📄 PDF Download Examples

* Personalized Diet Plan
* Strength Training Routine
* Mental Health Plan

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

```bash
# Fork the repo
# Create your feature branch
git checkout -b feature/YourFeature

# Commit changes
git commit -m "Add your feature"

# Push and PR
git push origin feature/YourFeature
```

---

## 📃 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Developed By

**Waris**
📧 Reach me out at: Warishayat666@gmail.com

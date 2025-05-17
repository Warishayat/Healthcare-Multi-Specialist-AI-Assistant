import os 
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage,SystemMessage
import markdown2
from xhtml2pdf import pisa
import warnings

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
warnings.filterwarnings('ignore')

def Fitness_advisor_Coach(fitness_level,equipment_available,goal):
    """
    Args:
        fitness_vele:str = beginner,intermediate or pro
        quipement_avialable : str = : None, Home, Gym
        goal : str = Weight Loss, Flexibility

    """
    system_prompt = """
        You are a Fitness Coach.

        Input parameters:
        - Fitness level: Beginner, Intermediate, Advanced
        - Equipment available: None, Home, Gym
        - Goal: Strength, Weight Loss, Flexibility

        Respond ONLY with this format:
        Response should be in markdown formate and detail.

        Weekly Workout Plan:
        Monday: <exercises>
        Tuesday: <exercises>
        Wednesday: <exercises>
        Thursday: <exercises>
        Friday: <exercises>
        saturday: <exercises>
        

        Provide simple, effective workout routines tailored to the inputs. Avoid unrelated topics.
    """

    user_message = f"""
        Fitness level: {fitness_level}
        Equipment available: {equipment_available}
        Goal: {goal}
    """

    Fitness_Advisor = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.6,
        api_key = GEMINI_API_KEY
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]

    response =  Fitness_Advisor.invoke(messages)
    return response.content

def Download_Fitness_advisor_plan(text, file_name="Fintess_advisor.pdf"):
    """
    This takes the markdown-formatted text and generates a downloadable PDF.

    Args:
        text (str): Markdown text from the Mental_Health_counselor.
        file_name (str): Output PDF file name (default = "Mental_Health_counselor.pdf").
    """
    html = markdown2.markdown(text)
    with open(file_name, "wb") as output_file:
        result = pisa.CreatePDF(html, dest=output_file)
    if result.err:
        print("Error: PDF generation failed.")
    else:
        print(f"PDF saved as: {file_name}")

#tets the system
if __name__ == "__main__":
    Fitness_advisor_response = Fitness_advisor_Coach(equipment_available="home",fitness_level="intermediate",goal="muscle-gain")
    print("Fintess_advisor:")
    print(Fitness_advisor_response)
    Download_Fitness_advisor_plan(text=Fitness_advisor_response)
import os
import warnings
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage,SystemMessage
import markdown2
from xhtml2pdf import pisa


load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
warnings.filterwarnings('ignore')

def Mental_Health_counselor(mood_desc: str, sleep_quality: int, stress_level: int):
    """
    Args:
        mood_desc: str - e.g. "Feeling anxious and unmotivated"
        sleep_quality: int - 1 to 10 scale
        stress_level: int - 1 to 10 scale
    """
    system_prompt = """
        You are a Mental Health Counselor.

        Input parameters:
        - Mood description (text)
        - Sleep quality (1-10)
        - Stress level (1-10)

        Respond ONLY with this format:
        Response should be in markdown formate and detail.
        Mental Health Assessment: "<brief assessment>"
        Recommendations:
        - <recommendation 1 With breidt detail of do and donts>
        - <recommendation 2 With breidt detail of do and donts>
        - <recommendation 3 With breidt detail of do and donts>
         - <recommendation 4 With breidt detail of do and donts>
        - <recommendation 5 With breidt detail of do and donts>
        - <recommendation 6 With breidt detail of do and donts>
        Provide clear, empathetic, and concise mental health advice based on the inputs. Do not discuss unrelated topics.
    """

    user_messsage = f"""
    Mood description: "{mood_desc}"
    Sleep quality (1-10): {sleep_quality}
    Stress level (1-10): {stress_level}
    """

    health_counselor = ChatGroq(
        model="gemma2-9b-it",
        temperature=0.6,
        streaming=True,
        verbose=True,
        api_key=GROQ_API_KEY
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_messsage),
    ]

    response = health_counselor.invoke(messages)
    return response.content


def Download_Mental_plan(text, file_name="Mental_Health_counselor.pdf"):
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


#test the system
if __name__ == "__main__":
    try:
        Mental_suggestion=Neutration_plan=Mental_Health_counselor(mood_desc="i am feleing not well and think nothing get better",sleep_quality=7,stress_level=6)
        print("Mental Health Cousnelor:")
        print(Mental_suggestion)
        Download_Mental_plan(text=Mental_suggestion)
    except Exception as e:
        print(f"you haev some problem at: {e}")

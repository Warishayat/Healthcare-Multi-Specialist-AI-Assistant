from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
import markdown2
from xhtml2pdf import pisa
import warnings


load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
warnings.filterwarnings('ignore')

def Diet_Neutration_planner(age,weight,height,activity_level,goal,dietary_restrictions):
    """
    You are a general physician planner who helps people create personalized diet plans.

    Args:
        age (int): Age of the person
        weight (float): Weight in kilograms
        height (float): Height in centimeters
        activity_level (str): Beginner, intermediate, or pro
        goal (str): Weight loss or muscle gain
        dietary_restrictions (str): Vegan, gluten-free, diabetic, etc.
    """

    system_prompt = """
    You are a diet and nutrition planner AI. Provide a detailed, clear 7-day meal plan.

    Response format:
    Response should be in the markdown formate.
    Calorie Target: "xxxx kcal/day"
    7-Day Meal Plan: List meals per day with estimated calories (breakfast, lunch, dinner, snacks)
    Grocery List: List all ingredients needed for the 7 days

    Make the meal plan tailored to the input parameters and dietary restrictions.
    """

    user_message = (
        f"Patient details:\n"
        f"- Age: {age}\n"
        f"- Weight: {weight} kg\n"
        f"- Height: {height} cm\n"
        f"- Activity Level: {activity_level}\n"
        f"- Goal: {goal}\n"
        f"- Dietary Restrictions: {dietary_restrictions}\n\n"
        "Please create a detailed 7-day meal plan with calorie targets and grocery list."
    )

    Neutration_planner = ChatGroq(
        model="gemma2-9b-it",
        temperature=0.6,
        streaming=True,
        verbose=True
        )
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message),
    ]
    response = Neutration_planner.invoke(messages)
    return response.content

def Download_Diet_plan(text, file_name="Dietplan.pdf"):
    """
    This takes the markdown-formatted text and generates a downloadable PDF.

    Args:
        text (str): Markdown text from the diet_nutrition_planner.
        file_name (str): Output PDF file name (default = "Dietplan.pdf").
    """
    html = markdown2.markdown(text)
    with open(file_name, "wb") as output_file:
        result = pisa.CreatePDF(html, dest=output_file)
    if result.err:
        print("Error: PDF generation failed.")
    else:
        print(f"PDF saved as: {file_name}")


if __name__ == "__main__":
    try:
        Diet_plan=Neutration_plan=Diet_Neutration_planner(28, 70, 175, "intermediate", "muscle gain", "gluten-free")
        print("Diet_neutration_plan:")
        print(Diet_plan)
        Download_Diet_plan(text=Diet_plan)
    except Exception as e:
        print(f"you haev some problem at: {e}")

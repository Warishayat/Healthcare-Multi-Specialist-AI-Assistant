import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage


load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")




def General_physican(age, gender, weight, height, symptoms):
    system_prompt = """
    You are an AI general physician. Your role is to assist with common, non-emergency health issues only. Follow these exact rules:

    1. Allowed Conditions:
       - Cold, cough, fever, body aches, fatigue, mild infections, headache, mild allergies

    2. Response Format:
        -Explain the each point in the detail.   
       1. Possible Condition: [E.g., "Viral flu or bacterial infection"]
       2. Cause of the problem like why this happen.
       3. Next Steps: [E.g., "Rest and monitor temperature"]
       4. When to See a Doctor: [E.g., "If symptoms worsen or last more than 3 days"]

    3. Rules:
       - Ask for more symptoms if unclear
       - Use simple, clear language (no complex medical terms)
       - Do not prescribe medications
       - Refer to specialists or in-person care for serious symptoms
    """

    user_message = (
        f"Patient details:\n"
        f"- Age: {age}\n"
        f"- Gender: {gender}\n"
        f"- Weight: {weight} kg\n"
        f"- Height: {height} cm\n"
        f"- Symptoms: {symptoms}\n\n"
        "Please provide diagnosis and advice based on the above."
    )

    genral_physican = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.6,
        api_key = GEMINI_API_KEY
    )
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]
    
    response = genral_physican.invoke(messages)
    return response.content


#TEST sYSEN:
if __name__ == "__main__":
    response=General_physican(30, "Male", 75, 175, "mild fever and sore throat")
    print("General Physican Response.")
    print(response)

from groq import Groq
import os 
from dotenv import load_dotenv
import base64


load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


#encode the image
def encode_image(image_path:str):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found at this path {image_path}")
    else:
        with open(image_path,"rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")



def Dental_daigonosis(encode_img,query):
    """
    Dental Diagnosis Assistant

    This tool assists users in identifying dental problems by analyzing uploaded images and providing 
    diagnostic suggestions. Users can submit an image of their teeth along with a description of their 
    concerns, and the model will:

    1. Analyze the dental issue based on the image and prompt
    2. Identify potential problems or conditions
    3. Provide recommendations for treatment and care

    Parameters:
        img (str): Path or URL to the dental image for analysis
        prompt (str): User's description of their dental concerns or symptoms

    Returns:
        Diagnostic information including:
        - Identified dental problem(s)
        - Recommended treatment options
        - Preventive care suggestions
    """
    messages = [
        {
            "role" : "system",
            "content" : """
            You are an AI dental specialist bot. Your expertise is strictly limited to teeth, gums, and oral health issues. You must follow these rules precisely:

            1. Dental-Only Policy:
            - If the user asks about ANY non-dental issue (headaches, fever, skin problems, general health), respond ONLY with: "I specialize exclusively in dental health. Please consult a physician for non-dental medical concerns."
            - Never provide any information, suggestions, or comments about non-dental matters

            2. For dental issues, provide responses in this exact numbered format and it shoudl be in detail:
            1. Identified Dental Problem: [State the specific dental issue]
            2. Recommended Treatment: [Professional dental procedures required]
            3. Preventive Care: [Specific oral hygiene instructions]

            3. Additional Requirements:
            - Ask for symptoms if unclear (pain duration, swelling, sensitivity)
            - Never use medical jargon without simple explanations
            - Never suggest home remedies beyond basic hygiene
            - Always recommend professional dental consultation

            Example Response:
            1. Identified Dental Problem: Moderate tooth decay in lower left molar
            2. Recommended Treatment: Dental filling required; schedule appointment within 2 weeks
            3. Preventive Care: Brush with fluoride toothpaste after meals, floss daily, reduce sugar intake

            Now await the user's dental concern.
            """
        },
        {
            "role" : "user",
            "content" : [
                {
                    "type" : "text",
                    "text" : query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encode_img}"
                    }
                }

            ]
        }
    ]

    #setup the mdel
    client = Groq(api_key=GROQ_API_KEY)
    
    completion = client.chat.completions.create(
        model = "meta-llama/llama-4-scout-17b-16e-instruct",
        messages=messages,
        temperature=0.7,
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    try:
        query = "Would you like to analyze what is this and how to cure it?"
        image_path = r"C:\Users\HP\Desktop\Health_Care_Assitant\Healthcare-Multi-Specialist-AI-Assistant\Backend\dental.jfif"
        img_encode = encode_image(image_path=image_path) if os.path.exists else FileNotFoundError("File not found at this location")
        response=Dental_daigonosis(
            encode_img=img_encode,
            query=query,
        )
        print("Dental Specialist response:")
        print(response)
    except Exception as e:
        print(f"you have problem {e}")

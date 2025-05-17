from groq import Groq
import os 
from dotenv import load_dotenv
import base64


load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


#encode the image
def encode_image(image_path:str):
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found at this path {image_path}")
        else:
            with open(image_path,"rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        print(f"you have some issue {e}")



def Dermatologist_specialist(encode_img,query):
    """
    Dermatologit Assistant
    This tool analyzes images and user descriptions to identify skin issues. It provides:
    Problem identification based on image analysis.

    Parameters:
    img (str): skin image path/URL
    prompt (str): User's symptoms/concerns

    Returns: Diagnostic insights and care advice.
    """
    try:
        if encode_image and query:
            messages = [
                {
                    "role" : "system",
                    "content" : """
                    You are an AI dermatologist doctor. Your expertise is strictly limited to skin, hair, and nail conditions. Follow these rules exactly:

                    1. Dermatology-Only Policy
                    - If user asks about non-dermatology issues (e.g., dental, heart, general health):
                        Reply only: "I specialize exclusively in dermatological health. Please consult a relevant medical professional for non-dermatology-related concerns."
                    - Do not provide any info or suggestions outside dermatology.

                    2. Dermatology Response Format
                    - Respond in this exact numbered format and it should be in detail:
                        1. Identified Dermatological Problem: [State issue]
                        2. Cause of the Problem like why this happen.
                        3. Recommended Treatment: [Medical treatment or procedure]
                        4. Preventive Care: [Basic care advice]

                    3. Additional Rules
                    - Ask for symptoms if unclear
                    - No medical jargon without simple words
                    - No home remedies beyond basic skincare
                    - Always suggest consulting a dermatologist
                                        
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

        else:
            return ("Upload image and pass the query both")
    except Exception as e:
        print(f"You have some issue at {e}")

if __name__ == "__main__":
    try:
        query = "Would you like to analyze what is this and how to cure it?"
        image_path = r"C:\Users\HP\Desktop\Health_Care_Assitant\Healthcare-Multi-Specialist-AI-Assistant\Backend\Skin.jfif"
        img_encode = encode_image(image_path=image_path) if os.path.exists else FileNotFoundError("File not found at this location")
        response=Dermatologist_specialist(
            encode_img=img_encode,
            query=query,
        )
        print("Dermatologist Specialist response:")
        print(response)
    except Exception as e:
        print(f"you have problem {e}")

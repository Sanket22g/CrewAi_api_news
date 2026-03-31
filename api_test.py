from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize the client
client = genai.Client()

def chat():
    """Interactive chat with Gemini"""
    print("🤖 Gemini Chat (type 'exit' to quit)")
    print("-" * 50)
    
    # Start a chat session with the model
    chat_session = client.chats.create(
        model="gemini-2.5-flash",
    )
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        try:
            # Send message and get response
            response = chat_session.send_message(user_input)
            assistant_message = response.text
            
            print(f"\n🤖 Gemini: {assistant_message}")
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                print("⚠️  API Quota exceeded. Please check your billing settings.")
            elif "404" in error_msg:
                print("⚠️  Model not found. Check available models.")
            else:
                print(f"❌ Error: {error_msg[:150]}")

if __name__ == "__main__":
    chat()

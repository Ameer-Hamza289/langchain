from dotenv import load_dotenv
from google.cloud import firestore
from google.oauth2 import service_account
from langchain_google_firestore import FirestoreChatMessageHistory
from langchain_openai import ChatOpenAI

"""
Steps to replicate this example:
1. Create a Firebase account
2. Create a new Firebase project and FireStore Database
3. Retrieve the Project ID
4. Install the Google Cloud CLI on your computer
    - https://cloud.google.com/sdk/docs/install
    - Authenticate the Google Cloud CLI with your Google account
        - https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev
    - Set your default project to the new Firebase project you created
5. pip install langchain-google-firestore
6. Enable the Firestore API in the Google Cloud Console:
    - https://console.cloud.google.com/apis/enableflow?apiid=firestore.googleapis.com&project=crewai-automation
"""

load_dotenv()

# Setup Firebase Firestore
PROJECT_ID = "langchain-a16d2"
SESSION_ID = "user_session_new"
COLLECTION_NAME = "chat_history"

print("🔧 Initializing Firestore Client...")

# Load credentials from service account
google_credentials = service_account.Credentials.from_service_account_file("firebase.json")

# Initialize Firestore client
client = firestore.Client(project=PROJECT_ID, credentials=google_credentials)

# Initialize Firestore chat message history
print("📚 Initializing Firestore Chat Message History...")
chat_history = FirestoreChatMessageHistory(
    session_id=SESSION_ID,
    collection=COLLECTION_NAME,
    client=client,
)
print("✅ Chat History Initialized.")

# Initialize Chat Model
model = ChatOpenAI()

print("💬 Start chatting with the AI. Type 'exit' to quit.\n")

# Chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("\n👋 Exiting chat...")
        break

    chat_history.add_user_message(user_input)

    ai_response = model.invoke(chat_history.messages)
    chat_history.add_ai_message(ai_response.content)

    print(f"AI: {ai_response.content}")

# Print full chat history
print("\n📜 Full Chat History:")
for message in chat_history.messages:
    print(f"{message.type.capitalize()}: {message.content}")

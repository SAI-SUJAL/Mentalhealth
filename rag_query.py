import pandas as pd
import uuid
from huggingface_hub import InferenceClient
from langchain.memory import ConversationBufferMemory
import streamlit as st

# Hugging Face Client Setup
HF_TOKEN = "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"
client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.3", token=HF_TOKEN)

# Memory Buffer for Conversation
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Load Dataset
dataset = pd.read_csv("C:/Users/91998/Desktop/mentalhealth/dataset.csv")

# Empathetic response for greetings


mental_health_keywords = [
    # General Mental Health Terms
    "mental health", "anxiety", "depression", "stress", "panic", "burnout", 
    "trauma", "grief", "sadness", "loneliness", "mood swings", "fear", 
    "negative thoughts", "anger", "emotional distress", "mindfulness", 
    "hopelessness", "overwhelmed", "worthlessness", "helplessness", 
    "self-harm", "suicide", "kill myself", "jump from building", "cut myself",
    "hang myself", "end my life", "take pills", "overdose", 
    "no reason to live", "life is meaningless", "nobody loves me", "mom call",
    "nobody needs me", "i'm invisible", "why am i alive", "beat ", "beat me","hit",
    "nervous breakdown", "crying every day", "giving up", "empty inside","child abuse",

    # Disorders and Conditions
    "PTSD", "post-traumatic stress disorder", "bipolar", "schizophrenia", 
    "OCD", "obsessive-compulsive disorder", "eating disorder", "anorexia", 
    "bulimia", "panic attacks", "social anxiety", "generalized anxiety disorder", 
    "clinical depression", "major depressive disorder", "manic depression", 
    "dissociation", "ADHD", "autism", "personality disorder", "fat","thin","insecure",
    "bodyshape","mood swings",
    "borderline personality disorder", "psychosis", "hallucinations",

    # Abuse and Trauma
    "harassment", "threatened", "abuse", "emotional abuse", "physical abuse", 
    "sexual abuse", "domestic violence", "beaten", "yelled at", "threatened my life", 
    "abandoned", "neglected", "violence at home", "childhood trauma", 
    "parental abuse", "family issues", "toxic family", "toxic parents", 
    "abusive parents", "parental neglect", "family fights", "family arguments", 
    "beaten by parents", "hit by mom", "hit by dad", "mom yells at me", 
    "dad yells at me", "parents hate me", "parents don't understand", 
    "abused by family", "siblings abuse", "violent home", "forced marriage", 
    "cultural pressure", "pressure from parents", "strict parents", 
    "emotional manipulation", "gaslighting by parents", "verbal abuse by family", 
    "unrealistic expectations", "family rejection", "feeling unloved at home","confidence",

    # Self-Care and Counseling Terms
    "therapy", "counseling", "cognitive behavioral therapy", "CBT", 
    "mental health resources", "psychotherapy", "psychological support", 
    "counselor", "therapist", "psychologist", "psychiatrist", "wellness", 
    "self-care", "healing", "mind-body connection", "stress relief", 
    "relaxation techniques", "coping mechanisms", "emotional resilience", 
    "mental strength", "support groups", "grief counseling","self-esteem","mom hitting","child abuse","sexual",
    "harrasing","molesting","perverted","die","feel","like",

    # Situational Contexts
    "relationship issues", "friendship problems", "family problems", "toxicity",
    "divorce", "breakup", "cheating", "loss of a loved one", 
    "workplace stress", "job loss", "financial stress", 
    "academic pressure", "exam stress", "failure", "rejection", 
    "peer pressure", "loneliness", "betrayal", "addiction", 
    "alcohol abuse", "drug abuse", "smoking", "substance abuse", 
    "gambling addiction", "internet addiction", "porn addiction","sexual","harrased","molesting","creepy"

    # Feelings and Emotions
    "sad", "happy", "worried", "relieved", "stressed", "calm", 
    "hopeful", "frustrated", "angry", "anxious", "excited", 
    "guilty", "ashamed", "confused", "lost", "isolated", "scared",
    "broken", "defeated", "disheartened", "trapped", "ashamed", 
    "disconnected", "rejected", "hurt", "betrayed", "insecure", 
    "apathetic", "vulnerable", "misunderstood"
]
emotional_expressions = [
        "i feel", "i am feeling", "i am", "i feel so", "i have been feeling", 
        "i want", "i've decided", "i feel like giving up", "i am going through", 
        "i think about", "i can't handle", "i don't want to", "i wish i could", 
        "i feel hopeless", "i feel worthless", "i feel like a burden", 
        "i feel overwhelmed", "i feel trapped", "i feel empty", 
        "i don't see a way out", "i feel unloved", "i can't take it anymore", 
        "i'm scared", "i'm anxious", "i'm stressed", "i can't sleep", 
        "i feel broken", "i can't do this", "i feel abandoned", 
        "i can't stop thinking about", "i feel ashamed", "i feel guilty", 
        "i feel useless", "i feel lost", "i don't belong", "i feel hated", 
        "nobody cares about me", "i feel helpless", "i feel like dying",
        "nobody listens to me", "nobody understands me", "i feel defeated",
        "i feel like crying all the time", "i can't stop crying", "i feel anxious all day",
        "why does nobody care", "why does this happen to me", 
        "i feel stuck", "i am losing control", "i feel like ending it all", 
        "why am i like this", "i don't know what to do anymore"
    ]
def query_dataset(user_query):
    relevant_data = dataset[dataset['Context'].str.contains(user_query, case=False, na=False)]
    if not relevant_data.empty:
        return relevant_data.iloc[0]['LLM']
    return None

def rag_query_with_keywords(query):
  
    # First, check the dataset for relevant responses
    dataset_response = query_dataset(query)
    if dataset_response:
        return dataset_response

    # Convert query to lowercase to check against keywords
    query_lower = query.lower()

    # Check if the query matches any mental health-related keywords
    matched_keywords = [keyword for keyword in mental_health_keywords if keyword in query_lower]

    # Check if the query contains emotional distress-related expressions
    matched_emotions = [phrase for phrase in emotional_expressions if phrase in query_lower]

    # If the query matches mental health keywords or emotional distress phrases, generate an empathetic response
    if matched_keywords or matched_emotions:
        empathetic_prompt = (
             "You are a compassionate mental health assistant, and a user is going through a tough time. "
             "Reply -Please ask questions related to mental health only. I'm here to help with mental health concerns to If the query is not related to mental health or is just one word irrelevant query."
            "The user may be feeling betrayed, confused, or hurt, and needs understanding and emotional support. "
            "Offer an empathetic and understanding response. Avoid clinical or diagnostic language. "
            "Encourage the user to take care of themselves and seek appropriate help if needed. "
            "Emphasize healing, self-care, and that it’s okay to feel upset and ask for help. Be specific in your response, "
            "acknowledge the emotions, and suggest ways to cope or seek support.Don't every say you are unable to address the issue, understand the query and answer accordingly \n\n"
            "User query: {query}"
        )
        
        # Format the prompt with the user's query
        prompt = empathetic_prompt.format(query=query)
        messages = [{"role": "user", "content": prompt}]
        
        # Call the LLM to get an empathetic response
        response_content = client.chat_completion(messages=messages, max_tokens=2000, stream=False)
        response = response_content.choices[0].message.content.strip()

        # Add the response to conversation memory
        memory.chat_memory.add_ai_message(response)
        return response

    # If the query doesn't match any mental health-related criteria, prompt for relevant query
    return "Please ask questions related to mental health only. I'm here to help with mental health concerns."

def rag_query_with_prompt(query):
    # First, check the dataset for relevant responses
    dataset_response = query_dataset(query)
    if dataset_response:
        return dataset_response

    # Define an empathetic prompt with additional instructions for non-mental health queries
    empathetic_prompt = (
        "You are a supportive mental health assistant, dedicated to providing emotional comfort and understanding during difficult moments. "
        "It's important to respond with empathy, encouragement, and positivity. "
        "Reply -Please ask questions related to mental health only. I'm here to help with mental health concerns to If the query is not related to mental health or is just one word irrelevant query."
        "Your goal is to uplift the user, acknowledging their feelings without judgment, and helping them navigate through this challenging experience. "
        "You should give clinical advice and also focus on emotional healing, encouraging the user to focus on their strengths and the opportunities ahead. "
        "Remind them that healing takes time, and it's okay to lean on others for support. Emphasize self-care, self-love, and remind them that they deserve happiness. "
        "If the user expresses feelings of hopelessness or low self-worth, reassure them that these feelings are temporary and that they are valuable and capable of overcoming challenges. \n\n"
        "If the user's query is not related to mental health or emotional well-being, kindly let them know strictly that ""I am a mental health chatbot. Please ask questions related to mental health, such as coping with stress, anxiety, or sadness."
        "For example, the user might want to talk about coping with stress, anxiety, or sadness. Please gently guide the user back to mental health topics if their question diverges.Don't every say you are unable to address the issue, understand the query and answer accordingly \n\n"
        "User query: {query}"
    )

    # Format the prompt with the user's query
    prompt = empathetic_prompt.format(query=query)

    # Generate the response from the LLM
    messages = [{"role": "user", "content": prompt}]
    response_content = client.chat_completion(messages=messages, max_tokens=150, stream=False)
    response = response_content.choices[0].message.content.strip()

    # If the response indicates that it's not related to mental health, suggest related topics
    if "I am a mental health chatbot" in response.lower():
        return "I am a mental health chatbot. Please ask questions related to mental health, such as coping with stress, anxiety, or sadness."

    return response
def rag_query(query):
    
    keyword_response = rag_query_with_keywords(query)
    
    if keyword_response:
        return keyword_response

    # If no response from the keyword-based query, fall back to the prompt-based query
    return rag_query_with_prompt(query)
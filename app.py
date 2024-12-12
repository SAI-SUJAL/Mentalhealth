import streamlit as st
from rag_query import rag_query  # Import the rag_query function from rag_query.py

# Set page config
st.set_page_config(page_title="Mental Health Chatbot", page_icon="🤖", layout="wide")
st.title("Mental Health Chatbot")
st.subheader("Ask me something related to mental health:")

# Initialize session state for storing chat history if not already initialized
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'not_satisfied' not in st.session_state:
    st.session_state['not_satisfied'] = False

# Function to display conversation in the main chat area
def display_conversation():
    for message in st.session_state['messages']:
        if message['role'] == 'user':
            st.chat_message("user").markdown(message['content'])
        else:
            st.chat_message("assistant").markdown(message['content'])

# Handle user input
if prompt := st.chat_input("What is your question?"):
    # Display user message in the chat message container
    st.session_state['messages'].append({"role": "user", "content": prompt})

    # Get the assistant's response from rag_query
    response = rag_query(prompt)

    # Ensure the response is not empty or None
    if response:
        # Display assistant response in chat message container
        st.session_state['messages'].append({"role": "assistant", "content": response})
    else:
        st.session_state['messages'].append({"role": "assistant", "content": "Sorry, I couldn't provide a response."})

    # Display the updated conversation after the new message
    display_conversation()

# Sidebar for additional controls (Clear chat history and Not Satisfied button)
with st.sidebar:
    st.header("Options")

    # Handle "Not Satisfied" Button
    if st.button("Not Satisfied"):
        # Set the flag to trigger response regeneration
        st.session_state['not_satisfied'] = True

    # Clear Chat History button
    if st.button("Clear Chat History"):
        st.session_state['messages'] = []  # Clear the conversation history
        st.session_state['not_satisfied'] = False  # Reset the not_satisfied flag
        # No rerun needed, simply update the UI with the cleared state
        st.rerun()  # Force a re-run of the app to reset the state
  # Reset the state by forcing a re-run (this is okay to use here for a full reset)

# Process "Not Satisfied" logic if set to True
if st.session_state['not_satisfied']:
    if st.session_state['messages']:
        last_user_message = st.session_state['messages'][-1]['content']
        new_response = rag_query(last_user_message)
        if new_response:
            # Remove the last assistant message to replace with the new response
            st.session_state['messages'][-1] = {"role": "assistant", "content": new_response}
        else:
            # Add a fallback if no new response
            st.session_state['messages'][-1] = {"role": "assistant", "content": "Sorry, I couldn't provide a response."}

    # Reset the "Not Satisfied" flag to avoid redundant updates
    st.session_state['not_satisfied'] = False

    # Display the updated conversation with the new response
    display_conversation()
# Process "Not Satisfied" logic if set to True
# if st.session_state['not_satisfied']:
#     if st.session_state['messages']:
#         last_user_message = st.session_state['messages'][-1]['content']

#         # Adjust the prompt to be even more direct and empathetic
#         strict_support_prompt = (
#             "The user is not satisfied with the previous response and needs a more empathetic, "
#             "personalized answer. You should connect deeply with the user's emotions and offer a response "
#             "that addresses their specific concerns, providing actionable and compassionate advice. Avoid generic answers. "
#             "You should acknowledge their feelings, show understanding, and offer the best possible guidance to help them. \n\n"
#             "User query: {query}"
#         )

#         # Format the prompt with the user's query
#         formatted_prompt = strict_support_prompt.format(query=last_user_message)

#         # Generate a more strict and supportive response
#         response = generator(formatted_prompt, max_length=150, num_return_sequences=1)

#         # Replace the last assistant message with the new strict and supportive response
#         if response:
#             st.session_state['messages'][-1] = {"role": "assistant", "content": response[0]['generated_text'].strip()}
#         else:
#             # Fallback if no new response
#             st.session_state['messages'][-1] = {"role": "assistant", "content": "I understand your concerns, and I want to help. Let's address this together."}

#     # Reset the "Not Satisfied" flag to avoid redundant updates
#     st.session_state['not_satisfied'] = False

#     # Display the updated conversation with the new response
#     display_conversation()
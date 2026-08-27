import streamlit as st
from groq import Groq
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from duckduckgo_search import DDGS

# Sidebar for API Keys
st.sidebar.title("API Keys & Configurations")
astra_app_token = st.sidebar.text_input("Astra DB Application Token", type="password")
astra_client_id = st.sidebar.text_input("Astra DB Client ID", type="password")
astra_client_secret = st.sidebar.text_input("Astra DB Client Secret", type="password")
groq_api_key = st.sidebar.text_input("Groq API Key", type="password")

# Initialize Groq client
groq_client = Groq(api_key=groq_api_key)

# Title and Description
st.title("AI-Powered Recipe Generator with Web Search")
st.write("Upload a file, enter a query, or perform a web search to generate personalized recipes.")

# File Input
uploaded_file = st.file_uploader("Upload a file (optional)", type=["txt", "csv"])
file_content = ""
if uploaded_file:
    file_content = uploaded_file.read().decode("utf-8")
    st.write("File content:")
    st.write(file_content)

# Text Input
user_query = st.text_input("Enter your recipe query (e.g., 'How to prepare chicken biryani')")

# DuckDuckGo Search Functionality
def perform_duckduckgo_search(query):
    """Perform a DuckDuckGo search and return the results."""
    ddgs = DDGS()
    results = ddgs.text(query, max_results=5)  # Fetch top 5 results
    return results

# Connect to Astra DB
def connect_to_astra():
    auth_provider = PlainTextAuthProvider(astra_client_id, astra_client_secret)
    cluster = Cluster(["your_astra_db_endpoint"], auth_provider=auth_provider)
    session = cluster.connect()
    return session

# Fetch recipes from Astra DB
def fetch_recipes_from_db(session, query):
    session.set_keyspace("your_keyspace")
    rows = session.execute(f"SELECT * FROM recipes WHERE query='{query}'")
    return rows

# Generate recipe using Groq API
def generate_recipe_groq(prompt):
    response = groq_client.chat.completions.create(
        model="llama3-70b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates recipes."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=500,
    )
    return response["choices"][0]["message"]["content"]

# Process user input and generate recipe
if user_query or uploaded_file:
    context = file_content if uploaded_file else ""
    
    # Perform DuckDuckGo Search if enabled
    if st.checkbox("Include Web Search"):
        search_results = perform_duckduckgo_search(user_query)
        search_context = "\n".join([f"{result['title']}: {result['href']}" for result in search_results])
        context += f"\n\nWeb Search Results:\n{search_context}"
    
    # Create the prompt
    prompt_text = f"Generate a detailed recipe for: {user_query}\n\nContext:\n{context}"
    
    # Generate recipe using Groq API
    recipe_output = generate_recipe_groq(prompt_text)
    
    # Display the generated recipe
    st.subheader("Generated Recipe")
    st.write(recipe_output)

    # Save to Astra DB (optional)
    if astra_app_token and astra_client_id and astra_client_secret:
        session = connect_to_astra()
        session.execute(
            f"INSERT INTO recipes (query, recipe) VALUES ('{user_query}', '{recipe_output}')"
        )

# Recipe Generator Application

This project is an AI-powered **Recipe Generator** that takes user inputs (text or files) and generates detailed recipes. It integrates with **Groq API**, **Astra DB**, and **DuckDuckGo Search** to provide dynamic, personalized results.

## Features
- **Chat Input**: Enter recipe-related queries.
- **File Input**: Upload recipe-related files for context.
- **Web Search**: Fetch supplementary data using DuckDuckGo.
- **Groq AI Integration**: Generate recipes dynamically.
- **Astra DB**: Store and retrieve recipes.

## Workflow
1. User inputs query or uploads a file.
2. Context is enriched with DuckDuckGo search results.
3. Groq API generates the recipe based on the input and context.
4. Results are displayed and optionally stored in Astra DB.


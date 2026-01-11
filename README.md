  Project: AI-Powered Customer Support Automation System

  Overview:
  A modular and scalable AI chatbot system designed to provide automated, knowledge-based customer support for
  small businesses. The system uses a Retrieval-Augmented Generation (RAG) pipeline to deliver accurate answers
  grounded in the company's specific knowledge base, ensuring it never provides fabricated information.

  Key Features:

   * Multi-Channel Support: Designed for both website chatbots (via a REST API) and WhatsApp, using a single,
     unified backend to ensure a consistent user experience.
   * Grounded AI Responses: Employs a RAG pipeline that forces the AI to answer questions using only information
     from a dedicated knowledge base (e.g., FAQs, product manuals). If information is not available, the system is
     designed to politely say "I don't know."
   * Intelligent Human Escalation: Automatically detects user requests to speak with a person (e.g., "I want to
     talk to an agent"). It then stops the AI, marks the conversation for handoff, and sends an automated
     notification.
   * Automated Agent Notification: Upon escalation, the system instantly notifies human support staff via email,
     providing them with the session details to ensure a seamless transition.
   * Persistent Conversation Logging: Every interaction, including user messages, AI responses, and escalation
     events, is logged to a SQLite database for analytics, quality assurance, and auditing purposes.
     
      Technical Architecture:

   * Backend: FastAPI (Python) for creating a high-performance, asynchronous API.
   * AI/RAG Pipeline: LangChain to orchestrate the pipeline, from document loading and chunking to response
     generation.
   * Vector Database: FAISS for efficient, in-memory similarity searches to find the most relevant context for user
     queries.
   * Embeddings: Hugging Face Sentence Transformers to convert knowledge base text into semantic vector embeddings.
   * Database: SQLAlchemy ORM with SQLite for structured logging of conversation data.
   * Configuration: A clean, environment-variable-driven setup using Pydantic for robust and secure configuration
     management.


     
  How to Run the System

   1. Install Dependencies:
   1     pip install -r customer-support-ai/requirements.txt

   2. Configure Environment:
      Open customer-support-ai/.env and fill in the required values:
       * LLM_API_KEY: Your API key for the language model (e.g., OpenAI).
       * SMTP_...: Your SMTP server details for sending escalation emails.

   3. Ingest Knowledge:
      Run the ingestion script to process your documents and build the vector store.
   1     python3 customer-support-ai/run_ingestion.py

   4. Start the Server:
   1     python3 customer-support-ai/main.py
      The server will be accessible at http://127.0.0.1:8001.

   5. Test the API:
      You can use the interactive API documentation at http://127.0.0.1:8001/docs to send requests to the
  /api/v1/chat/web endpoint.




https://github.com/user-attachments/assets/eb67b0b0-9903-44d4-a5d5-08dee0c38676



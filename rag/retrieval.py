
import logging
from operator import itemgetter

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.messages import get_buffer_string
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import ChatOpenAI

from core.config import settings
from rag.prompts import RAG_USER_PROMPT_TEMPLATE, RAG_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class RAGChain:
    """
    A class to encapsulate the RAG chain logic.
    """

    def __init__(self):
        self.vector_store = self._load_vector_store()
        self.retriever = self._get_retriever()
        self.llm = self._get_llm()
        self.chain = self._create_chain()

    def _load_vector_store(self):
        """
        Load the FAISS vector store from the specified path.
        """
        logger.info(f"Loading vector store from {settings.VECTOR_STORE_DIR}")
        embedding_function = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)
        return FAISS.load_local(
            settings.VECTOR_STORE_DIR,
            embedding_function,
            allow_dangerous_deserialization=True,  # This is required for FAISS
        )

    def _get_retriever(self):
        """
        Get the retriever from the vector store.
        """
        return self.vector_store.as_retriever()

    def _get_llm(self):
        """
        Get the language model.
        
        NOTE: This is a placeholder. You can replace ChatOpenAI with any other
        LangChain-compatible chat model.
        """
        return ChatOpenAI(api_key=settings.LLM_API_KEY, model="gpt-3.5-turbo")

    def _create_chain(self):
        """
        Create the RAG chain.
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", RAG_SYSTEM_PROMPT),
                ("user", RAG_USER_PROMPT_TEMPLATE),
            ]
        )

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain_from_docs = (
            RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
            | prompt
            | self.llm
            | StrOutputParser()
        )

        rag_chain_with_source = RunnableParallel(
            {"context": self.retriever, "question": RunnablePassthrough()}
        ).assign(answer=rag_chain_from_docs)

        return rag_chain_with_source

    def invoke(self, question: str):
        """
        Invoke the RAG chain with a user query.
        """
        return self.chain.invoke(question)

# Example usage
if __name__ == "__main__":
    rag_chain = RAGChain()
    
    # Test with a question
    question = "What are your business hours?"
    response = rag_chain.invoke(question)
    
    print("Question:", question)
    print("Answer:", response.get("answer"))
    print("Source Documents:", response.get("context"))

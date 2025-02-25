import traceback
from llm import ModelService
from utils.pdf_processor import load_pdf
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser  # Updated import
from langchain.schema.runnable import RunnablePassthrough  # Updated from langchain.runnables
import os

class ChatService:
    def __init__(self, pdf_path: str):
        """
        Initializes by loading a PDF, splitting it into chunks, and setting up retrieval.

        Args:
            pdf_path (str): Path to the PDF file.

        Raises:
            Exception: If LLM or embeddings are missing, or if an error occurs.
        """
        self.service = ModelService()
        self.llm = self.service.get_llm_model()
        self.embeddings = self.service.get_embedding_model()
        self.store_directory = "./vector_store"

        if not self.llm:
            raise Exception('LLM not found')
        if not self.embeddings:
            raise Exception('Embedding model not initialized')

        # Ensure the storage directory exists
        os.makedirs(self.store_directory, exist_ok=True)

        # Try to load existing vector store; if loading fails, create a new one.
        try:
            self.vectorstore = self._load_vectorstore()
        except Exception as e:
            print(f"Error loading existing vector store: {e}")
            self.vectorstore = self._create_new_vectorstore(pdf_path)

        # Set up retriever with search parameters
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )

        # Define prompt template
        template = (
            "Answer the question based only on the provided context. "
            "If the answer cannot be found in the context, say \"I cannot answer this based on the provided context.\"\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n\n"
            "Answer:"
        )
        self.prompt = ChatPromptTemplate.from_template(template)

        # Build the chain using the pipe operator chaining
        self.chain = (
            {
                "context": self.retriever,
                "question": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def _create_new_vectorstore(self, pdf_path: str):
        """
        Creates a new FAISS vector store from PDF content.
        """
        # Load PDF document
        doc = load_pdf(pdf_path)
        if not doc:
            raise Exception("Failed to load PDF document")

        # Split the document into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            add_start_index=True
        )
        split_docs = splitter.split_documents(doc)
        if not split_docs:
            raise Exception("No content extracted from PDF")

        # Create the FAISS vector store using the provided embeddings
        vectorstore = FAISS.from_documents(split_docs, self.embeddings)

        # Save the vector store locally using FAISS's built-in methods
        self._save_vectorstore(vectorstore)
        return vectorstore

    def _save_vectorstore(self, vectorstore):
        """
        Saves the FAISS vector store to disk.
        """
        vectorstore.save_local(self.store_directory)
        print("Vector store saved locally.")

    def _load_vectorstore(self):
        """
        Loads the FAISS vector store from disk.
        """
        vectorstore = FAISS.load_local(self.store_directory, self.embeddings)
        print("Vector store loaded from disk.")
        return vectorstore

    def chat(self, question: str) -> str:
        """
        Answers a question based on the vector store derived from the PDF content.
        """
        if not question or not question.strip():
            return "Please provide a valid question."

        try:
            # Invoke the chain with the user's question
            return self.chain.invoke(question)
        except Exception as e:
            error_msg = f"Error processing your question: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return error_msg


if __name__ == "__main__":
    try:
        pdf_path = r"E:/Music_and_Movie_Recommendation_System.pdf"
        chat_service = ChatService(pdf_path)
        print("Chat service initialized successfully. Type 'quit' to exit.")

        while True:
            question = input("\nEnter your question: ").strip()
            if question.lower() == 'quit':
                print("Exiting chat service...")
                break
            response = chat_service.chat(question)
            print("\nResponse:", response)

    except Exception as e:
        print(f"Fatal error: {str(e)}")
        traceback.print_exc()

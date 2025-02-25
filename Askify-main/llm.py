import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings


class ModelService:
    """
    This class provides a service for loading and interacting with a generative AI model.
    It handles environment variable loading and ensures the presence of a required API key.
    """

    def __init__(self):
        """
        Initializes the service by loading environment variables and retrieving API keys.

        Raises:
            ValueError: If the GOOGLE_API_KEY environment variable is not set.
        """

        # Load environment variables from a .env file
        load_dotenv()

        # Access the API key
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        self.LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
        self.LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")

        # Ensure the API key is present
        if self.GOOGLE_API_KEY is None :
            raise ValueError("No GOOGLE_API_KEY set for Django application")

    def get_llm_model(self, model_name="gemini-1.5-flash"):
        """
        This function is used to instantiate a ChatGoogleGenerativeAI model.

        Args:
            model_name (str, optional): The name of the model to be loaded. Defaults to "gemini-1.5-flash".

        Returns:
            ChatGoogleGenerativeAI: An instance of the ChatGoogleGenerativeAI class representing the generative AI model.
        """

        return ChatGoogleGenerativeAI(model=model_name)

    def get_embedding_model(self, model_name="models/text-embedding-004"):
        """
        Returns a GoogleGenerativeAIEmbeddings model for text embedding.

        Args:
            model_name (str, optional): Name of the embedding model. Defaults to "models/text-embedding-004".

        Returns:
            GoogleGenerativeAIEmbeddings: The loaded text embedding model.
        """
        return GoogleGenerativeAIEmbeddings(model=model_name)



if __name__ == "__main__":
    """
    Example usage demonstrating how to create a ModelService instance, get a model, and interact with it.
    """

    service = ModelService()
    llm = service.get_llm_model()

    print(llm.invoke("What is python").content)
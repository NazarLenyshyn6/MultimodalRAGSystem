
from langchain.prompts import PromptTemplate

from TheBatch.the_batch_vectorestore_pipeline import the_batch_vectorestore
from LLM.rag_llm import RAGLLMI
from LLM.rag_llm import OllamaRAGLLM

the_batch_prompt_template = PromptTemplate(
    input_variables=["context", "user_query"],
    template=""" You are an advanced AI assistant designed to provide 
    comprehensive and well-reasoned answers to user queries
    based on relevant news articles. You have access to the 
    following context, which may include text from news articles 
    and associated images (described in text form).

    Context:
        {context}

    Instructions:
        - Carefully read the context above, which contains multiple news articles relevant to the user's question.
        - If any images are described (e.g., captions, OCR, extracted text), incorporate them into your analysis.
        - Summarize and synthesize the information to answer the user's question.
        - Ensure your answer is accurate, relevant, and concise.

    User query:
        {user_query}

    Your answer:
    """
)

TheBatchLLM = OllamaRAGLLM(prompt_template=the_batch_prompt_template,
                           vectorstore=the_batch_vectorestore)


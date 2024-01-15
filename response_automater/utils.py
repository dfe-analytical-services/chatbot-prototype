from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from pydantic import BaseModel

from .config import settings

QA_PROMPT = PromptTemplate(template=settings.chat_prompt_template, input_variables=["context", "question", "links"])


def makechain(callback) -> load_qa_chain:
    model = ChatOpenAI(
        streaming=True,
        verbose=True,
        callbacks=[callback],
        model=settings.openai_model,
        openai_api_key=settings.openai_api_key,
    )

    chain = load_qa_chain(llm=model, chain_type="stuff", prompt=QA_PROMPT)

    return chain


# pydantic validation of the request
class StreamRequest(BaseModel):
    """Request body for streaming."""

    question: str


def temp_method_for_proof_of_concept_tests(some_number):
    return 2 * some_number

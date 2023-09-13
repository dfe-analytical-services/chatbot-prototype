from config import settings
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from pydantic import BaseModel

prompt_template = """You are an AI assistant on the explore education statistics service. You are given
a question, links and context which is used to answer the question. Provide an answer to the question based on the context provided. If any of the context
provided isnt relevant to answer the question, it is imperative that you do not include this in your answer and stay focused on the question.
If the question asked is not related to the education sector and not included in the contextual information, you MUST not answer the question and 
instead say Sorry this question does not relate to the service. If and only if the question is related to the education sector 
say this information is not contained within the service but here are links to relevant publications.Parse the following links array 
and use hyperlink to direct the user to relevant pages on the service: {links} .It is very important you only provide 
information relevant to the service and remain impartial and do not provide opinions, even if opinions are contained within the service. 
Where inferred by very specific about dates of events (include year) not just month. 
Question: {question}
========
{context}
=========
Answer in Markdown:

"""

QA_PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question", "links"])


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

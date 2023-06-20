import logging
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import AsyncIteratorCallbackHandler
from dotenv import load_dotenv
import os
from langchain.prompts.prompt import PromptTemplate


load_dotenv()

prompt_template = """You are an AI assistant on the explore education statistics service. You are given the following pieces of 
a question and the following context relating to education information. Provide a succint answer based on the context provided. If the question the huma asks is not related to the
 the contextual information, you MUST not answer the question and instead say Sorry this question does not relate to the service. It is very important you only provide information relevant to the report.
Question: {question}
 =========
{context}

  =========

  Answer in Markdown:

"""

QA_PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

def makechain(callback) -> load_qa_chain:
    model = ChatOpenAI(
        streaming=True,
        verbose=True,
        callbacks=[callback],
        model='gpt-4',
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )

    chain = load_qa_chain(llm=model, chain_type='stuff', prompt = QA_PROMPT)

    return chain
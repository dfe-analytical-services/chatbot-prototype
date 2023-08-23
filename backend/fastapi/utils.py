import os

from dotenv import load_dotenv
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate

load_dotenv()

prompt_template = """You are an AI assistant on the explore education statistics service. You are given the following pieces of 
a question and the following context relating to education information. Provide a succint answer based on the context provided.
If the question asked is not related to the education sector and not included in the contextual information, you MUST not answer the question and instead say Sorry this question does not relate to the service. 
If and only if the question is related to the education sector say this information is not contained within the service
but here are links to relevant publications. Parse the following links array and use as hyperlink if do this: {links}
It is very important you only provide information relevant to the service and remain impartial and do not provide opinions, even if opinions
are contained within the service. Where inferred by very specifc about dates of events (include year) not just month. 
Question: {question}
========
{context}
=========
Answer in Markdown:

"""

QA_PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question", "links"])


def makechain(callback) -> load_qa_chain:
    model = ChatOpenAI(
        streaming=True, verbose=True, callbacks=[callback], model="gpt-4", openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    chain = load_qa_chain(llm=model, chain_type="stuff", prompt=QA_PROMPT)

    return chain

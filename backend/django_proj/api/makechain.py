import logging
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
#from langchain.callbacks import CallbackManager
#from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import pinecone
from django.conf import settings

from .langchainprompt import QA_PROMPT

logger = logging.getLogger(__name__)

def init_pine():
    try:
        pinecone.init(api_key= settings.PINECONE_API_KEY,  # app.pinecone.io (console)
                      environment=settings.PINECONE_ENV)
        logger.debug("Pinecone initialised")
    except Exception as e:
        logging.error("Failed to initialise pinecone %s", e)

def make_chain() -> load_qa_chain:
    llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY,
                   temperature=0,
                   model_name=settings.OPENAI_MOD,
                   request_timeout = 120)#,
                   #callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
    
    chain = load_qa_chain(llm = llm, chain_type='stuff', prompt= QA_PROMPT)
    return chain

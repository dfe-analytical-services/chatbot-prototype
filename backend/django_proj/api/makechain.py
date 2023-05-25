from langchain.chat_models import ChatOpenAI
from langchain.vectorstores.pinecone import Pinecone
from langchain.chains import ConversationalRetrievalChain
#from langchain.embeddings import OpenAIEmbeddings
from langchain.callbacks import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from .langchainprompt import CONDENSE_QUESTION_PROMPT, QA_PROMPT
import pinecone
from django.conf import settings





def init_pine():
    try:
        pinecone.init(api_key= settings.PINECONE_API_KEY,  # app.pinecone.io (console)
                      environment=settings.PINECONE_ENV)
        print('Pinecone Initilaised successfully')
    except Exception as e:
        print('Error', e)

def make_chain(vectorStore: Pinecone) -> ConversationalRetrievalChain:
    
    llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY,
                   temperature=0,
                   model_name='gpt-4',
                   request_timeout = 120,
                   callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
    
    chain = ConversationalRetrievalChain.from_llm(
        retriever = vectorStore.as_retriever(),
        llm=llm,
        return_source_documents = True,
        condense_question_prompt=CONDENSE_QUESTION_PROMPT,
        qa_prompt=QA_PROMPT)
    
    return chain


#vec_store = Pinecone.from_existing_index(index_name='edtech-gpt', 
#                                         embedding=OpenAIEmbeddings(openai_api_key=""),
#                                         text_key='text')

#chain = make_chain(vec_store)

#chat_history = []
#query = "What is the report about"

#result = chain({"question": query, "chat_history": chat_history})

#print(result)
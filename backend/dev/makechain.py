from langchain.llms.openai import OpenAI
from langchain.vectorstores.pinecone import Pinecone
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.callbacks import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchainprompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
import pinecone


pinecone.init(
    api_key='',  # app.pinecone.io (console)
    environment="northamerica-northeast1-gcp")

def make_chain(vectorStore: Pinecone) -> ConversationalRetrievalChain:
    
    llm = OpenAI(openai_api_key="",
                   temperature=0,
                   model_name='gpt-4',
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

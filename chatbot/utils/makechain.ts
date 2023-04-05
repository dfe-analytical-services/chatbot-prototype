import { OpenAIChat } from "langchain/llms";
import { LLMChain, ChatVectorDBQAChain, loadQAChain} from "langchain/chains";
import { PineconeStore } from "langchain/vectorstores";
import { PromptTemplate } from "langchain/prompts";
import { CallbackManager } from "langchain/callbacks";

const CONDENSE_PROMPT =   PromptTemplate.fromTemplate(`Answer the following question: {question}`);

const QA_PROMPT = PromptTemplate.fromTemplate(
    `You are an AI assistant providing helpful on education documents. You are given the following extracted parts of a long document and a question. Provide a conversational answer based on the context provided.
  You should only provide hyperlinks that reference the context below. Do NOT make up hyperlinks.
  If you can't find the answer in the context below, just say "Hmm, I'm not sure." Don't try to make up an answer.
  If the question is not related to the context, you must not answer the question and instead say Sorry this is not related to the question. It is very important 
  you only provide information relevant to the document.
  Question: {question}
  =========
  {context}
  =========
  Answer in Markdown:`,
  );

export const makeChain = (
    vectorstore: PineconeStore,
    onTokenStream?: (token: string) => void,
) => {
    const question = new LLMChain({
        llm: new OpenAIChat({temperature: 0}),
        prompt: CONDENSE_PROMPT,
    });
    const docChain = loadQAChain(
        new OpenAIChat({
            temperature: 0,
      modelName: 'gpt-4', 
      streaming: Boolean(onTokenStream),
      callbackManager: onTokenStream
        ? CallbackManager.fromHandlers({
            async handleLLMNewToken(token) {
              onTokenStream(token);
              console.log(token);
            },
        })
        : undefined
        }),
    {prompt: QA_PROMPT}
    );

    return new ChatVectorDBQAChain({
        vectorstore,
        combineDocumentsChain: docChain,
        questionGeneratorChain: question,
        returnSourceDocuments: true,
        k: 2, //number of source documents to return
      });
    };
    
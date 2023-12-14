import { Message } from '@/hooks/useChatbot';

const api_url =
  process.env.NEXT_PUBLIC_CHAT_URL_API ?? 'http://localhost:8010/api/chat';

const strangle_api = process.env.NEXT_TEMP_STRANGLE_API ?? false;
const delay = (ms: number) => new Promise((res) => setTimeout(res, ms));

const parseResponseFromAPI = async (response: Response): Promise<Message> => {
  const data = response.body;

  if (!data) {
    throw new Error('Response contained no body.');
  }

  const reader = data.getReader();
  const decoder = new TextDecoder();
  let done = false;

  let content = '';
  let links = undefined;

  while (!done) {
    const { value, done: doneReading } = await reader.read();
    done = doneReading;
    const chunkValue = decoder.decode(value);
    if (chunkValue.startsWith('{"sourceDocuments":')) {
      links = JSON.parse(chunkValue).sourceDocuments;
    } else {
      content += chunkValue;
    }
  }

  return {
    content,
    links,
    type: 'apiMessage',
  };
};

const sendMessage = async (message: string): Promise<Message> => {
  if (strangle_api) {
    await delay(3000);

    const fakeMessage: Message = {
      content: 'This is a fake mocked out message',
      type: 'apiMessage',
    };
    return fakeMessage;
  }

  const response = await fetch(api_url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      question: message,
    }),
  });

  const responseMessage = await parseResponseFromAPI(response);

  return responseMessage;
};

const ChatBotService = {
  sendUserMessage(message: string): Promise<Message> {
    return sendMessage(message);
  },
};

export default ChatBotService;

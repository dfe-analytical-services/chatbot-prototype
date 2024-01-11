import { Message } from '@/hooks/useChatbot';

let apiUrl = '';

export function initChatbotService(url: string) {
  if (!apiUrl) {
    apiUrl = url;
  }
}

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
  const response = await fetch(apiUrl, {
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
    if (!apiUrl) {
      throw new Error('Not initialised');
    }
    return sendMessage(message);
  },
};

export default ChatBotService;

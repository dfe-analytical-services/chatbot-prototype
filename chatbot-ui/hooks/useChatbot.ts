import { useState } from 'react';

const api_url =
  process.env.NEXT_PUBLIC_CHAT_URL_API ?? 'http://localhost:8010/api/chat';

const strangle_api = process.env.NEXT_TEMP_STRANGLE_API ?? true;
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

function useChatbot(): UseChatbotState {
  const [fetching, setFetching] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [messageHistory, setMessageHistory] = useState<Message[]>([
    {
      content:
        'Hi, what would you like to know about the latest publications on EES?',
      type: 'apiMessage',
    },
  ]);

  const recordMessageInHistory = (message: Message) => {
    setMessageHistory(messageHistory.concat([message]));
  };

  const sendMessage = async (userInput: string) => {
    recordMessageInHistory({ content: userInput, type: 'userMessage' });
    setFetching(true);

    if (strangle_api) {
      await delay(5000);

      const fakeMessage: Message = {
        content: 'This is a fake mocked out message',
        type: 'apiMessage',
      };
      recordMessageInHistory(fakeMessage);
      setFetching(false);
      return;
    }

    try {
      const response = await fetch(api_url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userInput,
        }),
      });

      const responseMessage = await parseResponseFromAPI(response);

      recordMessageInHistory(responseMessage);
    } catch (error) {
      setError('An error occurred while fetching the data. Please try again.');
    }
    setFetching(false);
  };

  return {
    messages: messageHistory,
    sendMessage,
    fetching,
    error,
  };
}

export interface UseChatbotState {
  sendMessage: (userInput: string) => Promise<void>;
  messages: Message[];
  fetching: boolean;
  error: string | null;
}

export type MessageType = 'apiMessage' | 'userMessage';

export type Message = {
  content: string;
  type: MessageType;
  isStreaming?: boolean;
  links?: string[];
};

export default useChatbot;

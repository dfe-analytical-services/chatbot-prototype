import { useState } from 'react';
import ChatBotService from '@/services/chatbot-service';

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

  const recordMessageInHistory = (messages: Message[]) => {
    setMessageHistory(messageHistory.concat(messages));
  };

  const sendMessage = async (userInput: string) => {
    const userMessage: Message = { content: userInput, type: 'userMessage' };
    recordMessageInHistory([userMessage]);
    setFetching(true);

    try {
      const responseMessage = await ChatBotService.sendUserMessage(userInput);

      // TODO: Refactor state management so this works without having to re-add user message
      recordMessageInHistory([userMessage, responseMessage]);
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

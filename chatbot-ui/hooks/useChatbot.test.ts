import _ChatBotService from '@/services/chatbot-service';
import { renderHook, waitFor, act } from '@testing-library/react';
import useChatbot from './useChatbot';

jest.mock('../services/chatbot-service.ts');
const ChatBotService = _ChatBotService as jest.Mocked<typeof _ChatBotService>;

describe('useChatbot', () => {
  it('Initialises', () => {
    const { result } = renderHook(() => useChatbot());

    const { messages } = result.current;
    expect(messages).toHaveLength(1);
    expect(messages[0].content).toBe(
      'Hi, what would you like to know about Explore Education Statistics?',
    );
  });

  it('Sends the question and adds it and the response to the messages list', async () => {
    ChatBotService.sendUserMessage.mockResolvedValue({
      content: 'I am the response',
      type: 'apiMessage',
    });
    const { result } = renderHook(() => useChatbot());
    const { messages } = result.current;
    expect(messages).toHaveLength(1);
    expect(messages[0].content).toBe(
      'Hi, what would you like to know about Explore Education Statistics?',
    );

    await act(() => result.current.sendMessage('I am a message'));

    await waitFor(() => {
      expect(ChatBotService.sendUserMessage).toHaveBeenCalledWith(
        'I am a message',
      );
    });

    const { messages: updatedMessages } = result.current;
    expect(updatedMessages).toHaveLength(3);
    expect(updatedMessages[1].content).toBe('I am a message');
    expect(updatedMessages[2].content).toBe('I am the response');
  });

  it('Returns the error if sendMessage errors', async () => {
    ChatBotService.sendUserMessage.mockRejectedValue('I am the error');
    const { result } = renderHook(() => useChatbot());
    const { messages } = result.current;
    expect(messages).toHaveLength(1);

    await act(() => result.current.sendMessage('I am a message'));

    await waitFor(() => {
      expect(ChatBotService.sendUserMessage).toHaveBeenCalledWith(
        'I am a message',
      );
    });

    const { error, messages: updatedMessages } = result.current;
    expect(updatedMessages).toHaveLength(2);

    expect(error).toBe(
      'An error occurred while fetching the data. Please try again.',
    );
  });

  it('Resets the error state after sending a new message', async () => {
    ChatBotService.sendUserMessage.mockRejectedValue('I am the error');
    const { result } = renderHook(() => useChatbot());

    await act(() => result.current.sendMessage('I am a message'));

    await waitFor(() => {
      expect(ChatBotService.sendUserMessage).toHaveBeenCalledWith(
        'I am a message',
      );
    });

    const { error, messages: updatedMessages } = result.current;
    expect(updatedMessages).toHaveLength(2);

    expect(error).toBe(
      'An error occurred while fetching the data. Please try again.',
    );

    ChatBotService.sendUserMessage.mockResolvedValue({
      content: 'I am a future successful message',
      type: 'apiMessage',
    });

    await act(() => result.current.sendMessage('I am a second message'));

    const { error: errorTwo, messages: updatedMessagesTwo } = result.current;
    expect(updatedMessagesTwo).toHaveLength(4);
    expect(errorTwo).toBeNull();
  });
});

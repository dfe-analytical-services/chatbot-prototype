import MessageHistory from '@/components/MessageHistory';
import { Message } from '@/hooks/useChatbot';
import React from 'react';
import { render, screen } from '@testing-library/react';

describe('Message history', () => {
  const testMessages: Message[] = [
    { content: 'This is the first message from the bot', type: 'apiMessage' },
    {
      content: 'This is the first message from the human',
      type: 'userMessage',
    },
    { content: 'This is the second message from the bot', type: 'apiMessage' },
  ];

  it('Renders a list of messages', () => {
    render(<MessageHistory messages={testMessages} loading={false} />);

    const botMessages = screen.getAllByTestId('api-message');
    expect(botMessages).toHaveLength(2);
    expect(botMessages[0]).toHaveTextContent(
      'This is the first message from the bot',
    );
    expect(botMessages[1]).toHaveTextContent(
      'This is the second message from the bot',
    );

    const userMessages = screen.getAllByTestId('user-message');
    expect(userMessages).toHaveLength(1);
    expect(userMessages[0]).toHaveTextContent(
      'This is the first message from the human',
    );
  });
});

import UserInputDialog from '@/components/UserInputDialog';
import React from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('Message history', () => {
  it('Renders the form', () => {
    render(
      <UserInputDialog
        sendMessage={() => Promise.resolve()}
        fetching={false}
        error=""
      />,
    );

    expect(screen.getByLabelText('What is your question?')).toBeInTheDocument();

    expect(screen.getByRole('button', { name: 'Send' })).toBeInTheDocument();
  });

  it('Calls `sendMessage` when successfully submitted', async () => {
    const handleSend = jest.fn();
    render(
      <UserInputDialog sendMessage={handleSend} fetching={false} error="" />,
    );

    fireEvent.change(screen.getByLabelText('What is your question?'), {
      target: { value: 'Is the ski village on fire?' },
    });

    await userEvent.click(screen.getByRole('button', { name: 'Send' }));

    await waitFor(() => {
      expect(handleSend).toHaveBeenCalledWith('Is the ski village on fire?');
    });
  });

  it('Shows an error message when submitted without a question', async () => {
    const handleSend = jest.fn();
    render(
      <UserInputDialog sendMessage={handleSend} fetching={false} error="" />,
    );

    await userEvent.click(screen.getByRole('button', { name: 'Send' }));

    expect(handleSend).not.toHaveBeenCalled();
    expect(screen.getByText('There is a problem')).toBeInTheDocument();
    expect(
      screen.getByRole('link', { name: 'Enter a question' }),
    ).toBeInTheDocument();
  });
});

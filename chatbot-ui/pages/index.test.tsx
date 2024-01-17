import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Home from '@/pages';

describe('Root Index Page', () => {
  it('Renders', () => {
    render(<Home apiUrl={'some-url'} authPassword={'the-right-password'} />);

    expect(screen.getByRole('heading', { name: 'Support bot' })).toBeVisible();
  });

  it('Shows the chatbot dialog once proper auth is entered', async () => {
    render(<Home apiUrl={'some-url'} authPassword={'the-right-password'} />);

    await userEvent.type(
      screen.getByLabelText('Please enter the password'),
      'the-right-password',
    );

    await userEvent.click(screen.getByRole('button', { name: 'Enter' }));

    expect(screen.getByLabelText('What is your question?')).toBeVisible();
  });
});

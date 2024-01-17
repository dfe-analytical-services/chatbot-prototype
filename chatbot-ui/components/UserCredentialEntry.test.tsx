import UserCredentialEntry from '@/components/UserCredentialEntry';
import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

const mockOnCorrectEntry = jest.fn();

describe('User Credential Entry', () => {
  beforeEach(() => {
    render(
      <UserCredentialEntry
        onCorrectEntry={mockOnCorrectEntry}
        authPassword="the-right-password"
      />,
    );
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  const getPasswordInput = () => {
    return screen.getByLabelText('Please enter the password');
  };

  it('Renders', () => {
    expect(
      screen.getByRole('heading', { name: 'Please enter the password' }),
    ).toBeVisible();
  });

  it('Autofocuses the first form field', () => {
    expect(getPasswordInput()).toHaveFocus();
  });

  it('Allows the user to type a password', async () => {
    await userEvent.type(getPasswordInput(), 'myPassword');

    expect(getPasswordInput()).toHaveValue('myPassword');
  });

  it('Invokes the callback if entered password matches', async () => {
    await userEvent.type(getPasswordInput(), 'the-right-password');

    await userEvent.click(screen.getByRole('button', { name: 'Enter' }));

    expect(mockOnCorrectEntry).toHaveBeenCalled();
  });

  it('Does not invoke the callback if entered password does not match', async () => {
    await userEvent.type(getPasswordInput(), 'the-wrong-password');

    await userEvent.click(screen.getByRole('button', { name: 'Enter' }));

    expect(mockOnCorrectEntry).not.toHaveBeenCalled();
  });

  it('Displays a validation error if a password was not entered', async () => {
    await userEvent.click(screen.getByRole('button', { name: 'Enter' }));

    expect(screen.getByText('A password is required')).toBeVisible();
  });

  it('Displays an error message if the password was incorrect', async () => {
    await userEvent.type(getPasswordInput(), 'the-wrong-password');

    await userEvent.click(screen.getByRole('button', { name: 'Enter' }));

    expect(screen.getByText('The password was incorrect')).toBeVisible();
  });
});

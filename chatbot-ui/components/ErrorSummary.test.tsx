import { render, screen } from '@testing-library/react';
import ErrorSummary from '@/components/ErrorSummary';
import React from 'react';

describe('Error Summary', () => {
  it('Renders', () => {
    render(<ErrorSummary error="This is an error" />);

    expect(
      screen.getByRole('heading', { name: 'There is a problem' }),
    ).toBeInTheDocument();
  });

  it('Displays the error as a link', () => {
    render(<ErrorSummary error="This is an error" />);

    expect(
      screen.getByRole('link', { name: 'This is an error' }),
    ).toHaveAttribute('href', '#user-input-form');
  });
});

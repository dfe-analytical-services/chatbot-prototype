import { render, screen } from '@testing-library/react';
import PageBanner from '@/components/PageBanner';
import React from 'react';

describe('Page Banner', () => {
  it('Renders', () => {
    render(<PageBanner />);

    expect(screen.getByText(/This is a new service/)).toBeInTheDocument();
  });

  // TODO: Query if this is the correct target, update if not
  it('Displays a link for providing feedback', () => {
    render(<PageBanner />);

    expect(screen.getByRole('link', { name: 'feedback' })).toHaveAttribute(
      'href',
      '#',
    );
  });
});

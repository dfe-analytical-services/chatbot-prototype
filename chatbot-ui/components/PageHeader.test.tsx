import { render, screen } from '@testing-library/react';
import PageHeader from '@/components/PageHeader';
import React from 'react';

describe('Page Banner', () => {
  it('Renders', () => {
    render(<PageHeader />);

    expect(screen.getByRole('banner')).toBeInTheDocument();
  });

  // TODO: Query if this is the correct target, update if not
  it('Displays the expected links', () => {
    render(<PageHeader />);

    expect(
      screen.getByRole('link', { name: 'Skip to main content' }),
    ).toHaveAttribute('href', '#main-content');

    expect(
      screen.getByRole('link', { name: 'Explore education statistics' }),
    ).toHaveAttribute('href', '#');
  });
});

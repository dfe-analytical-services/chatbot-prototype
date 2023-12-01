import { render, screen } from '@testing-library/react';
import PageTitle from '@/components/PageTitle';
import React from 'react';

describe('Page Title', () => {
  it('Renders', () => {
    render(<PageTitle title="Test Page Title"></PageTitle>);

    expect(
      screen.getByRole('heading', { name: 'Test Page Title' }),
    ).toBeInTheDocument();
  });

  it('Renders a caption if one is provided', () => {
    render(
      <PageTitle
        title="Test Page Title"
        caption="Test Caption Text"
      ></PageTitle>,
    );

    expect(screen.getByText('Test Caption Text')).toBeInTheDocument();
  });

  it('Does not render a caption if none is provided', () => {
    render(<PageTitle title="Test Page Title"></PageTitle>);

    expect(screen.queryByText('Test Caption Text')).toBeNull();
  });
});

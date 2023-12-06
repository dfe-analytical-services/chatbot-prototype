import { render, screen } from '@testing-library/react';
import Page from '@/components/Page';

describe('Page', () => {
  it('Renders', () => {
    render(<Page title={'Test Page Title'} />);

    expect(screen.getByRole('main')).toBeInTheDocument();
  });

  it('Renders a title and caption if provided', () => {
    render(<Page title="Test Page Title" caption="Test Page Caption" />);

    expect(
      screen.getByRole('heading', { name: 'Test Page Title' }),
    ).toBeInTheDocument();

    expect(screen.getByText('Test Page Caption')).toBeInTheDocument();
  });

  it('Renders children if provided', () => {
    render(
      <Page title={'Test Page Title'}>
        <span>This is some child content</span>
      </Page>,
    );

    expect(screen.getByText(/This is some child content/)).toBeInTheDocument();
  });
});

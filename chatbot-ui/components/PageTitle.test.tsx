import { render, screen } from '@testing-library/react';
import PageTitle from './PageTitle';

describe('Page Title', () => {
  it('Renders', () => {
    render(<PageTitle title="Test Page Title"></PageTitle>);

    expect(
      screen.getByRole('heading', { name: 'Test Page Title' }),
    ).toBeVisible();
  });
});

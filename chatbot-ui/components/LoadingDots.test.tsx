import { render, screen } from '@testing-library/react';
import LoadingDots from './LoadingDots';

describe('Loading Dots', () => {
  it('Renders', () => {
    render(<LoadingDots color="red" />);

    expect(
      screen.getByRole('heading', { name: 'Test Page Title' }),
    ).toBeVisible();
  });
});

import { render } from '@testing-library/react';
import LoadingDots from '@/components/LoadingDots';

describe('Loading Dots', () => {
  it('Renders', () => {
    render(<LoadingDots color="red" />);
  });
});

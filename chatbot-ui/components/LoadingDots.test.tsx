import { render } from '@testing-library/react';
import LoadingDots from '@/components/LoadingDots';
import React from 'react';

describe('Loading Dots', () => {
  it('Renders', () => {
    render(<LoadingDots color="red" />);
  });
});

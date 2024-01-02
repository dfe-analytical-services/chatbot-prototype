import React from 'react';
import { render, screen } from '@testing-library/react';
import Home from '../pages/index';

describe('Home Page', () => {
  it('Renders', () => {
    render(<Home />);

    expect(screen.getByText('Chatbot prototype')).toBeInTheDocument();
  });
});

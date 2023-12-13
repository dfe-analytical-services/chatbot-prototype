import React from 'React';
import { render, screen } from '@testing-library/react';
import Home from './index';

describe('Home Page', () => {
  it('Renders', () => {
    render(<Home />);

    expect(screen.getByText('Chatbot prototype')).toBeInTheDocument();
  });
});

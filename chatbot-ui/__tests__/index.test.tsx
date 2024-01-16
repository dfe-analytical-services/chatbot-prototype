import React from 'react';
import { render, screen } from '@testing-library/react';
import Home from '../pages/index';

describe('Home Page', () => {
  it('Renders', () => {
    render(<Home apiUrl="https://localhost" chatbotPassword="testPassword" />);

    expect(screen.getByText('Support bot')).toBeInTheDocument();
  });
});

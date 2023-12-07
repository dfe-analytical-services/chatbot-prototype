import React from 'React';
import { render, screen } from '@testing-library/react';
import HomePage from './index';

jest.mock('react-markdown');

describe('Home Page', () => {
  it.skip('Renders', () => {
    render(<HomePage />);

    expect(screen.getByRole('not-a-role')).toBeInTheDocument();
  });
});

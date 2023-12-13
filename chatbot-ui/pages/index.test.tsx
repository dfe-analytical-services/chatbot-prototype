import React from 'React';
import { render, screen } from '@testing-library/react';
import HomePage from './index';

jest.mock('react-markdown');

// TODO: Make whatever changes necessary to be able to test these components.
// Currently, anything which uses react-markdown fails to compile with messages like:

// export {Markdown as default, defaultUrlTransform} from './lib/index.js'
// ^^^^^^
//
//  SyntaxError: Unexpected token 'export'

describe('Home Page', () => {
  it.skip('Renders', () => {
    render(<HomePage />);

    expect(screen.getByRole('not-a-role')).toBeInTheDocument();
  });
});

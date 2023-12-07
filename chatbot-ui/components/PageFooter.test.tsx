import { render, screen } from '@testing-library/react';
import PageFooter from '@/components/PageFooter';

describe('Page Footer', () => {
  it('Renders', () => {
    render(<PageFooter />);

    expect(screen.getByRole('contentinfo')).toBeInTheDocument();
  });

  it('Displays the expected links', () => {
    render(<PageFooter />);

    const expectedLinks: ExpectedLink[] = [
      { name: 'Cookies', target: '#' },
      { name: 'Privacy notice', target: '#' },
      { name: 'Contact us', target: '#' },
      { name: 'Accessibility statement', target: '#' },
      { name: 'Glossary', target: '#' },
      { name: 'Help and support', target: '#' },
      {
        name: 'Open Government Licence v3.0',
        target:
          'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
      },
      {
        name: '© Crown copyright',
        target:
          'https://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/uk-government-licensing-framework/crown-copyright/',
      },
    ];

    expectedLinks.forEach((link) => {
      expect(screen.getByRole('link', { name: link.name })).toHaveAttribute(
        'href',
        link.target,
      );
    });
  });
});

interface ExpectedLink {
  name: string;
  target: string;
}

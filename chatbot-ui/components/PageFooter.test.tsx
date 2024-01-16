import { render, screen } from '@testing-library/react';
import PageFooter from '@/components/PageFooter';

describe('Page Footer', () => {
  const OLD_ENV = process.env;

  beforeEach(() => {
    jest.resetModules();
    process.env = { ...OLD_ENV };
  });

  afterAll(() => {
    process.env = OLD_ENV;
  });

  it('Renders', () => {
    render(<PageFooter />);

    expect(screen.getByRole('contentinfo')).toBeInTheDocument();
  });

  it('Displays the build number if one is present', () => {
    process.env.NEXT_PUBLIC_BUILD_NUMBER = 'Testing123';

    render(<PageFooter />);

    expect(screen.getByText('Build: Testing123')).toBeInTheDocument();
  });

  it('Hides the build number if one is absent', () => {
    process.env.NEXT_PUBLIC_BUILD_NUMBER = undefined;

    render(<PageFooter />);

    expect(screen.queryByText('Build: Testing123')).toBeNull();
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

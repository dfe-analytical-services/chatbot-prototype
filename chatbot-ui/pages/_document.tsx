import { Html, Head, Main, NextScript } from 'next/document';

export default function Document() {
  return (
    <Html lang="en" className="govuk-template app-html-class">
      <Head>
        <link
          rel="shortcut icon"
          sizes="16x16 32x32 48x48"
          href="/assets/images/favicon.ico"
          type="image/x-icon"
        />
        <link
          rel="mask-icon"
          href="/assets/images/govuk-mask-icon.svg"
          color="#0b0c0c"
        />
        <link
          rel="apple-touch-icon"
          sizes="180x180"
          href="/assets/images/govuk-apple-touch-icon-180x180.png"
        />
        <link
          rel="apple-touch-icon"
          sizes="167x167"
          href="/assets/images/govuk-apple-touch-icon-167x167.png"
        />
        <link
          rel="apple-touch-icon"
          sizes="152x152"
          href="/assets/images/govuk-apple-touch-icon-152x152.png"
        />
        <link
          rel="apple-touch-icon"
          href="/assets/images/govuk-apple-touch-icon.png"
        />
      </Head>
      <body className="govuk-template__body app-body-class">
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}

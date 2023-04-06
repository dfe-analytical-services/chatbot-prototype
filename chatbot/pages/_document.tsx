import { Html, Head, Main, NextScript } from "next/document";

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        <link
          rel="stylesheet"
          href="/node_modules/govuk-frontend/govuk/all.css"
          integrity="gZHDqf5vdlHjmx0NGJiNT12XLyR3d5KCS4AnlC3xTWOObJ0kQROrkIFyp3w4/PY3EQiYdgacVaJ6lizzygnzYw=="
          crossOrigin="anonymous"
        />
      </Head>
      <body className="govuk-template__body">
        <script src="/node_modules/govuk-frontend/govuk/all.js" />
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}


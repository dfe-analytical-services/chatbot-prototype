import type { AppProps } from 'next/app';
import Head from 'next/head';
import '../styles/_all.scss';

function App({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <title>Explore Education Statistics Support Bot</title>
        <meta name="robots" content="noindex, nofollow" />
      </Head>
      <Component {...pageProps} />
    </>
  );
}

export default App;

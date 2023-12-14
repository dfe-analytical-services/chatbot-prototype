import type { AppProps } from 'next/app';
import Head from 'next/head';
import '../styles/_all.scss';

function App({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <title>Chatbot prototype</title>
      </Head>
      <Component {...pageProps} />
    </>
  );
}

export default App;

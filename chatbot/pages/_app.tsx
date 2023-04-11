import type { AppProps } from 'next/app';
import { Inter } from 'next/font/google';
//import 'govuk-frontend/govuk/govuk.scss';
import 'govuk-frontend/govuk/all.scss';


const inter = Inter({
  variable: '--font-inter',
  subsets: ['latin'],
});

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
      <main className={inter.variable}>
        <Component {...pageProps} />
      </main>
    </>
  );
}

export default MyApp;

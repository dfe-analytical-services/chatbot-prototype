import type { AppProps } from "next/app";
import "../styles/_all.scss";

function App({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}

export default App;

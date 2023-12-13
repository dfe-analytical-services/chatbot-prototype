import { ReactNode } from 'react';
import PageBanner from './PageBanner';
import PageFooter from './PageFooter';
import PageHeader from './PageHeader';
import PageTitle from './PageTitle';

type Props = {
  title: string;
  caption?: string;
  children?: ReactNode;
  wide?: boolean;
};

const Page = ({ title, caption = '', children = null }: Props) => {
  return (
    <>
      <PageHeader />

      <div className="govuk-width-container ">
        <PageBanner />
        <main className="govuk-main-wrapper" id="main-content" role="main">
          <PageTitle title={title} caption={caption} />
          {children}
        </main>
      </div>

      <PageFooter />
    </>
  );
};

export default Page;

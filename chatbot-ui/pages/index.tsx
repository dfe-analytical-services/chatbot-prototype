import Page from '@/components/Page';
import React from 'react';
import type { InferGetServerSidePropsType, GetServerSideProps } from 'next';

export default function Home({}: InferGetServerSidePropsType<
  typeof getServerSideProps
>) {
  return (
    <Page title="Support bot">
      <div>
        Nothing to see here (I just moved chatbot stuff into its own route to
        make the redirects from login obvious. Could move it back again or
        leave, whatever). We should never see this since submitting the login
        form redirects you straight to /chatbot
      </div>
    </Page>
  );
}

export const getServerSideProps = (async () => {
  return {
    props: {
      authPassword: process.env.AUTH_PASSWORD,
    },
  };
}) satisfies GetServerSideProps<{ authPassword: string | undefined }>;

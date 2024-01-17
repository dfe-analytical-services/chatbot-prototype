import Page from '@/components/Page';
import React from 'react';
import type { InferGetServerSidePropsType, GetServerSideProps } from 'next';
import UserCredentialEntry from '@/components/UserCredentialEntry';

export default function Login({
  authPassword,
}: InferGetServerSidePropsType<typeof getServerSideProps>) {
  return (
    <Page title="Support bot">
      <UserCredentialEntry authPassword={authPassword} />
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

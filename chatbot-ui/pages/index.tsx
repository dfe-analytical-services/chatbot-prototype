import Page from '@/components/Page';
import React, { useState } from 'react';
import ErrorSummary from '@/components/ErrorSummary';
import MessageHistory from '@/components/MessageHistory';
import useChatbot from '@/hooks/useChatbot';
import UserInputDialog from '@/components/UserInputDialog';
import { initChatbotService } from '@/services/chatbot-service';
import type { InferGetServerSidePropsType, GetServerSideProps } from 'next';
import UserCredentialEntry from '@/components/UserCredentialEntry';

export default function Home({
  apiUrl,
  chatbotPassword,
}: InferGetServerSidePropsType<typeof getServerSideProps>) {
  initChatbotService(apiUrl);
  const { messages, sendMessage, fetching, error } = useChatbot();
  const [hasAuth, setHasAuth] = useState<boolean>(false);

  return (
    <Page title="Support bot">
      {!hasAuth && (
        <UserCredentialEntry
          passwordRequired={chatbotPassword}
          onCorrectEntry={() => {
            setHasAuth(true);
          }}
        />
      )}
      {hasAuth && (
        <>
          {error && <ErrorSummary error={error} />}

          <MessageHistory messages={messages} loading={fetching} />

          <UserInputDialog sendMessage={sendMessage} fetching={fetching} />
        </>
      )}
    </Page>
  );
}

export const getServerSideProps = (async () => {
  return {
    props: {
      apiUrl: process.env.CHAT_URL_API ?? 'http://localhost:8010/api/chat',
      // Could put this in KeyVault, but probably sufficient for now as an urgent stop-gap just for today?
      chatbotPassword: process.env.AUTH_PASSWORD,
    },
  };
}) satisfies GetServerSideProps<{ apiUrl: string }>;

import Page from '@/components/Page';
import React from 'react';
import ErrorSummary from '@/components/ErrorSummary';
import MessageHistory from '@/components/MessageHistory';
import useChatbot from '@/hooks/useChatbot';
import UserInputDialog from '@/components/UserInputDialog';
import { initChatbotService } from '@/services/chatbot-service';
import type { InferGetServerSidePropsType, GetServerSideProps } from 'next';

export default function Home({
  apiUrl,
}: InferGetServerSidePropsType<typeof getServerSideProps>) {
  initChatbotService(apiUrl);
  const { messages, sendMessage, fetching, error } = useChatbot();

  return (
    <Page title="Support bot">
      <>
        {error && <ErrorSummary error={error} />}

        <MessageHistory messages={messages} loading={fetching} />

        <UserInputDialog
          sendMessage={sendMessage}
          fetching={fetching}
          error={error}
        />
      </>
    </Page>
  );
}

export const getServerSideProps = (async () => {
  return {
    props: {
      apiUrl: process.env.CHAT_URL_API ?? 'http://localhost:8010/api/chat',
    },
  };
}) satisfies GetServerSideProps<{ apiUrl: string }>;

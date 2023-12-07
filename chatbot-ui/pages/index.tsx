import Page from '@/components/Page';
import React from 'react';
import ErrorSummary from '@/components/ErrorSummary';
import MessageHistory from '@/components/MessageHistory';
import useChatbot from '@/hooks/useChatbot';
import UserInputDialog from '@/components/UserInputDialog';

function Home() {
  const { messages, sendMessage, fetching, error } = useChatbot();

  return (
    <Page title="Chatbot prototype">
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

export default Home;

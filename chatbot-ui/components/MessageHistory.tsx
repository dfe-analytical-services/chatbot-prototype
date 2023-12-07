import React from 'react';
import styles from '@/styles/Home.module.css';
import RobotIcon from '@/public/assets/images/icons/robot.svg';
import UserIcon from '@/public/assets/images/icons/user.svg';
import classNames from 'classnames';
import ReactMarkdown from 'react-markdown';
import { Message, MessageType } from '@/hooks/useChatbot';

type Props = {
  messages: Message[];
  loading: boolean;
};

const MessageHistory = ({ messages, loading }: Props) => {
  const deriveCssClass = (messageType: MessageType, index: number): string => {
    if (messageType === 'apiMessage') {
      return styles.apimessage;
    }

    if (loading === true && index === messages.length - 1) {
      return styles.usermessagewaiting;
    }

    return styles.usermessage;
  };

  return (
    <div className={'govuk-body'}>
      <div className={styles.chat}>
        <div className={styles.messagelist}>
          {messages.map((message, index) => (
            <div
              key={`chatMessage-${index}`}
              className={classNames(
                'govuk-body',
                deriveCssClass(message.type, index),
              )}
            >
              {message.type === 'apiMessage' ? (
                <RobotIcon height="1.1em" fill="#1d70b8" />
              ) : (
                <UserIcon height="1.1em" fill="#00703c" />
              )}

              <div className={styles.markdownanswer}>
                <ReactMarkdown>{message.content}</ReactMarkdown>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MessageHistory;

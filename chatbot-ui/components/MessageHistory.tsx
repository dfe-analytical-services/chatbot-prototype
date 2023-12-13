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

// TODO: This could maybe be renamed
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
    <div>
      <div className={styles.chat}>
        <div className={styles.messagelist}>
          {messages.map((message, index) => (
            <div
              key={`chatMessage-${index}`}
              className={classNames(deriveCssClass(message.type, index))}
              data-testid={
                message.type === 'apiMessage' ? 'api-message' : 'user-message'
              }
            >
              {message.type === 'apiMessage' ? (
                <RobotIcon
                  className={styles.icon}
                  height="1.1em"
                  fill="#1d70b8"
                />
              ) : (
                <UserIcon
                  className={styles.icon}
                  height="1.1em"
                  fill="#00703c"
                />
              )}

              <div className={styles.markdownanswer}>
                <ReactMarkdown className="govuk-body">
                  {message.content}
                </ReactMarkdown>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MessageHistory;

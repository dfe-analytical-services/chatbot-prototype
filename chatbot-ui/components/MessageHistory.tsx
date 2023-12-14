import React from 'react';
import styles from '@/styles/Home.module.css';
import RobotIcon from '@/public/assets/images/icons/robot.svg';
import UserIcon from '@/public/assets/images/icons/user.svg';
import classNames from 'classnames';
import ReactMarkdown from 'react-markdown';
import { Message } from '@/hooks/useChatbot';

type Props = {
  messages: Message[];
  loading: boolean;
};

const MessageHistory = ({ messages, loading }: Props) => {
  return (
    <div>
      <div className={styles.chat}>
        <div className={styles.messagelist}>
          {messages.map((message, index) => (
            <div
              key={`chatMessage-${index}`}
              className={classNames(styles.message, {
                [styles.usermessagewaiting]:
                  loading === true && index === messages.length - 1,
                [styles.usermessage]: message.type === 'userMessage',
              })}
              data-testid={
                message.type === 'apiMessage' ? 'api-message' : 'user-message'
              }
            >
              {message.type === 'apiMessage' ? (
                <RobotIcon
                  className={classNames(styles.icon, styles.robot)}
                  fill="#1d70b8"
                />
              ) : (
                <UserIcon className={styles.icon} fill="#00703c" />
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

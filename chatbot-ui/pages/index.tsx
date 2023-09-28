import { useRef, useState, useEffect } from "react";
import Page from "@/components/Page";
import styles from "@/styles/Home.module.css";
import ReactMarkdown from "react-markdown";
import LoadingDots from "@/components/LoadingDots";
import classNames from "classnames";
import React from "react";
import RobotIcon from "../public/assets/images/icons/robot.svg";
import UserIcon from "../public/assets/images/icons/user.svg";

type Message = {
  type: "apiMessage" | "userMessage";
  message: string;
  isStreaming?: boolean;
  links?: string[];
};

function Home() {
  const [query, setQuery] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [messageState, setMessageState] = useState<{
    messages: Message[];
    history: [string, string][];
    pending?: string;
  }>({
    messages: [
      {
        message:
          "Hi, what would you like to know about the latest publications on EES?",
        type: "apiMessage",
      },
    ],
    history: [],
  });

  const { messages } = messageState;

  const messageListRef = useRef<HTMLDivElement>(null);
  const textAreaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    textAreaRef.current?.focus();
  }, []);

  //handle form submission
  async function handleSubmit(e: any) {
    e.preventDefault();

    if (!query) {
      setError("Enter a question");
      return;
    }

    setError(null);

    const question = query.trim();

    setMessageState((state) => ({
      ...state,
      messages: [
        ...state.messages,
        {
          type: "userMessage",
          message: question,
        },
      ],
    }));

    setLoading(true);
    setQuery("");

    try {
      const response = await fetch("http://localhost:8010/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question,
        }),
      });

      const data = response.body;

      setMessageState((state) => ({
        history: [...state.history],
        messages: [
          ...state.messages,
          {
            type: "apiMessage",
            message: "",
          },
        ],
      }));

      if (!data) {
        return;
      }

      const reader = data.getReader();
      const decoder = new TextDecoder();
      let done = false;

      let pending = "";
      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        const chunkValue = decoder.decode(value);
        if (chunkValue.startsWith('{"sourceDocuments":')) {
          setMessageState((state) => {
            let messages = state.messages;
            messages[messages.length - 1].links =
              JSON.parse(chunkValue).sourceDocuments;
            return { ...state, messages: [...messages] };
          });
        } else {
          pending += chunkValue;
          setMessageState((state) => {
            let messages = state.messages;
            messages[messages.length - 1].message = pending;
            return { ...state, messages: [...messages] };
          });
        }
      }
      setLoading(false);

      //scroll to bottom
      //messageListRef.current?.scrollTo(0, messageListRef.current.scrollHeight);
    } catch (error) {
      setLoading(false);
      setError("An error occurred while fetching the data. Please try again.");
    }
  }

  //prevent empty submissions
  const handleEnter = (e: any) => {
    if (e.key === "Enter" && query) {
      handleSubmit(e);
    } else if (e.key == "Enter") {
      e.preventDefault();
    }
  };

  return (
    <Page title="Chatbot prototype">
      <>
        {error && (
          <>
            <div
              className="govuk-error-summary"
              data-module="govuk-error-summary"
            >
              <div role="alert">
                <h2 className="govuk-error-summary__title">
                  There is a problem
                </h2>
                <div className="govuk-error-summary__body">
                  <ul className="govuk-list govuk-error-summary__list">
                    <li>
                      <a href="#">{error}</a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </>
        )}

        <div className={"govuk-body"}>
          <div className={styles.chat}>
            <div ref={messageListRef} className={styles.messagelist}>
              {messages.map((message, index) => {
                let icon;
                let className;

                if (message.type === "apiMessage") {
                  icon = <RobotIcon height="1.1em" fill="#1d70b8" />;
                  className = styles.apimessage;
                } else {
                  icon = <UserIcon height="1.1em" fill="	#00703c" />;
                  // The latest message sent by the user will be animated while waiting for a response
                  className =
                    loading && index === messages.length - 1
                      ? styles.usermessagewaiting
                      : styles.usermessage;
                }
                return (
                  <>
                    <div
                      key={`chatMessage-${index}`}
                      className={classNames("govuk-body", className)}
                    >
                      {icon}
                      <div className={styles.markdownanswer}>
                        <ReactMarkdown>{message.message}</ReactMarkdown>
                      </div>
                    </div>
                  </>
                );
              })}
            </div>
          </div>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="govuk-form-group govuk-form-group--error">
            <h1 className="govuk-label-wrapper">
              <label className="govuk-label govuk-label--l" htmlFor="question">
                What is your question?
              </label>
            </h1>
            <div id="question-hint" className="govuk-hint">
              Ask whatever question you like...
            </div>

            <p id="more-detail-error" className="govuk-error-message">
              <span className="govuk-visually-hidden">Error:</span> Enter a
              question
            </p>

            <textarea
              className="govuk-textarea"
              disabled={loading}
              onKeyDown={handleEnter}
              ref={textAreaRef}
              autoFocus={false}
              rows={3}
              maxLength={5000}
              id="userInput"
              name="userInput"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              aria-describedby="question-hint"
            />

            <button
              className="govuk-button"
              disabled={loading}
              data-module="govuk-button"
            >
              Send
              {loading && (
                <div className={styles.loadingwheel}>
                  <LoadingDots color="#000" />
                </div>
              )}
            </button>
          </div>
        </form>
      </>
    </Page>
  );
}

export default Home;

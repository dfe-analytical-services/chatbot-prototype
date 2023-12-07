import { useEffect, useRef, useState } from 'react';
import styles from '@/styles/Home.module.css';
import LoadingDots from '@/components/LoadingDots';
import { UseChatbotState } from '@/hooks/useChatbot';
import ErrorSummary from '@/components/ErrorSummary';

const UserInputDialog = ({ sendMessage, error: APIError, fetching }: Props) => {
  const [query, setQuery] = useState<string>('');
  const [userInputError, setUserInputError] = useState<string | null>(null);
  const textAreaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    textAreaRef.current?.focus();
  }, []);

  async function handleSubmit() {
    if (!query) {
      setUserInputError('Enter a question');
      return;
    }

    setUserInputError(null);

    const question = query.trim();

    await sendMessage(question);
  }

  //prevent empty submissions
  const handleEnter = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && query) {
      handleSubmit();
    } else if (e.key == 'Enter') {
      e.preventDefault();
    }
  };

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        handleSubmit();
      }}
    >
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
          <span className="govuk-visually-hidden">Error:</span> Enter a question
        </p>

        {userInputError && <ErrorSummary error={userInputError} />}
        <textarea
          className="govuk-textarea"
          disabled={fetching || APIError !== null}
          onKeyDown={handleEnter}
          ref={textAreaRef}
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
          disabled={fetching}
          data-module="govuk-button"
        >
          Send
          {fetching && (
            <div className={styles.loadingwheel}>
              <LoadingDots color="#000" />
            </div>
          )}
        </button>
      </div>
    </form>
  );
};

interface Props extends Omit<UseChatbotState, 'messages'> {}

export default UserInputDialog;

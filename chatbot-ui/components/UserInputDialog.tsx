import { useEffect, useRef, useState } from 'react';
import { UseChatbotState } from '@/hooks/useChatbot';
import ErrorSummary from '@/components/ErrorSummary';
import classNames from 'classnames';

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
    setQuery('');
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <form
      id="user-input-form"
      onSubmit={(e) => {
        e.preventDefault();
        handleSubmit();
        setQuery('');
      }}
    >
      <div
        className={classNames('govuk-form-group', {
          'govuk-form-group--error': userInputError,
        })}
      >
        <h1 className="govuk-label-wrapper">
          <label className="govuk-label govuk-label--l" htmlFor="userInput">
            What is your question?
          </label>
        </h1>
        <div id="question-hint" className="govuk-hint">
          Ask a question relevant to the Explore Education Statistics service...
        </div>

        {userInputError && <ErrorSummary error={userInputError} />}
        <textarea
          className="govuk-textarea"
          disabled={fetching || APIError !== null}
          onKeyDown={handleKeyDown}
          ref={textAreaRef}
          rows={3}
          maxLength={5000}
          id="userInput"
          name="userInput"
          value={query}
          onBlur={() => {
            if (query) {
              setUserInputError(null);
            }
          }}
          onChange={(e) => {
            setQuery(e.target.value);
          }}
          aria-describedby="question-hint"
        />

        <button
          className="govuk-button"
          disabled={fetching}
          data-module="govuk-button"
        >
          Send
        </button>
      </div>
    </form>
  );
};

interface Props extends Omit<UseChatbotState, 'messages'> {}

export default UserInputDialog;

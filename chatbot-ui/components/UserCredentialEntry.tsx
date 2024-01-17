import classNames from 'classnames';
import { useEffect } from 'react';
import { SubmitHandler, useForm } from 'react-hook-form';

interface AuthData {
  password: string;
}

const UserCredentialEntry = ({ onCorrectEntry, authPassword }: Props) => {
  const {
    register,
    formState: { errors },
    setError,
    handleSubmit,
    setFocus,
  } = useForm<AuthData>();

  useEffect(() => {
    setFocus('password');
  }, [setFocus]);

  const onSubmit: SubmitHandler<AuthData> = (data) => {
    if (data.password === authPassword) {
      onCorrectEntry();
    } else {
      setError('password', { message: 'Incorrect password', type: 'wrong' });
    }
  };

  return (
    <form id="user-input-form" onSubmit={handleSubmit(onSubmit)}>
      <div className={classNames('govuk-form-group')}>
        <div className="govuk-form-group">
          <h1 className="govuk-label-wrapper">
            <label
              className="govuk-label govuk-label--l"
              htmlFor="auth-password"
            >
              Please enter the password
            </label>
          </h1>
          <div id="account-number-hint" className="govuk-hint">
            This service is still a prototype - access is restricted.
          </div>
          {errors.password?.type === 'wrong' && (
            <p id="passport-issued-error" className="govuk-error-message">
              <span className="govuk-visually-hidden">Error:</span>The password
              was incorrect
            </p>
          )}
          {errors.password?.type === 'required' && (
            <p id="passport-issued-error" className="govuk-error-message">
              <span className="govuk-visually-hidden">Error:</span>A password is
              required
            </p>
          )}
          <input
            {...register('password', {
              required: true,
            })}
            className="govuk-input"
            id="auth-password"
            name="password"
            type="password"
          />
        </div>
        <br />
        <button className="govuk-button" data-module="govuk-button">
          Enter
        </button>
      </div>
    </form>
  );
};

interface Props {
  onCorrectEntry: () => void;
  authPassword?: string;
}

export default UserCredentialEntry;

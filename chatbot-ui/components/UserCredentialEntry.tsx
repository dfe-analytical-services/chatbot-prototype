import authenticateCredentials, {
  EESCredential,
} from '@/services/auth-service';
import classNames from 'classnames';
import { SubmitHandler, useForm } from 'react-hook-form';

const UserCredentialEntry = ({ onCorrectEntry }: Props) => {
  const {
    register,
    formState: { errors },
    setError,
    handleSubmit,
  } = useForm<EESCredential>();

  const onSubmit: SubmitHandler<EESCredential> = (data) => {
    if (authenticateCredentials(data)) {
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
              Please sign in
            </label>
          </h1>
          <div id="account-number-hint" className="govuk-hint">
            This service is still a prototype - access is restricted.
          </div>
          <div className="govuk-form-group">
            <label className="govuk-label" htmlFor="auth-username">
              Username
            </label>
            {errors.username?.type === 'required' && (
              <p id="passport-issued-error" className="govuk-error-message">
                <span className="govuk-visually-hidden">Error:</span>A username
                is required
              </p>
            )}
            <input
              {...register('username', {
                required: true,
              })}
              className="govuk-input"
              id="auth-username"
              name="username"
              type="text"
            />
          </div>
          <div className="govuk-form-group">
            <label className="govuk-label" htmlFor="auth-password">
              Password
            </label>
            {errors.password?.type === 'wrong' && (
              <p id="passport-issued-error" className="govuk-error-message">
                <span className="govuk-visually-hidden">Error:</span>The
                password was incorrect
              </p>
            )}
            {errors.password?.type === 'required' && (
              <p id="passport-issued-error" className="govuk-error-message">
                <span className="govuk-visually-hidden">Error:</span>A password
                is required
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
}

export default UserCredentialEntry;

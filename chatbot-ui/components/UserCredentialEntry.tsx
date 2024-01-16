import classNames from 'classnames';
import { SubmitHandler, useForm } from 'react-hook-form';

interface AuthData {
  password: string;
}

const UserCredentialEntry = ({ onCorrectEntry, passwordRequired }: Props) => {
  const {
    register,
    formState: { errors },
    setError,
    handleSubmit,
  } = useForm<AuthData>();

  const onSubmit: SubmitHandler<AuthData> = (data) => {
    if (data.password === passwordRequired) {
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
          {errors.password?.type === 'wrong' && (
            <p role="alert">Password was incorrect</p>
          )}
          {errors.password?.type === 'required' && (
            <p role="alert">Password required</p>
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
  passwordRequired: string;
}

export default UserCredentialEntry;

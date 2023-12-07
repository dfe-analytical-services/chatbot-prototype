const ErrorSummary = ({ error }: Props) => {
  return (
    <div className="govuk-error-summary" data-module="govuk-error-summary">
      <div role="alert">
        <h2 className="govuk-error-summary__title">There is a problem</h2>
        <div className="govuk-error-summary__body">
          <ul className="govuk-list govuk-error-summary__list">
            <li>
              <a href="#">{error}</a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

interface Props {
  error: string;
}

export default ErrorSummary;

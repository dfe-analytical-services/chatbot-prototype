// TODO: Improve this component (I have only naively copied across what was already in app)
// I don't think this needs to be a list, nor an anchor tag. Or alternatively we take an actual list of errors in the props.
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

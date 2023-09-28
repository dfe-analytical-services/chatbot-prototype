import React from "react";

interface Props {
  caption?: string;
  title: string;
}

const PageTitle = ({ caption, title }: Props) => {
  return (
    <>
      {caption && <span className="govuk-caption-xl">{caption}</span>}

      <h1 className="govuk-heading-xl">{title}</h1>
    </>
  );
};

export default PageTitle;

FROM python:3.12-slim as base

# Setup env
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

FROM base as builder

RUN pip install pipenv

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base as runtime

# Copy virtual env from builder
COPY --from=builder /app/.venv .venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy the app
COPY data_ingestion data_ingestion

# Create and switch to a new user
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "data_ingestion.main:app", "--host", "0.0.0.0", "--port", "8000"]
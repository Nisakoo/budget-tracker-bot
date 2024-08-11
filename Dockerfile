# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11-slim AS builder

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY poetry.lock pyproject.toml ./

# Install poetry 1.7.1
RUN pip install -U pip setuptools \
    && pip install --no-cache-dir poetry==1.7.1 \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi


FROM python:3.11-slim

COPY --from=builder /app /app
ADD src ./

ENV PATH="/app/.venv/bin"

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "main.py"]

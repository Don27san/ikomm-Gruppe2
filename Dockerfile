FROM python:3.13

WORKDIR /app

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Copy Pipenv files
COPY Pipfile Pipfile.lock ./

# Generate a fresh Pipfile.lock for the Linux environment and install dependencies
# This is important to ensure platform-specific dependencies are correctly resolved.
RUN pipenv install --deploy

# Copy the rest of your code
COPY . .

CMD ["pipenv", "run", "client-prod"]
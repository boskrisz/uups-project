FROM python:3.12

# Add a work directory
WORKDIR /uups-post-migrator

# Install the dependencies first, as they change less frequently
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

# Copy the application code
COPY ./app ./app

# Run the application
ENTRYPOINT ["sh", "-c", "python -m app"]
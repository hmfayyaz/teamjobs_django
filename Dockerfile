# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11
ARG requirements=requirements.txt
EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements

COPY ${requirements} /tmp/requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm -f /tmp/requirements.txt \
    && python -m pip install --no-cache-dir git+https://github.com/benoitc/gunicorn.git@792edf6 \
    && adduser -u 5678 --disabled-password --gecos "" --home /app appuser \
    && install -d -m 0755 -o appuser -g appuser /app/static \
    && install -d -m 0755 -o appuser -g appuser /app/media

USER appuser:appuser

WORKDIR /app
COPY --chown=appuser:appuser . /app
RUN chmod +x docker/*.sh

VOLUME /app/static
VOLUME /app/media
ENV DJANGO_ENV=production

ENTRYPOINT [ "/app/docker/entrypoint.sh" ]
CMD [ "/app/docker/start.sh", "server"]

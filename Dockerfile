FROM python:3.10.8-alpine
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /app
RUN chmod 777 "/app/docker-entrypoint.sh"
CMD ["/app/docker-entrypoint.sh"]
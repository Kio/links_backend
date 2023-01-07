FROM python:3.10.8-alpine
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
RUN apk update && apk add nspr nss libx11 libxcb libxcomposite libxcursor libxdamage libxext libxfixes libxi libxrender libxtst icu-libs cups-libs dbus-libs libxscrnsaver libxrandr glib alsa-lib pango cairo libatk-1.0 libatk-bridge-2.0 gtk+3.0 gdk-pixbuf libgcc gcompat chromium
COPY . /app
RUN chmod 777 "/app/docker-entrypoint.sh"
CMD ["/app/docker-entrypoint.sh"]
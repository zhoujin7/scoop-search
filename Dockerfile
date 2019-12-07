FROM python:3.7-slim
WORKDIR /opt/scoop-search
COPY . .
RUN pip install -r requirements.txt
ENV GITHUB_WEBHOOK_SECRET github_webhook_secret
EXPOSE 8080
CMD ["gunicorn", "app:app", "-c", "gunicorn_conf.py"]

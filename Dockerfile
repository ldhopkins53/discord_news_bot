FROM ubuntu:latest

COPY . /app
RUN apt update && apt install -y python3 python3-pip && pip install -r requirements.txt
ENTRYPOINT ["python3", "/app/bot.py", "--config_file", "bot_config.ini"]

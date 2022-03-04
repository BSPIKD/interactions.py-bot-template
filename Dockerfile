FROM python:3.8.6

# Zapnutí logování v consoli
ENV PYTHONUNBUFFERED="true"

# V případě použití mariadb je potřeba naistalovat libmariadb3 a libmariadb-dev
RUN apt-get -y update && apt-get install -y libmariadb3 libmariadb-dev

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "bot.py"]
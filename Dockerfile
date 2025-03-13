# Определяем основной образ
FROM python:3.4

# Переменная окружения для того, чтобы uWSGI заработал без ошибок
ENV CFLAGS="-Wno-error"

# Запускаем заданную инструкцию внутри контейнера
RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
RUN pip install Flask==0.10.0 uWSGI==2.0.8 requests==2.5.1 redis==2.10.3
# Определяем рабочий каталог для последующих инструкций
WORKDIR /app
# Копируем содержимое наших каталогов в каталог образа
COPY app /app
COPY cmd.sh /

# Объявляем порты доступные для хоста и других контейнеров
EXPOSE 9090 9191
# Определяем имя пользователя для последующих строк (в том числе и CMD)
USER uwsgi

# Запускаем данную инструкцию во время инициализации контейнера
CMD [ "/cmd.sh" ]

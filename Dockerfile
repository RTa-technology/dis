# pull official base image
FROM python:3.9.6-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


ENV LC_CTYPE='C.UTF-8'
ENV TZ='Asia/Tokyo'
ENV DEBIAN_FRONTEND=noninteractive



# create Django directory for the app user
ENV BOT_HOME=/usr/src/bot
RUN mkdir -p $BOT_HOME

# create the app user
RUN addgroup -S bot && adduser -S bot -G bot

# set work directory
WORKDIR $BOT_HOME

# install dependencies
COPY ./requirements.txt .
COPY ./iachara/ ./iachara/

RUN apk update && \
    apk add postgresql-dev gcc python3-dev build-base musl-dev libpq g++ git

RUN cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    pip install --upgrade pip  setuptools wheel greenlet && \
    pip install -r requirements.txt && \
    pip install -U git+https://github.com/Rapptz/discord.py && \
    pip install ./iachara
    
RUN apk del build-base  && \
    rm -rf /var/cache/apk/*

# copy entrypoint shell file
COPY ./bot.sh $BOT_HOME

# copy project
COPY . $BOT_HOME

# chown all the files to the app user
RUN chown -R bot:bot $BOT_HOME

# change to the app user
USER bot

# run entrypoint shell file
ENTRYPOINT ["/usr/src/bot/bot.sh"]
FROM mongo:latest
COPY /auth/mongodb-keyfile /data
RUN chmod 400 /data/mongodb-keyfile
RUN chown 999:999 /data/mongodb-keyfile
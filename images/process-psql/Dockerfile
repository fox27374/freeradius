FROM python:3.9-alpine

ARG USER=processpsql
ARG USERID=1100
ARG GROUP=processpsql
ARG GROUPID=2100
ARG HOME=/home/$USER

# Create user and group
RUN \
addgroup -g $GROUPID $GROUP \
&& adduser --uid $USERID -G $GROUP -h $HOME -D $USER

# Install additional software
#RUN \ 
#apk add -q --no-cache \
#libpq-dev \
#gcc \
#libc-dev \
#&& rm -rf /tmp/* /var/cache/apk/*

WORKDIR $HOME
COPY --chown=root:$GROUP process-psql/requirements.txt .
RUN pip install -r requirements.txt

COPY --chown=root:$GROUP process-psql/process-psql.py .
RUN chmod g+x process-psql.py

USER $USER
#ENTRYPOINT ["entrypoint.sh"] 
CMD ["python", "process-psql.py"]

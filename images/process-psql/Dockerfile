FROM python:3.9-alpine

ARG USER=process-psql
ARG USERID=1100
ARG GROUP=process-psql
ARG GROUPID=2100
ARG HOME=/home/$USER

# Create user and group
RUN \
addgroup -g $GROUPID $GROUP \
&& adduser --uid $USERID -G $GROUP -h $HOME -D $USER

# Install additional software
RUN \ 
apk add -q --no-cache \
libpq-dev \
gcc \
libc-dev \
&& rm -rf /tmp/* /var/cache/apk/*

WORKDIR $HOME

COPY --chown=root:$GROUP process-psql/requirements.txt .
COPY --chown=root:$GROUP process-psql/process-psql.py .
RUN \
chmod u+x process-psql.py \
&& pip install -r requirements.txt

#ENTRYPOINT ["entrypoint.sh"] 
CMD ["sleep 3000"]

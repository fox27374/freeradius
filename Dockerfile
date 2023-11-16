FROM alpine:latest

# Install freeradius with the postgresql module
RUN apk add -q --no-cache bash freeradius freeradius-radclient freeradius-postgresql freeradius-sqlite tzdata \
    && rm -rf /tmp/* /var/cache/apk/*

ARG USER=radius
ARG GROUP=radius
ARG HOME=/home/$USER
ENV PATH="$PATH:/usr/local/bin"
ENV DEBUG=false
ENV RADIUSD_OPTS=

# Create user and group
#RUN addgroup -g $GROUPID $GROUP
#RUN adduser --uid $USERID -G $GROUP -h $HOME -D $USER
#RUN addgroup $USER $GROUP

# Use new directory and user
WORKDIR $HOME
USER $USER

#COPY --chown=$USER:$GROUP entrypoint.sh .
COPY --chown=$USER:$GROUP entrypoint.sh /usr/local/bin/

RUN chmod u+x /usr/local/bin/entrypoint.sh

EXPOSE 1812/udp 1813/udp
ENTRYPOINT ["entrypoint.sh"] 
CMD ["radiusd"]

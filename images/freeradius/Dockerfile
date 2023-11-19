FROM alpine:latest

ARG USER=radius
ARG USERID=1100
ARG GROUP=radius
ARG GROUPID=2100
ARG HOME=/home/$USER
ENV PATH="$PATH:/usr/local/bin"
ENV DEBUG=false
ENV RADIUSD_OPTS=

# Create user and group
RUN \
addgroup -g $GROUPID $GROUP \
&& adduser --uid $USERID -G $GROUP -h $HOME -D $USER

# Install freeradius with the postgresql module
RUN \ 
apk add -q --no-cache \
bash \
freeradius \
freeradius-postgresql \
freeradius-sqlite \
&& rm -rf /tmp/* /var/cache/apk/*

COPY --chown=root:$GROUP freeradius/entrypoint.sh /usr/local/bin/
COPY --chown=root:$GROUP freeradius/sql /etc/raddb/mods-available/
RUN chmod u+x /usr/local/bin/entrypoint.sh

WORKDIR /etc/raddb/mods-enabled
RUN ln -sf ../mods-available/sql sql
WORKDIR $HOME

EXPOSE 1812/udp 1813/udp
ENTRYPOINT ["entrypoint.sh"] 
CMD ["radiusd"]

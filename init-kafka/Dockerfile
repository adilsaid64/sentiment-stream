FROM confluentinc/cp-kafka:7.4.0

WORKDIR /init-kafka

COPY init-kafka.sh /init-kafka.sh
# RUN chmod +x /init-kafka.sh
COPY --chmod=0755 init-kafka.sh /init-kafka.sh

CMD ["/bin/bash", "/init-kafka.sh"]

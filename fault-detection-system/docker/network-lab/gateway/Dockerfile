FROM alpine:latest
RUN apk add --no-cache python3 iproute2 iptables
COPY run.py /app/run.py
WORKDIR /app
CMD ["python3", "run.py"]
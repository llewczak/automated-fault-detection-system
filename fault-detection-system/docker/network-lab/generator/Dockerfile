FROM alpine:latest
RUN apk add --no-cache iproute2 python3 py3-numpy
COPY run.py /app/run.py
WORKDIR /app
CMD ["python3", "run.py"]
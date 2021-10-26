FROM python:3.8-alpine

# Dependencies for python-bitcoinlib and sanity check.
RUN apk --no-cache add \
      binutils \
      libressl-dev \
      openssl-dev && \
    python -c "import ctypes, ctypes.util; ctypes.cdll.LoadLibrary(ctypes.util.find_library('ssl') or 'libeay32')"

RUN pip install --no-cache-dir \
        prometheus_client \
        python-bitcoinlib \
        riprova

ADD ./monitor.py /

USER nobody

ENV PROMETHEUS_PORT "$PROMETHEUS_PORT"
ENV LBCCTL_PATH "$LBCCTL_PATH"

CMD ["/monitor.py"]

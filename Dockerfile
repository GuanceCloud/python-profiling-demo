FROM python:3.8

WORKDIR /usr/local/python-profiling-demo
COPY . ./
RUN pip install --no-cache-dir -r requirements.txt
CMD DD_ENV=demo DD_SERVICE=python-profiling-demo DD_VERSION=v0.0.1 DD_PROFILING_ENABLED=true DD_AGENT_HOST=localhost DD_TRACE_AGENT_PORT=9529 ddtrace-run python server.py

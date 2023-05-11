FROM python:3.10.11-bullseye
LABEL authors="guance.com" \
      email="zhangyi905@guance.com"
WORKDIR /usr/local/python-profiling-demo
COPY . ./
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

ENV DD_SERVICE "python-profiling-demo"
ENV DD_VERSION "v0.0.1"
ENV DD_ENV testing
ENV DD_AGENT_HOST datakit
ENV DD_TRACE_AGENT_PORT 9529

CMD DD_PROFILING_ENABLED=true ddtrace-run python server.py

FROM python:3.8
LABEL authors="guance.com" \
      email="zhangyi905@guance.com"
WORKDIR /usr/local/python-profiling-demo
COPY . .
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
RUN pip cache purge

CMD DD_ENV=test DD_SERVICE=python-profiling-demo DD_VERSION=v0.0.1 DD_PROFILING_ENABLED=true DD_AGENT_HOST=datakit DD_TRACE_AGENT_PORT=9529 ddtrace-run python server.py

#!/usr/bin/env bash

DD_SERVICE="python-profiling-demo" DD_VERSION="v0.0.1" DD_ENV=testing DD_AGENT_HOST=127.0.0.1 DD_TRACE_AGENT_PORT=9529 DD_LOGS_INJECTION=true DD_PROFILING_ENABLED=true ddtrace-run gunicorn -w 4 --bind 0.0.0.0:8080 app:app

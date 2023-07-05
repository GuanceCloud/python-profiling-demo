#!/usr/bin/env bash

DD_SERVICE="python-profiling-demo" DD_VERSION="v0.0.1" DD_ENV=testing DD_TRACE_AGENT_PORT=9529 DD_LOGS_INJECTION=true DD_PROFILING_ENABLED=true ddtrace-run python3.10 server.py

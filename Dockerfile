FROM python:3.8

WORKDIR /usr/local/python-profiling-demo
COPY . ./
RUN pip install --no-cache-dir -r requirements.txt

ARG DK_DATAWAY=https://openway.guance.com?token=tkn_f5b2989ba6ab44bc988cf7e2aa4a6de3

RUN DK_DATAWAY=${DK_DATAWAY} bash -c "$(curl -L https://static.guance.com/datakit/install.sh)"
CMD /bin/sh run.sh

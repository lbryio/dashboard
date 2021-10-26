run with:

```
pip3 install prometheus_client
LBCCTL_PATH=/home/ubuntu/lbcd/lbcctl PROMETHEUS_PORT=2114 python3.7 monitor.py  &
```

everything else is WIP and copied from https://github.com/jvstein/bitcoin-prometheus-exporter

docker stuff is unfinished. here's where i left off:

to build: `docker build -t lbcd-monitor .`

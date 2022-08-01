# LBRY Dashboard

Important metrics:

- num of peers
  - [x] blockchain (nodes.madiator.com)
  - [ ] dht
  - [ ] apps?
- space
  - [ ] storage space allocated to network
  - [ ] storage space used by network
  - [ ] % of downloads coming from reflector
- activity
  - [ ] total claims and identities
  - [ ] claims / week
  - [ ] txns
  - [ ] weekly active addresses



## notes to self

make sure you `ufw allow to 172.17.0.1/16` so that prometheus can access the host

https://stackoverflow.com/questions/64768618/ufw-forbids-docker-container-to-connect-to-postgres


requires CSV plugin: https://github.com/marcusolsson/grafana-csv-datasource

then import `dashboards/grafana-dashboard.json`


## madiator's dashboard

needs plugin https://grafana.com/grafana/plugins/yesoreyeram-infinity-datasource/

after adding, set the name to "nodes.madiator.com" so they match the dashboard json

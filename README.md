# Web-KPI

This page summarizes how to extract Key performance indicator (KPI) 
for web services (web portal or RestFul APIs) hosted by several web
servers (typically Nginx and Apache) using GoAccess.

## Introduction

Servers usually log every access and error in specific directories
typically located under `/var/log` in Ubuntu. For instance:

| Server:          | Nginx                       | Apache                        |
|------------------|-----------------------------|-------------------------------|
| Access log file: | `/var/log/nginx/access.log` | `/var/log/apache2/access.log` |
| Error log file:  | `/var/log/nginx/error.log`  | `/var/log/apache2/error.log`  |


In Ubuntu, you might see also several g-zipped files, e.g.
`access.1.log.gz`, `access.2.log.gz`, and so on. These are files
created by the utility `logrotate` which regularly checks
and optimizes spaces on disk by compressing old log files
(you can check out the settings in `/etc/logrotate.d/`)

## GoAccess

GoAccess is the quickest solution for creating a simple report in HTML
from a given access log. Contrarily to Matomo, it works also without HTML,
it does not require JavaScript injection, but it might need some workaround
to catch specific metrics from the report, which is packed with a lot of 
info.


First Install GoAccess (`brew install goaccess` on macos, see 
[here](https://goaccess.io/download) otherwise)


### Create HTML Web Analytics report (`report.html`)

Assuming you are in the log directory:

1. To create an HTML report of **all log files** (compressed and uncompressed):
   ```commandline
   zcat -f access.log* | goaccess -o report2.html --ignore-crawlers --log-format=COMBINED
   ```
2. To create an HTML report of **the most recent log file only**:
   ```commandline
   goaccess access.log -o report.html --ignore-crawlers --log-format=COMBINED
   ```
(for info on the pipe command see [here](https://stackoverflow.com/a/39240021))

Manual page of GoAccess (all commands and examples):
[GoAccess Man Page](https://goaccess.io/man)

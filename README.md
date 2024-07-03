# Web-KPI-memo

Key performance inicators (KPI) for web services can be extracted in several ways, usually
via analytics tools. In this document, we shortly describe how to install and run [GoAccess](https://goaccess.io/man), 
an analytics tool that parses and collect data from the server access logs.

<details>

   <summary>Compare with Google analytics and Matomo (click for details)</summary>
   
   PROs:
   
   1. Privacy (100% data ownership, as Matomo) and full control over what can be disseminated or not
   
   2. No injection of JavaScript code in your hosted HTML, which in turn allows to:

      2a. Keep core and analytics codebase separated

      2b. Track each request, not only HTML pages. In other words, track access to URLs serving any data format (e.g. RestFul APIs URLs)
   
   CONs:
   
   1. By tracking the server log, a lot of noise might be included in the final report (see e.g. by [web crawlers](https://en.wikipedia.org/wiki/Web_crawler)).
      See option `--ignore-crawlers` below or the [filtering the logs](#Filtering-server-logs)) section. In any case, you might still need some workaround to extract
      the KPIs you need
   
   3. In several cases, some knoweledge of [server logs might be required](#Servers-logging)

</details>

First Install GoAccess (`brew install goaccess` on macos, see [here](https://goaccess.io/download) otherwise).

Then, assuming you are in the [log directory](#Servers-logging), and that the directory contains a GeoIP database named `dbip-country-lite.mmdb` (see [Download GeoIP database](#download-geoip-database) for info.
For ref, a database file is included in this repo, but it is not regularly updated)

1. To create an HTML report of **all log files**, compressed and uncompressed (Explanation [here](https://stackoverflow.com/a/39240021)):
   ```commandline
   zcat -f access.log* | goaccess -o report.html -q --log-format=COMBINED --ignore-crawlers --anonymize-ip --geoip-database=dbip-country-lite.mmdb
   ```
2. To create an HTML report of **the most recent log file only**:
   ```commandline
   goaccess access.log -o report.html -q --log-format=COMBINED --ignore-crawlers --anonymize-ip --geoip-database=dbip-country-lite.mmdb
   ```

**All parameters explanation and examples can be found in the [GoAccess Man Page](https://goaccess.io/man)**


## Appendix

<img align="right" width="350" src="https://github.com/rizac/web-KPI-memo/blob/main/server-access-report-example.jpg?raw=true" />


### Example report

This repository contains an example server access report, converted as image 
for illustrative purposes and embedded in this document (see image on the right) 


### Download GeoIP Database

A GeoIP database is a database mapping IPs to a Geo location, allowing to know the provenance of the 
IPs accessing your web service. To get a GeoIP database:

- Download the IP to Country database *in MMDB format* from here: https://db-ip.com/db/download/ip-to-country-lite
  (one copy also in this repo, but is is not updated regularly).
  You can also download other databases (e.g., IP to city and so on).

- Unzip the file (`gunzip <file_name>.mmdb.gz`) and then pass the unzipped name/full path as `--geoip-database` argument 

See also [Geolocation options in the GoAccess man page](https://goaccess.io/man)


### Servers logging


Servers usually log every access request and error request in specific **log directories**
typically located under `/var/log/` in Ubuntu. For instance:

  |                     | Nginx                       |
  |---------------------|-----------------------------|
  | Access log file:    | `/var/log/nginx/access.log` |
  | Error log file:     | `/var/log/nginx/error.log`  |
  | logrotate file:     | `/etc/logrotate.d/nginx`    |

  
  |                     | Apache                        |
  |---------------------|-------------------------------|
  | Access log file:    | `/var/log/apache2/access.log` |
  | Error log file:     | `/var/log/apache2/error.log`  |
  | logrotate file:     | `/etc/logrotate.d/apache2`    |


<!--
| Server:             | Nginx                       | Apache                        |
|---------------------|-----------------------------|-------------------------------|
| Access log file:    | `/var/log/nginx/access.log` | `/var/log/apache2/access.log` |
| Error log file:     | `/var/log/nginx/error.log`  | `/var/log/apache2/error.log`  |
| logrotate file:     | `/etc/logrotate.d/nginx`    | `/etc/logrotate.d/apache2`    |
-->


#### Logrotate

In Ubuntu, alongside `access.log` you might see also several g-zipped files, e.g.
`access.1.log.gz`, `access.2.log.gz`. These files are created by the system utility 
[logrotate](https://linux.die.net/man/8/logrotate)

`logrotate` can be configured for both Nginx and Apache. Config files
are usually located under `/etc/logrotate.d/` and can be easily modified [with no need to restart anything](https://unix.stackexchange.com/a/620676).
For instance, here below the content of the file `/etc/logrotate.d/nginx`
shows how `logrotate` is configured to rename and compress (`compress`) 
every day (`daily`) 
any file matching `/var/log/nginx/*.log`
only if not empty (`notifempty`),
eventually deleting it after 14 days (`rotate 14`):

```
      /var/log/nginx/*.log {
        daily
        missingok
        rotate 14
        compress
        delaycompress
        notifempty
        create 0640 www-data adm
        sharedscripts
        prerotate
                if [ -d /etc/logrotate.d/httpd-prerotate ]; then \
                        run-parts /etc/logrotate.d/httpd-prerotate; \
                fi \
        endscript
        postrotate
                invoke-rc.d nginx rotate >/dev/null 2>&1
        endscript
      }
```

If you need to extract yearly-based KPIs, i.e., run analytics on the logs of the last year, then
you could set `rotate 365` or, to keep less files, set `weekly` instead of `daily` and `rotate 55` (or any number >=54). 
In any case, remember that the main goal of logrotate is to optimize the amount of log files and space. If your site has a high
traffic, be careful with the settings.

Please [**read the man page of logrotate**](https://linux.die.net/man/8/logrotate) for further info.


### Filtering server logs 

If your report still contains a lot of noise (even with the `--ignore-crawlers` option activated), you can filter
server logs beforehand before feeding GoAccess. See a nice article [here](https://www.philnewton.net/blog/filtering-referer-spam/)

### Copy log files locally

(replace `local_access_log_dir` with the path of your destination directory)

- Nginx:
  ```
  rsync -havz "user@host:/var/log/nginx/access.log*" local_access_log_dir
  ```
- Apache:
  ```
  rsync -havz "user@host:/var/log/apache2/access.log*" local_access_log_dir
  ```

**Note**
  The trailing slash on `local_access_log_dir` is **irrelevant**. 
  For ref (not the case in the examples above), a  trailing slash on a source path means "copy the contents of this directory", 
  without a trailing slash it means "copy the directory".

  Here e alink for a useful [shell interactive explanation tool](https://explainshell.com/explain?cmd=rsync+-havz+--delete+user%40remote.host%3A%2Fpath%2Fto%2Fcopy+%2Fpath%2Fto%2Flocal%2Fstorage)

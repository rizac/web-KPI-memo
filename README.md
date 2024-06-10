# Web-KPI-memo

Key performance inicators (KPI) for web services can be extracted in several ways, usually
via web service analytics tools.

In this document, we shortly describe how to install and run [GoAccess](https://goaccess.io/man), 
an analytics tool that parses and collect data from the server access logs.

<details>

   <summary>With respect to other analytics tools that were investigated (Google analytics, Matomo)
   the procedure described is more low-level and generally simpler (click for details)</summary>
   
   PROs:
   
   1. Privacy (100% data owneership) and full control over what can be disseminated or not
   
   2. No injection of JavaScript code in your hosted HTML, which in turn allows to:

      2a. Keep core and analytics codebase separated

      2b. Track each request, not only HTML pages. In other words, track access to URLs serving any data format (e.g. RestFul APIs URLs)
   
   CONs:
   
   1. By tracking the server log and not single HTML pages, a lot of noise might be generated (e.g. by [web crawlers](https://en.wikipedia.org/wiki/Web_crawler)).
      Although with some settings the output can be cleaned up, users might need to spend some time filtering the final report page
   
   2. In several cases, some knoweledge of [server logs might be required](#Servers-Logging-and-logrotate)

</details>

First Install GoAccess (`brew install goaccess` on macos, see [here](https://goaccess.io/download) otherwise).

Assuming you are in the [log directory](#Servers-Logging-and-logrotate), and that the directory contains a GEoIP database named `dbip-country-lite.mmdb` (see [Download GeoIP database](#download-geoip-database) for info.
For ref, a database file is included in this repo, but it is not regularly updated)

1. To create an HTML report of **all log files** (compressed and uncompressed):
   ```commandline
   zcat -f access.log* | goaccess -o report.html --ignore-crawlers --log-format=COMBINED --geoip-database dbip-country-lite.mmdb
   ```
2. To create an HTML report of **the most recent log file only**:
   ```commandline
   goaccess access.log -o report.html --ignore-crawlers --log-format=COMBINED --geoip-database dbip-country-lite.mmdb
   ```
(for info on the pipe command see [here](https://stackoverflow.com/a/39240021))

Manual page of GoAccess (all commands and examples): [GoAccess Man Page](https://goaccess.io/man)


## Appendix


### Servers Logging and logrotate


Servers usually log every access request and error request in specific directories
typically located under `/var/log` in Ubuntu. For instance:

| Server:             | Nginx                       | Apache                        |
|---------------------|-----------------------------|-------------------------------|
| Access log file:    | `/var/log/nginx/access.log` | `/var/log/apache2/access.log` |
| Error log file:     | `/var/log/nginx/error.log`  | `/var/log/apache2/error.log`  |
| logrotate file [*]: | `/etc/logrotate.d/nginx`    | `/etc/logrotate.d/apache2`    |


[*] In Ubuntu, alongside `access.log` you might see also several g-zipped files, e.g.
    `access.1.log.gz`, `access.2.log.gz`, and so on. These are files
    created by the utility `logrotate` which regularly checks
    and optimizes spaces on disk by compressing old log files.
    For instance, `less /etc/logrotate.d/nginx` might show the content of a typical logrotate config. for Nginx:
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

You can change e,g, `daily` to `weekly` to log rotate every week, set `rotate 55` (or any number >= 54 in order to save at least last year with `weekly`), 
and even specify a `mail <email_address>` parameter so that the logs are sent to the email when deleted. More info [here](https://linux.die.net/man/8/logrotate)


### Download GeoIP Database

- Download the IP to Country database *in MMDB format* from here: https://db-ip.com/db/download/ip-to-country-lite
  (one copy also in this repo, but is is not updated regularly).
  You can also download other databases (e.g., IP to city and so on).

- Unzip the file (`gunzip <file_name>.mmdb.gz`) and then pass the unzipped name/full path as `--geoip-database` argument 

See also [Geolocation options in the GoAccess man page](https://goaccess.io/man)


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

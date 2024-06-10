# Web-KPI-memo

Simple Memo to obtain    
web services key performance indicators (KPI) by
visualizing the server access logs with 
[GoAccess](https://goaccess.io/man)

With respect to other analytics tools that were investigated (Google analytics, Matomo)
the process exemplified here has:

PROs:
1. Privacy (or more in general, full control over what can be disseminated or not)
2. No injection of JavaScript code in your hosted HTML, which in turn allows to:
   2a. Keep code and analytics separated
   2b. Track each request, not only HTML pages. In other words, we will be able to track access to URLs serving all possible data formats (e.g. RestFul APIs URLs)

CONs:
1. By tracking the server log and not single HTML pages, a lot of noise might be generated (e.g. by [web crawlers](https://en.wikipedia.org/wiki/Web_crawler)).
   Users will need to spend some time filtering this in the final report page
2. In several cases, some knoweledge of server logs might be required (see e.g. `logorotate` below)

   
**In a nutshell**, you can install GoAccess, go into your server log directory, and then create an HTML report of the
logs via:
```
goaccess access.log -o report.html --ignore-crawlers --log-format=COMBINED
```

However, depending on your server configuration, the command generates the analytics only for the last day/week. 
In this document, we will walk the user through a more detailed guide explaining how to customize
your analytics


## Introduction


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

You can change e,g, `daily` to `weekly` to log rotate every week, set `rotate 55` (or any number >= 54 in order to save at least last year with `weekly`), and even specify a `mail <email_address>` parameter so that the logs are sent to the email when deleted. More info [here](https://linux.die.net/man/8/logrotate)

## GoAccess

GoAccess is the quickest solution for creating a simple report from a given access log. 

First Install GoAccess (`brew install goaccess` on macos, see 
[here](https://goaccess.io/download) otherwise)


### Create HTML Web Analytics report (`report.html`)

Assuming you are in the log directory:

1. To create an HTML report of **all log files** (compressed and uncompressed):
   ```commandline
   zcat -f access.log* | goaccess -o report.html --ignore-crawlers --log-format=COMBINED
   ```
2. To create an HTML report of **the most recent log file only**:
   ```commandline
   goaccess access.log -o report.html --ignore-crawlers --log-format=COMBINED
   ```
(for info on the pipe command see [here](https://stackoverflow.com/a/39240021))

Manual page of GoAccess (all commands and examples):
[GoAccess Man Page](https://goaccess.io/man)


## Misc

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

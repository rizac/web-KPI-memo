# Server access analyzer

Simple parser for Nginx or Apache files into a simple html file with stats


## 1 Setup your server access log directory

If you are already on a server skip, your `access_log_dir` will be:
 - Nginx: /var/log/nginx
 - Apache /var/log/apache2

If you are not on a server, you need to download the server access files locally on your chosen `local_access_log_dir`:

- Nginx:
  ```
  rsync -havz "root@rz-vm153:/var/log/nginx/access.log*" local_access_log_dir
  ```
- Apache:
  ```
  rsync -havz "root@rz-vm153:/var/log/apache2/access.log*" local_access_log_dir
  ```

**Note**
  The trailing slash on `local_access_log_dir` is **irrelevant**. 
  For ref (not the case in the examples above), a  trailing slash on a source path means "copy the contents of this directory", 
  without a trailing slash it means "copy the directory".




**Now move to the access local directory**: the one created above or the server directory

If you are already on a server, just move to the access dir:
 - Nginx: /var/log/nginx
 - Apache /var/log/apache2
   

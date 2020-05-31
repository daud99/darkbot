# DARKBOT
This documentation is tested and specifically designed for debian Linux distro's!!

## Making changes to existing code in production

You can skip the first two steps if you have made no changes in DB Models

- Make sure you are at the root directory of the project 

1- Enable virtual environment
```shell script
source myprojectenv/bin/activate
```
2- Updating changes in the database
```shell script
python3 manage.py migrate
python3 manage.py makemigrations
python3 manage migrate
```
3- If you update your Django application, you can restart the Gunicorn process to pick up the changes by
```shell script
sudo systemctl restart gunicorn
```
4- If you change Gunicorn socket or service files, reload the daemon and restart the process by
```shell script
sudo systemctl daemon-reload
sudo systemctl restart gunicorn.socket gunicorn.service
```
5- If you change the Nginx server block configuration, test the configuration and then Nginx by
```shell script
sudo nginx -t && sudo systemctl restart nginx
```
## SETTING UP THE DARKBOT

### PYTHON

- By default python is installed on the kali linux, you can check python3 by simply writing
```sh
    python3
```
-  pip often doesn’t seem to work so, download by giving this command
```sh 
    sudo apt-get install python3-pip
```
```sh
    pip3
```
### Setting up Environment

```shell script
sudo -H pip3 install virtualenv
```

Make sure you are in the root directory of your project will giving below command

```shell script
virtualenv myprojectenv
```

Activating the virtual environment

```shell script
source myprojectenv/bin/activate
```
```shell script
pip install gunicorn psycopg2-binary
```
Note: When the virtual environment is activated (when your prompt has (myprojectenv) preceding it), use pip instead of pip3, even if you are using Python 3. The virtual environment’s copy of the tool is always named pip, regardless of the Python version.

### INSTALLING DEPENDENCIES

-	open terminal
```shell script
sudo apt update
```
```shell script
sudo apt install libpq-dev postgresql postgresql-contrib nginx curl
```
```shell script
cd Darkbot
```
```shell script
pip3 install -r requirements.txt
```
```shell script
apt-get install tor
```
```shell script
sudo apt-get install rabbitmq-server
```

#### NOTE!
Sometimes the apt-get install tor doesn’t work. So, what you need to do is 
-	Switch to root
```shell script
su
```
-	Change directory
```shell script
cd /
```
-	Open sources.list file
```shell script
nano /etc/apt/sources.list
```

-	add the below two links in it
 ```shell script
deb http://http.kali.org/kali kali-rolling main non-free contrib
deb-src http://http.kali.org/kali kali-rolling main non-free contrib
```
-	close file and save changes
-	Update the repository resources
```shell script
apt-get update
```
-	Now, try installing TOR
```shell script
apt-get install tor
```

If you are having issue with rabbitmq server restart it by following command
```shell script
sudo service rabbitmq-server restart
```

Hopefully! This will work and makes you feel good.

### Creating the PostgreSQL Database and User

```shell script
sudo -u postgres psql
```
```shell script
CREATE DATABASE darkbot;
```
```shell script
CREATE USER darkbot WITH PASSWORD 'darkbot';
```
```shell script
ALTER ROLE darkbot SET client_encoding TO 'utf8';
ALTER ROLE darkbot SET default_transaction_isolation TO 'read committed';
ALTER ROLE darkbot SET timezone TO 'UTC';
```
```shell script
GRANT ALL PRIVILEGES ON DATABASE darkbot TO darkbot;
```
```shell script
\q
```

### SETTING UP PROJECT

```shell script
python3 manage.py migrate
```

```shell script
python3 manage.py makemigrations
```

```shell script
python3 manage.py migrate
```

```shell script
python manage.py createsuperuser
```

Now, you can successfully login as admin with formerly provided email and password.


### STARTING SERVICES
```shell script
sudo service tor start
```

```shell script
celery -A dark_bot worker -l info
```
  
Make sure while giving the second command you are in the root folder of the project as well as the virtual environment is on if it's showing no command found kindly close and open the terminal again it will work fine.

### RUNNING SERVER IN DEVELOPMENT

```shell script
python3 manage.py runserver
```

### RUNNING SERVER IN PRODUCTION
```shell script
python3 manage.py collectstatic
```
```shell script
cd ~/darkbot
gunicorn --bind 0.0.0.0:8000 dark_bot.wsgi
```
```shell script
deactivate
```
```shell script
sudo nano /etc/systemd/system/gunicorn.socket
```
Paste below text into the gunicorn.socket
```text
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```
```shell script
sudo nano /etc/systemd/system/gunicorn.service
```
Paste below text into the gunicorn.service and make sure the paths are correct according to your project location this is my current project configuration for your refrence
```text
[Unit]

Description=gunicorn daemon

Requires=gunicorn.socket

After=network.target



[Service]

User=darkbot

Group=www-data

WorkingDirectory=/home/darkbot/code/darkbot_postgres

ExecStart=/home/darkbot/code/darkbot_postgres/myprojectenv/bin/gunicorn \

          --access-logfile - \
          
          --workers 3 \

          --bind unix:/run/gunicorn.sock \

          dark_bot.wsgi:application
          


[Install]

WantedBy=multi-user.target
```
```shell script
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```
```shell script
sudo nano /etc/nginx/sites-available/darkbot
```
```text
server {
    listen 80;
    server_name 85.195.114.172;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/darkbot/code/darkbot_postgres;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```
```shell script
sudo ln -s /etc/nginx/sites-available/darkbot /etc/nginx/sites-enabled
```
```shell script
sudo nginx -t
sudo systemctl restart nginx
```
If firewall is enable
```shell script
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'
```

Now, you can access the website by the public IP of the machine.

#### REFRENCES FOR HELP
```text
https://www.postgresql.org/download/linux/debian/
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-debian-10
```

# In case of furthur support contact me at
daud.ahmed@tranchulas.com

## Project Leader:
Daud Ahmed	

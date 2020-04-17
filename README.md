# SETTING UP THE DARKBOT
This documentation is tested and specifically designed for Kali Linux this may work on other Linux distros but not sure this documentation works or not!!

## OS
We recommend using Kali Linux latest version although you can use any other Linux distribution. 

## PYTHON

1.	By default python is installed on the kali linux, you can check python3 by simply writing
```sh
    python3
```
2.	pip often doesn’t seem to work so, download by giving this command
```sh 
    sudo apt-get install python3-pip
```
```sh
    pip3
```
## Setting up Environment

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

Note: When the virtual environment is activated (when your prompt has (myprojectenv) preceding it), use pip instead of pip3, even if you are using Python 3. The virtual environment’s copy of the tool is always named pip, regardless of the Python version.

## Setting up Database

1. Follow the instruction at below link

```shell script
https://www.postgresql.org/download/linux/debian/
```

2. Installing GUI for postgresSQL

```shell script
  apt-get install pgadmin4
```

### Note!!!

You may face error while installing pgadmin4 because many linux distrbution has pre installed postgreSQL so you need to overwrite the existing fiel to migrate to the latest version
```shell script
sudo dpkg -i --force-overwrite /var/cache/apt/archives/alembic_1.0.11-5kali1_all.deb
```

## INSTALLING DEPENDENCIES

1.	Go to the Darkbot project folder
cd Darkbot
2.	Pip3 install -r requirements.txt
3.	apt-get install tor
4. sudo apt-get install rabbitmq-server

### NOTE!
Sometimes the apt-get install tor doesn’t work. So, what you need to do is 
1.	su
2.	cd /
3.	nano /etc/apt/sources.list
4.	add the below two links in it
 ```sh 
    deb http://http.kali.org/kali kali-rolling main non-free contrib
```
```sh
    deb-src http://http.kali.org/kali kali-rolling main non-free contrib
```
5.	press ctrl+x
6.	press y then enter 
7.	apt-get update
8.	apt-get install tor

If you are having issue with rabbitmq server restart it by following command
1.  sudo service rabbitmq-server restart

Hopefully! This will work and makes you feel good.

## CREATING ADMIN
1.	python manage.py migrate
2.	python manage.py makemigrations
3.	python manage.py migrate
4.	python manage.py createsuperuser
5.	Give in your emails and other required detail
6.	Now, you can successfully login as admin


## STARTING SERVICES
1.	sudo service tor start
2.  celery -A dark_bot worker -l info

Make sure while giving the second command you are in the root folder of the project as well as the virtual environment is on if it's showing no command found kindly close and open the terminal again it will work fine.

## RUNNING SERVER
1.	python manage.py runserver


# In case of furthur support contact me at
daud.ahmed@tranchulas.com

## Project Leader:
Daud Ahmed	

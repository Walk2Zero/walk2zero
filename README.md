<img src="https://github.com/Walk2Zero/walk2zero/blob/API_key_guide/screenshots/walk2zero_logo.png?raw=true" alt="Walk2Zero logo" title="Walk2Zero" align="right" height="60" />

# Walk2Zero
Walk2Zero is a group project undertaken as part of the Code First Girls Nanodegree.

              __        __    _ _      ____    _____              
              \ \      / /_ _| | | __ |___ \  |__  /___ _ __ ___  
               \ \ /\ / / _` | | |/ /   __) |   / // _ \ '__/ _ \ 
                \ V  V / (_| | |   <   / __/   / /|  __/ | | (_) |
                 \_/\_/ \__,_|_|_|\_\ |_____| /____\___|_|  \___/ 
                                                                  
                 C L I M A T E   C O N S C I O U S   S T E P S                  


## 🏗 About 
Walk2Zero is a program that calculates how much carbon a user can 
potentially offset if they opt for walking or use public 
transport to get to their point of destination. User can register and 
log in to the service, check and track their impact. 

The program interacts with Google Maps API and MySQL database.

## 👯 The Team‍️
- [Lakshika Juneja](https://github.com/Laksh-13)
- [Rajwinder Bhatoe](https://github.com/rajwinderb)
- [Robyn Seymour-Jones](https://github.com/robynfsj)
- [Shuyan Liu](https://github.com/clemcodes)
- [Sravya Betina](https://github.com/Sravya12379)


## Getting Started

1. Clone the repo<br/>

In the terminal go on the working directory where you want to clone the project<br/>
Use the `git clone` command and paste the clone URL then press enter :

```shell
$ git clone https://github.com/Walk2Zero/walk2zero.git
```

2. On your local machine go inside of the *walk2zero* directory :

```shell
$ cd walk2zero
```

## Prerequisites

The requirements to run the project are :<br/>

certifi==2021.5.30<br/>
charset-normalizer==2.0.4<br/>
colorama==0.4.4<br/>
idna==3.2<br/>
mysql-connector-python==8.0.26<br/>
numpy==1.21.2<br/>
pandas==1.3.2<br/>
protobuf==3.17.3<br/>
pyfiglet==0.8.post1<br/>
python-dateutil==2.8.2<br/>
pytz==2021.1<br/>
requests==2.26.0<br/>
six==1.16.0<br/>
urllib3==1.26.6

To install these requirements, run in the terminal :

```shell
$ pip install requirements.txt
```

## Config

1. Set up database

Go to `db/create-db.sql` and run the script in MySQL workbench to set up the database

2. config password 

Go to `config.py`, replace "password" with your own database password :
```shell
PASSWORD = "password"
```

3. config API key

In `config.py`, replace "Your API Key" with your Google Maps API key :

```shell
API_KEY = "Your API Key"
```

Refer to <a href="https://github.com/Walk2Zero/walk2zero/blob/API_key_guide/API_key_guide.md" target="_blank">this guide</a> on how to get you own Google Maps API key


## Run the code
make sure you are in the *walk2zero* directory and run the following command :

```shell
$ python main.py
```

## Finally 
To get started on the app :
- Enter email
- Register yourself
- Enter a journey
- Get user stats
- Log out









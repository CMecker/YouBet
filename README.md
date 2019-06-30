# YouBet
GithubProject-WebTechniken2019

## Initialise:

### Clone by HTTPS:

* go to path where you want to save your repo
* _git clone https://github.com/CMecker/YouBet.git_

### Clone per SSH(recommended)

#### Create Key 

* _ssh-keygen -t rsa -C "Hier@eure.email"  
* Path is not needed if its first key  
* set passphrase (not necessary)  
* public key located at  
* /c/Users/User/.ssh/id_rsa.pub  
* add on git to Profile/Settings/SSH_and_GPG_keys  
* go to path where you want to save your repo
* _git clone github.com/CMecker/YouBet.git_  

### VirtualEnv (optional)

* pip install virtualenv  
* virtualenv venv  
* . venv/Scripts/activate (under Windows to activate virtual Env)  

### install MySQL

* xampp (https://www.apachefriends.org/de/download.html)
* Xampp Control Panel --> start Apache, MySQL --> access: http://localhost/phpmyadmin/
* flask db migrate -m "Changed db"(if changes made)  
* flask db upgrade  

### Run Flask

* pip install -r requirements.txt  
* export FLASK_APP=main.py  
* flask run  
* open in Browser localhost:5000  
* -> user: test  
* -> pw: 123  

# YouBet
GithubProject-WebTechniken2019

## Einrichtung:

### Clone per HTTPS:

* Im Path wo ihr das Repo speichern wollt  
* _git clone https://github.com/CMecker/YouBet.git_

### Clone per SSH(empfohlen)

#### Create Key 

* _ssh-keygen -t rsa -C "Hier@eure.email"  
* Pfad angeben(nicht benoetigt, falls es der erste Key ist)  
* Passwort angeben(nicht benoetigt)  
* Den public Key findet ihr in der Datei  
* /c/Users/User/.ssh/id_rsa.pub  
* Diesen im Github unter Profile/Settings/SSH_and_GPG_keys hinzufuegen  
* Zurück zum Path wo ihr euer Repo speichern wollt  
* _git clone github.com/CMecker/YouBet.git_  

### VirtualEnv (optional)

* pip install virtualenv  
* virtualenv venv  
* . venv/Scripts/activate (under Windows to activate virtual Env)  

### install MySQL

* xampp (https://www.apachefriends.org/de/download.html)
* Bei Xampp im Control Panel Apache, MySQL starten --> Zugriff ueber http://localhost/phpmyadmin/
* flask db migrate -m "Changed db"(if changes made)  
* flask db upgrade  

### Run Flask

* pip install -r requirements.txt  
* export FLASK_APP=main.py  
* flask run  
* open in Browser localhost:5000  
* -> user: test  
* -> pw: 123  

## Arbeiten im Git

* git co master_  
* git pull_  
* git co -b NEUERBRANCH_  
* git add FILE_  
* git ci -m "BRANCHNAME: Lorem Ipsum"_  
* git push origin AKTUELLERBRANCH_  
* git st_ (Hilfreich beim Adden, Committen etc)  
* git diff BRANCH_ (Anzeige von Aenderungen defaultBRANCH-master)  

### Shortcuts

* git config --global alias.co checkout_  
* git config --global alias.ci commit_  
* git config --global alias.st status_  

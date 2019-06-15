# YouBet
GithubProject-WebTechniken2019

## Einrichtung:

### Clone per HTTPS:

Im Path wo ihr das Repo speichern wollt  
_git clone https://github.com/CMecker/YouBet.git_

### Clone per SSH(empfohlen)

#### Create Key 

_ssh-keygen -t rsa -C "Hier@eure.email"  
Pfad angeben(nicht benoetigt, falls es der erste Key ist)  
Passwort angeben(nicht benoetigt)  
Den public Key findet ihr in der Datei  
*/c/Users/User/.ssh/id_rsa.pub*  
Diesen im Github unter Profile>Settings>SSH_and_GPG_keys hinzufuegen  
Zurück zum Path wo ihr euer Repo speichern wollt  
_git clone github.com/CMecker/YouBet.git_  

### VirtualEnv (optional)

pip install virtualenv  
virtualenv venv  
. venv/Scripts/activate (under Windows to activate virtual Env)  

### install MySQL

* xampp (https://www.apachefriends.org/de/download.html) oder MySQL (https://dev.mysql.com/downloads/installer/) herunterladen und installieren
* Bei Xampp im Control Panel Apache, MySQL starten --> Zugriff ueber http://localhost/phpmyadmin/
* Bei der direkten Installation: pfad/bin den Systemvariablen hinzufügen
* Start + Zugriff des Servers über mysql -u 'user' -p 'password'
* Zum vereinfachten Zugriff auf die DB, kann HeidiSQL helfen (https://www.heidisql.com/download.php)
* OPTIONAL: C:\...\YouBet\venv\Lib\site-packages\flask_sqlalchemy\__init__.py --> z.829 auf 'False' statt 'None' setzen, um eine Warnung beim Serverstart zu deaktivieren

### Run Flask

pip install -r requirements.txt  
export FLASK_APP=main.py  
flask db upgrade  
flask db migrate -m "Changed db"(if changes made)  
flask run  
--> open in Browser localhost:5000  
--> user: test  
    pw: 123  

## Arbeiten im Git

_git co master_  
_git pull_  
_git co -b NEUERBRANCH_  
_git add FILE_  
_git ci -m "BRANCHNAME: Lorem Ipsum"_  
_git push origin AKTUELLERBRANCH_  
_git st_ (Hilfreich beim Adden, Committen etc)  
_git diff BRANCH_ (Anzeige von Aenderungen defaultBRANCH-master)  

### Shortcuts

_git config --global alias.co checkout_  
_git config --global alias.ci commit_  
_git config --global alias.st status_  

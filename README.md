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

###VirtualEnv (optional)
pip install virtualenv
virtualenv venv
. venv/Scripts/activate (under Windows to activate virtual Env)

###Run Flask
pip install -r requirements.txt
export FLASK_APP=app.py
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

* Markus Test zum Pushen (Nummer 2)
* Christian Test Merge

# YouBet
GithubProject-WebTechniken2019

#Einrichtung:

##Clone per HTTPS:

Im Path wo ihr das Repo speichern wollt
_git clone https://github.com/CMecker/YouBet.git_

##Clone per SSH(empfohlen)

###Create Key 

_ssh-keygen -t rsa -C "Hier@eure.email"
Pfad angeben(nicht benoetigt, falls es der erste Key ist)
Passwort angeben(nicht benoetigt)

Den public Key findet ihr in der Datei
*/c/Users/User/.ssh/id_rsa.pub*

Diesen im Github unter Profile>Settings>SSH_and_GPG_keys hinzufuegen

Zurück zum Path wo ihr euer Repo speichern wollt
_git clone https://github.com/CMecker/YouBet.git_

##Shortcuts
_git config --global alias.co checkout_
_git config --global alias.ci commit_
_git config --global alias.st status_

#Arbeiten im Git
_git co master_
_git pull_
_git co -b NEUERBRANCH_
_git add FILE_
_git ci -m "BRANCHNAME: Lorem Ipsum"_
_git push origin AKTUELLERBRANCH_
_git st_ (Hilfreich beim Adden, Committen etc)
_git diff BRANCH_ (Anzeige von Aenderungen defaultBRANCH-master)

* Markus Test zum Pushen (Nummer 2)
* Christian Test Merge

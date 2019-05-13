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

### Shortcuts
_git config --global alias.co checkout_
_git config --global alias.ci commit_
_git config --global alias.st status_

## Arbeiten im Git
_git co master_
_git pull_
_git co -b NEUERBRANCH_
_git add FILE_
_git ci -m "BRANCHNAME: Lorem Ipsum"_
_git push origin AKTUELLERBRANCH_
_git st_ (Hilfreich beim Adden, Committen etc)
_git diff BRANCH_ (Anzeige von Aenderungen defaultBRANCH-master)

## XAMPP-Installation (Webserver und DB)

1. XAMPP installieren (https://www.apachefriends.org/de/download.html)
	* Sollte keine Probleme bereiten
2. Der 'Installations/Pfad/von/xampp/htdocs' ist der Pfad an dem die Dateien des Webservers ausgeführt werden (Der Documentroot). solltet ihr das Repo reinclonen, damit es ausgeführt werden kann.
	* Ihr könnt den Pfad auch in der 'httpd.conf' ändern
3. Xampp-Control panel öffnen und Apache und MySQL starten
4. http://localhost/ sollte jetzt im Browser abrufbar sein
5. Unter http://localhost/phpmyadmin/ habt ihr eine Oberfläche, um auf die DB zugreifen zu können
#### Anmerkungen:
* Mit HeidiSQL (https://www.heidisql.com/download.php) habt ihr ein Tool mit dem ihr auf die DB noch etwas nutzerfreundlicher zugreifen können, das braucht ihr aber nicht zwingend
* Den Inhalt aus htdocs könnt ihr komplett rauslöschen, das ist nicht wichtig
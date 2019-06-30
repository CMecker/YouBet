# YouBet 
## Projekt Webtechniken 2019
In diesem Projekt k&ouml;nnen Mitglieder verschieden Events erstellen
und auf diese Events wetten. Als W&auml;hrung dient ein internes Coin-
System. Viel Spaß!
### Einrichtung:
1 `git clone https://github.com/CMecker/YouBet.git`

##### Virtual Envirement installieren (optional, aber empfohlen)
2.1 `pip install virtualenv`  
2.2 `virtualenv venv`  
2.3.1 Linux/Mac: `. venv/bin/activate`  
2.3.2 Windows: `venv\Scripts\activate`

##### Datenbank installieren

3.1 Xampp herunterladen (https://www.apachefriends.org/de/download.html)  
3.2 Xampp mit Standardeinstellungen installieren  
3.3 Im Xampp Control-Panel Apache und MySQL starten  
3.4 unter http://localhost/phpmyadmin/ eine neue DB erstellen  
Name: **beliebig**  
Kollation: **utf8_general_ci**

##### Projekt initialisieren

4.1 _db_config.py_ in Hauptverzeichnis kopieren  und Variablen anpassen  
4.2 `pip install -r requirements.txt`  
4.3.1 Linux/Mac: `export FLASK_APP=main.py`  
4.3.2 Windows: `set FLASK_APP=main.py`  
4.4 Tabellen in DB erstellen lassen `flask db init` (evtl migrations-
Ordner l&ouml;schen)

##### Server starten
5.1 virtualEnv aktiviert? --> Siehe Schritt 2.3  
5.2 `flask run`  
5.3  http://localhost:5000/ im Browser aufrufen  

##### Sonstiges
- Bei DB- &Auml;nderungen im Code (models.py):  
    - `flask db migrate -m "Changed db"`  
    - `flask db upgrade`  

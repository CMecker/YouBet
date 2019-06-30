# YouBet 
## Projekt Webtechniken 2019
YouBet is a ScoialNetwork for your bets. You can create your own events and bet with your friends with virtual money
## Initialise:
1 `git clone https://github.com/CMecker/YouBet.git`

### Virtual Envirement install (optional)
2.1 `pip install virtualenv`  
2.2 `virtualenv venv`  
2.3.1 Linux/Mac: `. venv/bin/activate`  
2.3.2 Windows: `venv\Scripts\activate`

### Database install (necessary)

3.1 Xampp download and install (https://www.apachefriends.org/de/download.html)  
3.2 Xampp Control-Panel --> start Apache und MySQL  
3.3 Access: http://localhost/phpmyadmin/ create new Db  
Name: **any**  
Kollation: **utf8_general_ci**

### Projekt initialise (necessary)

4.1 _db_config.py_ copy into directory 
4.2 `pip install -r requirements.txt`  
4.3.1 Linux/Mac: `export FLASK_APP=main.py`  
4.3.2 Windows: `set FLASK_APP=main.py`  
4.4 Create tables `flask db init` (deleted migrations directory if there are problems)

### Server run (necessary)
5.1 `flask run`  
5.2  http://localhost:5000/   

### Db updates
- if changes made in models:  
    - `flask db migrate -m "Changed db"`  
    - `flask db upgrade`  

# notebook_researcher
To run the server, you must follow these instructions:
- At the very beginning, just clone the repo and create a "venv" for it and install the requirements via:
```python
  pip install -r requirements.txt
```
## windows
- First, you have to install postgresql. The instructions are held in this link below: 
    https://www.postgresqltutorial.com/install-postgresql/
  - Set "password" and "port" carefully, as you should know them further.
- Then, open pgadmin and create a database named "notebook_researcher". After that, open file 
  "quran_django/settings/production.py" and change these items:
    - On line 88, set "Name" property to "notebook_researcher"
    - On line 90, set "Password" property to your postgresql password
    - On line 92, set "Port" property to your postgresql port
- Final_Step:
  - Migrate the initial DB config:
  ```python
    python manage.py makemigrations
    python manage.py migrate
  ```
  - Create your admin account via:
  ```python
    python manage.py createsuperuser
  ```
After you've done these steps, you can run the server via:
```python
  python manage.py runserver
```
After that, there will be a link that if you put "/admin" in the end of it, admin panel will be opened.

# Phoenix Version 2
Project Manager
Doctor Assistant
Market
Accounting
Transport


create a venv:
```bash
python -m venv venv
```
activate it in linux:
```bash
source ./venv/bin/avtivate
```
or activate it in windows:
```bash
./venv/Scripts/avtivate.bat
```
install requirement:
```python
pip install -r requirements.txt
```

put your site root address,'/' , '/phoenix/' eg:
```python
echo "SITE_URL='/'" >> phoenix/settings_pars.py
```
or for special subdomain (for example '/phoenix/'):

```python
echo "SITE_URL='/phoenix/'" >> phoenix/server_settings.py
```
generate and view secret key:
```python
rm phoenix/secret_key.py
echo "SECRET_KEY = 'yj)%c-)__z_null-_l-ned!$6*cs)_=w@g&t=0vj^wg)knwm3z'" >> phoenix/secret_key.py
python manage.py djecrety
```


```bash

cp phoenix/local_settings.py phoenix/server_settings.py 

```

copy and put it in specific file:
```bash
vi phoenix/secret_key.py
```


put my sql db credential in files like right below:

```
[client]
database = your_database_name
host = your_host_name
user = your_user_name
password = your_password
default-character-set = utf8
```
for production:
```bash
rm phoenix/secret_my_sql.cnf
echo "[client]">> phoenix/secret_my_sql.cnf
echo "database = your_database_name">> phoenix/secret_my_sql.cnf
echo "host = your_host_name">> phoenix/secret_my_sql.cnf
echo "user = your_user_name">> phoenix/secret_my_sql.cnf
echo "password = your_password">> phoenix/secret_my_sql.cnf
echo "default-character-set = utf8" >> phoenix/secret_my_sql.cnf
```



migrate : 
```python
python manage.py migrate
```

create superuser : 
```python
python manage.py createsuperuser
```

collectstatic : 
```python
python manage.py collectstatic
```

https://tonyteaches.tech/django-nginx-uwsgi-tutorial/



```bash
cp ./server/phoenix.ini /etc/uwsgi/sites/phoenix.ini
cp ./server/phoenix /etc/nginx/sites-available/phoenix
```



test uwsgi:
```bash
uwsgi --http :8000 --module /home/leo/phoenix4/phoenix.wsgi
```


deploy: 
```bash
sudo vi /home/leo/phoenix/uwsgi_params
```



```bash
sudo vi /home/leo/phoenix/phoenix_uwsgi.ini
```
#copy phoenix_uwsgi.ini





```bash
sudo vi /etc/nginx/sites-available/phoenix.conf
```
#copy phoenix.conf




```bash
sudo ln -s /etc/nginx/sites-available/phoenix.conf /etc/nginx/sites-enabled/
```


uwsgi --socket phoenix.sock --module phoenix.wsgi --chmod-socket=666


```bash
uwsgi --ini phoenix_uwsgi.ini
```



vassals

```bash
cd /home/leo/phoenix/venv/
mkdir vassals
sudo ln -s /home/leo/phoenix/phoenix_uwsgi.ini /home/leo/phoenix/venv/vassals/
```



```bash
uwsgi --emperor /home/leo/phoenix/venv/vassals --uid www-data --gid www-data
```





```bash
sudo vi /etc/systemd/system/emperor.uwsgi.service
```
#copy emperor.uwsgi.service



```bash
systemctl enable emperor.uwsgi.service
systemctl start emperor.uwsgi.service
```


restart service:
```bash
sudo systemctl restart emperor.uwsgi.service
sudo /etc/init.d/nginx restart
```

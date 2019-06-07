# UploadCSV

This projects will take the csv file as an input from browser that contains name,sku,description fields and render those details in the form of an table and user can search the records by typing keyword in search box.

# UI 
![uploadcsvui](https://user-images.githubusercontent.com/35727060/59103830-864a1580-894d-11e9-8e45-9108ae8c84c1.png)

## Stack details
```bash
Framework : python-Django
version : Django-2.2.2

Database:
Db : sqlite (default)

Backend:
Language : python
verison : python3

Front-end:
HTML : HTML5
css : bootstrap4
js

Log file:
location : /var/log/uploadcsv.log 

Hostname:
host : localhost (default)
```
## Installation


```bash
git clone https://github.com/goutham9032/UploadCSV.git
cd UploadCSV
```

```bash
pip3 install -r requirements.txt
```

```bash
python3 manage.py makemigrations
```

```bash
python3 manage.py migrate
```


## Running Locally
```bash
python3 manage.py runserver 0:2222 
```
> Note: when you want to run this application on server, please add domain name/ip address in ALLOWEDHOSTS in settings.py

## In browser
```python
http://localhost:2222 
     or
http://<ipaddress/domain name>:2222 # when you are running on server
```

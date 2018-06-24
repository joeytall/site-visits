# site-visits

## API framework
Install Flask
`pip3 install flask`

## Add CSV
put data.csv in project folder

## Start Server
`python3 app.py`

data.db will be created if not exist.

## Query Sample
An average query takes less than a second to complete.
```
curl "http://127.0.0.1:5000/unique-users?device=1,3,4&os=0,2"
{
  "count": 4669715
}
curl "http://127.0.0.1:5000/loyal-users"                                                                      
{
  "count": 563740
}
curl "http://127.0.0.1:5000/loyal-users?device=1,2,3,4&os=3"
{
  "count": 10282
}
curl "http://127.0.0.1:5000/loyal-users?device=3&os=3"                                          
{
  "count": 43
}
```

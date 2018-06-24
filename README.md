# site-visits

## Steps
1. API framework
Install Flask
`pip3 install flask`

2. Add CSV
put data.csv in project folder

3. Start Server
`python3 app.py`

data.db will be created if not exist.

# Query Sample
An average query takes less than a second to complete.
```
curl "127.0.0.1:5000/unique-users?device=1,3,4&os=0,2"
{
  "count": 4669715
}
curl "127.0.0.1:5000/loyal-users"                                                                      
{
  "count": 563740
}
curl "127.0.0.1:5000/loyal-users?device=1,2,3,4&os=3"
{
  "count": 10282
}
curl "127.0.0.1:5000/loyal-users?device=3&os=3"                                          
{
  "count": 43
}
```

# Docker
## Build Docker Image
`docker build -t site-visits:latest .`

## Run Container
`docker run -d -p 5000:5000 site-visits:latest`
It takes up to 4 min to load and serve the 1GB csv file.

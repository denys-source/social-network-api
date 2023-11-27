# Social Network API 📱

## ⚙️ Installing using GitHub

Linux/MacOS:

```shell
git clone https://github.com/denys-source/social-network-api
cd social-network-api/
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

Windows:
```shell
git clone https://github.com/denys-source/social-network-api
cd social-network-api/
python venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 🐳 Running with docker

Docker should be installed
```shell
sudo docker build -t social-network-api .
sudo docker run -p 8000:8000 social-network-api
```

## 🤖 Running automated bot

Update `config.json` as you like and run the following command:
```
python3 bot.py config.json
```

## 🔓 Getting access
1. Create user at `/api/user/register`
2. Get access and refresh token at `/api/user/token/`

## 📍 Features

* CRUD for posts
* JWT authentication
* like/unlike functionality
* Analytics about how many likes were made at `/api/analytics/` endpoint
* Analytics about user activity at `/api/analytics/user/` endpoint
* Documentation can be accessed at `/api/schema/swagger/` or `/api/schema/redoc/`

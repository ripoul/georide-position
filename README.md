<h1 align="center">Welcome to georide-position 👋</h1>

[![Build Status](https://travis-ci.org/ripoul/georide-position.svg?branch=master)](https://travis-ci.org/ripoul/georide-position)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![codecov](https://codecov.io/gh/ripoul/georide-position/branch/master/graph/badge.svg)](https://codecov.io/gh/ripoul/georide-position)
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=ripoul/georide-position)](https://dependabot.com)

> get the last day deplacement of the georide tracker for public sharing (road trip for example)

### 🏠 [Homepage](https://georide.ripoul.fr)

In this project I use [georide](https://georide.fr/). Georide is a gps tracker for motorcycle. Feel free to check their work. 

## :hammer: Install

```sh
pip install --user tox
tox
```

## :wrench: Usage

for dev purpose you don't need anything else.

To start the server : 

```sh
source .tox/test/bin/activate
python manage.py runserver
```

For production you need to set the parameter for your database and the secret key of your app : 
- db_host : the database host
- db_name : the database name
- db_pass : the database password
- db_port : the database port (ex: 5432)
- db_user : the database user 
- secret_key : a long secret key

## :interrobang: Help with georide api

All the informations you need can be find on the georide api documentation [here](https://api.georide.fr/).

To get a georide token : 
```sh
curl --request POST \
  --url https://api.georide.fr/user/login \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data 'email=[your email]&password=[your password]'
```

To get your tracker id : 
```sh
curl --request GET \
  --url https://api.georide.fr/user/trackers \
  --header 'Authorization: Bearer [your token]' \
  --header 'cache-control: no-cache'
```

To get the position history : 
```sh
curl --request GET \
  --url 'https://api.georide.fr/tracker/[tracker id]/trips/positions?from=[start date]&to=[end date]' \
  --header 'Authorization: Bearer [your token]'
```
The date has to be formated like that : `YYYYMMDDTHHmmSS`.

## :white_check_mark: Run tests

```sh
tox
```

## Author

👤 **Jules LE BRIS**

* Github: [@ripoul](https://github.com/ripoul)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/ripoul/georide-position/issues).

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2019 [Jules LE BRIS](https://github.com/ripoul).<br />
This project is [MIT](https://github.com/ripoul/georide-position/blob/master/LICENSE) licensed.

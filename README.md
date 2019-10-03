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
pip install -r requirements.txt
```

## :wrench: Usage

You need to set 5 environment variables to use the project : 
- trackerID : it's the id of the tracker you want to follow
- userGeoride : it's the user use to connect to your georide account
- passwordGeoride : it's the password use to connect to your georide account

To set those environment variables you can use a `.env` file in the root of the project. This file is build like that : 
```
trackerID=[your tracker id]
userGeoride=[the email of your account]
passwordGeoride=[the password of your account]
startDate=[the start date of your road trip]
endDate=[the end date of your road trip]
```

The date in the env variable has to be formated like that : `YYYY/MM/DD`

To start the server : 

```sh
python manage.py runserver
```

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
  --url 'https://api.georide.fr/tracker/[tracker id]/trips/positions?from=[start date]&to=[end date]'
```
The date has to be formated like that : `YYYYMMDDTHHmmSS`.

## :white_check_mark: Run tests

```sh
python manage.py test
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

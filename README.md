<h1 align="center">Welcome to georide-position 👋</h1>

[![Build Status](https://travis-ci.org/ripoul/georide-position.svg?branch=master)](https://travis-ci.org/ripoul/georide-position)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![codecov](https://codecov.io/gh/ripoul/georide-position/branch/master/graph/badge.svg)](https://codecov.io/gh/ripoul/georide-position)

> get the last day deplacement of the georide tracker

### 🏠 [Homepage](https://github.com/ripoul/georide-position)

## Install

```sh
pip install -r requirements.txt
```

## Usage

You need to set two environment variables two use the project : 
- georideToken : it's the token for the georide public api (it expires every 30 days)
- trackerID : it's the id of the tracker you want to follow

Those information can be find on the georide api documentation [here](https://api.georide.fr/).

To set those environment variables you can use a `.env` file in the root of the project. This file is build like that : 
```
georideToken=[your token]
trackerID=[the tracker id]
```

To have a georide token : 
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

And finally to start the server : 

```sh
python manage.py runserver
```

## Run tests

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

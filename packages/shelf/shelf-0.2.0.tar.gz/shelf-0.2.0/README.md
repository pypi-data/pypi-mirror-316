

# REST on shelf
Simple and universal async REST API client library.

## Install
```
$ pip install shelf
```

## Usage
```python
import shelf
import asyncio

github = shelf.Client('https://api.github.com/')

async def find_user_name(login: str):
    user = await github.users[login]()
    return user.name

asyncio.run(find_user_name('hanula'))
```

## Features
* Dot notation URL path traversal.
* Dot notation access of the response data.

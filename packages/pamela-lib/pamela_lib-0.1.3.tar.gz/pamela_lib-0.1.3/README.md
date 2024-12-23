# Pamela
Pamela is a python library to simplify API usage in programs

## General Information
- Pamela is a python library to simplify API usage in programs. It has different features to optimize the workflow with APIs.
- API usage in programs is sometimes very annoying. To optimize all things connected with APIs, Pamela is your helper!
  
## Technologies Used
- Python
- Requests
  
## Features
- Receive data
- Create sessions
- Get status of session
- Choose file format

## Installation
```bash
pip install pamela-lib
```

or

```bash
git clone github.com/zlElo/Pamela.git
cd Pamela
pip install .
```

## Code examples (simple)
```py
# import pamela with all classes
from pamela import Pamela, Session

# create pamela instance
pamela = Pamela()

# create session with pamela
session1 = Session.create("address", "username", "password")

# status of session
status_session = Session.status(address="address", session=session1)

# receive data with session
response = pamela.receive_data(address="address", session=session1)

# receive data with no credentials
response = pamela.receive_data(address="address")

# send data with session
response = pamela.send_data(address="address", session=session1, data="123")

# send data with no credentials
response = pamela.send_data(address="address", data="123")
```

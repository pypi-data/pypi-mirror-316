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
pip install pamela
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
answer = pamela.receive_data(address="address", session=session1)

# receive data with no credentials
answer = pamela.receive_data(address="address")
```

</ul><h2>Contact</h2>
<hr><p><span style="margin-right: 30px;"></span><a href="https://github.com/zlElo"><img target="_blank" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" style="width: 10%;"></a></p>

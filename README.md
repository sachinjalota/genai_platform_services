# GenAI Platform Services
## Chat-As-Service
## How to Setup this service
- Clone the Repo 
- Setup your environment
    - Install poetry: ```brew install poetry```
    - Create venev  : ``` python3.11 -m venev venev ```
    - Activate venv : ``` source venv/bin/activate ```
    - Install dependencies in verbose mode : ``` poetry install -vvv ```
    - Install fastapi : ``` pip install "fastapi[standard]" ```
    - Run the service : ``` fastapi run src/main.py --reload ```
# Language Buddy

## Description

Language Buddy lets you practice conversations in any language using an AI model. I built this because I suck at Spanish and would love to have conversation to get better and I don't have friends familar with the langauge so I made my friend fluent in any langauge. 

## Features

- Integration with [Appwrite](https://appwrite.io/) for user management and data storage
- Real-time chat with [Gemini AI](https://ai.google.dev/gemini-api/docs)
- Leveraging Gemini API for AI-powered language capabilities 


## Installation

1. **Prerequisites:** 
   - Docker: Make sure you have [Docker](https://www.docker.com/) installed.
   - Docker Compose:  Install [Docker Compose](https://docs.docker.com/compose/install/) if you don't have it already.

2. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/language-buddy.git 
   cd language-buddy
   ```

3. **Create & activate your virtualenv:**
  ```bash
    python3 -m venv env 

    source env/bin/activate # MacOS
    .\env\Scripts\activate # Windows OS 
  ```

4. **Install dependencies**: 
  ```bash
   pip install -r requirements.txt
  ```

5. **Run the project via terminal**: 
  ```bash
   python manage.py runserver
  ```


6. **Run the project via docker**:
 ```bash
   docker-compose up
  ```


7. Access the application: Open your browser and go to http://localhost:8000. 



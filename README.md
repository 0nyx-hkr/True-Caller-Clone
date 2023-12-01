# Project Name

Truecaller clone minimal

## Requirements

Ensure you have the following software installed on your machine:

- Python (version x.x.x)
- MySQL Server (or SQLite for local development)

## Installation

1. Unzip the file

2. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - **For Windows:**

        ```bash
        venv\Scripts\activate
        ```

    - **For macOS/Linux:**

        ```bash
        source venv/bin/activate
        ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Configure the Database:

    - **For MySQL (Production):**
      - Create a MySQL database
            List of commands to start a database

    ```  SQL
            show databases;
            use mysql;
            show tables;
            select user from user;
            create user your_database_user@localhost identified by 'your_database_passwd';
            create database your_database_name;
            show databases;
            grant all privileges on your_database_name.* to your_database_user@localhost;

        ```
        and update the `DATABASES` configuration in `.env`:

        declare them in .env file
        DATABASE_ENGINE=django.db.backends.mysql
        DATABASE_NAME=your_database_name
        DATABASE_USER=your_database_user
        DATABASE_PASSWORD=your_database_passwd
        DATABASE_HOST=127.0.0.1
        DATABASE_PORT=3306

OR
    - **For SQLite (Local Development):**
      - Comment the MySQL configuration and uncomment the SQLite configuration:

```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / "db.sqlite3",
            }
        }
    ```

6. Migrate the database:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
    Data populations:

    ```bash
python manage.py datapopulate.py
```

## Usage

Explain how to run the project locally.

```bash
python manage.py runserver
```

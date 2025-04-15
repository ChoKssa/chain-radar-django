# EEN1037 Assignment 3: ChainRadar

## Overview

This web application was developed for EEN1037 Assignment 3 by extending the official Django tutorial project from <https://docs.djangoproject.com/en/5.1/intro/tutorial01/>. It includes custom models, views, templates, user authentication, Docker integration, and client-side interactivity via JavaScript and AJAX.

The project is configured for both local development and containerized deployment using Docker. A SQL database can be connected using the `DATABASE_URL` environment variable.

---

## 📦 Installation (Local without Docker)

1. **Create and activate a virtual environment:**

```bash
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
```

2. **Install the required dependencies:**

```bash
pip install -r requirements.txt
```

3. **Create a `.env` file (or set environment variables manually):**

```env
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
SECRET_KEY=your-django-secret-key
```

4. **Apply migrations:**

```bash
python manage.py migrate
```

5. **Create a superuser (optional, for accessing Django Admin):**

```bash
python manage.py createsuperuser
```

6. **Run the development server:**

```bash
python manage.py runserver
```

---

## 📚 Sample Data Import

A **data/** folder is included in the project root containing sample files to populate the database with example cryptocurrencies and historical price snapshots.

1. **Import cryptocurrencies and snapshots from CSV files**

This command imports data from cryptos.csv and snapshots.csv:
```bash
python manage.py import_cryptos --cryptos data/cryptos.csv --snapshots data/snapshots.csv
```
The crypto import handles creation of CryptoCurrency objects. The snapshot import attaches time-based metrics (price, volume, market cap, etc.) to those cryptos.

2. **Import crypto logos from folder**

Use the following management command to import logos for existing cryptos based on their symbol (e.g., BTC.png, ETH.png):

```bash
python manage.py import_crypto_logos data/crypto_logos/
```

These commands are especially useful for testing and demo purposes.

---

## 🐳 Running as a Docker Container

A sample Dockerfile is provided that builds and runs the application with environment-based configuration.

If `DATABASE_URL` is not provided, the application defaults to SQLite on `/app/storage`.

### Docker Commands

**Build the Docker image:**

```bash
docker build . -t ChainRadar
```

**Create persistent volume for database and media storage:**

```bash
docker volume create ChainRadar-storage
```

**Run the container:**

```bash
docker run -ti \
  -e DATABASE_URL="mysql://ChainRadardbuser:ChainRadardbpass@host.docker.internal:3306/ChainRadardb" \
  -v ChainRadar-storage:/app/storage \
  -p 8000:8000 \
  ChainRadar
```

**Remove the storage volume (if needed):**

```bash
docker volume ChainRadar-storage
```

---

## ⚙️ Development Notes

### Generating database schema migrations:

```bash
python manage.py makemigrations
```

### Applying migrations:

```bash
python manage.py migrate
```

### Running the dev server:

```bash
python manage.py runserver
```

---

## 👤 User Authentication

The application includes registration, login, and logout functionality using Django's built-in authentication system.

- Regular users can register and log in through the frontend.
- Staff users can be promoted via Django Admin (`is_staff=True`).

To test different permissions, use `{% if request.user.is_staff %}` in templates and `request.user.is_staff` in views.

---

## 📁 Project Structure (simplified)

```
project-root/
│
├── app/                  # Django application logic
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── ...
│
├── templates/            # HTML templates
├── static/               # Static assets (CSS, JS)
├── data/                 # Sample data
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker_entrypoint.sh
└── .env                  # Environment variables (not committed)
```

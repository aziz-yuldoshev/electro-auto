# 🚗 ELECTRO AUTO — Car Marketplace Web Application

ELECTRO AUTO is a Django-based automotive web application designed to showcase cars and provide users with convenient tools for exploring and comparing vehicles.

The project demonstrates practical web development skills through car listings, filtering, favorites, vehicle comparisons, and test-drive functionality.

## ✨ Features

- 🚘 Browse car listings
- 🔎 Search and filter vehicles
- 🏷️ Browse car brands and categories
- ❤️ Add cars to favorites
- ⚖️ Compare vehicles
- 📅 Request a test drive
- 👤 User authentication
- 💵 Display vehicle prices
- ℹ️ About page with video content

*Features are described according to the project's intended functionality.*

## 🛠️ Technologies

- Python
- Django
- SQLite
- HTML5
- CSS3
- JavaScript
- Django Templates
- Git and GitHub

## 📁 Project Structure

```text
electro_auto/
├── config/
├── cars/
├── templates/
├── static/
├── manage.py
└── ...
```

*The folder structure is illustrative; actual names may differ.*

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/aziz-yuldoshev/electro-auto.git
cd electro-auto
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows CMD:**

```cmd
venv\Scripts\activate
```

### 4. Install dependencies

If `requirements.txt` exists:

```bash
pip install -r requirements.txt
```

Otherwise, install the Django version required by the project.

### 5. Configure environment variables

Configure the Django secret key and any other required environment variables. Never publish passwords or secret keys.

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## 🔐 Security

- Keep secret keys and credentials out of source control.
- Do not commit private databases or virtual environments.
- Set `DEBUG = False` and configure allowed hosts before production deployment.

## 🎯 Project Purpose

This project demonstrates Django development skills, database-driven car listings, user interactions, filtering, and automotive marketplace functionality.

## 👨‍💻 Author

**Aziz Yuldoshev**

GitHub: [@aziz-yuldoshev](https://github.com/aziz-yuldoshev)

## 📄 License

No specific open-source license is declared. Add a license if you intend to define reuse and distribution permissions.

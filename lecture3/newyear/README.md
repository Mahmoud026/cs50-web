# NewYear Django App

A Django web application that tracks various holidays and events including New Year, Eid al-Fitr, Eid al-Adha, and Ramadan. The app provides countdown timers, fun facts, and email subscription functionality.

## Features

- **New Year Countdown**: Shows days remaining until the next New Year
- **Eid Celebrations**: Tracks both Eid al-Fitr and Eid al-Adha with countdown timers
- **Ramadan Tracking**: Monitors the holy month of Ramadan
- **Email Subscriptions**: Users can subscribe for event reminders
- **Fun Facts**: Displays interesting facts about each holiday/event
- **Responsive Design**: Modern UI with CSS styling

## Prerequisites

Before running this application, make sure you have:

- Python 3.8 or higher installed
- pip (Python package installer)
- Git (optional, for cloning the repository)

## Installation

1. **Navigate to the project directory**:
   ```bash
   cd lecture3
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   
   **On Windows**:
   ```bash
   venv\Scripts\activate
   ```
   
   **On macOS/Linux**:
   ```bash
   source venv/bin/activate
   ```

4. **Install Django**:
   ```bash
   pip install django
   ```

5. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

## Running the Application

1. **Start the Django development server**:
   ```bash
   python manage.py runserver
   ```

2. **Open your web browser** and navigate to:
   ```
   http://127.0.0.1:8000/newyear/
   ```

## Available Pages

- **Home Page** (`/newyear/`): Landing page with email subscription form
- **New Year Countdown** (`/newyear/check/`): Shows days until next New Year
- **Eid al-Fitr** (`/newyear/eid-fitr/`): Countdown to Eid al-Fitr
- **Eid al-Adha** (`/newyear/eid-adha/`): Countdown to Eid al-Adha
- **Ramadan** (`/newyear/ramadan/`): Ramadan tracking and countdown

## Project Structure

```
lecture3/
├── newyear/                 # Main app directory
│   ├── templates/newyear/   # HTML templates
│   ├── static/newyear/      # CSS and static files
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # URL routing
│   └── README.md           # This file
├── lecture3/               # Django project settings
├── manage.py              # Django management script
└── db.sqlite3            # SQLite database
```

## Development

To make changes to the application:

1. **Create a superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

2. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

3. **Access the admin panel** at:
   ```
   http://127.0.0.1:8000/admin/
   ```

## Troubleshooting

- **Port already in use**: If port 8000 is busy, use a different port:
  ```bash
  python manage.py runserver 8080
  ```

- **Database errors**: If you encounter database issues, try:
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

- **Static files not loading**: Collect static files:
  ```bash
  python manage.py collectstatic
  ```

## Technologies Used

- **Django 5.2.4**: Web framework
- **SQLite**: Database
- **HTML/CSS**: Frontend styling
- **Python**: Backend logic

## License

This project is for educational purposes.

## Support

For issues or questions, please check the Django documentation or create an issue in the project repository. 
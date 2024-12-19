
# Django Sage Timezone Management

Django Sage Timezone Management is a Django package that allows administrators to easily select and apply a timezone for their session directly from the Django Admin interface. Once set, the timezone is automatically applied to all datetime displays during the session.

## Features

- Adds a "Select Timezone" option in the Django Admin navigation bar.
- Automatically applies the selected timezone to the user's session using middleware.
- Supports all timezones available through `pytz`.
- Simple integration with existing Django projects.

## Installation

### Using `pip` with `virtualenv`

1. **Create a Virtual Environment**:

    ```bash
    python -m venv .venv
    ```

2. **Activate the Virtual Environment**:

   - On Windows:

     ```bash
     .venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source .venv/bin/activate
     ```

3. **Install `django-sage-timezone`**:

    ```bash
    pip install django-sage-timezone
    ```

### Using `poetry`

1. **Initialize Poetry** (if not already initialized):

    ```bash
    poetry init
    ```

2. **Install `django-sage-timezone`**:

    ```bash
    poetry add django-sage-timezone
    ```

3. **Apply Migrations**:

    After installation, ensure to run the following commands to apply necessary migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

## Configuration

### Django Settings

Add `django-sage-timezone` to your `INSTALLED_APPS` in the Django settings:

```python
INSTALLED_APPS = [
    ...
    "sage_timezone",
    "django.contrib.admin"
]
```

Also, add the `TimezoneMiddleware` to your middleware settings:

```python
MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "sage_timezone.middleware.TimezoneMiddleware",
    ...
]
```

### Important Note:

The `sage_timezone.middleware.timezone.TimezoneMiddleware` must be placed after the `django.contrib.sessions.middleware.SessionMiddleware` in your `MIDDLEWARE` setting. This order is crucial to ensure that the session data is available when the timezone is set.

## Note:
You can set a custom session name in your Django settings using the `TIME_ZONE_SESSION_NAME` setting. For example:

```python
   TIME_ZONE_SESSION_NAME = 'your_custom_session_name'
```


## Usage

Once configured, the Django Admin will include a "Select Timezone" option in the navigation bar. Administrators can choose their preferred timezone, which will be applied to their session.

---

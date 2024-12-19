# Sage Language Middleware for Django

This Django project provides middleware and utility classes to support multilingual applications through URL prefixes and cookies for language settings. The core feature is a custom `CookieLocaleMiddleware`, which dynamically manages user language preferences and redirects users to the appropriate language version of the site based on URL paths or cookies.

## Features

- **Dynamic Language Detection**: Determines the preferred language by examining URL prefixes and cookies.
- **Custom Middleware**: `CookieLocaleMiddleware` extends Django's default `LocaleMiddleware`, enhancing support for multilingual content.
- **URL Prefix Management**: Utilities to add or remove language prefixes in URLs, supporting a clean and consistent URL structure.
- **Customizable Language Settings**: Integrates with Django's internationalization settings (`LANGUAGES`, `LANGUAGE_CODE`, etc.) for easy customization.
- **Error Checking**: Ensures proper configuration of language settings and middleware placement.

## Project Structure

- `middlewares/cookie.py`: Contains `CookieLocaleMiddleware` to manage language preferences dynamically.
- `utils/locale.py`: Provides `MultilingualService`, a utility class for adding and removing language prefixes in URLs.
- `views/locale.py`: Implements `SetLanguageView`, allowing users to set their preferred language through a POST request.
- `checks.py`: Validates the configuration of middleware, language settings, and cookies.
- `settings.py`: Configures Django's settings, including `LANGUAGES`, `LANGUAGE_CODE`, and middleware setup.
- `urls.py`: Configures routes for language switching and i18n patterns.

## Installation

### Using pip

1. **Create a Virtual Environment**:
    ```bash
    python -m venv .venv
    ```

2. **Activate the Virtual Environment**:
    - On Windows:
        ```bash
        .venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```bash
        source .venv/bin/activate
        ```

3. **Install the Package**:
    ```bash
    pip install python-sage-bbb
    ```

### Using Poetry

1. **Install Poetry**: Follow the official installation instructions at the [Poetry website](https://python-poetry.org/docs/#installation).

2. **Create a New Project (Optional)**:
    ```bash
    poetry new myproject
    cd myproject
    ```

3. **Add the Package as a Dependency**:
    ```bash
    poetry add python-sage-bbb
    ```

4. **Activate the Virtual Environment**:
    ```bash
    poetry shell
    ```

## Configuration

1. **Add `sage_language` to `INSTALLED_APPS`** in `settings.py`:
   ```python
   INSTALLED_APPS = [
       ...
       'sage_language',
   ]
   ```

2. **Middleware Configuration**:
   Ensure `CookieLocaleMiddleware` is added immediately after `SessionMiddleware` in the `MIDDLEWARE` setting:
   ```python
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'django.contrib.sessions.middleware.SessionMiddleware',
       'sage_language.middlewares.cookie.CookieLocaleMiddleware',
       ...
   ]
   ```

3. **Set Language Settings**:
   Define supported languages, default language, and cookie names:
   ```python
   LANGUAGES = [
       ('en', 'English'),
       ('fa', 'Farsi'),
       ('es', 'Spanish'),
   ]
   LANGUAGE_CODE = 'en'
   SAGE_LANGUAGE_COOKIE_NAME = "ivan_language"
   LANGUAGE_COOKIE_NAME = SAGE_LANGUAGE_COOKIE_NAME
   ```

4. **Add URL Configuration for Language Switching**:
   In `urls.py`, set up the language switching view:
   ```python
   from sage_language.views import SetLanguageView
   urlpatterns = [
       path('set-language/', SetLanguageView.as_view(), name='set_language'),
       path("i18n/", include("django.conf.urls.i18n")),
   ]
   ```

## Usage

1. **Setting Language Preference**:
   To change the language preference, make a POST request to `/set-language/` with `language` and `next` parameters:
   - `language`: The desired language code (e.g., 'en', 'fa', 'es').
   - `next`: The URL to redirect to after setting the language.

2. **URL Prefix Management**:
   The middleware automatically adds or removes language prefixes from URLs based on the user’s selected language and cookie settings.

3. **Automatic Language Redirection**:
   If a user’s preferred language (stored in a cookie) differs from the language in the URL, the middleware will redirect them to the correct URL.

## Notes

- Make sure to set `USE_I18N`, `USE_L10N`, and `USE_TZ` to `True` in `settings.py` for proper internationalization support.
- For production use, ensure `SAGE_LANGUAGE_COOKIE_NAME` and `LANGUAGE_COOKIE_NAME` are set to the same value for consistent cookie management.

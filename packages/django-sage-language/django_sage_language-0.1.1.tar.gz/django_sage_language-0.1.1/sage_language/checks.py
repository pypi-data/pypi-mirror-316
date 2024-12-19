from django.core.checks import Error, Warning, register
from django.conf import settings


@register()
def check_sage_language_installed(app_configs, **kwargs):
    errors = []

    # 1. Check if SAGE_LANGUAGE_COOKIE_NAME is set in settings
    if not hasattr(settings, 'SAGE_LANGUAGE_COOKIE_NAME'):
        errors.append(
            Error(
                'SAGE_LANGUAGE_COOKIE_NAME is not set in settings',
                id="sage_language.E005",
            )
        )
    else:
        # 2. Ensure LANGUAGE_COOKIE_NAME is set to SAGE_LANGUAGE_COOKIE_NAME
        if getattr(settings, 'LANGUAGE_COOKIE_NAME', None) != settings.SAGE_LANGUAGE_COOKIE_NAME:
            errors.append(
                Error(
                    f'LANGUAGE_COOKIE_NAME must be set to SAGE_LANGUAGE_COOKIE_NAME ("{settings.SAGE_LANGUAGE_COOKIE_NAME}")',
                    id="sage_language.E011",
                )
            )

    # 3. Check that "sage_language.middlewares.cookie.CookieLocaleMiddleware" is in MIDDLEWARE
    # and is exactly after 'django.contrib.sessions.middleware.SessionMiddleware'
    session_middleware = 'django.contrib.sessions.middleware.SessionMiddleware'
    cookie_middleware = "sage_language.middlewares.cookie.CookieLocaleMiddleware"

    if session_middleware in settings.MIDDLEWARE:
        session_index = settings.MIDDLEWARE.index(session_middleware)

        if cookie_middleware not in settings.MIDDLEWARE:
            errors.append(
                Error(
                    f"{cookie_middleware} is missing in MIDDLEWARE",
                    id="sage_language.E002",
                )
            )
        elif settings.MIDDLEWARE[session_index + 1] != cookie_middleware:
            errors.append(
                Error(
                    f"{cookie_middleware} must be placed immediately after {session_middleware}",
                    id="sage_language.E003",
                )
            )
    else:
        errors.append(
            Error(
                f"{session_middleware} is missing in MIDDLEWARE",
                id="sage_language.E004",
            )
        )

    # 4. Check if USE_I18N, USE_TZ, USE_L10N, LANGUAGES, and LANGUAGE_CODE are set in settings
    if not getattr(settings, 'USE_I18N', None):
        errors.append(
            Error(
                'USE_I18N must be set to True in settings',
                id="sage_language.E006",
            )
        )

    if not getattr(settings, 'USE_TZ', None):
        errors.append(
            Error(
                'USE_TZ must be set to True in settings',
                id="sage_language.E007",
            )
        )

    if not getattr(settings, 'USE_L10N', None):
        errors.append(
            Error(
                'USE_L10N must be set to True in settings',
                id="sage_language.E008",
            )
        )

    if not hasattr(settings, 'LANGUAGES'):
        errors.append(
            Error(
                'LANGUAGES must be defined in settings',
                id="sage_language.E009",
            )
        )

    if not hasattr(settings, 'LANGUAGE_CODE'):
        errors.append(
            Error(
                'LANGUAGE_CODE must be defined in settings',
                id="sage_language.E010",
            )
        )

    return errors

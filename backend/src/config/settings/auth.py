"""
Authentication and password validation settings for money-flow project.
"""

from datetime import timedelta

from config.settings.base import DEBUG, SECRET_KEY

AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

# JWT settings
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'jwt-auth'

SIMPLE_JWT = {
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
    'SIGNING_KEY': SECRET_KEY,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'TOKEN_BACKEND': 'rest_framework_simplejwt.token_blacklist.backends.BlacklistBackend',
    'BLACKLIST_TOKEN_CHECKS': [
        'rest_framework_simplejwt.token_blacklist.check_blacklisted_token',
    ],
}

# REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DATE_INPUT_FORMATS': [
        '%d.%m.%Y',
    ],
}

if not DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
        'rest_framework.renderers.JSONRenderer'
    ]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

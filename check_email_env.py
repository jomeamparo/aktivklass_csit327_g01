import os

print('--- ENVIRONMENT VARIABLES ---')
for key, value in os.environ.items():
    if 'EMAIL' in key.upper():
        print(f'{key}={value}')

print('\n--- DJANGO SETTINGS (if available) ---')
try:
    from django.conf import settings
    print(f'EMAIL_BACKEND: {getattr(settings, "EMAIL_BACKEND", None)}')
    print(f'EMAIL_HOST: {getattr(settings, "EMAIL_HOST", None)}')
    print(f'EMAIL_PORT: {getattr(settings, "EMAIL_PORT", None)}')
    print(f'EMAIL_USE_TLS: {getattr(settings, "EMAIL_USE_TLS", None)}')
    print(f'EMAIL_HOST_USER: {getattr(settings, "EMAIL_HOST_USER", None)}')
    print(f'EMAIL_HOST_PASSWORD: {getattr(settings, "EMAIL_HOST_PASSWORD", None)}')
    print(f'DEFAULT_FROM_EMAIL: {getattr(settings, "DEFAULT_FROM_EMAIL", None)}')
    print(f'EMAIL_SSL_KEYFILE: {getattr(settings, "EMAIL_SSL_KEYFILE", None)}')
    print(f'EMAIL_SSL_CERTFILE: {getattr(settings, "EMAIL_SSL_CERTFILE", None)}')
except Exception as e:
    print('Django settings not loaded:', e) 
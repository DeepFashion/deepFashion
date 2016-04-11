DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'CS654Project',                        # Or path to database file if using sqlite3.
        'USER': 'fashion',                      # Not used with sqlite3.
        'PASSWORD': 'fashion',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # 54.148.208.139 Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

INSTALLED_APPS = (
    'db',
    )

SECRET_KEY = '-srlyoddel%68@txqo0%qx#$_7gkao#k4(!gj$z4iq0yrd32bb'
# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
ALLOWED_HOSTS = ['pizzaparadiso-87c4c4557382.herokuapp.com', '127.0.0.1']

# Database

DB_NAME = "pizza_paradiso"
DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASS = "kwamirzw7samadi"

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = 'django-insecure-$f=hyksp4m0%u%_2ldo2a&$3)rffg@hj6blt+g0&sbnrn---q('


# Dj-stripe

STRIPE_WEBHOOK_SECRET = "whsec_Ra6exjACrpu6gOksXwfoldqqMs2UJxFm"

STRIPE_PUBLIC_KEY = \
    "pk_test_51OMqPMCdFC8wFAX1m6WBevbH8zAjHiVySXQ0qs3dT9CQbexTba9Z9AhbFD0xrwtbKSTQvlQID9O351ITpNthfYYk00Dggoadwk"

STRIPE_SECRET_KEY = \
    "sk_test_51OMqPMCdFC8wFAX1urg7tnrZBg1mktkl412sRohgfl6LDUUeR1Or7eIDV9T3QER6tAnWyQlxXSpazx12H1WuBiwh000PAVi4Xk"

DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"

YOUR_DOMAIN = 'https://pizzaparadiso-58e8f2528358.herokuapp.com'

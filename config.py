# web app config

CSRF_ENABLED = True
WTF_CSRF_ENABLED = True
SECRET_KEY = '389cy83ynr9384cn394runc34r93n4c834ucn89'


# bots config

HOST = 'https://f27b9d61.ngrok.io'

volunteer_access_token = '131cbce7111a80bbc3e89dfee1872d8ebd1b031f864d15a2d8afdcc10822e29ae47b8292a07ac2ec59d3e'
volunteer_confirmation_token = '426e74ba'

request_access_token = '8d5dd9156fa744c707c35e6700f066ac344e94e9c2d2b783cc8cff917b385eb5ed8c3dbdeb14f16e7a30a'
request_confirmation_token = 'a75cda96'


# Food Machine

from alg.experiments.foodmachine import foodMachine

fm = foodMachine()

from environs import Env
# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

TOKEN = env.str('TOKEN')
admin_id = env.list('admin_id')
# bot_id = env.int('bot_id')


user = env.str('SQL_USER', 'postgres')
password = env.str('SQL_PASSWORD', 'pass12345')
db_name = env.str('SQL_DATABASE', 'autoposting')
port = env.str('SQL_PORT', '5432')
host = env.str('SQL_HOST', 'db')

db_url = f'postgres://{user}:{password}@{host}:{port}/{db_name}'

CELERY_BROKER_URL = env.str('CELERY_BROKER', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = env.str('CELERY_BACKEND', 'redis://redis:6379/0')

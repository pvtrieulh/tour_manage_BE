AIC du lịch thông minh
===

SERVER BACKEND
------

### Setup docker

1. Install docker, docker-compose
1. cd into to forder root project (sibilings with docs, scripts, src, ...)
1. Use scripts/django_env.conf (copy from django_env.conf.example in same folder) or src/tetviet/tetviet/settings/local_settings.py (copy from local_settings.py.example in same folder) to setting project (db, redis, celery, ...)
1. Build docker: `docker-compose build`
1. Run project: `docker-compose -f docker-compose-dev.yml up`
1. Into web browser `localhost:8000`

###### Docker run
1. Run cmd: 
    dev: docker-compose -f docker-compose-dev.yml exec python python manage.py migrate  
    Product: docker-compose exec python python manage.py migrate  


## DB config docker develop
1. Name: 'aic_xkld'
2. Port: 3003
3. Host: localhost

### celery
1. Setting in django (local_setting):

    ```
        CELERY_RESULT_BACKEND = 'django-db'
        CELERY_CACHE_BACKEND = 'default'
        CELERY_BROKER_URL = 'redis://redis:6379/0'
    ```

1. Run cmd: `celery -A tetviet worker -l info`


### Note

1. file sh cron_tab open with unix line ending

# Планы:
- Запустить на сервере
- Добавить удаленную файловую систему
- Обсудить поддержку и развитие приложения после запуска!

# Теперь для запуска проекта на компьютере нужно лишь 

```shell
docker compose up
docker compose -f docker-compose-deploy.yml up --build
```
Чтобы отдавать команды нашей среде мы делае следующее:

```shell
docker compose exec app python manage.py migrate
```

При заруске могут возникнуть такая ошибка: `relation "django_session" does not exist`
Это значит что наша база не прошла миграцию. В новом окне терминала запускаем команду что с верху: `docker compose exec app python manage.py migrate`
Просто эта команда включена в запуск на сервере но не в запуск на компьютере.

Чтобы закончить работу напишите:

```shell
docker compose down
```
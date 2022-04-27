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
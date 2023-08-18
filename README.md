## Hammer test task

### Автор: 
Алаткин Александр

### Описание:
Реализация тестового задания от работодателя Hammer systems.<br>
Требовалось реализовать простую реферальную систему с возможностью авторизации по номеру телефона и системой реферальных инвайт кодов. Проект готов для работы локально, используется сеть докер контейнеров. Для авторизации используются jwt-токены.<br>
В корне проекта лежит файл Postman коллекции запросов.

### Использующиеся технологии:
```
Django
Django Rest Framework
JWT
PostgreSQL
Gunicorn
Nginx
Docker
```
### Установка. Как развернуть проект локально:

Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:COOLHax0r1337/api_yamdb.git
```

Запустить сеть докер контейнеров из корневой директории проекта:
```
docker compose -f docker-compose.yml up
```

Выполнить миграции:
```
docker compose -f docker-compose.yml up
```

Собрать и скопировать статику Django:
```
docker compose -f docker-compose.yml exec backend python manage.py collectstatic
docker compose -f docker-compose.yml exec backend cp -r /app/collected_static/. /backend_static/static/
```

### Примеры запросов API:

Авторизация по номеру телефона:<br>
Доступен всем.<br>
Для удобства тестирования в ответ добавлена информация необходимая для отправки последующих запросов:<br>
	id - для запроса к конкретному профилю пользователя,<br>
	authorization_code - для запроса на ввод кода авторизации,<br>
	invite_code - для PATCH запроса активации инвайт кода реферальной системы,<br>

```
POST http://127.0.0.1:8000/api/v1/auth/signup/
Content-Type: application/json

{
    "phone_number": "+79876543211"
}

Response 200 OK

{
    "id": 26,
    "invite_code": "fb2a5b",
    "phone_number": "+79876543211",
    "authorization_code": 2825
}

```

Запрос на ввод кода авторизации:<br>
Доступен всем.<br>
Для удобства тестирования в ответ добавлены jwt-токены, они будут необходимы при запросе на активацию инвайт кода.

```
POST http://127.0.0.1:8000/api/v1/auth/token/
Content-Type: application/json

{
    "phone_number": "+79876543211",
    "authorization_code": 2825
}

Response 200 OK

{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkzMjI5NzkxLCJpYXQiOjE2OTIzNjU3OTEsImp0aSI6IjUxMmRmZGY0YzQ2MDRhNmRiZTM1YjU4MDcyNjQ1OTMxIiwidXNlcl9pZCI6MjZ9.po3V-70Y4fxOV-8f_ga_LLR_Vf7oEk88bnPNS6SQXuQ",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MjQ1MjE5MSwiaWF0IjoxNjkyMzY1NzkxLCJqdGkiOiI2ZTk3MWNmMmQ1Yzc0Yjk2OTg0NGRkZDk3NjY5ZmIyNiIsInVzZXJfaWQiOjI2fQ.fYDkHAFcoOHkM81WJ7bD2oS3gXYJrr0Nf_s5HeUx0hk"
}

```

Запрос на активацию инвайт кода:<br>
Доступен только пользователю, который активирует код, необходим jwt-токен.

```
PATCH http://127.0.0.1:8000/api/v1/users/27/
Content-Type: application/json

{
    "activated_code": "fb2a5b"
}

Response 200 OK

{
    "id": 27,
    "phone_number": "+79876543212",
    "user_invite_code": "3e1221",
    "activated_code": "fb2a5b",
    "invited_users": []
}

```

Запрос на профиль пользователя:<br>
Доступен всем.

```
GET http://127.0.0.1:8000/api/v1/users/26/
Content-Type: application/json

Response 200 OK

{
    "id": 26,
    "phone_number": "+79876543211",
    "user_invite_code": "fb2a5b",
    "activated_code": null,
    "invited_users": [
        {
            "phone_number": "+79876543212"
        }
    ]
}

```

Запрос на удаление профиля пользователя:<br>
Доступен только пользователю, чей профиль удаляется, необходим jwt-токен.

```
DELETE http://127.0.0.1:8000/api/v1/users/27/
Content-Type: application/json

Response 204 No Content

```

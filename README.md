# Salary app
- [x] Код размещен и доступен в публичном репозитории GitLab
- [x] Оформлена инструкция по запуску сервиса и взаимодействию с проектом
- [x] Сервис реализован на FastAPI
- [x] Зависимости зафиксированы менеджером зависимостей poetry
- [x] Написаны тесты с использованием pytest
- [x] Реализована возможность собирать и запускать контейнер с сервисом в Docker

## Использование

### 1. Скопировать репозиторий и зайти в него

```
git clone https://gitlab.com/gorbruno/app-salary
cd app-salary
```

### 2. Настроить .env файл

```
cp .env.example .env
```
По необходимости изменить его параметры:
* DB_NAME — имя sqlite бд
* SERVICE_HOST — хост сервиса 
> 0.0.0.0 позволяет работать через docker
* SERVICE_PORT — порт сервиса
* SECRET_TOKEN — секретный токен для jwt
* ENCRYPTION_ALGORITHM — алгоритм шифрования
> Сейчас работает только HS256
* TIME_EXPIRES — время жизни токена в минутах
* CREATE_TABLE — создать БД из тестовой таблицы

### 3. Создать образ контейнера
```
docker build . -t salary-app

```
### 4. Запустить контейнер
```
docker run --rm -p 8000:8000 salary-app 
```

### 5. Теперь можно отправлять запросы

#### Получить токен
Хост и порт могут отличаться в зависимости от настроек
```
curl -X POST http://localhost:8000/auth/token  -d "username=<username>&password=<password>"  -H "Content-Type: application/x-www-form-urlencoded"
```

Пример пользователя:

> username=aagorbunov

> password=IFkWD13e88VNB

#### Получить информацию о зарплате
```
curl http://localhost:8000/salary -H "Authorization: Bearer <token>"
```

#### Получить информацию о дате повышения
```
curl http://localhost:8000/promotion -H "Authorization: Bearer <token>"
```

### Можно немного проще через Swagger

1) Зайти на http://localhost:8000/docs
2) Ввести пароль в `Authorize`
3) Отправлять запросы через GET-методы на странице


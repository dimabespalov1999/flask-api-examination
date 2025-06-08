
# 📘 Flask-API-Exam — экзаменационный проект

## 📌 Реализованы следующие эндпоинты:
- `POST /submit` — отправка имени и счета
- `GET /results` — получение всех записей
- `GET /ping` — проверка доступности (health-check)

---

## 📁 Структура проекта

```
flask-api-exam/
├── app/
│   ├── __init__.py       # инициализация Flask и БД
│   ├── models.py         # модель Result
│   └── routes.py         # маршруты и обработка API
├── run.py                # точка входа в приложение
├── requirements.txt      # зависимости
├── Dockerfile            # Docker-образ приложения
├── docker-compose.yml    # конфигурация docker-сервисов
├── .env.example          # переменные окружения
└── Jenkinsfile           # CI/CD pipeline для Jenkins
```

---

## 🔧 Как запустить проект локально

### 1. Установите зависимости:
- Docker
- Docker Compose
- Python (опционально, для flake8 и тестов)

### 2. Склонируйте проект:
```bash
git clone https://github.com/dimabespalov1999/flask-api-exam.git
cd flask-api-exam
```

### 3. Создайте `.env` файл:
```env
POSTGRES_USER=admin
POSTGRES_PASSWORD=adminpass
POSTGRES_DB=flaskdb
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### 4. Запуск через Docker Compose:
```bash
docker compose up --build
```

API будет доступен по адресу: [http://localhost:5000](http://localhost:5000)

---

## 🔧 Как настроить Jenkins

### 1. Установка Jenkins в Docker
```bash
docker run -d \
  --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
```

> `-v /var/run/docker.sock:/var/run/docker.sock` — позволяет Jenkins управлять Docker-контейнерами на хосте.

### 2. Установка Docker внутри Jenkins-контейнера
```bash
docker exec -it jenkins bash
```

Внутри контейнера:
```bash
apt update
apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

curl -fsSL https://download.docker.com/linux/debian/gpg | \
    gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
  https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
  > /etc/apt/sources.list.d/docker.list

apt update
apt install -y docker-ce-cli docker-compose
docker --version
```

### 3. Создание Pipeline Job
- `New Item` → `Pipeline`
- Имя: `flask-api-exam`
- SCM: `Git`
- URL: `https://github.com/dimabespalov1999/flask-api-exam.git`
- Script Path: `Jenkinsfile`

---

## 🚀 Как работает CI/CD

CI/CD реализован через `Jenkinsfile` и включает следующие этапы:

| Стадия        | Описание                                                                 |
|---------------|--------------------------------------------------------------------------|
| `Checkout`    | Клонирует код из Git-репозитория                                         |
| `Set up Python Environment` | Устанавливает Python, зависимости и виртуальное окружение |
| `Lint and Auto-fix` | Проверяет стиль кода с помощью `flake8`, автоматически исправляет с помощью `autopep8` |
| `Tests`       | Запускает тесты с использованием `pytest`                               |
| `Build and Deploy` | Собирает Docker-образ и запускает `docker compose up --build`      |

---

## 🧪 Тестирование проекта

### 📋 Используется `pytest`

Проверяется:
- `/ping` — ответ 200 OK
- `/submit` — валидные и невалидные данные
- `/results` — получение данных из БД

### 🚀 Запуск вручную:
```bash
pip install -r requirements.txt
pytest
```

---

## 🧹 Линтинг и автоисправление кода

Используются:
- `flake8` — проверка на соответствие PEP8
- `autopep8` — автоисправление стиля

### Проверка:
```bash
flake8 app/ run.py
```

### Автоисправление:
```bash
autopep8 --in-place --recursive app
```

В Jenkins это делается на этапе `Lint and Auto-fix` автоматически.

---

## 🔗 Примеры API-запросов

### ✅ Проверка:
```bash
curl http://localhost:5000/ping
```

### 📝 Отправка данных:
```bash
curl -X POST http://localhost:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"name": "Иван", "score": 88}'
```

### 📋 Получение результатов:
```bash
curl http://localhost:5000/results
```

---

## 📎 Ссылки
- GitHub: [https://github.com/dimabespalov1999/flask-api-exam](https://github.com/dimabespalov1999/flask-api-exam)

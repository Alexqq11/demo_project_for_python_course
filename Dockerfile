# используйте официальный образ Python в качестве базового образа
FROM python:3.9-slim

# установите рабочую директорию в контейнере
WORKDIR /app

# установите зависимости
COPY requirements.txt .
RUN pip install -r requirements.txt

# копируйте приложение в рабочую директорию
COPY . .

# запустите приложение при запуске контейнера
CMD ["python", "app.py"]

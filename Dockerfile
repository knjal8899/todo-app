FROM python:3.7

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["gunicorn", "todo_app.wsgi:application", "--bind", "0.0.0.0:8000"]

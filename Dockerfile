FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1  # Prevent Python from writing .pyc files to disk
ENV PYTHONUNBUFFERED 1  # Ensure that the output from the application is logged immediately

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "todoproject.wsgi:application"]

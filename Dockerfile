FROM python:3.10

COPY main.py utils.py colormaps.py requirements.txt .
COPY static/ static 
COPY templates/ templates

RUN pip install -r requirements.txt

CMD ["gunicorn", "main:app", "-b 0.0.0.0:80"]
FROM python:3.11-slim  
  
WORKDIR /app  
  
COPY pyproject.toml /app/  
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root --no-interaction  
  
COPY . /app  
  
EXPOSE 8000  
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]  
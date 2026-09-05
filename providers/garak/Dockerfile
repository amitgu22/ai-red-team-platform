FROM python:3.12-slim
WORKDIR /workspace
RUN pip install --no-cache-dir garak
COPY adapter.py .
CMD ["python", "--version"]

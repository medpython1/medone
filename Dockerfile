
# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --trusted-host pypi.python.org -r requirements.txt
# 
COPY ./apis /code/apis

# 
CMD ["uvicorn", "apis.barcode:app", "--host", "0.0.0.0", "--port", "8000"]


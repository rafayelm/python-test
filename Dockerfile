FROM python:3.10.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Add wait-for-it.sh script
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh .

# Grant execute permissions to the script
RUN chmod +x wait-for-it.sh

# Modify CMD to wait for the database before starting the Python app
CMD ["./wait-for-it.sh", "database:5432", "--", "python", "api/app.py"]
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

COPY factory_sensor_simulator_2040.csv .
COPY simulator.py .

CMD ["python", "-u", "simulator.py"]
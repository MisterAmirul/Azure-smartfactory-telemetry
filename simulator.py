#Edge-to-Cloud Telemetry producer
#================================================================================
#objective of simulation:

#-simulate a real industrial edge
#-standardize ingestion via OPenTelemetry metrics
#-capture telemetry via Azure Container Insights
#-trigger AI-Driven predicitive maintenance


#image:v1 = infrastructure smoke test and pipeline scaffolding
#image:v2 = integrate authentic synthetic data

#================================================================================

import csv
import json
import logging
import os
import sys
import time
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter

#1. Configure JSON Logging to STDOUT
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger("factory-telemetry")


#2. Initialize OpenTelemetry Metrics Provider
exporter = ConsoleMetricExporter()
reader = PeriodicExportingMetricReader(exporter, export_interval_millis=10000) #flash aggregate metrics every 10 seconds
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter("factory.sensor.telemetry")

#2.5 Define OpenTelemetry Gauges for dynamic measurements
temp_gauge = meter.create_gauge("factory.sensor.temperature_c", unit="Celsius", description="Machine Temperature")
vibration_gauge = meter.create_gauge("factory.sensor.vibration_mms", unit="mm/s", description="Machine Vibration")
power_gauge = meter.create_gauge("factory.sensor.power_kw", unit="kW", description="Power Consumption")
sound_gauge = meter.create_gauge("factory.sensor.sound_db", unit="dB", description="Sound Level")


#3. datafile path
CSV_PATH = os.getenv("DATASET_PATH", "factory_sensor_simulator_2040.csv")


#4. core logic
def stream_dataset():
    #5. check datafile exists or not 
    if not os.path.exists(CSV_PATH):
        logger.error(f"Dataset not found at {CSV_PATH}")
        sys.exit(1)

    logger.info(f"Loaded dataset from {CSV_PATH}. Starting telemetry stream...")


    #6. parse csv 
    while True:
        with open(CSV_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                machine_id = row.get("Machine_ID", "UNKNOWN")
                machine_type = row.get("Machine_Type", "UNKNOWN")
                
                #catch corrupted row and skip
                try:
                    temp = float(row.get("Temperature_C", 0.0))
                    vibration = float(row.get("Vibration_mms", 0.0))
                    power = float(row.get("Power_Consumption_kW", 0.0))
                    sound = float(row.get("Sound_dB", 0.0))
                    rul_days = float(row.get("Remaining_Useful_Life_days", 0.0))
                except ValueError:
                    continue


                #7. determine if failure is imminent based on column
                failure_imminent = row.get("Failure_Within_7_Days", "False").strip().lower() == "true"

                #8. labeling data
                labels = {"machine_id": machine_id, "machine_type": machine_type}
                temp_gauge.set(temp, labels)
                vibration_gauge.set(vibration, labels)
                power_gauge.set(power, labels)
                sound_gauge.set(sound, labels)

                #9. Prepare data payload for logging
                payload = {
                    "timestamp": time.time(),
                    "machine_id": machine_id,
                    "machine_type": machine_type,
                    "operational_hours": row.get("Operational_Hours"),
                    "temperature_c": temp,
                    "vibration_mms": vibration,
                    "sound_db": sound,
                    "power_kw": power,
                    "oil_level_pct": row.get("Oil_Level_pct"),
                    "coolant_level_pct": row.get("Coolant_Level_pct"),
                    "remaining_useful_life_days": rul_days,
                    "failure_within_7_days": failure_imminent,
                    "status": "CRITICAL_ALERT" if failure_imminent else "NORMAL"
                }


                #10. column handling, inject NONE for non-exist data
                for opt in ["Laser_Intensity", "Hydraulic_Pressure_bar", "Coolant_Flow_L_min"]:
                    val = row.get(opt, "").strip()
                    if val:
                        payload[opt.lower()] = val

                #emits one structure JSON log line per second to control nodes process two concurrent data
                #2 nodes run same process as backup, data redundancy. so process keep alive even one node down
                logger.info(json.dumps(payload))
                time.sleep(1.0)

#11. create opentelemetrymetrics
if __name__ == "__main__":
    stream_dataset()


#import cosmos library
import os
from datetime import timedelta
from azure.cosmos import CosmosClient
from azure.identity import AzureCliCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus


#credentials configuration
WORKSPACE_ID = "8485186f-e580-4e73-be3b-7949121f2173"
COSMOS_CONN_STR = os.getenv("COSMOS_CONN_STR")

if not COSMOS_CONN_STR:
    raise ValueError("COSMOS_CONN_STR environment variable is not set.")


#client instantiation and container targeting
credential = AzureCliCredential()
logs_client = LogsQueryClient(credential)
cosmos_client = CosmosClient.from_connection_string(COSMOS_CONN_STR)

db = cosmos_client.get_database_client("FactoryTelemetryDB")
container = db.get_container_client("CriticalIncidents")


#KQL script query extraction
query = """
ContainerLogV2
| where ContainerName == "factory-sim-container"
| where LogMessage has "machine_id"
| extend Telemetry = parse_json(LogMessage)
| where Telemetry.status == "CRITICAL_ALERT"
| project 
    TimeGenerated,
    Node = Computer,
    Pod = PodName,
    MachineID = tostring(Telemetry.machine_id),
    MachineType = tostring(Telemetry.machine_type),
    Temp_C = toreal(Telemetry.temperature_c),
    Vibration_mms = toreal(Telemetry.vibration_mms),
    RUL_Days = toreal(Telemetry.remaining_useful_life_days),
    Status = tostring(Telemetry.status)
| order by TimeGenerated desc
| take 30
"""


#execut KQL query
print("[*] Fetching critical alerts from Log Analytics...")
response = logs_client.query_workspace(
    workspace_id=WORKSPACE_ID,
    query=query,
    timespan=timedelta(days=2)
)


#upsert loop
if response.status == LogsQueryStatus.SUCCESS:
    table = response.tables[0]
    print(f"[+] Found {len(table.rows)} critical alert records to ingest.")
    
    for row in table.rows:
        time_gen, node, pod, machine_id, machine_type, temp, vibration, rul, status = row
        
        doc_id = f"INC-{machine_id}-{int(time_gen.timestamp())}"
        incident_doc = {
            "id": doc_id,
            "machine_id": machine_id,
            "machine_type": machine_type,
            "status": status,
            "remaining_useful_life_days": rul,
            "telemetry": {
                "temperature_c": temp,
                "vibration_mms": vibration
            },
            "cluster_context": {
                "node": node,
                "pod": pod
            },
            "incident_status": "OPEN",
            "ai_work_order": None,
            "timestamp": time_gen.isoformat()
        }
        
        container.upsert_item(incident_doc)
        print(f" -> Upserted incident: {doc_id} ({machine_type})")

    #log
    print("\n[✔] Sync complete. Documents written to Cosmos DB container 'CriticalIncidents'.")
else:
    print(f"[-] Query failed: {response.status}")

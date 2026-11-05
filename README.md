## Hands-on lab integrating a Kaggle dataset into Azure using a multi-service pipeline.


1. Provisioning an empty Azure Resource Group to logically contain all the microservices for the factory pipeline.
<img width="1894" height="930" alt="Screenshot From 2026-10-23 00-17-39" src="https://github.com/user-attachments/assets/dd757a23-0ae1-4f99-ba35-11bf8eef4c2c" />

<br><br><br>

2. Authenticated Podman using an Azure CLI token and successfully pushed an initial scaffolded image (factory-sim:v1) to the private container registry (detroitfactoryacr).
<img width="1895" height="412" alt="Screenshot From 2026-10-23 00-25-09" src="https://github.com/user-attachments/assets/6c184727-1cd7-4daa-9a91-1b435da45215" />

<br><br><br>

3. Deployed the Azure Kubernetes Service (AKS) cluster (factory-aks-eastus) into the resource group using the Standard tier and Azure CNI networking.
<img width="1863" height="920" alt="Screenshot From 2026-10-25 18-29-30" src="https://github.com/user-attachments/assets/ed72780d-4905-42d5-a02e-df9ec98e3a34" />

<br><br><br>

4. Pulled the AKS cluster credentials into the local ~/.kube/config and verified the worker node pool was ready using kubectl get nodes.
<img width="1899" height="536" alt="Screenshot From 2026-10-25 18-42-59" src="https://github.com/user-attachments/assets/4751a943-14c4-4571-b58d-7b3ecc23e31f" />

<br><br><br>



5. Validating the pod status across the cluster to verify that the initial deployment was successfully running.
<img width="1481" height="657" alt="Screenshot From 2026-10-25 19-02-13" src="https://github.com/user-attachments/assets/1fee2bb7-f309-4b49-9e22-4b3d7f42be0c" />

<br><br><br>



6. Downloaded the Industrial IoT (Synthetic) dataset from Kaggle to simulate realistic machine telemetry and sensor readings.
<img width="1905" height="940" alt="Screenshot From 2026-10-25 19-07-17" src="https://github.com/user-attachments/assets/c71a4ec2-29f0-44e7-a9f0-7edbae2a4973" />

<br><br><br>

7. Wrote the simulator.py script to generate edge-to-cloud telemetry and standardize metrics ingestion using OpenTelemetry.

<img width="1903" height="940" alt="Screenshot From 2026-10-25 19-47-47" src="https://github.com/user-attachments/assets/d809325d-590e-469d-b88d-7d6d267177de" />

<br><br><br>


8. Containerizing and built the Dockerfile locally into a final, runnable container image (factory-sim:v2) containing the synthetic data and pushed it securely to ACR.
<img width="1903" height="940" alt="Screenshot From 2026-10-25 20-02-29" src="https://github.com/user-attachments/assets/4325cc6c-f2b6-4f6d-8406-21d59c4a1981" />

<br><br><br>

9. Monitoring live pod telemetry using kubectl logs to confirm that the Python application was successfully streaming JSON telemetry for pumps, molders, and boilers.
<img width="1896" height="993" alt="Screenshot From 2026-10-25 20-49-40" src="https://github.com/user-attachments/assets/9e615036-d0f7-40bd-806f-3465746022c6" />

<br><br><br>

10. Executed a Kusto Query Language (KQL) command in Log Analytics to count and verify the total telemetry records being ingested per Kubernetes pod.
<img width="1895" height="920" alt="Screenshot From 2026-10-25 21-59-13" src="https://github.com/user-attachments/assets/7cb43b7e-e4b7-4d0d-b7ec-4123e2d24225" />

<br><br><br>


<img width="1895" height="920" alt="Screenshot From 2026-10-25 22-01-08" src="https://github.com/user-attachments/assets/b080ae9e-e104-4826-bd2a-d644af8a0064" />

<br><br><br>


<img width="1895" height="920" alt="Screenshot From 2026-10-25 22-01-23" src="https://github.com/user-attachments/assets/a8a6ce90-e614-4287-951f-ee92e9dc36b7" />

<br><br><br>

11. Provisioning Azure Cosmos DB NoSQL account (smartfactory-cosmos-oct2026) to serve as the hot storage layer for critical incidents.
<img width="1895" height="920" alt="Screenshot From 2026-10-25 22-53-47" src="https://github.com/user-attachments/assets/fcb6633e-ba88-475c-9808-4edf04146bc7" />

<br><br><br>


12. Ran sync_incidents.py to automatically query Log Analytics for critical alerts and upsert 30 isolated incident records directly into Cosmos DB.
<img width="1886" height="910" alt="Screenshot From 2026-10-26 23-10-27" src="https://github.com/user-attachments/assets/590fa63c-5e62-4bba-ac40-30ed69fded17" />

<br><br><br>

13. Verifying NoSQL Data Ingestion in the Data Explorer Azure Portal to confirm the JSON documents were perfectly structured inside the CriticalIncidents container.
<img width="1886" height="983" alt="Screenshot From 2026-10-26 23-11-14" src="https://github.com/user-attachments/assets/f0736031-9c3a-4a5c-bc2b-4e0fe87d5ba7" />

<br><br><br>

14. Provisioning Azure Managed Grafana
<img width="1916" height="1005" alt="Screenshot From 2026-10-30 23-16-46" src="https://github.com/user-attachments/assets/cada7016-5eb4-4c1b-b624-8b80b37b4c9b" />

<br><br><br>

15. Provisions and configured Grafana panels by writing direct KQL queries to Azure Monitor, visualizing live temperature and vibration metrics over a 7-day period.
<img width="1901" height="879" alt="Screenshot From 2026-10-31 20-11-49" src="https://github.com/user-attachments/assets/890ca843-992f-4bab-9d3f-e8d8fed80aa0" />

<br><br><br>

16. Created an additional Grafana table panel specifically designed to track and display critical machine alerts parsed directly from the log stream.
<img width="1901" height="879" alt="Screenshot From 2026-10-31 20-16-36" src="https://github.com/user-attachments/assets/fa71481d-4414-455b-9826-01a009538e50" />

<br><br><br>





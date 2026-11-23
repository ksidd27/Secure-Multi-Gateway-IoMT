\# Secure Multi-Gateway Architecture for the Internet of Medical Things (IoMT)



A containerized IoMT edge architecture integrating EdgeX Foundry, JWT-secured Kong API gateways, HAProxy load balancing, and PostgreSQL. The project evaluates gateway-level redundancy, failure recovery, request distribution, and performance under controlled load tests.



\## 1. Project Overview



Internet of Medical Things (IoMT) environments involve connected devices and services that exchange healthcare-related data. Securing API access and maintaining service availability are important considerations in such environments.



This project implements and evaluates a multi-gateway architecture using two Kong API Gateway instances behind an HAProxy load balancer. Both gateways share a PostgreSQL database, while EdgeX Foundry provides the edge-service environment.



The implementation focuses on:



\- JWT-based API authentication.

\- Multiple API gateway instances.

\- Load balancing using HAProxy.

\- Gateway failure detection and recovery.

\- Performance evaluation under different request rates.



\*\*Note:\*\* The experiments use the EdgeX Core Data ping endpoint. They do not represent real medical-device transactions or clinical workload validation.



\## 2. Architecture



!\[Proposed Architecture](architecture/proposed\_architecture.jpg)



\### Main Components



| Component | Purpose |

|---|---|

| EdgeX Foundry 1.0.1 | Edge computing and service environment |

| Kong API Gateway 1.0.3 | API gateway and JWT-based access control |

| PostgreSQL 9.6 | Shared Kong configuration database |

| HAProxy 2.8-alpine | Load balancing and gateway health monitoring |

| Docker Compose | Container deployment and orchestration |

| k6 | Performance and load testing |



Two Kong gateway instances operate behind HAProxy. HAProxy distributes requests using round-robin balancing and monitors gateway availability.



\## 3. Repository Structure



```text

.

├── architecture/

│   └── proposed\_architecture.jpg

│

├── docker/

│   ├── docker-compose-edinburgh-1.0.1.yml

│   ├── docker-compose-multigateway.yml

│   └── haproxy.cfg

│

├── documentation/

│   ├── docker\_deployment.png

│   ├── resource\_snapshot\_2026-11-01\_16-31-15.txt

│   └── response\_size\_validation.txt

│

├── experiments/

│   ├── comparative\_latency/

│   ├── multi\_gateway/

│   └── single\_gateway/

│

├── scripts/

│   ├── analysis/

│   └── performance/

│

├── .env.example

├── .gitignore

└── README.md

```



\## 4. Deployment



\### Prerequisites



\- Docker Desktop

\- Docker Compose

\- Git

\- A locally configured environment file



\### Configure Environment Variables



Clone the repository and navigate to its root directory.



Create a `.env` file using `.env.example` as a reference.



Set your own local PostgreSQL password:



```env

KONG\_PG\_PASSWORD=your\_local\_password

```



Do not commit the `.env` file.



\### Start the Deployment



Run the following command from the repository root:



```powershell

docker compose --env-file .env -f docker/docker-compose-edinburgh-1.0.1.yml -f docker/docker-compose-multigateway.yml up -d

```



The base Compose file defines the EdgeX environment, PostgreSQL, and the first Kong gateway. The additional Compose file adds the second Kong gateway and HAProxy.



\### Exposed Ports



| Service | Host Port |

|---|---:|

| EdgeX Core Data | 48080 |

| Kong Gateway 1 | 8000 |

| Kong Gateway 2 | 18000 |

| HAProxy | 18080 |

| PostgreSQL | 5432 |



The deployment uses legacy component versions for experimental reproducibility. It is intended for local research and testing, not as a production-ready healthcare deployment.



\*\*Configuration note:\*\* The Kong service, route, JWT plugin, and JWT credentials must be configured as required by the experiment. Starting the containers alone should not be interpreted as automatically provisioning all API authentication resources.



\## 5. Authentication and Gateway Failover



\### JWT Authentication



The API endpoint is protected using JWT authentication.



The observed behavior was:



\- Requests without a valid JWT receive HTTP 401.

\- Requests with a valid JWT receive HTTP 200.



\### Gateway Failure and Recovery



The failover experiment examined the behavior of HAProxy when one gateway became unavailable.



1\. Both Kong gateway instances were started.

2\. Kong Gateway 2 was stopped.

3\. HAProxy detected the unavailable gateway and marked it down.

4\. An authenticated request through HAProxy continued to receive HTTP 200 through Kong Gateway 1.

5\. Kong Gateway 2 was restarted.

6\. HAProxy detected its recovery and returned it to the active backend pool.

7\. Ten authenticated requests were observed: five handled by Kong Gateway 1 and five by Kong Gateway 2.



The HAProxy health check expects HTTP 401 from a protected ping endpoint. This confirms that the gateway responds and enforces authentication; it does not independently establish the health of the EdgeX upstream service.



\## 6. Performance Evaluation



Performance testing was conducted using k6 with a constant-arrival-rate executor for the comparative experiments.



Each run lasted 30 seconds and targeted the EdgeX ping endpoint through three configurations:



1\. Direct EdgeX access.

2\. Single Kong gateway.

3\. HAProxy with two Kong gateway instances.



\### Comparative Results



| Target RPS | Direct EdgeX Actual RPS | Direct P95 (ms) | Single Kong Actual RPS | Single P95 (ms) | Multi-Gateway Actual RPS | Multi P95 (ms) |

|---:|---:|---:|---:|---:|---:|---:|

| 100 | 100.03 | 3.79 | 100.01 | 4.80 | 100.01 | 5.85 |

| 200 | 200.02 | 1.97 | 200.01 | 2.94 | 200.00 | 3.08 |

| 350 | 350.00 | 1.69 | 349.99 | 2.28 | 350.00 | 2.75 |

| 500 | 500.00 | 1.63 | 496.01 | 3.43 | 498.67 | 2.82 |

| 700 | 687.67 | 2.02 | 699.72 | 2.64 | 699.49 | 3.21 |

| 850 | 849.77 | 1.60 | 849.71 | 2.68 | 849.54 | 3.34 |

| 1000 | 990.85 | 2.20 | 987.75 | 7.83 | 998.99 | 6.65 |



\*P95 values are in milliseconds. Results represent the recorded experimental runs; two runs were conducted at 100, 200, and 500 RPS, while one run was conducted at each of the other target rates.\*



\### Key Observations



\- Direct EdgeX access generally showed lower response latency because it did not include the additional gateway and load-balancing layers.

\- The multi-gateway configuration maintained approximately 999 actual requests per second at a target of 1000 RPS in the recorded run.

\- At 1000 target RPS, the multi-gateway configuration recorded 24 dropped iterations, compared with 361 for single Kong and 269 for direct EdgeX.

\- The multi-gateway configuration demonstrated gateway-level redundancy during the failure and recovery experiment.



\*\*Important:\*\* Dropped iterations represent scheduled iterations that k6 could not start. They are not equivalent to failed HTTP requests.



\### Graphs



Performance graphs and supporting experimental data are available under:



\- `experiments/multi\_gateway/graphs/`

\- `experiments/single\_gateway/graphs/`

\- `experiments/comparative\_latency/graphs/`



Raw and summarized data are available in the corresponding `data/` directories.



\## 7. Limitations



\- Experiments were conducted in a local Docker environment.

\- Performance tests used the EdgeX ping endpoint rather than real medical-device transactions.

\- No clinical validation or real-world medical-device interoperability testing was performed.

\- The gateway health check verifies gateway responsiveness and JWT enforcement, not the complete health of the upstream EdgeX service.

\- The deployed software versions are legacy versions and require modernization before any production-oriented application.

\- Performance results are specific to the experimental environment and should not be generalized to production IoMT deployments.



\## 8. Future Work



Potential extensions include:



\- Testing with realistic IoMT telemetry workloads.

\- Evaluating additional API gateway implementations.

\- Implementing end-to-end upstream health monitoring.

\- Evaluating TLS, stronger secret management, and hardened deployment configurations.

\- Conducting repeated experiments across different hardware and deployment environments.



\## 9. Technologies Used



`Docker` · `Docker Compose` · `EdgeX Foundry` · `Kong API Gateway` · `HAProxy` · `PostgreSQL` · `JWT` · `k6` · `Python` · `PowerShell`



\## 10. Author



Developed as an academic research and implementation project focused on API security, gateway redundancy, and performance evaluation in an IoMT-oriented edge architecture.

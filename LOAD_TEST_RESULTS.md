# WorkFlow API Load Test Results

## 1. Overview

This document presents the results of a load test performed on the WorkFlow REST API using Locust. The purpose of the test was to evaluate API response times, request throughput, and reliability under concurrent user load.

## 2. Test Configuration

| Parameter | Value |
|---|---|
| Load testing tool | Locust |
| Test duration | 5 minutes |
| Number of concurrent users | 30 |
| Spawn rate | 3 users/second |
| Target endpoint | `http://localhost:8000` |
| Tested endpoints | `POST /users/login/`, `GET /projects/` |

## 3. Overall Results

| Metric | Result |
|---|---:|
| Total requests | 4,455 |
| Total failures | 0 |
| Failure rate | 0% |
| Overall average response time | 22.04 ms |
| Overall median response time | 14 ms |
| 95th percentile response time | 35 ms |
| 99th percentile response time | 83 ms |
| Maximum response time | 919 ms |

## 4. Endpoint Performance

| Endpoint | Requests | Failures | Average (ms) | Median (ms) | P95 (ms) | P99 (ms) |
|---|---:|---:|---:|---:|---:|---:|
| `GET /projects/` | 4,425 | 0 | 17.28 | 14 | 33 | 59 |
| `POST /users/login/` | 30 | 0 | 724.55 | 730 | 910 | 920 |

## 5. Analysis

- **Reliability:** No request failures were recorded during the test.
- **Project listing:** The `GET /projects/` endpoint showed an average response time of 17.28 ms.
- **Authentication:** The login endpoint had a higher average response time of 724.55 ms. Password hashing and verification may contribute to authentication latency.
- **Response time distribution:** The overall 95th percentile was 35 ms, meaning that 95% of recorded requests completed within approximately 35 ms.

## 6. Conclusion

The WorkFlow API completed 4,455 requests with zero recorded failures during this five-minute test with 30 concurrent users.

The project listing endpoint demonstrated low response times under the tested conditions. Authentication was slower than project listing and may warrant further investigation if authentication performance becomes a concern.

These results represent a local test environment and should not be interpreted as a measure of production capacity. Further testing with higher concurrency and a production-like environment would be needed to assess scalability.

## 7. Limitations

- The test was conducted against a locally hosted application.
- Results may depend on hardware, database state, caching, and the test environment.
- The test covered only the login and project-listing endpoints.
- The results do not establish the maximum capacity of the application.

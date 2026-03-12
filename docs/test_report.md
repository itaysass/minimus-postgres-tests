# PostgreSQL Image Compatibility Test Report

## Summary

This report documents the compatibility testing performed between the reference PostgreSQL container image and the custom PostgreSQL image.

Images tested:

Reference image:

bitnami/postgresql:latest

Custom image:

halex1985/postgresql:latest

Testing was performed in two environments:

1. OCI container runtime (Docker)
2. Kubernetes deployment using the Bitnami PostgreSQL Helm chart

---

# Environment

Local environment:

- Windows host
- Ubuntu (WSL)
- Docker

Kubernetes environment:

- Minikube cluster
- Helm
- Bitnami PostgreSQL Helm chart

---

# Test Results Overview

| Test | Reference Image | Custom Image |
|-----|-----|-----|
OCI startup | PASS | FAIL |
Helm deployment | PASS | PASS |
Database connectivity | PASS | PASS |
SQL operations | PASS | PASS |
Bitnami init directory compatibility | PASS | FAIL |

---

# Test 1 — OCI Container Startup

## Objective

Verify that the PostgreSQL container starts correctly using Docker.

## Reference Image

Command:

docker run --rm -d \
  --name pg-ref \
  -e POSTGRESQL_USERNAME=testuser \
  -e POSTGRESQL_PASSWORD=testpass123 \
  -e POSTGRESQL_DATABASE=testdb \
  -p 5432:5432 \
  bitnami/postgresql:latest

Result:

Container starts successfully and PostgreSQL initializes correctly.

---

## Custom Image

Command:

docker run --rm -d \
  --name pg-test \
  -e POSTGRESQL_USERNAME=testuser \
  -e POSTGRESQL_PASSWORD=testpass123 \
  -e POSTGRESQL_DATABASE=testdb \
  -p 5433:5432 \
  halex1985/postgresql:latest

Result:

Container exits immediately.

Observed error:

mkdir: cannot create directory '/bitnami/postgresql/data': Permission denied

### Root Cause

Directory `/bitnami/postgresql` is not writable by the runtime user (`uid 1001`), preventing database initialization.

### Severity

P1 — container cannot start in OCI mode.

---

# Test 2 — Helm Deployment

## Objective

Verify compatibility with the Bitnami PostgreSQL Helm chart.

## Reference Image

Command:

helm install pg-ref bitnami/postgresql

Result:

Pod starts successfully and database initializes normally.

---

## Custom Image

Command:

helm install pg-test bitnami/postgresql \
  --set image.repository=halex1985/postgresql \
  --set image.tag=latest \
  --set global.security.allowInsecureImages=true

Result:

Pod starts successfully and becomes ready.

---

# Test 3 — Database Connectivity

Connectivity verified using a PostgreSQL client pod.

Command:

psql -h pg-test-postgresql -U testuser -d testdb -c "SELECT 1;"

Result:

 ?column?
----------
        1
(1 row)

Database connectivity is functional.

---

# Test 4 — SQL Operations

SQL operations were verified.

Create table:

CREATE TABLE smoke(id INT);

Insert row:

INSERT INTO smoke VALUES (1);

Query table:

SELECT * FROM smoke;

Result:

 id
----
  1

Database operations function normally.

---

# Test 5 — Bitnami Initialization Script Compatibility

The Bitnami PostgreSQL container supports initialization scripts via the following directories:

/docker-entrypoint-preinitdb.d
/docker-entrypoint-initdb.d

These directories should be readable by the container runtime user.

Observed behavior in the custom image:

Logs contain permission errors:

find: '/docker-entrypoint-preinitdb.d/': Permission denied
find: '/docker-entrypoint-initdb.d/': Permission denied

### Impact

Initialization scripts placed in these directories will not be executed.

This breaks compatibility with the expected Bitnami initialization mechanism.

### Severity

P2 — Helm deployment works but initialization hooks are broken.

---

# Additional Observation

The custom image sets:

ALLOW_EMPTY_PASSWORD=yes

by default, which weakens the container security configuration.

### Severity

P2 — unsafe default configuration.

---

# Conclusion

The custom PostgreSQL image contains several compatibility issues:

1. The container fails to start in OCI environments due to incorrect filesystem permissions.
2. The container cannot access Bitnami initialization directories, breaking Helm chart compatibility.
3. The image enables an unsafe default configuration.

Although the database starts successfully under Helm due to mounted volumes masking the permission issue, the image is not fully compatible with the Bitnami PostgreSQL container contract.

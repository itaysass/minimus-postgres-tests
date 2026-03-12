# PostgreSQL Image Compatibility Evaluation

This repository contains the compatibility evaluation between the Bitnami PostgreSQL container image and a custom PostgreSQL container image.

Custom image tested:

halex1985/postgresql:latest

Reference image:

bitnami/postgresql:latest

The goal is to verify that the custom image behaves correctly when used with the Bitnami PostgreSQL Helm chart.

---

# Repository Structure

minimus-postgres-tests
│
├── docs
│ ├── test_plan.md
│ └── test_report.md
│
├── tests
│
└── README.md

- **docs/test_plan.md** — testing strategy
- **docs/test_report.md** — detailed findings
- **tests/** — automation scripts 

---

# Environment

Testing environment used:

Host:
- Windows
- Ubuntu (WSL)

Tools:
- Docker
- Kubernetes (Minikube)
- Helm
- kubectl

---

# Tested Images

Reference image: bitnami/postgresql:latest
Custom image: halex1985/postgresql:latest

---

# Test Coverage

The following compatibility areas were validated:

- OCI container startup
- Helm deployment compatibility
- Database connectivity
- SQL operations
- Bitnami initialization scripts

---

# Key Findings

### 1. OCI Container Startup Failure

The custom image fails to start when run directly via Docker.

Observed error:
mkdir: cannot create directory '/bitnami/postgresql/data': Permission denied

Root cause:

The directory `/bitnami/postgresql` is not writable by the runtime user (`uid 1001`).

Severity: **P1**

---

### 2. Bitnami Initialization Script Permissions

Logs contain:
find: '/docker-entrypoint-preinitdb.d/': Permission denied
find: '/docker-entrypoint-initdb.d/': Permission denied

Impact:

Initialization scripts will not execute correctly.

Severity: **P2**

---

### 3. Unsafe Default Configuration

The container enables:
ALLOW_EMPTY_PASSWORD=yes
This weakens security and should not be enabled by default.

Severity: **P2**

---

# Successful Tests

The following tests succeeded:

- Helm deployment
- PostgreSQL startup in Kubernetes
- Database connectivity
- SQL operations

Example test:
SELECT 1;
Result: 1

---

# Reproducing the Tests

## Start Minikube
minikube start


---

## Install PostgreSQL Reference Deployment
helm install pg-ref bitnami/postgresql
--set auth.username=testuser
--set auth.password=testpass123
--set auth.database=testdb
--set primary.persistence.enabled=false
---

## Install Custom Image Deployment
helm install pg-test bitnami/postgresql
--set image.repository=halex1985/postgresql
--set image.tag=latest
--set auth.username=testuser
--set auth.password=testpass123
--set auth.database=testdb
--set primary.persistence.enabled=false
--set global.security.allowInsecureImages=true
---

## Connectivity Test
kubectl run pg-test-client --rm -i --restart='Never'
--image registry-1.docker.io/bitnami/postgresql:latest
--env="PGPASSWORD=testpass123"
--command -- psql --host pg-test-postgresql -U testuser -d testdb -c "SELECT 1;"

---

# Conclusion

The custom PostgreSQL image partially works with the Bitnami Helm chart but contains compatibility issues that prevent it from being a drop-in replacement.

The main issues are:

- incorrect filesystem permissions
- initialization script directory access
- unsafe default configuration

These issues should be resolved before the image can be considered fully compatible.

---

# Running the Automated Tests

The repository contains two automated test suites implemented using `pytest`.

Before running the tests, activate the Python virtual environment:

source venv/bin/activate

1. Baseline Tests (Reference Image):

These tests validate the behavior of the official Bitnami PostgreSQL image.

pytest -s tests/reference_tests.py

Expected result:

All tests should PASS.

Example output:
tests/reference_tests.py::test_reference_image_starts PASSED
tests/reference_tests.py::test_reference_helm_deployment PASSED

These tests verify:
container startup
database connectivity
SQL functionality
Helm deployment compatibility

2. Bug Reproduction Tests (Custom Image)

These tests validate the custom PostgreSQL image:
halex1985/postgresql:latest

Run:

pytest -s tests/bug_repro_tests.py

Expected result:
Tests FAIL, because they reproduce the defects identified during the evaluation.

Example output:

FAILED tests/bug_repro_tests.py::test_custom_oci_container_should_start
FAILED tests/bug_repro_tests.py::test_custom_image_should_not_have_init_permission_errors
FAILED tests/bug_repro_tests.py::test_empty_password_configuration_should_not_be_enabled

Bugs Detected by Automation:
test_custom_oci_container_should_start --> Container fails to start in OCI runtime due to filesystem permission issues
test_custom_image_should_not_have_init_permission_errors --> Helm deployment logs contain permission errors for Bitnami init directories
test_empty_password_configuration_should_not_be_enabled --> Container enables ALLOW_EMPTY_PASSWORD=yes, creating an insecure configuration

Notes
The failing tests demonstrate the compatibility issues between the custom PostgreSQL image and the Bitnami PostgreSQL container expectations.
These defects are documented in detail in:
docs/test_report.md

and the testing methodology is described in:
docs/test_plan.md

# Author

Itay Sasson:

itaysasss@gmail.com

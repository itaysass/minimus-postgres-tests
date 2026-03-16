
Test Report – PostgreSQL Slim Image Evaluation

Overview
This report summarizes the evaluation of the custom PostgreSQL slim image compared with the Bitnami PostgreSQL reference image.

Reference image: bitnami/postgresql:latest
Custom image: halex1985/postgresql:latest

Test Environment
Ubuntu (WSL) on Windows
Docker
Kubernetes (Minikube)
Helm
Python 3.x
pytest

Image Size Comparison
Reference image size: ~117 MB
Custom image size: ~38 MB
The custom image is approximately 67 percent smaller than the reference image.

Functional Validation
Basic PostgreSQL functionality works correctly once the container starts successfully.

Example operations validated:
SELECT version()
CREATE TABLE smoke(id INT)
INSERT INTO smoke VALUES (1)
SELECT * FROM smoke

Identified Issues

Secret leakage in logs
The container entrypoint runs with shell debugging enabled (set -x).
Sensitive environment variables such as POSTGRESQL_PASSWORD appear in container logs.

PostgreSQL version mismatch
Custom image version: PostgreSQL 18.1
Reference image version: PostgreSQL 18.3

Missing PostgreSQL extensions
The directory /opt/bitnami/postgresql/share/extension in the custom image contains no extensions while the reference image contains many.

Invalid environment variable
The image defines BUG=/bitnami/postgresql/bug but the referenced path does not exist.

OCI startup failure
The image ships /bitnami/postgresql with permissions incompatible with the non-root runtime user (uid=1001, gid=0), causing OCI startup failure when PostgreSQL attempts to create /bitnami/postgresql/data.

Initialization directory permission issues:
Helm deployment logs show permission denied errors for /docker-entrypoint-preinitdb.d and /docker-entrypoint-initdb.d, breaking Bitnami init script compatibility.

Positive Findings
- significant image size reduction
- container runs as non‑root user (UID 1001)
- logs redirected to stdout
- OCI metadata labels present
- custom analytics metadata labels exist

Automation
Automation tests implemented with pytest validate:
- image size sanity
- secret leakage detection
- PostgreSQL version comparison
- environment variable path validation

Tests are located in the tests directory and executed with:
pytest

Conclusion
The slim PostgreSQL image successfully reduces container size while maintaining core database functionality. However several issues were discovered including credential exposure in logs, version mismatch with the reference image, missing extensions, invalid configuration variables and permission inconsistencies.

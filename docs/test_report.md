# Test Report – PostgreSQL Slim Image Evaluation

## Overview

This report summarizes the evaluation of the custom PostgreSQL slim image compared with the Bitnami PostgreSQL reference image.

Reference image:

bitnami/postgresql:latest

Custom image:

halex1985/postgresql:latest

The evaluation included manual inspection and automated tests implemented with Python and pytest.


## Test Environment

- Ubuntu (WSL) on Windows
- Docker
- Kubernetes (Minikube)
- Helm
- Python 3.x
- pytest


## Image Size Comparison

Reference image size:

~117 MB

Custom image size:

~38 MB

The custom image is approximately **67% smaller** than the reference image.


## Functional Validation

Basic PostgreSQL functionality works correctly once the container starts successfully.

Example operations validated:
```
SELECT version();
CREATE TABLE smoke(id INT);
INSERT INTO smoke VALUES (1);
SELECT * FROM smoke;
```


## Identified Issues


### Secret Leakage in Logs

Severity: High

The container entrypoint enables shell debugging (`set -x`).  
This causes sensitive environment variables such as database passwords to appear in container logs.

Example log output:
```
POSTGRESQL_PASSWORD=SuperSecret123
```

Impact:

Credentials may be exposed through container logging systems.


### PostgreSQL Version Mismatch

Severity: Medium

Custom image:

PostgreSQL 18.1

Reference image:

PostgreSQL 18.3

Impact:

Possible compatibility differences and missing security patches.


### Missing PostgreSQL Extensions

Severity: Medium

The directory
```
/opt/bitnami/postgresql/share/extension
```


contains no extensions in the custom image while the reference image contains many.

Impact:

Applications requiring extensions such as `pg_trgm` may fail.


### Filesystem Permission Incompatibility

Severity: Medium

The container runs as a non-root user (`uid=1001`, `gid=0`), but required directories such as:
```
/bitnami/postgresql
```

are owned by `root:root`.

Impact:

PostgreSQL initialization fails when running as a normal OCI container because the process cannot create:
```
/bitnami/postgresql/data
```



### Helm Initialization Directory Permission Errors

Severity: Medium

During Helm deployment permission errors may occur when accessing the following directories:
```
/docker-entrypoint-preinitdb.d
/docker-entrypoint-initdb.d
```


Impact:

Initialization scripts may fail to execute.


### Invalid Environment Variable

Severity: Low

The image defines the environment variable:
```
BUG=/bitnami/postgresql/bug
```


However the referenced path does not exist.

Impact:

Likely leftover build or debugging artifact.


## Positive Findings

- Significant image size reduction
- Container runs as non-root user (UID 1001)
- Logs redirected to stdout
- OCI metadata labels present
- Custom analytics metadata labels included

Example labels:
```
io.minimus.images.galleryURL
io.minimus.images.line
io.minimus.images.version
```


## Automation

Automation tests were implemented using pytest.

Automated checks include:

- Image size validation
- Secret leakage detection
- PostgreSQL version comparison
- Environment variable path validation

Tests are located in the `tests` directory.

Run the tests using:
```
pytest
```



## Conclusion

The slim PostgreSQL image successfully reduces container size while maintaining core database functionality.

However several compatibility and security issues were identified including credential leakage in logs, PostgreSQL version mismatch, missing extensions, filesystem permission incompatibilities and invalid configuration variables.

Addressing these issues would improve compatibility and security while preserving the benefits of the slim image approach.
```דג
פטאש

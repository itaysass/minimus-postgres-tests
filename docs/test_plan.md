# Test Plan – PostgreSQL Slim Image Evaluation

## Objective

The objective of this evaluation is to compare a custom slim PostgreSQL container image with the official Bitnami PostgreSQL image.

Reference image:

bitnami/postgresql:latest

Custom image under evaluation:

halex1985/postgresql:latest

The goal is to verify:

- Functional compatibility
- Container security posture
- Image size optimization
- Filesystem integrity
- Configuration correctness
- Metadata and analytics capabilities


## Test Environment

- Ubuntu (WSL) on Windows
- Docker
- Kubernetes (Minikube)
- Helm v3
- Python 3.x
- pytest


## Scope

The evaluation focuses on the following areas:

Functional compatibility
- PostgreSQL startup
- Database initialization
- SQL operations
- Helm deployment compatibility

Security validation
- Secret exposure in logs
- Unsafe configuration flags
- Runtime user privileges

Image integrity
- Filesystem structure
- Extension availability
- Environment variable correctness

Image quality
- Image size reduction

Metadata validation
- OCI labels
- Image analytics metadata


## Test Strategy

Two complementary approaches were used.


### Manual Validation

Manual inspection was performed using Docker commands to analyze:

- Container runtime behavior
- Filesystem structure
- Runtime user permissions
- Metadata labels
- Configuration files


### Automated Validation

Automated tests were implemented using Python and pytest.

Automation validates:

- Image size sanity
- Secret leakage in logs
- PostgreSQL version comparison
- Environment variable path validation
- Container startup behavior

Automation tests are located in the `tests` directory.


## Test Cases


### Container Startup

Verify the container starts successfully when required environment variables are provided.


### Database Initialization

Confirm the container correctly creates the configured database and user.


### Basic SQL Functionality

Execute simple SQL operations to verify PostgreSQL functionality.

Example queries:
```
SELECT version();
CREATE TABLE smoke(id INT);
INSERT INTO smoke VALUES (1);
SELECT * FROM smoke;
```



### Helm Deployment Compatibility

Deploy PostgreSQL using the official Helm chart while overriding the container image.


### Initialization Scripts

Verify that Bitnami initialization directories behave correctly.


### Secret Exposure Test

Ensure database credentials do not appear in container logs.


### Runtime User Validation

Confirm the container runs as a non-root user.


### Filesystem Permissions

Verify the runtime user can access required directories such as:
```
/bitnami/postgresql
```

### Extension Availability

Verify PostgreSQL extensions exist under:
```
/opt/bitnami/postgresql/share/extension
```



### Environment Variable Validation

Detect environment variables referencing non-existent filesystem paths.


### Image Size Sanity

Verify the custom image is significantly smaller than the reference image.


### Version Alignment

Verify PostgreSQL version matches the reference image.


## Exit Criteria

The image is considered acceptable if:

- Container starts successfully
- Database functionality works
- Helm deployment succeeds
- Credentials are not exposed in logs
- Runtime user is non-root
- Filesystem layout remains compatible
- Image size reduction objective is achieved

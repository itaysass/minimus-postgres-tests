
# Test Plan – PostgreSQL Slim Image Evaluation

## 1. Objective

The objective of this test plan is to evaluate a custom slim PostgreSQL container image against a reference PostgreSQL image.

Reference image:
bitnami/postgresql:latest

Custom image under test:
halex1985/postgresql:latest

The evaluation focuses on:

- Functional compatibility
- Container security posture
- Image size optimization
- Filesystem integrity
- Configuration correctness
- Metadata and analytics capabilities

The testing approach combines manual validation and automated testing.

---

# 2. Test Environment

| Component | Version |
|---|---|
| OS | Ubuntu (WSL) |
| Docker | Latest |
| Kubernetes | Local cluster |
| Helm | v3 |
| Python | 3.x |
| Test Framework | pytest |

---

# 3. Test Scope

The following aspects of the container image are evaluated.

### Functional compatibility

- PostgreSQL startup
- Database initialization
- SQL operations
- Helm deployment compatibility

### Security validation

- Secret leakage in logs
- Unsafe configuration flags
- Runtime user permissions

### Image integrity

- Filesystem structure
- Extension availability
- Configuration files
- Environment variable correctness

### Image quality

- Image size reduction
- Package composition
- Binary dependencies

### Metadata validation

- OCI labels
- Image analytics labels

---

# 4. Test Strategy

Testing is performed using two complementary approaches.

### Manual validation

Manual commands are used to inspect the container image, filesystem layout, and runtime behavior.

Examples:

- docker run
- docker inspect
- docker logs
- filesystem inspection inside container

### Automated testing

Automated tests are implemented using Python and pytest to validate:

- Image size sanity
- Secret leakage in logs
- PostgreSQL version alignment
- Environment variable correctness
- Container startup behavior

Automation tests are located in:

tests/

---

# 5. Test Cases

## Test Case 1 – Container Startup

Goal

Verify the container starts successfully using required environment variables.

Steps

1. Start container using docker run.
2. Provide database credentials and database name.
3. Inspect container logs.

Expected Result

Container starts successfully and PostgreSQL process runs.

---

## Test Case 2 – Database Initialization

Goal

Verify PostgreSQL initializes a database correctly.

Steps

1. Run container with initialization variables.
2. Connect to PostgreSQL using psql.
3. Validate that the database exists.

Expected Result

Database and user are created successfully.

---

## Test Case 3 – Basic SQL Operations

Goal

Verify PostgreSQL supports basic SQL functionality.

Steps

1. Connect using psql.
2. Execute SQL queries.

Example queries

SELECT version();
CREATE TABLE smoke(id INT);
INSERT INTO smoke VALUES (1);
SELECT * FROM smoke;

Expected Result

Queries execute successfully.

---

## Test Case 4 – Helm Deployment Compatibility

Goal

Verify the custom image works with the official Helm chart.

Steps

1. Deploy PostgreSQL using Helm.
2. Override the image repository with the custom image.
3. Wait for pods to start.

Expected Result

Pod reaches Running state.

---

## Test Case 5 – Initialization Scripts

Goal

Ensure initialization scripts execute correctly during container startup.

Steps

1. Deploy PostgreSQL with initialization scripts.
2. Inspect container logs.

Expected Result

Initialization scripts execute without permission errors.

---

# 6. Security Tests

## Test Case 6 – Secret Leakage in Logs

Goal

Ensure sensitive environment variables are not exposed in container logs.

Steps

1. Start container with a known password.
2. Retrieve container logs.
3. Search logs for the password value.

Expected Result

Password should not appear in logs.

---

## Test Case 7 – Unsafe Default Configuration

Goal

Detect insecure default configuration flags.

Steps

1. Inspect container environment variables.
2. Verify presence of insecure flags such as ALLOW_EMPTY_PASSWORD.

Expected Result

Container should not enable unsafe default configuration.

---

## Test Case 8 – Runtime User Verification

Goal

Ensure the container runs without root privileges.

Steps

Run inside container:

id
whoami

Expected Result

Container runs as non-root user.

---

# 7. Image Integrity Tests

## Test Case 9 – Filesystem Permissions

Goal

Verify required directories are writable by the runtime user.

Steps

Inspect directory:

/bitnami/postgresql

Expected Result

Directory permissions allow the runtime user to write.

---

## Test Case 10 – PostgreSQL Extension Availability

Goal

Verify PostgreSQL extensions are present.

Steps

Inspect directory:

/opt/bitnami/postgresql/share/extension

Expected Result

Extensions should be available similarly to the reference image.

---

## Test Case 11 – Filesystem Layout Consistency

Goal

Compare filesystem layout between custom and reference images.

Steps

Inspect library paths:

/opt/bitnami/postgresql/lib

Expected Result

Filesystem layout is compatible with the reference image.

---

## Test Case 12 – Environment Variable Path Validation

Goal

Ensure environment variables referencing filesystem paths are valid.

Steps

1. Inspect image environment variables.
2. Verify referenced paths exist.

Expected Result

All referenced filesystem paths exist.

---

# 8. Image Metadata Tests

## Test Case 13 – OCI Metadata Validation

Goal

Verify that OCI metadata labels exist.

Steps

Inspect image labels using docker inspect.

Expected Result

Image includes OCI labels such as:

- image version
- vendor
- creation time

---

## Test Case 14 – Custom Image Analytics Metadata

Goal

Verify presence of platform-specific analytics labels.

Steps

Inspect labels in the custom image.

Expected Result

Labels such as the following should exist:

io.minimus.images.galleryURL
io.minimus.images.line
io.minimus.images.version

---

# 9. Sanity Tests

## Test Case 15 – Image Size Sanity Test

Goal

Verify the custom image is significantly smaller than the reference image.

Steps

1. Inspect image sizes using Docker.
2. Compare sizes.

Expected Result

Custom image should be substantially smaller than the reference image.

---

## Test Case 16 – PostgreSQL Version Alignment

Goal

Verify the custom image uses the same PostgreSQL version as the reference image.

Steps

Run inside container:

postgres --version

for both images.

Expected Result

PostgreSQL versions should match.

---

# 10. Exit Criteria

The container image is considered acceptable if:

- Container starts successfully
- Database functionality works
- Helm deployment works
- No secrets are exposed in logs
- No unsafe configuration flags exist
- Filesystem layout remains compatible
- Image metadata is valid
- Image size reduction objective is achieved


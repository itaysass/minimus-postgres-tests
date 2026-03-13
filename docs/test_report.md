
# Test Report – PostgreSQL Slim Image Evaluation

## 1. Overview

This report summarizes the evaluation of a custom slim PostgreSQL container image compared to the reference image:

Reference image:
bitnami/postgresql:latest

Custom image under test:
halex1985/postgresql:latest

The goal of the evaluation was to verify:

- Functional compatibility
- Container security posture
- Image size optimization
- Configuration correctness
- Filesystem integrity
- Metadata availability

Testing included both manual validation and automated tests implemented with Python and pytest.

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

# 3. Test Execution Summary

| Test Category | Result |
|---|---|
| Functional tests | Passed |
| Kubernetes / Helm compatibility | Passed |
| Image size reduction | Passed |
| Security tests | Failed |
| Image integrity tests | Failed |
| Metadata validation | Passed |

---

# 4. Image Size Comparison

| Image | Size |
|---|---|
| Reference Image | ~389 MB |
| Custom Image | ~122 MB |

Size reduction achieved:

~67% smaller than the reference image.

This confirms the slim image successfully achieves its main objective of reducing image size.

---

# 5. Functional Validation

The following functionality was validated successfully:

- Container starts successfully
- PostgreSQL initializes correctly
- Database and user are created using environment variables
- SQL operations function normally
- Helm chart deployment works with the custom image

Example SQL operations tested:

SELECT version();
CREATE TABLE smoke(id INT);
INSERT INTO smoke VALUES (1);
SELECT * FROM smoke;

All operations executed successfully.

---

# 6. Security Findings

## Issue 1 – Secret Leakage in Logs

Severity: High

The container startup script enables shell tracing (`set -x`).  
As a result, sensitive environment variables are printed in container logs.

Example log output:

POSTGRESQL_PASSWORD=SuperSecret123

This exposes secrets through container logs which may be collected by logging systems or monitoring tools.

Impact:

- Password exposure
- Credential leakage risk
- Violates container security best practices

Recommendation:

Disable shell debugging in entrypoint scripts or mask sensitive variables before printing logs.

---

## Issue 2 – Unsafe Default Configuration

Severity: Medium

The container includes the environment variable:

ALLOW_EMPTY_PASSWORD=yes

Although a warning is printed, enabling this variable allows containers to run without a password if misconfigured.

Impact:

- Potential insecure deployment configuration
- Increased risk of unauthorized database access

Recommendation:

Remove this variable or enforce password requirements during startup.

---

# 7. Image Integrity Findings

## Issue 3 – PostgreSQL Version Mismatch

Severity: Medium

The custom image includes PostgreSQL version:

postgres (PostgreSQL) 18.1

While the reference image uses:

postgres (PostgreSQL) 18.3

Impact:

- Potential compatibility issues
- Missing security patches
- Unexpected behavior compared to reference image

Recommendation:

Ensure the slim image is built using the same upstream PostgreSQL version as the reference image.

---

## Issue 4 – Missing PostgreSQL Extensions

Severity: Medium

The reference image contains many PostgreSQL extensions under:

/opt/bitnami/postgresql/share/extension

However, the custom slim image contains **zero extensions** in this directory.

Impact:

Applications that rely on extensions (such as pg_trgm, postgis, etc.) will fail.

Recommendation:

Either include commonly used extensions or document that the slim image intentionally removes them.

---

## Issue 5 – Invalid Environment Variable

Severity: Low

The custom image defines the environment variable:

BUG=/bitnami/postgresql/bug

However, the referenced path does not exist.

Impact:

Likely leftover debug configuration from the image build process.

Recommendation:

Remove unused environment variables to avoid confusion.

---

# 8. Positive Findings

The custom image demonstrates several improvements:

- Significant image size reduction (~67%)
- Container runs as non-root user (UID 1001)
- Logs redirected to stdout (container-friendly logging)
- OCI metadata labels present
- Custom image analytics labels provided

Example custom labels:

io.minimus.images.galleryURL  
io.minimus.images.line  
io.minimus.images.version  

These labels provide useful metadata for image analytics platforms.

---

# 9. Automation

Automation tests were implemented using Python and pytest.

The automated tests validate:

- Image size sanity check
- Secret leakage detection in container logs
- PostgreSQL version comparison
- Invalid environment variable detection

Automation test directory:

tests/

Tests can be executed using:

pytest

---

# 10. Conclusion

The slim image successfully achieves its primary objective of reducing container size while maintaining core PostgreSQL functionality.

However, several issues were identified:

1. Sensitive credentials printed in container logs
2. PostgreSQL version mismatch
3. Missing PostgreSQL extensions
4. Insecure default configuration option
5. Invalid environment variable present

These issues should be addressed to ensure full compatibility and production readiness.

Overall, the image demonstrates strong potential but requires several fixes to match the stability and security posture of the reference implementation.

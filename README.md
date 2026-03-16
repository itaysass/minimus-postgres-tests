# PostgreSQL Slim Image Compatibility Evaluation

This repository contains the solution for the PostgreSQL image compatibility evaluation assignment.

The goal of the evaluation was to analyze a custom slim PostgreSQL container image and compare it with the official Bitnami PostgreSQL image in terms of:

- Functional compatibility
- Container security
- Configuration integrity
- Image size optimization
- Metadata and analytics capabilities

Reference image used for comparison:

bitnami/postgresql:latest

Custom image evaluated:

halex1985/postgresql:latest


## Test Environment

The evaluation was performed using the following environment:

- Ubuntu (WSL) on Windows
- Docker
- Kubernetes (Minikube)
- Helm
- Python 3.x
- pytest


## Repository Structure
minimus-postgres-tests
│
├── README.md
├── requirements.txt
│
├── docs
│ ├── test_plan.md
│ └── test_report.md
│
└── tests
├── reference_tests.py
├── bug_repro_tests.py
└── image_security_tests.py

## Running the Automated Tests

Install dependencies:
pip install -r requirements.txt

Run all tests:
pytest

Run a specific test file:
pytest tests/bug_repro_tests.py



## Automation Coverage

The automated tests validate several aspects of the container image:

- Container startup behavior
- Image size comparison
- Secret leakage detection
- PostgreSQL version comparison
- Environment variable validation


## Key Findings

During the evaluation several compatibility and security issues were identified:

- Secret leakage in container logs due to shell debugging (`set -x`)
- PostgreSQL version mismatch between images
- Missing PostgreSQL extensions in the slim image
- Filesystem permission incompatibility causing OCI startup issues
- Helm initialization directory permission errors
- Invalid environment variable referencing a non-existent path

A detailed explanation of the testing approach and findings is available in:

docs/test_plan.md  
docs/test_report.md


## Conclusion

The slim image achieves a significant reduction in container size while preserving basic PostgreSQL functionality. However, several configuration and compatibility issues should be addressed to ensure full parity with the reference image.

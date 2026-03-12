# PostgreSQL Image Compatibility Test Plan

## Objective

Validate that the custom PostgreSQL container image:

halex1985/postgresql:latest

is compatible with the Bitnami PostgreSQL Helm chart and behaves similarly to the reference image:

bitnami/postgresql:latest

The image is tested in both OCI (Docker) and Kubernetes environments.

---

## Test Scope

Two deployment modes are validated:

1. OCI container runtime (Docker)
2. Helm deployment in Kubernetes

The following aspects are verified:

- container startup
- database initialization
- database connectivity
- SQL functionality
- Helm compatibility

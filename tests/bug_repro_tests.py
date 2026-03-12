import subprocess
import time


def run(cmd):
    print(f"\n[RUN] {cmd}")
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    print(result.stdout)
    print(result.stderr)
    return result


def cleanup():
    run("docker rm -f pg-test 2>/dev/null || true")
    run("helm uninstall pg-test 2>/dev/null || true")



# BUG 1: OCI container should start
def test_custom_oci_container_should_start():
    """
    Expected behavior:
    PostgreSQL container should start successfully
    and remain running.

    Actual behavior (bug):
    Container exits due to permission errors.
    """

    cleanup()

    run(
        "docker run -d "
        "--name pg-test "
        "-e POSTGRESQL_USERNAME=testuser "
        "-e POSTGRESQL_PASSWORD=testpass123 "
        "-e POSTGRESQL_DATABASE=testdb "
        "-p 5433:5432 "
        "halex1985/postgresql:latest"
    )

    time.sleep(10)

    running = run("docker ps --filter name=pg-test")

    if "pg-test" not in running.stdout:
        logs = run("docker logs pg-test")

        raise AssertionError(
            "Custom PostgreSQL image failed to stay running in OCI mode.\n"
            "Expected: container should remain running.\n"
            "Actual: container exited.\n\n"
            f"Container logs:\n{logs.stdout}\n{logs.stderr}"
        )



# BUG 2: Helm deployment should not have permission errors
def test_custom_image_should_not_have_init_permission_errors():
    """
    Expected behavior:
    Bitnami init directories should be accessible
    and logs should not contain permission errors.

    Actual behavior (bug):
    Permission denied errors appear in logs.
    """

    cleanup()

    run(
        "helm install pg-test bitnami/postgresql "
        "--set image.repository=halex1985/postgresql "
        "--set image.tag=latest "
        "--set global.security.allowInsecureImages=true "
        "--set auth.username=testuser "
        "--set auth.password=testpass123 "
        "--set auth.database=testdb "
        "--set auth.postgresPassword=postgrespass123 "
        "--set primary.persistence.enabled=false"
    )

    print("Waiting for pod startup...")
    time.sleep(30)

    logs = run("kubectl logs pg-test-postgresql-0")

    # Expected: no permission errors
    assert "Permission denied" not in logs.stdout


# BUG 3: Container should not allow empty passwords
def test_empty_password_configuration_should_not_be_enabled():
    """
    Expected behavior:
    Container should NOT enable ALLOW_EMPTY_PASSWORD by default.

    Actual behavior (bug):
    ALLOW_EMPTY_PASSWORD=yes is set.
    """

    result = run(
        "docker run --rm "
        "--entrypoint /bin/bash "
        "halex1985/postgresql:latest "
        "-c 'echo $ALLOW_EMPTY_PASSWORD'"
    )

    # Expected: variable should be empty or not set
    assert "yes" not in result.stdout.lower()
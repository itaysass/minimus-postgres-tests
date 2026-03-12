import subprocess
import time


def run(cmd):
    print(f"\n[RUN] {cmd}")
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    print(result.stdout)
    print(result.stderr)
    return result


def cleanup():
    run("docker rm -f pg-ref pg-test 2>/dev/null || true")
    run("helm uninstall pg-ref pg-test 2>/dev/null || true")


def test_reference_image_starts():
    cleanup()

    run(
        "docker run -d "
        "--name pg-ref "
        "-e POSTGRESQL_USERNAME=testuser "
        "-e POSTGRESQL_PASSWORD=testpass123 "
        "-e POSTGRESQL_DATABASE=testdb "
        "-p 5432:5432 "
        "bitnami/postgresql:latest"
    )

    time.sleep(10)

    result = run("docker ps --filter name=pg-ref")
    assert "pg-ref" in result.stdout


def test_custom_image_fails():
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

    result = run("docker ps -a --filter name=pg-test")
    assert "Exited" in result.stdout

    logs = run("docker logs pg-test")
    assert "Permission denied" in logs.stdout + logs.stderr


def test_helm_deployment():
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

    print("Waiting for pod to start...")
    time.sleep(60)

    pod = run("kubectl get pods")
    assert "pg-test-postgresql-0" in pod.stdout

    logs = run("kubectl logs pg-test-postgresql-0")

    assert "Permission denied" in logs.stdout
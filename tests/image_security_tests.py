import subprocess
import json
import re


CUSTOM_IMAGE = "halex1985/postgresql:latest"
REFERENCE_IMAGE = "bitnami/postgresql:latest"


def run(cmd):
    return subprocess.check_output(cmd, shell=True, text=True).strip()


def test_image_size_sanity():
    custom = int(run(f"docker image inspect {CUSTOM_IMAGE} --format='{{{{.Size}}}}'"))
    ref = int(run(f"docker image inspect {REFERENCE_IMAGE} --format='{{{{.Size}}}}'"))

    reduction = 1 - (custom / ref)

    assert reduction > 0.5, f"Image reduction too small: {reduction:.2%}"


def test_postgres_version_alignment():
    custom = run(
        f"docker run --rm --entrypoint /bin/bash {CUSTOM_IMAGE} "
        "-c '/opt/bitnami/postgresql/bin/postgres --version'"
    )

    ref = run(
        f"docker run --rm --entrypoint /bin/bash {REFERENCE_IMAGE} "
        "-c '/opt/bitnami/postgresql/bin/postgres --version'"
    )

    assert custom == ref, f"Version mismatch: {custom} vs {ref}"


def test_secret_not_leaked_in_logs():
    run("docker rm -f pg-sec-test 2>/dev/null || true")

    run(
        f"docker run -d --name pg-sec-test "
        "-e POSTGRESQL_USERNAME=test "
        "-e POSTGRESQL_PASSWORD=Secret123 "
        "-e POSTGRESQL_DATABASE=testdb "
        f"{CUSTOM_IMAGE}"
    )

    run("sleep 5")

    logs = run("docker logs pg-sec-test 2>&1")

    assert "Secret123" not in logs, "Secret leaked into logs!"


def test_invalid_env_paths():
    env = run(
        f"docker inspect {CUSTOM_IMAGE} --format='{{{{json .Config.Env}}}}'"
    )

    env = json.loads(env)

    path_vars = [v.split("=", 1)[1] for v in env if "=" in v and v.endswith("/bug")]

    for p in path_vars:
        exists = run(
            f"docker run --rm --entrypoint /bin/bash {CUSTOM_IMAGE} "
            f"-c 'test -e {p} && echo exists || echo missing'"
        )

        assert exists == "exists", f"Invalid path referenced in env: {p}"
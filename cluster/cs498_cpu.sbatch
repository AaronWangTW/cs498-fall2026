#!/bin/bash
#SBATCH --account=26fa-cs498sw3-eng
#SBATCH --partition=eng-instruction
#SBATCH --job-name=cs498-cpu-smoke
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --output=logs/%x-%j.out

set -euo pipefail

echo "CS498 CPU smoke test"
echo "job_id=${SLURM_JOB_ID}"
echo "host=$(hostname)"
echo "cpus=${SLURM_CPUS_PER_TASK:-unknown}"
echo "workdir=${SLURM_SUBMIT_DIR}"
date --iso-8601=seconds

python3 - <<'PY'
import json
import os
import platform
import time

started = time.time()
value = sum(i * i for i in range(1_000_000))
result = {
    "status": "PASS",
    "hostname": platform.node(),
    "python": platform.python_version(),
    "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
    "checksum": value,
    "elapsed_seconds": round(time.time() - started, 3),
}
print(json.dumps(result, indent=2, sort_keys=True))
PY

echo "CS498_CPU_SMOKE_TEST=PASS"


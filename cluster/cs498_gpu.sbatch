#!/bin/bash
#SBATCH --account=26fa-cs498sw3-eng
#SBATCH --partition=eng-instruction
#SBATCH --job-name=cs498-gpu-smoke
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=00:15:00
#SBATCH --gres=gpu:A10:1
#SBATCH --output=logs/%x-%j.out

set -euo pipefail

echo "CS498 one-GPU smoke test"
echo "job_id=${SLURM_JOB_ID}"
echo "host=$(hostname)"
echo "cuda_visible_devices=${CUDA_VISIBLE_DEVICES:-unset}"
date --iso-8601=seconds

nvidia-smi
python3 gpu_smoke_test.py --output "logs/gpu-smoke-${SLURM_JOB_ID}.json"

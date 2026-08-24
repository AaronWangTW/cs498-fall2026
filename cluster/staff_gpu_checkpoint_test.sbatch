#!/bin/bash
#SBATCH --account=26fa-cs498sw3-eng
#SBATCH --partition=eng-instruction
#SBATCH --job-name=cs498-gpu-checkpoint
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=00:30:00
#SBATCH --gres=gpu:A10:1
#SBATCH --output=logs/%x-%j.out

set -euo pipefail

nvidia-smi
python3 gpu_checkpoint_test.py \
  --seconds 1200 \
  --checkpoint "logs/gpu-checkpoint-${SLURM_JOB_ID}.pt" \
  --result "logs/gpu-checkpoint-${SLURM_JOB_ID}.json"

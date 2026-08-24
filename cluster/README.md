# CS 498 Campus Cluster tutorial

This guide covers the Engineering Instructional partition of the Illinois Campus Cluster.

## Course resources and limits

- Account: `26fa-cs498sw3-eng`
- Partition: `eng-instruction`
- Maximum wall time: 6 hours per job
- Maximum resources per job: 1 node, 1 GPU, 8 CPU cores, and 64 GB host RAM
- Maximum concurrent GPU work: one running GPU job per student
- GPU job arrays must include a `%1` concurrency limit

The 64 GB limit refers to host RAM, not GPU memory. These limits are course policy while staff confirm which limits can also be enforced by Slurm/QOS.

## 1. Log in and verify the course account

Connect with your Illinois NetID:

```bash
ssh YOUR_NETID@cc-login.campuscluster.illinois.edu
```

Then verify that the CS 498 Engineering account appears:

```bash
/projects/illinois/eng/shared/shared/examples/my-accounts-eng
```

If `26fa-cs498sw3-eng` is missing more than 24 hours after course access was announced, contact the teaching staff. Do not use another course's allocation.

## 2. Inspect the partition

```bash
sinfo -p eng-instruction -N -o "%.12N %.8c %.12m %.20G %.30f"
```

This displays nodes, CPU cores, host memory, generic resources, and node features. Staff will confirm whether the GPU type should be requested generically as `gpu:1` or with a typed A10 resource.

## 3. Prepare a working directory

Use your home directory only for small source files and configuration. Use an approved course/project storage location for datasets and checkpoints after staff publish it.

```bash
mkdir -p ~/cs498-cluster/logs
cd ~/cs498-cluster
```

Copy this folder from the public course repository, or download only the files you need. Do not make restricted data, credentials, or private tokens world-readable.

## 4. Discover software

Available software changes over time, so inspect the live module tree instead of copying an old module name:

```bash
module avail
module spider cuda
module spider python
module spider pytorch
```

Load the modules required by your job or activate your own tested environment inside the batch script. Record module and package versions in your experiment log.

## 5. Submit the CPU smoke test

```bash
mkdir -p logs
sbatch cs498_cpu.sbatch
```

The command prints a job ID. Inspect it with:

```bash
squeue -u "$USER"
scontrol show job JOB_ID
sacct -j JOB_ID --format=JobID,JobName,Partition,Account,State,Elapsed,AllocCPUS,ReqMem,MaxRSS,ExitCode
```

After completion, read `logs/cs498-cpu-smoke-JOB_ID.out`.

## 6. Submit a one-GPU smoke test

The supplied template requests one GPU and verifies that the job can see exactly one CUDA device:

```bash
mkdir -p logs
sbatch cs498_gpu.sbatch
```

The job runs `nvidia-smi`, imports PyTorch, performs a small matrix multiplication, and writes a JSON result. A successful job ends with `CS498_GPU_SMOKE_TEST=PASS`.

If the job remains pending, inspect the reason:

```bash
squeue -j JOB_ID -o "%.18i %.12P %.24j %.8T %.12M %.30R"
```

Do not repeatedly resubmit the same pending job. A smaller time or resource request is easier for Slurm to schedule.

## 7. Monitor, cancel, and review jobs

```bash
squeue -u "$USER"
sacct -j JOB_ID --format=JobID,State,Elapsed,AllocCPUS,ReqMem,MaxRSS,ExitCode
scancel JOB_ID
```

Cancel jobs that are obsolete, stuck because of a bad command, or producing invalid output. Never run training, preprocessing, or other intensive work directly on a login node.

## 8. Checkpoint long jobs

Jobs longer than 30 minutes must save restartable checkpoints. Save checkpoints at least every 30 minutes and on normal shutdown. Keep only the checkpoints needed for recovery and final evaluation.

The staff validation script `staff_gpu_checkpoint_test.sbatch` demonstrates checkpoint creation and reload. It is not the default student template.

## 9. Job arrays

GPU arrays must limit concurrency to one task:

```bash
#SBATCH --array=0-9%1
```

This does not replace the one-running-GPU-job policy. Do not submit multiple separate GPU jobs to bypass the limit.

## Common failures

- `Invalid account or account/partition combination`: confirm both the account and partition names.
- `Invalid generic resource specification`: run the `sinfo` command above and report its `%G` output to staff.
- `Module not found`: use `module spider` and load prerequisites in the order it reports.
- `OUT_OF_MEMORY`: lower the batch size or data-loader worker count; do not exceed the course memory cap.
- `TIMEOUT`: add checkpoint/restart support and split the experiment into jobs of at most 6 hours.
- Missing output file: create `logs/` before calling `sbatch` and inspect the job's `WorkDir` with `scontrol show job`.

## Official documentation

- [Getting started](https://docs.ncsa.illinois.edu/systems/icc/en/latest/getting_started.html)
- [Running jobs](https://docs.ncsa.illinois.edu/systems/icc/en/latest/user_guide/running_jobs.html)
- [Storage](https://docs.ncsa.illinois.edu/systems/icc/en/latest/user_guide/storage_data.html)
- [Software](https://docs.ncsa.illinois.edu/systems/icc/en/latest/user_guide/software.html)


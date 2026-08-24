# Live validation record

## August 24, 2026

The following checks were performed from `cc-login2.campuscluster.illinois.edu` using Shenlong's authenticated Campus Cluster session.

### Confirmed

- The `eng-instruction` partition is visible through `sinfo`.
- It contains three idle CPU nodes with 128 CPU cores and approximately 1 TB host RAM each.
- It contains two idle GPU nodes with 64 CPU cores, approximately 256 GB host RAM, and `gpu:A10:3` each.
- The guarded templates pass local static validation and shell/Python syntax checks.
- The test bundle can be transferred to the login node without running compute work there.

### Waiting for account propagation

The course account `26fa-cs498sw3-eng` did not appear in either the Engineering account helper or Shenlong's Slurm associations. A minimal CPU submission was rejected with:

```text
sbatch: error: Batch job submission failed: Invalid account or account/partition combination specified
```

No alternate research account was used because that would charge the wrong allocation. Re-run the account and smoke-test checks after the course account appears; the access notification advised allowing up to 24 hours for roster propagation.

### Retest

```bash
/projects/illinois/eng/shared/shared/examples/my-accounts-eng
cd "$HOME/cs498_cluster_test"
sbatch --parsable cs498_cpu.sbatch
sbatch --parsable cs498_gpu.sbatch
```

After each job completes, inspect the `cs498-*.out` and `cs498-*.err` files and use `sacct -j JOB_ID` to verify the account, partition, requested resources, state, and exit code.

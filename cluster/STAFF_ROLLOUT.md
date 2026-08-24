# Staff rollout checklist

Do not merge or publish the student tutorial until every blocking item is complete.

## Access and partition discovery

- [ ] Course roster access has propagated for at least one instructor/TA and one test student.
- [ ] `/projects/illinois/eng/shared/shared/examples/my-accounts-eng` reports `26fa-cs498sw3-eng`.
- [ ] `sinfo` confirms the `eng-instruction` node count, A10 GRES name, CPU count, memory, and partition wall-time limit.
- [ ] Staff have recorded whether `--gres=gpu:1` or a typed A10 request is preferred.

## Smoke tests

- [ ] `cs498_cpu.sbatch` completes and its `sacct` record matches the requested account, partition, CPUs, memory, and time.
- [ ] `cs498_gpu.sbatch` completes, exposes exactly one GPU, and writes a PASS JSON record.
- [ ] `staff_gpu_checkpoint_test.sbatch` trains for 20 minutes, writes a checkpoint, and reloads it successfully.
- [ ] A cancelled test job terminates cleanly and leaves no unexpected processes.
- [ ] A test student can reproduce the workflow from the tutorial without staff shell history or undocumented setup.

## Policy and enforcement

- [ ] Engineering Technical Representatives confirm whether account/QOS limits can enforce six hours, one GPU, one running GPU job per user, eight CPUs, and 64 GB host RAM.
- [ ] Storage location, quota, backup status, purge policy, and cleanup deadline are documented.
- [ ] Support routing is documented: cluster problems to `help@campuscluster.illinois.edu`; course allocation/storage questions to `techrep@engr.illinois.edu`; assignment questions to course staff.

## Publication

- [ ] Remove all provisional language that has been resolved.
- [ ] Add the confirmed storage path and module/environment instructions.
- [ ] Validate every command in a clean login shell.
- [ ] Merge through normal review into the public course repository.
- [ ] Add the tutorial to Canvas only after the public repository version is live.


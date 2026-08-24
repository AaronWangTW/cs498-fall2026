# CS 498 Campus Cluster resource policy

These rules protect a six-GPU shared instructional resource and apply to every job charged to `26fa-cs498sw3-eng`.

## Per-job limits

- Use only the `eng-instruction` partition and the `26fa-cs498sw3-eng` account.
- Request at most one node.
- Request at most one GPU.
- Request at most eight CPU cores.
- Request at most 64 GB of host RAM.
- Request at most 6 hours of wall time.
- Run at most one GPU job at a time per student.
- Limit GPU job arrays to one concurrent task with `%1`.

## Responsible use

- Run computational work only through Slurm. Login nodes are for editing, environment preparation, compilation, submission, and short non-intensive checks.
- Use the smallest resource request that will complete the work.
- Cancel invalid, obsolete, or duplicate jobs promptly.
- Checkpoint jobs longer than 30 minutes and make them restartable.
- Do not bypass limits by splitting one experiment into concurrently running jobs.
- Do not store credentials, restricted course data, or private tokens in world-readable paths or logs.
- Follow the storage location, quota, retention, and cleanup instructions published by course staff.

## Enforcement status

The course will ask Engineering Technical Representatives to enforce the limits through the course account or a Slurm QOS where supported. Until that is confirmed, these limits remain mandatory course policy and the supplied templates encode them by default.

The 64 GB host-memory limit allows three one-GPU jobs to share a 256 GB, three-GPU node while retaining operating-system and filesystem headroom.

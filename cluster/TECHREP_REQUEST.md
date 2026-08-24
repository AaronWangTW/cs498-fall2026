# Draft request to Engineering Technical Representatives

Subject: CS 498 eng-instruction resource limits and course storage

Hello Engineering Technical Representatives,

CS 498 Machine Perception has been granted access to the shared `eng-instruction` partition under account `26fa-cs498sw3-eng`. The course expects students to run single-GPU machine-learning jobs on the six A10 GPUs.

To preserve fair access, could you confirm whether the following limits can be enforced through the account association or a Slurm QOS?

- maximum wall time: 6 hours per job;
- maximum one node and one GPU per job;
- maximum eight CPU cores and 64 GB host RAM per job;
- maximum one concurrently running GPU job per user;
- GPU job arrays limited to one concurrent task.

Please also confirm:

1. the exact GRES or feature string students should use for one A10 GPU on `eng-instruction`;
2. the partition's configured maximum wall time;
3. whether a dedicated course software module or shared environment is recommended;
4. the approved course storage location, quota, retention/purge policy, and access procedure;
5. any account-level monitoring or reporting tools you recommend to course staff.

The GPU nodes each have 256 GB host RAM and three A10 GPUs. We proposed a 64 GB host-memory cap so three single-GPU jobs can coexist with system and filesystem headroom, but we welcome your recommended value.

Thank you,

CS 498 Machine Perception teaching staff


# CS 498: Machine Perception — Fall 2026

Public assignment handouts, starter code, and tests for CS 498 Machine Perception at the University of Illinois Urbana-Champaign.

This repository does not contain instructor reference solutions. Course staff publish clean student-facing snapshots from a separate private development repository.

## Course assessment

| Item | Weight | Topic |
| --- | ---: | --- |
| HW0 | 10% | Perspective, Homography, Stereo |
| HW1 | 10% | Point Cloud Segmentation |
| HW2 | 15% | SLAM and Mapping |
| HW3 | 15% | Detection and Tracking |
| HW4 | 13% | NeRF |
| HW5 | 13% | Diffusion Policy |
| Final Project | 20% | Two project tracks |
| Attendance | 4% | Course attendance |

## Repository layout

Each `hwN/` directory owns its handout, Python package, tests, data notes, and output directory. HW0 is the first runnable package; later homework directories currently record the planned scope.

```text
hw0/
  latex/                  assignment handout source
  src/cs498_hw0/          student starter package
  tests/                  public interface checks
  data/                    dataset notes
  outputs/                 generated results (ignored by Git)
hw1/ ... hw5/             later assignments
final-track1/             final-project track 1
final-track2/             final-project track 2
```

## Contributing

Only the course maintainers have direct write access. If you identify a bug, please open an issue or submit a pull request from a fork. See [CONTRIBUTING.md](CONTRIBUTING.md).

# 06 · ML infrastructure

**Status: planned. No code, tests or benchmarks exist in this section.** Topic directories will be
created with their first tested implementation ([ADR 0003](../docs/decisions/0003-no-empty-directories.md)).

## Prerequisites
Section [05](../05-backend-distributed-systems/) (APIs, databases, reliability). Basic ML knowledge
(overfitting, generalisation) is assumed and recorded in the
[progress tracker](../docs/progress-tracker.md) as *Introduced*.

## Topic map

| Topic | Question to answer with evidence | First planned implementation |
|-------|----------------------------------|------------------------------|
| data-pipelines | How is data ingested and validated reproducibly? | Schema validation step with failing-record tests |
| dataset-versioning | How do you reproduce a training set? | Content-hash manifest; same inputs → same hash test |
| training-pipelines | What makes a training run repeatable? | Seeded small training script emitting a manifest |
| experiment-tracking | How are runs compared? | Run-record schema and a comparison table |
| model-registry | How are versions promoted and rolled back? | Registry stub with stage transitions (reuses the lifecycle-state-machine pattern from project 01) |
| model-deployment | Canary and rollback | Deployment of the project 02 service with a version switch |
| monitoring-drift | Data vs concept drift | Distribution-shift check on recorded data (e.g. population stability index) with tests |
| gpu-fundamentals | Memory hierarchy, numerical precision (FP32, FP16, BF16) | Notes plus a precision-error experiment; GPU hardware not assumed |

Diagram of the intended lifecycle:
[ML lifecycle](../docs/architecture/diagrams/ml-lifecycle-and-distributed-inference.md) (planned).

## Exit evidence (roadmap phase 6)
Same inputs reproduce the same artefact; a drift check runs on a recorded dataset.

## References (primary)
* PyTorch documentation: <https://pytorch.org/docs/stable/>
* Hugging Face documentation: <https://huggingface.co/docs>
* NVIDIA CUDA documentation: <https://docs.nvidia.com/cuda/>

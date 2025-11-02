# Single and Multi-node Launchers with SLURM

The following are complete SLURM scripts that demonstrate how to integrate various launchers with software that uses `torch.distributed` (but should be easily adaptable to other distributed environments).

- [torchrun](https://github.com/stas00/ml-engineering/blob/master/orchestration/slurm/launchers/torchrun-launcher.slurm) - to be used with [PyTorch distributed](https://github.com/pytorch/pytorch).
- [accelerate](https://github.com/stas00/ml-engineering/blob/master/orchestration/slurm/launchers/accelerate-launcher.slurm) - to be used with [HF Accelerate](https://github.com/huggingface/accelerate).
- [lightning](https://github.com/stas00/ml-engineering/blob/master/orchestration/slurm/launchers/lightning-launcher.slurm) - to be used with [Lightning](https://lightning.ai/) ("PyTorch Lightning" and "Lightning Fabric").
- [srun](https://github.com/stas00/ml-engineering/blob/master/orchestration/slurm/launchers/srun-launcher.slurm) - to be used with the native SLURM launcher - here we have to manually preset env vars that `torch.distributed` expects.

All of these scripts use [torch-distributed-gpu-test.py](https://github.com/stas00/ml-engineering/blob/master/debug/torch-distributed-gpu-test.py) as the demo script, which you can copy here with just:
```
cp ../../../debug/torch-distributed-gpu-test.py .
```
assuming you cloned this repo. But you can replace it with anything else you need.

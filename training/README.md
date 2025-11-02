# Training

**Subsections**:

- [Model parallelism](/training/model-parallelism/)

- [Performance](/training/performance/)

- [Fault Tolerance](/training/fault-tolerance/)

- [Reproducibility](/training/reproducibility/)

- [Instabilities](/training/instabilities/)

- [Checkpoints](/training/checkpoints/)

- [Training hyper-parameters and model initializations](/training/hparams.md)

- [Tensor precision / Data types](/training/dtype.md)

- [Emulate a multi-node setup using just a single node](/training/emulate-multi-node.md) - instructions on how to emulate a multi-node setup using just a single node - we use the `deepspeed` launcher here.

- [Re-train HF hub models from scratch using finetuning examples](/training/re-train-hub-models.md)

- [Datasets](/training/datasets.md)

**Tools**:

- [printflock.py](https://github.com/stas00/ml-engineering/blob/master/training/tools/printflock.py) - a tiny library that makes your `print` calls non-interleaved in a multi-gpu environment.

- [multi-gpu-non-interleaved-print.py](https://github.com/stas00/ml-engineering/blob/master/training/tools/multi-gpu-non-interleaved-print.py) - a `flock`-based wrapper around `print` that prevents messages from getting interleaved when multiple processes print at the same time - which is the case with `torch.distributed` used with multiple-gpus.

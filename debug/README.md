# Debugging and Troubleshooting


## Guides

- [Debugging PyTorch programs](/debug/pytorch.md)

- [Diagnosing Hangings and Deadlocks in Multi-Node Multi-GPU Python Programs](/debug/torch-distributed-hanging-solutions.md)

- [Network Debug](/network/debug/)

- [Troubleshooting NVIDIA GPUs](/compute/accelerator/nvidia/debug.md)

- [Underflow and Overflow Detection](/debug/underflow_overflow.md)



## Tools

- [Debug Tools](/debug/tools.md)

- [torch-distributed-gpu-test.py](https://github.com/stas00/ml-engineering/blob/master/debug/torch-distributed-gpu-test.py) - this a `torch.distributed` diagnostics
  script that checks that all GPUs in the cluster (one or many nodes) can talk to each other and allocate gpu memory.

- [NicerTrace](https://github.com/stas00/ml-engineering/blob/master/debug/NicerTrace.py) - this is an improved `trace` python module with multiple additional flags added to the constructor and more useful output.

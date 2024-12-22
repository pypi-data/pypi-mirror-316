# Torch Submit

## Introduction

Torch Submit is a lightweight, easy-to-use tool for running distributed PyTorch jobs across multiple machines. It's designed for researchers and developers who:

- Have access to a bunch of machines with IP addresses
- Want to run distributed PyTorch jobs without the hassle
- Don't have the time, energy, or patience to set up complex cluster management systems like SLURM or Kubernetes

Under the hood, Torch Submit uses Fabric to copy your working directory to the remote addresses and TorchRun to execute the command.

It's encouraged to read `torch_submit/executor.py` to understand how jobs are created and scheduled.

## Features

- Simple cluster configuration: Just add your machines' IP addresses
- Easy job submission: Run your PyTorch jobs with a single command
- Job management: Submit, stop, restart, and monitor your jobs
- Log tailing: Easily view the logs of your running jobs
- Optuna Integration for parallel hyperparameter optimization

## Installation

```bash
pip install torch-submit
```

or from source:

```bash
pip install -e . --prefix ~/.local
```

## Quick Start

1. Set up a cluster:
   ```bash
   torch-submit cluster create
   ```
   Follow the interactive prompts to add your machines.

2. Submit a job:
   ```bash
   torch-submit job submit --cluster my_cluster -- <entrypoint>
   # for example:
   # torch-submit job submit --cluster my_cluster -- python train.py
   # torch-submit job submit --cluster my_cluster -- python -m main.train
   ```

3. List running jobs:
   ```bash
   torch-submit job list
   ```

4. Tail logs:
   ```bash
   torch-submit logs tail <job_id>
   ```

5. Stop a job:
   ```bash
   torch-submit job stop <job_id>
   ```

6. Restart a stopped job:
   ```bash
   torch-submit job restart <job_id>
   ```

## Usage

### Cluster Management

- Create a cluster: `torch-submit cluster create`
- List clusters: `torch-submit cluster list`
- Remove a cluster: `torch-submit cluster remove <cluster_name>`

### Job Management

- Submit a job: `torch-submit job submit --cluster my_cluster -- <entrypoint>`
- List jobs: `torch-submit job list`
- Stop a job: `torch-submit job stop <job_id>`
- Restart a job: `torch-submit job restart <job_id>`

### Log Management

- Tail logs: `torch-submit job logs <job_id>`

### Optuna

The Optuna exectuor requires setting a database connection. This can be done via `torch-submit db create`. This will create a new database within the specified connection called `torch_submit`. This database should be accessible to all machines in a cluster. Study name and storage info will be accessible to to the job via "OPTUNA_STUDY_NAME" and "OPTUNA_STORAGE" environment variables.

## Configuration

Torch Submit stores cluster configurations in `~/.cache/torch-submit/config.yaml`. You can manually edit this file if needed, but it's recommended to use the CLI commands for cluster management.

## Requirements

- Python 3.7+
- PyTorch (for your actual jobs)
- SSH access to all machines in your cluster

## Contributing

We welcome contributions! Please see our Contributing Guide for more details.

## License

Torch Submit is released under the MIT License. See the LICENSE file for more details.

## Support

If you encounter any issues or have questions, please file an issue on our GitHub Issues page.

Happy distributed training!

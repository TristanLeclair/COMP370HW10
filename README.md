# MLP network modeling

I used a [dataset of my little pony dialog](https://www.kaggle.com/datasets/liury123/my-little-pony-transcript) to do a network analysis of discussion between characters in the show.

This repo contains

- `./scripts/python/compute_network_stats.py`
  A python script that computes network statistics for the MLP dataset.
- `./scripts/python/build_interaction_network.py`
  A python script that builds a json network from the MLP dataset.


## Pitfalls

# Setup/Installation

```bash
pip install -r requirements.txt
```

## Make

```bash
make script-build-network-run
```

```bash
make script-compute-network-run
```

Replace `run` with `help` to get help on the scripts.

## Python


```bash
python -m scripts.python.compute_network_stats -h
```

```bash
python -m scripts.python.build_interaction_network -h
```


import torch
from torch import Tensor
from pathlib import Path
from typing import Tuple, List, Dict, Literal, Generator

from epilepsy_bids_loader import Segment


def read_json(json_file: str | Path) -> Dict:
    import json
    with open(json_file, "r") as f:
        meta = json.load(f)
    return meta


def read_yaml(path: Path) -> Dict:
    import yaml
    with open(path) as f:
        out: dict = yaml.safe_load(f)
        return out


def batch_segments(
    segments: List[Segment],
    batch_size: int,
    usage: Literal['all', 'train', 'test']
) -> Generator[Tuple[Tensor, Tensor, Tensor], None, None]:
    """
    Creates batches of data from a list of segments.

    Args:
        segments (List[Segment]): List of segments.
        batch_size (int): Size of the batch dimension "N".

    Returns:
        Generator[Tuple[Tensor, Tensor, Tensor]]: Tuple of:
        - x: (N, C, L)
        - y: (N,)
        - t: (N,)
    """
    # batches: List[Tuple[ndarray, ndarray, ndarray]] = []
    for i in range(0, len(segments), batch_size):
        j = i + batch_size
        batch: List[Segment] = segments[i : j]
        batch_x = []
        batch_y = []
        batch_t = []

        for seg in batch:
            x, y, t = seg.data(usage=usage)
            batch_x.append(x) # (1, C, L)
            batch_y.append(torch.tensor(1 if y.any() else 0)) # (L,) -> 1
            batch_t.append(t[0]) # (L,) -> 1, use the start of the seg
            continue

        batch = (
            torch.concatenate(batch_x, axis=0), # (N, C, L)
            torch.stack(batch_y, axis=0), # (N,)
            torch.stack(batch_t, axis=0) # (N,)
        )
        yield batch
    return

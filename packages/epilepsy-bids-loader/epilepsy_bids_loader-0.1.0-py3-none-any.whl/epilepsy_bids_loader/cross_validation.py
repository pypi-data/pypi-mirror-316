import torch
from torch import Tensor
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from typing import Tuple, List, Dict, Literal, Generator

from epilepsy_bids_loader import Segment
from epilepsy_bids_loader import Status, ZScoreScaler
from epilepsy_bids_loader import batch_segments


@dataclass
class CVFold:
    train: List[Segment]
    dev: List[Segment]
    test: List[Segment]


@dataclass
class TestBatch:
    run: str
    ref: Path
    date_time: datetime
    duration: float
    segments: List[Segment] = field(default_factory=list)
    batches: Generator[Tuple[Tensor, Tensor, Tensor], None, None] = None

    def __len__(self):
        return len(self.batches)

    def __iter__(self):
        return iter(self.batches)

    def append_segment(self, seg: Segment):
        self.segments.append(seg)
        return

    def create_batches(self, batch_size: int):
        self.batches = batch_segments(
            segments=self.segments,
            batch_size=batch_size,
            usage="test"
        )
        return


@dataclass
class CrossValidation:
    method: Literal["subject_specific", "subject_independent"]
    folds: List[CVFold] = field(default_factory=list)

    def __len__(self):
        return len(self.folds)

    def append(self, fold: CVFold):
        self.folds.append(fold)
        return

    def _train_batch_default(
        self,
        fold: int,
        batch_size: int,
        **kwargs
    ) -> Generator[Tuple[Tensor, Tensor, Tensor], None, None]:
        """
        Standard training batching process
        - Use all bckg, repeat sz, randomise
        """
        from random import sample
        segments: List[Segment] = self.folds[fold].train

        # Balanced selection of sz and bckg segments
        sz_segs = [
            seg for seg in segments
            if seg.label() == 1
        ]
        bckg_segs = [
            seg for seg in segments
            if seg.label() == 0
        ]
        segments = (
            bckg_segs
            + sz_segs * (len(bckg_segs) // len(sz_segs))
        )

        # Randomise
        segments = sample(segments, k=len(segments))

        batches = batch_segments(
            segments=segments,
            batch_size=batch_size,
            usage="train"
        )
        return batches

    def train_batch(
        self,
        fold: int,
        method: Literal["default"],
        batch_size: int,
        **kwargs
    ) -> Generator[Tuple[Tensor, Tensor, Tensor], None, None]:
        _batch_fn = {
            "default": self._train_batch_default,
            # TODO Extend options here as needed
        }[method]
        return _batch_fn(
            fold=fold,
            batch_size=batch_size,
            **kwargs
        )

    def test_batch_by_run(
        self,
        fold: int,
        batch_size: int,
    ) -> Dict[Tuple[str, str, str], TestBatch]:
        """
        Generates batches of test samples grouped by run.

        Args:
            fold (int): The cross validation fold number.
            batch_size (int): Batch size

        Returns:
            Dict[Tuple[str, str, str], TestBatch]: Keys are (sub, ses, run)
        """
        segments: List[Segment] = self.folds[fold].test

        # Organise segments by run
        batches: Dict[str, TestBatch] = {}
        for seg in segments:
            sub = seg.subject
            ses = seg.session
            run = seg.run
            key = (sub, ses, run)
            if key not in batches:
                run_meta = seg.run_meta()
                batches[key] = TestBatch(
                    run=run,
                    ref=run_meta["ref"],
                    date_time=run_meta["date_time"],
                    duration=run_meta["duration"]
                )
            batches[(sub, ses, run)].append_segment(seg)

        # Create batched data by run
        for test_batch in batches.values():
            test_batch.create_batches(batch_size=batch_size)
        return batches

    def fit_scaler(
        self,
        fold: int = 0
    ) -> ZScoreScaler:
        status = Status("[loader] fitting z-score scaler on training data")
        x = torch.concatenate(
            [
                seg.data("all")[0] # (1, C, L)
                for seg in self.folds[fold].train
            ],
            axis=2
        ) # (1, C, L+)
        scaler = ZScoreScaler()
        scaler.fit(x)
        status.done()
        return scaler
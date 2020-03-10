import os
import sys
import numpy as np
import multiprocessing
from transients import transients
import itertools
import uuid


here = os.path.abspath(os.path.dirname(__file__))
audio_file = os.path.join(here, "squeeking.wav")

RESOLUTION = 3

blocksize_c = np.linspace(100, 4096, num=RESOLUTION, dtype="int32")
clumplength_c = np.linspace(3, 100, num=RESOLUTION, dtype="int32")
order_c = np.linspace(20, 3948, num=RESOLUTION, dtype="int32")
padsize_c = np.linspace(2, 512, num=RESOLUTION, dtype="int32")
skew_c = np.linspace(-10.0, 10.0, num=RESOLUTION, dtype="float64")
threshfwd_c = np.linspace(0.001, 8, num=RESOLUTION, dtype="float64")
threshback_c = np.linspace(0.001, 8, num=RESOLUTION, dtype="float64")
windowsize_c = np.linspace(3, 20, num=RESOLUTION, dtype="int32")

possibilities = [
    blocksize_c,
    clumplength_c,
    order_c,
    padsize_c,
    skew_c,
    threshfwd_c,
    threshback_c,
    windowsize_c,
]

combos = list(itertools.product(
    *possibilities
))

NUM_JOBS = len(combos)
print(NUM_JOBS)


def extract(workable):
    identifier = uuid.uuid4().hex[:6]
    out_path = os.path.join(
        here, 'outs', f"{identifier}.wav"
    )
    transients(*workable, source=audio_file, output=out_path)


if __name__ == "__main__":
    with multiprocessing.Pool(16) as p:
        for i, _ in enumerate(p.imap_unordered(extract, combos), 1):
            sys.stdout.write(f"\rAnalyse Progress {i/NUM_JOBS}")

import os
import sys
import numpy as np
import multiprocessing
from transients import transients
from jsonutils import write_json
import itertools
import uuid


RESOLUTION = 2

blocksize_c = np.linspace(100, 4096, num=RESOLUTION, dtype="int32")
clumplength_c = np.linspace(3, 100, num=RESOLUTION, dtype="int32")
order_c = np.linspace(20, 3948, num=RESOLUTION, dtype="int32")
padsize_c = np.linspace(2, 512, num=RESOLUTION, dtype="int32")
skew_c = np.linspace(-10.0, 10.0, num=RESOLUTION, dtype="float64")
threshfwd_c = np.linspace(0.001, 1.4, num=RESOLUTION, dtype="float64")
threshback_c = np.linspace(0.001, 1.4, num=RESOLUTION, dtype="float64")
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

combos = list(itertools.product(*possibilities))

num_jobs = len(combos)


class Worker():
    def __init__(self):
        self.here = os.path.abspath(os.path.dirname(__file__))
        self.source = os.path.join(self.here, "squeeking.wav")
        self.metadata = multiprocessing.Manager().dict()
        self.outfolder = os.path.join(self.here, 'out')
        self.metadata_json = os.path.join(self.outfolder, 'metadata.json')
        if not os.path.exists(self.outfolder):
            os.makedirs(self.outfolder)

    def extract(self, workable):
        print(workable)
        identifier = uuid.uuid4().hex[:6]
        out_path = os.path.join(
            self.outfolder, f"{identifier}.wav"
        )
        transients(*workable, source=self.source, output=out_path)
        self.metadata[identifier] = workable
    
    def dump_meta(self):
        write_json(self.metadata_json, dict(self.metadata))


if __name__ == "__main__":
    worker = Worker()
    with multiprocessing.Pool() as p:
        for i, _ in enumerate(p.imap_unordered(worker.extract, combos), 1):
            sys.stdout.write(f"\rAnalyse Progress {i/num_jobs}")
    worker.dump_meta()

import subprocess


def transients(
    blocksize: int,
    # clumplength: int,
    order: int,
    # padsize: int,
    skew: int,
    threshback: float,
    threshfwd: float,
    # windowsize: int,
    source: str,
    output: str,
):

    subprocess.call(
        [
            "fluid-transients",
            "-source", source,
            "-transients", output,
            "-blocksize",
            str(blocksize),
            "-clumplength", "25",
            "-order",
            str(order),
            "-padsize", "128",
            "-skew",
            str(skew),
            "-threshback",
            str(threshback),
            "-threshfwd",
            str(threshfwd),
            "-windowsize", "14",
        ]
    )
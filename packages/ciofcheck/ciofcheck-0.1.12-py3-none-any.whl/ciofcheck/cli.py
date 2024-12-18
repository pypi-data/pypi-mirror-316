import argparse
import glob
import logging
import os
import re
import sys
from dataclasses import dataclass
from enum import Enum

from cioseq.sequence import Sequence
from .bar_chart import BarChart

LOG_FORMATTER = logging.Formatter(
    "%(asctime)s  %(name)s%(levelname)9s %(filename)s-%(lineno)d %(threadName)s:  %(message)s"
)
STATUS_ENDPOINT = "/downloads/status"
FORMAT_SUMMARY = "summary"
FORMAT_ASCII_CHART = "ascii"
FORMAT_BAR_CHART = "bar"


class DisplayOptions(str, Enum):
    """
    Supported output formats for displaying sequence analysis results.

    Values:
        SUMMARY: Text summary of findings
        ASCII: ASCII art chart showing file sizes
        BAR: Interactive bar chart visualization
    """

    SUMMARY = "summary"
    ASCII = "ascii"
    BAR = "bar"


DISPLAY_OPTIONS = [format.value for format in DisplayOptions]
PATTERN_REGEX = re.compile(
    r"^(?P<prefix>[^\[\]]+)(?:\[(?P<spec>(?P<frame_spec>[0-9x\-,]+)(?P<hashes>#+))?\])?(?P<extension>[^\[\]]*)$"
)
BYTES_TO_MB = 1.0 / (1024 * 1024)
DEFAULT_WIDTH = 80
DEFAULT_PADDING = 1
HUGE_NUMBER = 9999999999
MAX_FILE_SIZE = 1024**4

logger = logging.getLogger("conductor.check_sequence")


@dataclass
class FileStats:
    """
    Statistics and metadata about a single file in the sequence.

    Attributes:
        filepath (str): Full path to the file
        frame (int): Frame number of this file in the sequence
        size (int): File size in bytes
        exists (bool): Whether the file exists on disk
        corrupt (bool): Whether the file appears to be corrupted
        human_size (str): Human readable file size (e.g. "1.5 MB")
    """

    filepath: str
    frame: int
    size: int
    exists: bool
    corrupt: bool
    human_size: str


def run(pattern, display=DisplayOptions.SUMMARY.value, width=DEFAULT_WIDTH):
    """
    Analyze a sequence of files and report statistics about them.

    The pattern argument specifies the file sequence using frame number notation, e.g.:
    - 'myfile[1-100####].png' matches myfile0001.png through myfile0100.png
    - 'render[1,5,10-20##].exr' matches render01.exr, render05.exr, render10.exr through render20.exr

    Args:
        pattern (str): Pattern specifying the sequence of files to analyze.
            Should be in the format: prefix[frame-spec][extension]
        display (str, optional): How to display the results. One of:
            'summary' - Text summary of findings (default)
            'ascii' - ASCII art chart showing file sizes
            'bar' - Interactive bar chart visualization
        width (int, optional): Width in characters for the ASCII chart output.
            Only used when display='ascii'. Defaults to 80.

    Raises:
        ValueError: If the pattern is invalid or cannot be parsed.

    Returns:
        None
    """

    logger.debug("Running ciofcheck.py")

    if width <= 0:
        raise ValueError("Width must be positive")

    match = PATTERN_REGEX.match(pattern)
    if not match:
        raise ValueError(
            f"Invalid pattern: '{pattern}'. Should be prefix[frame-spec][extension]. e.g. 'myfile[1-100####].png'"
        )

    prefix = match.group("prefix")
    extension = match.group("extension")
    if match.group("spec"):
        frame_spec = match.group("frame_spec")
        padding = len(match.group("hashes"))
        sequence = Sequence.create(frame_spec)
    else:
        sequence, padding = _infer_expected(prefix, extension)

    stats = _get_stats(prefix, extension, padding, sequence)

    logger.debug("Padding: %s", padding)
    logger.debug("Sequence: %s", sequence)
    logger.debug("Min Size: %s", stats["min_size"])
    logger.debug("Max Size: %s", stats["max_size"])

    exists_sequence, bad_sequence = _get_sequences(stats["files"])

    expected_sequence_report = f"Expected: {sequence} ({len(sequence)} frames)"

    if exists_sequence:
        exists_sequence_report = (
            f"Exists: {exists_sequence} ({len(exists_sequence)} frames)"
        )
    else:
        exists_sequence_report = "Exists: None"

    if bad_sequence:
        bad_sequence_report = (
            f"Missing or Zero: {bad_sequence} ({len(bad_sequence)} frames)"
        )
    else:
        bad_sequence_report = "Missing or Zero: None"

    if display == DisplayOptions.ASCII.value:
        _make_ascii_chart(stats, width)
    elif display == DisplayOptions.BAR.value:
        _make_bar_chart(stats)

    print(expected_sequence_report)
    print(exists_sequence_report)
    print(bad_sequence_report)
    print(f"Min Size: {stats['min_size']}")
    print(f"Max Size: {stats['max_size']}")
    print(f"Padding: {padding}")


def _get_stats(prefix, extension, padding, sequence):
    result = {
        "files": [],
        "max_size": 0,
        "min_size": MAX_FILE_SIZE,
        "padding": padding,
        "prefix": prefix,
        "extension": extension,
        "sequence": str(sequence),
        "descriptor": f"{prefix}[{sequence}{'#'*padding}]{extension}",
    }
    for frame in sequence:
        file_path = f"{prefix}{frame:0{padding}}{extension}"
        size = 0
        exists = False
        try:
            with open(file_path, "rb") as f:
                stat = os.stat(file_path)
                exists = True
                size = stat.st_size
                if size > result["max_size"]:
                    result["max_size"] = size
                if size < result["min_size"]:
                    result["min_size"] = size
        except FileNotFoundError:
            pass
        result["files"].append(
            {
                "filepath": file_path,
                "frame": frame,
                "size": size,
                "exists": exists,
                "corrupt": False,
                "human_size": _human_file_size(size),
            }
        )
    return result


def _get_sequences(files):
    exist_frames = []
    bad_frames = []

    for file in files:
        if file["exists"]:
            exist_frames.append(file["frame"])

        if file["size"] == 0:
            bad_frames.append(file["frame"])

    exist_sequence = Sequence.create(exist_frames) if exist_frames else None
    bad_sequence = Sequence.create(bad_frames) if bad_frames else None
    return exist_sequence, bad_sequence


def _infer_expected(prefix, extension):
    sequence_regex_pattern = re.compile(
        r"{}(\d+){}".format(re.escape(prefix), re.escape(extension))
    )
    sequence_glob_pattern = "{}*{}".format(prefix, extension)

    files = glob.glob(sequence_glob_pattern)
    # print("files", files)

    padding = DEFAULT_PADDING
    start = HUGE_NUMBER
    end = -start
    if not files:
        return None, 1
    for file in files:
        match = sequence_regex_pattern.match(file)
        if not match:
            # It should always match, but just in case
            continue
        digits = match.group(1)
        frame_number = int(digits)
        if frame_number < start:
            start = frame_number
        if frame_number > end:
            end = frame_number

        frame_number_length = len(digits)
        if padding > 1 and frame_number_length < padding:
            padding = frame_number_length

    return Sequence.create(f"{start}-{end}"), padding


def _make_ascii_chart(stats, width):
    mult = width / stats["max_size"]
    padding = stats["padding"]

    for file in stats["files"]:
        exists = file["exists"]
        nbytes = file["size"]
        size = file["human_size"]
        frame = file["frame"]

        fstr = f"{frame:0{padding}}"
        fstr = fstr.rjust(6)

        if exists:
            print("{}: {}| {}".format(fstr, "-" * int(nbytes * mult), size))
        else:
            print("{}: {}".format(fstr, "MISSING"))


def _make_bar_chart(stats):
    chart = BarChart()
    chart.update(stats)
    chart.show()


def _human_file_size(bytes):
    """
    Convert file size in bytes to human-readable format.

    Args:
        bytes (int): File size in bytes.

    Returns:
        str: Human-readable file size.

    """

    # Define the suffixes for different file sizes
    suffixes = ["B", "KB", "MB", "GB", "TB", "PB"]

    # Get the closest matching suffix and the corresponding divisor
    for suffix in suffixes:
        if bytes < 1024:
            return f"{bytes:.2f} {suffix}"
        bytes /= 1024

    return f"{bytes:.2f} {suffixes[-1]}"


def main():
    parser = argparse.ArgumentParser(description="Check and analyze sequence files.")
    parser.add_argument(
        "pattern",
        help="Pattern of the expected file names (e.g., 'myfile[1-100####].png')",
    )
    parser.add_argument(
        "--display",
        choices=[f.value for f in DisplayOptions],
        default=DisplayOptions.SUMMARY.value,
        help="Output format (default: summary)",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=DEFAULT_WIDTH,
        help="Width of the ASCII chart output (default: 80)",
    )

    args = parser.parse_args()

    try:
        run(args.pattern, display=args.display, width=args.width)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

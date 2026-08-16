import argparse
import numpy as np
import ffmpeg
from pathlib import Path
import sys


parser = argparse.ArgumentParser(description="Data Preprocessor") #create parser and use that to parse arguments

def change_video_resalution(args: argparse.Namespace):
    probe = ffmpeg.probe(args.input_path)
    output_resolution = (args.rheight , args.rwidth)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

    if video_stream is None:
        raise ValueError("No Video Stream Found ")

    if ((video_stream["height"],video_stream["width"]) == output_resolution ):
        raise ValueError("Can't Convert to same resallution")


    (
    ffmpeg
    .input(str(args.input_path)) 
    .filter('scale', width=output_resolution[1], height=output_resolution[0])
    .output(str(args.output_path))
    .run(overwrite_output=True)
    )



def create_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        prog="vidconvert",
        description="pre-process video",
        
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    convert = subparsers.add_parser("covertrs",help="will covert video")

    convert.add_argument("input_path", type=Path ,help = "input path for video")

    convert.add_argument("rheight", type = int  ,help = "input path for video")

    convert.add_argument("rwidth", type = int  ,help = "input path for video")

    convert.add_argument("output_path", type=Path ,help = "output path for video")

    convert.set_defaults(func = change_video_resalution )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)   
    return args.func(args) 

if __name__ == "__main__":
    sys.exit(main())

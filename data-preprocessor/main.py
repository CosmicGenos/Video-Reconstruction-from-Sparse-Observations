import argparse
import numpy as np
import ffmpeg
from pathlib import Path
import sys
from scenedetect import detect , ContentDetector , split_video_ffmpeg
import uuid


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


def scene_splitter(args:argparse.Namespace):
    probe = ffmpeg.probe(args.input_path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

    if video_stream is None:
        raise ValueError("No Video Stream Found ")

    scenes = detect(str(args.input_path),ContentDetector())

    data = args.output_path

    videofolder: Path = data / f"{args.input_path.name}_{uuid.uuid4()}"
    videofolder.mkdir(parents=True, exist_ok=True)

    split_video_ffmpeg(
        args.input_path,
        scenes,
        output_dir=videofolder,
        show_progress = True
    )

    file_names = list(videofolder.iterdir())

    less_tha_3s_videos = [f for f in file_names if float(ffmpeg.probe( str(f))["format"].get("duration",0)) < 3.0 ]

    for f in less_tha_3s_videos:
        (f).unlink(missing_ok = True)

    

    













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

    spiltv = subparsers.add_parser("spiltv",help="will split the video")

    spiltv.add_argument("input_path", type=Path ,help = "input path for video")

    spiltv.add_argument("output_path", type=Path ,help = "output path for video")

    spiltv.set_defaults(func = scene_splitter )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)   
    return args.func(args) 

if __name__ == "__main__":
    sys.exit(main())

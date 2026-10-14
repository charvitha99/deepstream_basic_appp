#!/usr/bin/env python3
"""Entry point for the DeepStream basic video analytics application."""

import argparse
import logging
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
LOG_DIR = PROJECT_DIR / "logs"


def configure_logging() -> None:
    """Write logs to a file and display them in the terminal."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    log_file = LOG_DIR / "deepstream_app.log"
    log_format = "%(asctime)s | %(levelname)s | %(message)s"

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="DeepStream video analytics application."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input video file.",
    )
    parser.add_argument(
        "--config",
        default=str(PROJECT_DIR / "config" / "config_infer_primary.txt"),
        help="Path to the primary inference configuration.",
    )
    parser.add_argument(
        "--output",
        default=str(PROJECT_DIR / "output" / "processed_video.mp4"),
        help="Path for the processed output video.",
    )
    return parser.parse_args()


def validate_paths(
    args: argparse.Namespace,
) -> tuple[Path, Path, Path]:
    """Validate input, configuration, and output paths."""
    input_path = Path(args.input).expanduser().resolve()
    config_path = Path(args.config).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    if not input_path.is_file():
        raise FileNotFoundError(
            f"Input video does not exist or is not a file: {input_path}"
        )

    if not config_path.is_file():
        raise FileNotFoundError(
            f"Inference configuration does not exist: {config_path}"
        )

    if input_path == output_path:
        raise ValueError("Input and output paths must be different.")

    if config_path == output_path:
        raise ValueError("Configuration and output paths must be different.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    return input_path, config_path, output_path


def main() -> int:
    """Application entry point."""
    try:
        configure_logging()

        logging.info("DeepStream Basic Video Analytics Application")
        logging.info("Project directory: %s", PROJECT_DIR)

        args = parse_arguments()
        input_path, config_path, output_path = validate_paths(args)

        logging.info("Input video: %s", input_path)
        logging.info("Inference configuration: %s", config_path)
        logging.info("Output video: %s", output_path)

        logging.error(
            "Pipeline execution is not implemented yet. "
            "No inference was performed and no output video was generated."
        )
        return 1

    except (FileNotFoundError, ValueError) as exc:
        logging.error("%s", exc)
        return 1

    except OSError as exc:
        logging.error("File system error: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
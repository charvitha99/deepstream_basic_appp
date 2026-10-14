
import argparse
import logging
import os
import sys
from pathlib import Path

import gi

gi.require_version("Gst", "1.0")
from gi.repository import Gst, GLib


PROJECT_DIR = Path(__file__).resolve().parent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(PROJECT_DIR / "logs" / "deepstream_app.log"),
    ],
)
logger = logging.getLogger("deepstream_app")


def make_element(factory, name):
    element = Gst.ElementFactory.make(factory, name)
    if not element:
        raise RuntimeError(
            f"Could not create GStreamer element: {factory}. "
            "Check that the required DeepStream plugin is installed."
        )
    return element


def on_decode_pad_added(decodebin, pad, streammux):
    caps = pad.get_current_caps() or pad.query_caps(None)
    if not caps or caps.get_size() == 0:
        return

    structure = caps.get_structure(0)
    media_type = structure.get_name()

    if not media_type.startswith("video/"):
        return

    sink_pad = streammux.request_pad_simple("sink_0")
    if not sink_pad:
        logger.error("Could not get streammux sink pad")
        return

    if sink_pad.is_linked():
        logger.warning("Video pad is already linked")
        return

    result = pad.link(sink_pad)
    if result != Gst.PadLinkReturn.OK:
        logger.error("Could not link decoded video to streammux: %s", result)
    else:
        logger.info("Decoded video linked to DeepStream pipeline")


def on_bus_message(bus, message, loop):
    message_type = message.type

    if message_type == Gst.MessageType.EOS:
        logger.info("Video processing completed")
        loop.quit()

    elif message_type == Gst.MessageType.ERROR:
        error, debug = message.parse_error()
        logger.error("GStreamer error: %s", error)
        if debug:
            logger.error("Debug details: %s", debug)
        loop.quit()

    elif message_type == Gst.MessageType.WARNING:
        warning, debug = message.parse_warning()
        logger.warning("GStreamer warning: %s", warning)
        if debug:
            logger.warning("Debug details: %s", debug)

    return True


def build_pipeline(input_path, config_path, output_path):
    pipeline = Gst.Pipeline.new("deepstream-video-pipeline")
    if not pipeline:
        raise RuntimeError("Could not create pipeline")

    source = make_element("filesrc", "video-source")
    decoder = make_element("decodebin", "video-decoder")
    streammux = make_element("nvstreammux", "stream-muxer")
    pgie = make_element("nvinfer", "primary-inference") #capsfilter
    converter = make_element("nvvideoconvert", "video-converter")
    osd = make_element("nvdsosd", "onscreen-display")
    output_converter = make_element("nvvideoconvert", "output-converter")
    encoder = make_element("nvv4l2h264enc", "h264-encoder")
    parser = make_element("h264parse", "h264-parser")
    muxer = make_element("qtmux", "mp4-muxer")
    sink = make_element("filesink", "output-file")

    source.set_property("location", str(input_path))

    # One input video stream.
    streammux.set_property("batch-size", 1)
    streammux.set_property("width", 1920)
    streammux.set_property("height", 1080)
    streammux.set_property("batched-push-timeout", 40000)

    pgie.set_property("config-file-path", str(config_path))

    # Save the encoded output video to disk.
    encoder.set_property("bitrate", 4000000)
    sink.set_property("location", str(output_path))
    sink.set_property("sync", False)

    elements = [
        source,
        decoder,
        streammux,
        pgie,
        converter,
        osd,
        output_converter,
        encoder,
        parser,
        muxer,
        sink,
    ]

    for element in elements:
        pipeline.add(element) #link errors

    if not source.link(decoder):
        raise RuntimeError("Could not link file source to decoder")

    decoder.connect("pad-added", on_decode_pad_added, streammux)

    linked_elements = [
        (streammux, pgie),
        (pgie, converter),
        (converter, osd),
        (osd, output_converter),
        (output_converter, encoder),
        (encoder, parser),
        (parser, muxer),
        (muxer, sink),
    ]

    for first, second in linked_elements:
        if not first.link(second):
            raise RuntimeError(
                f"Could not link {first.get_name()} to {second.get_name()}"
            )

    return pipeline


def main():
    parser = argparse.ArgumentParser(
        description="Basic NVIDIA DeepStream GPU inference application"
    )
    parser.add_argument(
        "--input",
        default=str(PROJECT_DIR / "input" / "sample_video.mp4"),
        help="Path to the input video",
    )
    parser.add_argument(
        "--config",
        default=str(PROJECT_DIR / "config" / "config_infer_primary.txt"),
        help="Path to the nvinfer configuration file",
    )
    parser.add_argument(
        "--output",
        default=str(PROJECT_DIR / "output" / "processed_video.mp4"),
        help="Path to the output MP4 video",
    )
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    config_path = Path(args.config).resolve()
    output_path = Path(args.output).resolve()

    if not input_path.is_file():
        logger.error("Input video does not exist: %s", input_path)
        return 1

    if not config_path.is_file():
        logger.error("Inference configuration does not exist: %s", config_path)
        return 1

    if input_path == output_path or config_path == output_path:
        logger.error("Output path must differ from input and configuration")
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    (PROJECT_DIR / "logs").mkdir(parents=True, exist_ok=True)

    Gst.init(None)

    try:
        pipeline = build_pipeline(input_path, config_path, output_path)
    except Exception:
        logger.exception("Failed to construct DeepStream pipeline")
        return 1

    loop = GLib.MainLoop() #
    bus = pipeline.get_bus() #
    bus.add_signal_watch() #
    bus.connect("message", on_bus_message, loop) #

    logger.info("Input: %s", input_path)
    logger.info("Inference config: %s", config_path)
    logger.info("Output: %s", output_path)
    logger.info("Starting DeepStream pipeline")

    result = pipeline.set_state(Gst.State.PLAYING)
    if result == Gst.StateChangeReturn.FAILURE:
        logger.error("Could not start pipeline")
        pipeline.set_state(Gst.State.NULL)
        return 1

    try:
        loop.run()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    finally:
        pipeline.set_state(Gst.State.NULL)

    logger.info("Pipeline stopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())

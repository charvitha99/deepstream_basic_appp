
# DeepStream Basic GPU Application

A basic video analytics application using NVIDIA DeepStream,
GStreamer, and TensorRT.

## Goals

- Read a video file
- Decode video through GStreamer
- Run object detection with DeepStream `nvinfer`
- Draw detection overlays with `nvdsosd`
- Save processed video to MP4
- Log pipeline status and errors

## Requirements

- Compatible NVIDIA GPU and driver
- Supported Ubuntu and NVIDIA DeepStream inst
## Project structureallation
- GStreamer and required NVIDIA plugins
- Compatible inference model and configuration
- NVIDIA encoder plugin compatible with the target machine


```text
deepstream_basic_app/
├── main.py
├── config/
├── input/
├── models/
├── output/
├── logs/
├── requirements.txt
└── README.md
```

## Running

After installing and validating DeepStream and configuring a supported
inference model:

```bash
python3 main.py \
  --input input/sample_video.mp4 \
  --config config/config_infer_primary.txt \
  --output output/processed_video.mp4
```

## Status

Application code prepared; target-environment compatibility,
model configuration, and GPU inference must be tested before claiming
a successful end-to-end run.

# NVIDIA DeepStream Basic Video Analytics Application

## 1. Project Overview

This project aims to develop a basic NVIDIA DeepStream application using Python and GStreamer. It will process a video file, perform object detection using the YOLOv8n model, draw bounding boxes and labels, and save the processed video.

Project files are being prepared on a Windows development PC. Runtime execution will take place on a separate Ubuntu computer equipped with an NVIDIA GPU.

**Current status:** Project structure, initial Python application, documentation, and sample video preparation are complete. DeepStream integration, model configuration, and GPU execution remain pending.

## 2. Project Objectives

- Build a video-processing pipeline using NVIDIA DeepStream and GStreamer.
- Read a video file from a configurable input path.
- Batch frames using `nvstreammux`.
- Perform object detection using `nvinfer` and a compatible YOLOv8n integration.
- Draw bounding boxes and labels using `nvdsosd`.
- Encode and save the processed video.
- Log application activity and report errors clearly.
- Accept input video, inference configuration, and output paths through command-line arguments.
- Document the target environment and verify actual execution results.

## 3. Intended Pipeline Architecture

Input Video -> Video Decoder -> nvstreammux -> nvinfer -> nvdsosd -> Video Encoder -> Output Video

The exact GStreamer elements, caps, encoder, and muxer will be selected according to the installed DeepStream version and the capabilities of the target Ubuntu system.

This describes the intended architecture, not a functioning pipeline. Pipeline implementation and runtime verification remain pending.

## 4. Technology Stack

- Programming language: Python
- Video pipeline: GStreamer
- Video analytics framework: NVIDIA DeepStream SDK
- Inference backend: NVIDIA TensorRT, where required
- Object detection model: YOLOv8n
- Development environment: Windows
- Execution environment: Ubuntu Linux with a compatible NVIDIA GPU
- Video preparation and inspection: FFmpeg and FFprobe

The final software versions and dependencies will be documented after inspecting the target GPU computer.

## 5. Project Structure

```text
deepstream_basic_app/
|-- config/
|   `-- config_infer_primary.txt
|-- input/
|   |-- PNNL_Parking_LOT(1).avi
|   `-- sample_video.mp4
|-- logs/
|-- models/
|   `-- README.md
|-- output/
|-- main.py
|-- README.md
|-- requirements.txt
`-- .gitignore
```

### Directory and file responsibilities

| File or directory | Purpose |
|---|---|
| `main.py` | Python entry point, command-line arguments, path validation, and logging |
| `config/` | DeepStream inference configuration |
| `models/` | Model artifacts and supporting files |
| `input/` | Original and converted sample videos |
| `output/` | Processed output videos |
| `logs/` | Application execution logs |
| `requirements.txt` | Additional Python dependencies, if required |
| `.gitignore` | Excludes generated files and local environment artifacts |
| `README.md` | Project documentation and setup instructions |

## 6. Sample Input Video

The project contains a parking-lot video for testing.

### Verified MP4 properties

| Property | Value |
|---|---|
| Filename | `input/sample_video.mp4` |
| Video codec | H.264 |
| Resolution | 1920 x 1080 |
| Frame rate | 29 FPS |
| Duration | Approximately 34.41 seconds |
| Pixel format | `yuv420p` |
| File size | 11,196,836 bytes |
| Audio | Removed during conversion |

The original file, `input/PNNL_Parking_LOT(1).avi`, is retained for reference. It uses MPEG-4 Part 2 video encoding.

The MP4 was created using FFmpeg and inspected using FFprobe. Its codec, resolution, frame rate, pixel format, duration, and file size were verified.

**Verification limitation:** Successful decoding and processing on the target Ubuntu DeepStream system have not yet been verified.

## 7. Development and Execution Environments

### Windows development PC

The Windows PC is used to:

- Create and organize project files.
- Prepare Python source code and documentation.
- Inspect and convert sample videos.
- Perform Python syntax checks.
- Prepare the project for transfer to Ubuntu.

Python 3.9.13 and FFmpeg 9.0.1 are available on the development PC.

### Ubuntu GPU computer

The target Ubuntu system will be used to:

- Inspect the Ubuntu release and NVIDIA GPU.
- Check the NVIDIA driver and installed DeepStream version.
- Verify GStreamer and required DeepStream plugins.
- Select and prepare a compatible YOLOv8n integration.
- Configure inference and prepare model artifacts.
- Execute the complete video-processing pipeline.

The target Ubuntu version, DeepStream version, driver, and GPU model have not yet been established.

## 8. Model and Inference Configuration

The intended object detection model is YOLOv8n, a lightweight variant of the YOLOv8 family.

The `nvinfer` plugin requires a valid inference configuration and compatible model artifacts. Requirements depend on the selected integration.

Potential requirements include:

- An exported model, such as ONNX.
- A compatible custom parser library, if required.
- A DeepStream inference configuration.
- A TensorRT engine, if required by the selected workflow.

The model files and configuration will be selected after inspecting the target DeepStream environment and verifying the chosen integration.

The current `config/config_infer_primary.txt` is a temporary placeholder. It is **not a valid inference configuration** and must be replaced before running the inference pipeline.

TensorRT engines may depend on the GPU architecture, TensorRT version, and other environment details. Their portability must not be assumed.

## 9. Planned Command-Line Interface

The intended application interface is:

```bash
python3 main.py \
  --input input/sample_video.mp4 \
  --config config/config_infer_primary.txt \
  --output output/processed_video.mp4
```

The current Python entry point supports argument parsing, path validation, and logging. The inference configuration remains a placeholder, and the GStreamer pipeline has not been implemented.

Therefore, this command documents the intended interface; it is not yet a command for successful DeepStream execution.

## 10. Logging and Error Handling

The current application is designed to:

- Accept input, configuration, and output paths.
- Check whether the input video and inference configuration exist.
- Create the output directory when necessary.
- Report path-validation errors.
- Write application messages to the terminal and `logs/deepstream_app.log`.

The completed application will additionally handle missing GStreamer plugins, pipeline construction and linking failures, inference errors, and runtime bus messages.

Successful inference, output generation, and runtime error handling remain to be verified on Ubuntu.

## 11. Setup and Execution Plan

1. Complete portable project preparation on Windows.
2. Inspect the Ubuntu version and NVIDIA GPU.
3. Identify the installed DeepStream version and compatible dependencies.
4. Select a documented YOLOv8n integration.
5. Obtain or generate the required model artifacts.
6. Replace the temporary inference configuration with a valid configuration.
7. Implement and validate the GStreamer pipeline.
8. Run the application with `input/sample_video.mp4`.
9. Verify inference results, bounding boxes, and output video playback.
10. Inspect execution logs and document the tested environment.

## 12. Current Development Status

- [x] Create the project directory structure.
- [x] Create the initial Python application.
- [x] Create the inference configuration placeholder.
- [x] Prepare model directory documentation.
- [x] Create the project README and `.gitignore`.
- [x] Verify Python syntax using `py_compile`.
- [x] Inspect the original AVI video properties.
- [x] Convert the sample video to H.264 MP4.
- [x] Verify the converted video properties using FFprobe.
- [ ] Inspect the target Ubuntu and NVIDIA GPU environment.
- [ ] Select a compatible YOLOv8n integration.
- [ ] Obtain or generate the required model artifacts.
- [ ] Finalize the inference configuration.
- [ ] Implement the DeepStream GStreamer pipeline.
- [ ] Execute the pipeline on the NVIDIA GPU.
- [ ] Verify object detections and the processed output video.
- [ ] Verify runtime logging and error handling.
- [ ] Document successful end-to-end execution.

## 13. Limitations and Important Notes

- Windows preparation does not prove that the application runs on DeepStream.
- The current inference configuration is a placeholder.
- YOLOv8n integration may require a compatible custom parser or additional supporting files.
- Model conversion and TensorRT engine generation depend on the selected integration and target environment.
- The availability of individual GStreamer plugins must be verified on Ubuntu.
- The application has not yet generated an inference-processed output video.

## 14. Expected Final Result

Once development and GPU validation are complete, the application should:

1. Read the sample video.
2. Decode video frames.
3. Batch frames using `nvstreammux`.
4. Perform YOLOv8n object detection through `nvinfer`.
5. Draw bounding boxes and labels using `nvdsosd`.
6. Encode and save the processed video.
7. Record useful execution logs.
8. Report errors clearly.
9. Provide documented setup instructions and verified execution evidence.

The project will be considered complete only after the end-to-end pipeline has successfully run on the target Ubuntu NVIDIA GPU computer.
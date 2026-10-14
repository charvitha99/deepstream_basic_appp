# Model Directory

This directory will contain the model artifacts required by the DeepStream application.

## Planned Model

- Model family: YOLOv8
- Model variant: YOLOv8n (nano)
- Intended task: Object detection

## Model Integration

The final model format and supporting files will be selected after checking the target Ubuntu computer's NVIDIA DeepStream version and the chosen YOLOv8 integration.

Depending on the selected implementation, the required files may include:

- An exported model file, such as ONNX
- A compatible custom parser library, if required
- A DeepStream inference configuration
- A generated TensorRT engine, if required by the chosen workflow

TensorRT engines may depend on the GPU and software environment. They must not be assumed to be portable between different computers.

No model inference is claimed to be configured or tested yet.
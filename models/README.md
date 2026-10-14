
# Models

This directory stores model artifacts used by the DeepStream application.

## Model requirements

The model must be compatible with the installed NVIDIA DeepStream and
TensorRT versions.

For YOLOv8n integration, verify:

- YOLOv8n ONNX export compatibility
- TensorRT engine generation on the target GPU
- Correct YOLO output parser
- Matching inference configuration and class labels

Large model files and generated TensorRT engines should not normally
be committed to Git.

No model or GPU inference result is considered verified until the
application has been tested on the target Ubuntu GPU machine.

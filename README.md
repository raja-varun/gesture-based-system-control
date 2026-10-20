# Gesture-Based System Control

A Windows-only computer-vision prototype that uses MediaPipe hand landmarks to
switch between volume, brightness, and scrolling modes. OpenCV reads the
webcam; PyAutoGUI and Windows audio/brightness libraries perform the selected
desktop actions.

## Status and safety

This is an early prototype, not a hardened accessibility product. Running it
opens the camera and can change system volume, change display brightness, or
scroll the active window. Test in a controlled environment, keep the emergency
quit key available, and review every dependency before use. No automated tests
are provided.

## Requirements

- Windows with a working webcam.
- Python environment compatible with the installed MediaPipe and Pycaw wheels.
- Dependencies in `requirements.txt`.

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Run

The published repository contains the original prototype:

```powershell
python prototype1.py
```

Press `q` while the OpenCV window is focused to exit. The prototype uses
thumb/index/middle/ring/pinky landmark heuristics to activate modes. A second
experimental variant exists in the local workspace but is intentionally not
published because its timing/state behavior is incomplete.

## Architecture

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the camera, landmark,
mode, and operating-system side-effect flow.

## Verification

```powershell
python -m py_compile prototype1.py prototype2.py
```

## Limitations

- Gesture thresholds are hard-coded and may vary by camera, hand position, and
  lighting.
- There is no permission layer, configuration file, calibration flow, or unit
  test suite.
- `prototype2.py` contains experimental timing/state behavior and should not be
  described as production-ready.

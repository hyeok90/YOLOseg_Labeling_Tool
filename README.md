# YOLO11-seg Active Learning-based Annotation Tool

This is a GUI-based image annotation tool developed with Python and PyQt5, designed for efficient object segmentation tasks. It leverages YOLOv11-seg models to implement an active learning workflow, significantly speeding up the labeling process.

## ✨ Features

- **🧠 Active Learning:** Automatically pre-annotates images without labels using a loaded YOLOv11-seg model.
- **🖋️ Smart Polygon Annotation:** 
    - **Polygon Tool:** Create, edit, and delete polygon-shaped annotations.
    - **Paint Brush Tool:** Draw masks naturally with a smooth brush. Supports RDP algorithm for automatic curve simplification.
    - **SAM (Segment Anything Model):** Interactively segment objects using positive/negative points.
- **🤖 YOLOv11 Model Integration:** Easily loads custom-trained YOLOv11-seg `.pt` models for inference and fine-tuning.
- **🚀 Model Fine-Tuning & Dataset Management:** 
    - **YAML Creator:** Create dataset YAML files directly within the app by selecting train/val folders.
    - **Fine-Tuning:** Configure hyperparameters (epochs, batch, lr, etc.) and augmentations via a dedicated dialog.
    - Training runs in the background with console logging.
    - The loaded model is automatically updated with the best weights after training.
- **📊 Confidence Score Visualization:** Displays the confidence score for each instance.
- **↔️ Flexible Export:** Export images and labels to user-selected folders.
- **🖱️ User-Friendly Interface:**
  - Zoom/Pan controls.
  - Stable layout with dockable panels.
  - Rich keyboard shortcuts.

## ⚙️ Requirements

The main dependencies are listed in `requirements.txt`.

- Python 3.8+
- PyQt5
- ultralytics
- numpy
- rdp
- opencv-python-headless
- torch
- torchvision
- shapely
- PyYAML

## 🚀 Installation

We recommend using [uv](https://github.com/astral-sh/uv) for fast package management.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/hyeok90/PyQt_active_learning
    cd PyQt_active_learning
    ```

2.  **Install uv (if not already installed):**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

3.  **Create and Activate Virtual Environment:**
    ```bash
    uv venv
    source .venv/bin/activate
    ```

4.  **Install PyTorch (with CUDA support):**
    ```bash
    uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
    ```
    *If you only need CPU support, you can skip this step.*

5.  **Install other dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```

6.  **Fix OpenCV Compatibility:**
    ```bash
    uv pip uninstall opencv-python
    uv pip install --force-reinstall opencv-python-headless
    ```

## 🏃‍♂️ Usage

1.  **Run the application:**
    ```bash
    python main.py
    ```

2.  **Workflow:**
    - **1. Load Model:** Run inference or train directly.
    - **2. Open Image Folder:** Load your dataset images.
    - **3. Annotate:** Use Polygon (W), Paint (B), or SAM (S) tools.
    - **4. Train:** Create a YAML config, set params, and fine-tune your model.
    - **5. Export:** Save your dataset.

## ⌨️ Shortcuts

### Global / Navigation
| Key | Action |
| :--- | :--- |
| `A` / `D` | Previous / Next Image |
| `W` | Toggle Polygon Draw Mode |
| `B` | Toggle Paint Mode |
| `S` | Toggle SAM Mode |
| `Ctrl+S` | Save Current Labels |
| `Ctrl+Z` | Undo Last Shape Modification |
| `Delete` | Delete Selected Instance(s) |
| `Mouse Wheel` | Zoom In / Out |
| `Middle Drag` | Pan Image |

### Paint Mode (B)
| Key | Action |
| :--- | :--- |
| `Q` | Switch to Brush |
| `E` | Switch to Eraser |
| `[` / `]` | Decrease / Increase Brush Size |
| `,` / `.` | Decrease / Increase Brush Smoothness (Epsilon) |

### SAM Mode (S)
| Key | Action |
| :--- | :--- |
| `Q` | Add Positive Point |
| `E` | Add Negative Point |
| `G` | Clear All SAM Points |
| `F` | Finalize & Add Shape |

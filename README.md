# MarkIt! 📸
> **Professional Layered Watermarking for Windows**

[![GitHub release](https://img.shields.io/github/v/release/tomDeller80/MarkIt)](https://github.com/tomDeller80/markit/releases)
[![Platform](https://img.shields.io/badge/platform-windows-blue)](https://github.com/tomDeller80/markit/releases)
![Language](https://img.shields.io/badge/python-3.10+-3776ab?logo=python)

## 📥 Quick Download
**Download the latest standalone executable from the [Releases Page](https://github.com/tomDeller80/the-markit-project/releases/tag/v1.0.0).**
*No Python installation required. Just download and run.*

---

**The Markit! Project** is a desktop utility built with Python and Tkinter, designed for high-precision image and text watermarking. It features a layered processing engine and a responsive workspace tailored for Windows users.

---

## 🖥️ System Requirements

* Operating System: Windows 10/11 (Required for pywindnd native drag-and-drop support).

* Minimum Resolution: 1280 x 720 (HD).

* Recommended Resolution: 1920 x 1080 (Full HD).

* Note: The interface utilizes dual 320px sidebars; resolutions below 1280px wide will significantly restrict the central editing canvas.

---

## 🛠️ Key Functionality
**1. Layer-Based Processing**

Unlike simple image editors, Markit treats every watermark as an independent "Layer."

* **Non-Destructive Editing:** You can adjust the opacity, rotation, and position of a watermark even after placing it.


* **History Stack:** Full Undo/Redo support for layer adjustments.

**2. Smart Tiling Engine**

The app includes a dedicated tiling algorithm that goes beyond simple grids:

* **Single:** Precise placement using a 9-point coordinate system (Top-Left, Center, etc.).


* **Parallel:** A standard grid-repeat across the entire image.


* **Diagonal:** Offset tiling that follows a 45-degree flow, ideal for security watermarking.

**3. Dynamic Text Rendering**

The text engine scans your **Windows System Fonts** (.ttf) and allows for real-time adjustments of:

* Font family, size, and hex-color selection.


* Styling (Bold, Italic, Underline).


* Real-time debounced updates to the canvas to ensure smooth performance.

---

## 📖 Usage Guide

**Step 1: Uploading**

Launch the app and either click the "Add Image" button or simply Drag and Drop an image file (JPG, PNG, WEBP, BMP) directly onto the dark workspace.

**Step 2: Choosing Your Type**

Use the top navigation bar to toggle between Image Watermark (for logos/icons) and Text Watermark.

**Step 3: Placement & Tiling**

* Select a location from the Location Grid (Right Sidebar).


* Choose a Tile Mode. If Parallel or Diagonal is selected, use the Spacing Slider to adjust the density of the pattern.

**Step 4: Refinement**

Adjust the Opacity (0-255) and Rotation (-180° to 180°) sliders. For images, you can scale the logo size; for text, you can pick any system font and color.

**Step 5: Committing & Saving**

* Click **"Apply Changes"** to lock a layer.


* If you need to move or change a previously applied layer, select it and click **"Edit Selection"**.


* Once satisfied, click the "Save" icon in the top right to export your watermarked image.

---

## 🚀 Getting Started


**1. Clone the repository:**

``` bash
    git clone https://github.com/tomDeller80/the-markit-project.git
    cd markit
```

**2. Install dependencies:**

``` bash
    pip install -r requirements.txt
```

**3. Run the app:**

```python
    python main.py
```
---

## 📦 Dependencies

* **ttkbootstrap:** Modern UI themes and widgets.

* **Pillow:** High-performance image manipulation.

* **pywindnd:** Native Windows drag-and-drop integration.

* **matplotlib:** Cross-platform system font discovery.

---



## 📝 License

This project is open-source and available under the MIT License.

---

**Project Status**: Active Maintenance / Low Frequency Updates.
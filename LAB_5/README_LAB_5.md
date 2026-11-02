# LAB 5: Marr--Hildreth Edge Detection

## Aim

To implement the **Marr--Hildreth edge detection algorithm** using
Python and OpenCV, and to study the effect of different Gaussian
smoothing parameters (`sigma`) and zero-crossing thresholds on the
detected edges.

## Overview

The Marr--Hildreth algorithm is a second-order edge detection technique.
It combines Gaussian smoothing with the Laplacian operator and
identifies edges by detecting zero crossings in the Laplacian response.

This program processes one grayscale input image using three parameter
combinations:

    Sigma  Gaussian kernel size
  ------- ----------------------
        4        25 × 25
        7        35 × 35
        9        45 × 45

For each combination, the program generates a six-panel figure showing
the original image, smoothed image, Laplacian magnitude, signed
Laplacian, and zero-crossing results for two thresholds.

## Requirements

-   Python 3
-   OpenCV (`opencv-python`)
-   NumPy
-   Matplotlib

Install the required packages:

``` bash
pip install opencv-python numpy matplotlib
```

## Input Image

The program reads a grayscale image named `lab_5_ip.jpeg` from the
configured input location.

**Important:** Update `IMAGE_PATH` in the Python script so that it
points to the actual image on your computer. For example:

``` python
IMAGE_PATH = r"C:\Users\YourName\Downloads\lab_5_ip.jpeg"
```

If you want the image to be stored in the same folder as the Python
script, use:

``` python
IMAGE_PATH = os.path.join(BASE_DIR, "lab_5_ip.jpeg")
```

The script checks whether the image exists and whether OpenCV can load
it. It then converts the image to floating-point values in the range 0
to 1.

## Algorithm / Working

### 1. Load the image

-   Read the input image in grayscale using `cv2.imread()`.
-   Convert the image to `float64`.
-   Normalize pixel intensities by dividing by 255.

### 2. Gaussian smoothing

The image is smoothed using `cv2.GaussianBlur()`.

Gaussian smoothing reduces noise and small intensity variations before
the Laplacian operation. The program uses the following
`(sigma, kernel size)` pairs:

-   `(4, 25 × 25)`
-   `(7, 35 × 35)`
-   `(9, 45 × 45)`

### 3. Laplacian operation

The Laplacian operator is applied to the smoothed image using:

``` python
cv2.Laplacian(smoothed, cv2.CV_64F, ksize=3)
```

The Laplacian measures second-order intensity changes. The program
retains the signed Laplacian response and also calculates its absolute
magnitude for display.

### 4. Zero-crossing detection

An edge is identified when two neighboring Laplacian values have
opposite signs or one of them is zero. The program checks four
directions:

-   Horizontal
-   Vertical
-   Diagonal (down-right)
-   Diagonal (down-left)

The function `find_zero_crossings()` compares neighboring values and
marks both pixels when a sign change satisfies the selected threshold
condition.

### 5. Threshold selection

Two zero-crossing results are produced for each sigma value:

-   **T = 0:** Detects sign changes without an additional
    minimum-difference threshold.
-   **T = 4% of maximum response:** Uses
    `T4 = 0.04 × max(abs(Laplacian))` to reject sign changes whose
    neighboring response difference is not greater than this threshold.

### 6. Display and save results

For every sigma value, a 2 × 3 figure is generated containing:

  Position   Output
  ---------- --------------------------------------------
  \(a\)      Original image
  \(b\)      Gaussian-smoothed image
  \(c\)      Laplacian magnitude
  \(d\)      Signed Laplacian
  \(e\)      Zero crossings, T = 0
  \(f\)      Zero crossings, T = 4% of maximum response

The figures are saved at 300 DPI. Matplotlib uses the non-interactive
`Agg` backend, so the program saves the figures without opening GUI
windows.

## How to Run

1.  Save the Python program in your Lab 5 folder, for example as
    `lab_5.py`.
2.  Set `IMAGE_PATH` to the correct location of `lab_5_ip.jpeg`.
3.  Open a terminal or command prompt in the folder containing the
    script.
4.  Run:

``` bash
python lab_5.py
```

5.  After successful execution, open the `output` folder to view the
    generated figures.

## Output Files

The script creates an `output` directory alongside the Python script and
saves:

``` text
output/
├── Marr_Hildreth_Sigma_4.png
├── Marr_Hildreth_Sigma_7.png
└── Marr_Hildreth_Sigma_9.png
```

Each image contains the six result panels described above.

## Key Observations

-   Gaussian smoothing reduces noise before edge detection.
-   Changing `sigma` changes the amount of smoothing and can affect the
    detected edge details.
-   The Laplacian response contains positive and negative values around
    intensity transitions.
-   Zero crossings are used to locate potential edges.
-   Increasing the zero-crossing threshold can suppress weaker responses
    and produce fewer detected edge pixels.

The actual visual result depends on the input image and the selected
parameters.

## Conclusion

The Marr--Hildreth edge detection method was implemented using Gaussian
smoothing, the Laplacian operator, and zero-crossing detection. The
program compares three Gaussian smoothing settings (`sigma = 4, 7, 9`)
and two zero-crossing thresholds (`T = 0` and
`T = 4% of the maximum Laplacian response`). The resulting figures make
it possible to observe how smoothing and threshold selection affect the
detected edges.

## Troubleshooting

-   **`FileNotFoundError`:** Check that `IMAGE_PATH` points to the
    correct image file.
-   **Image could not be loaded:** Confirm that the image is valid and
    that the path and file extension are correct.
-   **Module not found:** Install the missing package using the
    `pip install` command above.
-   **No output folder:** Confirm that the program ran to completion and
    check the terminal for errors.

------------------------------------------------------------------------

**Lab:** 5\
**Topic:** Marr--Hildreth Edge Detection\
**Language:** Python

# Lab 1 – Image Intensity Transformations

## Aim

To study and implement basic image intensity transformation methods, namely **Negative Transformation, Power-Law (Gamma) Transformation, and Logarithmic Transformation**, using Python and OpenCV.

---

## Objectives

The objectives of this practical are:

* To understand the basics of image intensity transformations.
* To implement negative transformation on a grayscale image.
* To implement Power-Law (Gamma) transformation.
* To implement logarithmic transformation.
* To study the effect of transformations on pixel intensity values.
* To perform transformations using pixel matrices.
* To implement the transformations using OpenCV and NumPy.

---

## Theory

Image intensity transformation is a basic **Digital Image Processing** technique used to modify pixel values for image enhancement.

An intensity transformation maps an input intensity `r` to an output intensity `s`.

**s = T(r)**

where:

* `r` = input pixel intensity
* `s` = output pixel intensity
* `T` = transformation function

For an 8-bit grayscale image, pixel values range from **0 to 255**. Here, `0` represents black and `255` represents white.

Three intensity transformations are performed in this practical.

---

## 1. Negative Transformation

Negative transformation reverses the intensity values of an image.

The transformation is given by:

**s = (L - 1) - r**

For an 8-bit grayscale image:

**s = 255 - r**

where `L = 256` represents the total number of intensity levels.

For example:

| **Original Pixel** | **Negative Pixel** |
| ------------------ | ------------------ |
| 0                  | 255                |
| 50                 | 205                |
| 100                | 155                |
| 150                | 105                |
| 255                | 0                  |

This converts dark areas into bright areas and bright areas into dark areas.

---

## 2. Power-Law (Gamma) Transformation

Power-Law transformation, also called **Gamma transformation**, is represented by:

**s = c × r^γ**

The input intensity is first normalized to `[0, 1]`:

```
r_norm = r / 255
```

The transformation is then performed:

```
s_norm = c * (r_norm ** gamma)
```

The result is finally converted back to the range `[0, 255]`.

### Effect of Gamma

The Gamma value determines the brightness of the output image:

* **γ < 1** → image becomes brighter.
* **γ = 1** → image remains approximately unchanged.
* **γ > 1** → image becomes darker.

In this practical, the Gamma value used is:

```
γ = 0.5
```

A Lookup Table (LUT) can be used in OpenCV to apply the transformation efficiently.

---

## 3. Logarithmic Transformation

The logarithmic transformation is represented by:

**s = c × log(1 + r)**

where:

* `r` = input pixel intensity
* `s` = output pixel intensity
* `c` = scaling constant

The scaling constant is calculated as:

**c = 255 / log(1 + r_max)**

where `r_max` is the highest pixel intensity in the image.

Logarithmic transformation increases lower intensity values and compresses higher intensity values. It is useful for improving details in darker regions.

---

# Software and Libraries Used

The following software and Python libraries are used:

* **Python**
* **OpenCV (`cv2`)**
* **NumPy**
* **Matplotlib**

### Python Libraries

```
import cv2
import numpy as np
import matplotlib.pyplot as plt
```

---

# Implementation

The practical is performed in two stages:

1. **Manual implementation using a pixel matrix**
2. **Image processing using OpenCV and NumPy**

---

## Part A – Manual Matrix Implementation

A user-defined grayscale image matrix is taken as input.

The program accepts:

* Number of rows
* Number of columns
* Pixel values between 0 and 255
* Gamma value for Power-Law transformation

The input matrix is then processed using the three transformations.

### 1. Manual Natural Logarithm

A custom `manual_ln()` function is used to calculate the natural logarithm using a Taylor series.

The formula used is:

**ln(x) = 2 × [z + z³/3 + z⁵/5 + ...]**

where:

**z = (x - 1) / (x + 1)**

This provides the logarithm value without directly using Python's logarithm function.

### 2. Negative Transformation

The negative transformation is performed using:

```
new_pixel = max_intensity - pixel
```

For an 8-bit image:

```
new_pixel = 255 - pixel
```

The operation is applied to every pixel in the input matrix.

### 3. Power-Law Transformation

The input pixel is first normalized:

```
r_norm = pixel / max_intensity
```

The Power-Law transformation is then applied:

```
s_norm = c * (r_norm ** gamma)
```

The result is converted back to the intensity range `[0, 255]`.

### 4. Logarithmic Transformation

A scaling constant is calculated using the maximum intensity:

```
c = max_intensity / manual_ln(1 + max_intensity)
```

The logarithmic transformation is then applied:

```
s = c * manual_ln(1 + pixel)
```

The output values are limited to the range 0 to 255.

---

# Part B – Image Processing Using OpenCV

A grayscale image is loaded using OpenCV:

```
img = cv2.imread("Lab1/image.jpg", cv2.IMREAD_GRAYSCALE)
```

The three transformations are then applied to the image.

---

## Negative Transformation Using OpenCV

The negative image is generated using:

```
neg_img = cv2.bitwise_not(img)
```

This reverses the intensity value of each pixel.

---

## Power-Law Transformation Using OpenCV

A Lookup Table containing transformed values for all 256 grayscale levels is generated.

The Gamma value used is:

```
gamma = 0.5
```

The lookup table is created using:

```
lut = np.array(
    [((i / 255.0) ** 0.5) * 255 for i in np.arange(0, 256)]
).astype("uint8")
```

The LUT is then applied using:

```
gamma_img = cv2.LUT(img, lut)
```

Using a LUT reduces repeated calculations and makes the transformation faster.

---

## Logarithmic Transformation Using OpenCV and NumPy

The maximum pixel value is obtained using:

```
max_pixel_val = float(np.max(img))
```

The scaling constant is calculated as:

```
c = 255 / np.log(1 + max_pixel_val)
```

The logarithmic transformation is applied using NumPy:

```
log_img = np.array(
    c * np.log1p(img.astype(np.float32)),
    dtype=np.uint8
)
```

`np.log1p()` is used to calculate `log(1 + x)` accurately.

---

# Algorithm / Procedure

1. Start the program.
2. Define the grayscale image or pixel matrix.
3. Enter the required matrix dimensions and pixel values.
4. Enter the Gamma value.
5. Apply Negative Transformation.
6. Apply Power-Law (Gamma) Transformation.
7. Apply Logarithmic Transformation.
8. Display the transformed matrices.
9. Load the grayscale image using OpenCV.
10. Apply Negative Transformation using `cv2.bitwise_not()`.
11. Generate the Lookup Table for Gamma transformation.
12. Apply the LUT using `cv2.LUT()`.
13. Calculate the logarithmic scaling constant.
14. Apply logarithmic transformation using NumPy.
15. Display or save the transformed images.
16. End the program.

---

# Input

The input for the practical consists of:

* A grayscale image stored as `image.jpg`.
* Pixel intensity values between **0 and 255**.
* A user-defined Gamma value.

For the OpenCV implementation, the image is loaded from:

```
Lab1/image.jpg
```

---

# Result

The **Negative, Power-Law (Gamma), and Logarithmic intensity transformations** were successfully implemented using manual pixel-matrix operations and Python libraries.

The Negative Transformation inverted the intensity values. The Power-Law transformation with `γ = 0.5` produced a brighter image, while the Logarithmic Transformation improved details in darker regions.

Thus, the practical successfully demonstrated basic image intensity transformations using **Python, OpenCV, and NumPy**.

---

# Conclusion

In this practical, **Negative, Power-Law (Gamma), and Logarithmic Transformation** techniques were studied and implemented.

The experiment demonstrated how pixel intensity values can be modified mathematically for image enhancement. Both manual matrix operations and library-based methods were used to understand the practical implementation of intensity transformations in Python.

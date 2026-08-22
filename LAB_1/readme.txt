Lab 1 – Image Intensity Transformations
Aim

To study and implement basic image intensity transformations such as Negative, Power-Law (Gamma), and Logarithmic Transformation using Python and OpenCV.

Objectives

The objectives of this practical are:

To understand image intensity transformations.
To implement negative transformation.
To implement Power-Law (Gamma) transformation.
To implement logarithmic transformation.
To observe changes in pixel intensity values.
To perform transformations using pixel matrices and Python libraries.
Theory

Image intensity transformation is a technique used to change the intensity values of pixels for image enhancement.

It is represented as:

s = T(r)

where:

r = input pixel intensity
s = output pixel intensity
T = transformation function

For an 8-bit grayscale image, intensity values range from 0 to 255, where 0 represents black and 255 represents white.

1. Negative Transformation

Negative transformation reverses the intensity of every pixel.

s = (L - 1) - r

For an 8-bit image:

s = 255 - r

Example:

Original	Negative
0	255
50	205
100	155
255	0

Thus, dark pixels become bright and bright pixels become dark.

2. Power-Law (Gamma) Transformation

Power-Law transformation is given by:

s = c × r^γ

The pixel is first normalized:

r_norm = r / 255

Then:

s_norm = c * (r_norm ** gamma)

The result is converted back to the range 0–255.

Effect of Gamma
γ < 1 → image becomes brighter.
γ = 1 → image remains nearly unchanged.
γ > 1 → image becomes darker.

In this practical:

γ = 0.5

A Lookup Table (LUT) can be used in OpenCV for faster processing.

3. Logarithmic Transformation

Logarithmic transformation is represented by:

s = c × log(1 + r)

The scaling constant is:

c = 255 / log(1 + r_max)

It expands lower intensity values and compresses higher intensity values. Hence, it is useful for enhancing details in dark regions.

Software and Libraries Used
Python
OpenCV (cv2)
NumPy
Matplotlib
Python Libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
Implementation

The experiment is performed in two parts:

Manual pixel-matrix implementation
OpenCV and NumPy implementation
Part A – Manual Matrix Implementation

A small grayscale pixel matrix is entered manually. The matrix contains values between 0 and 255, along with a Gamma value.

The three transformations are then applied to the matrix.

1. Manual Natural Logarithm

A custom manual_ln() function can be used to calculate the natural logarithm using a Taylor series.

ln(x) = 2 × [z + z³/3 + z⁵/5 + ...]

where:

z = (x - 1) / (x + 1)

2. Negative Transformation

Each pixel is transformed using:

new_pixel = 255 - pixel

The operation is performed on every element of the input matrix.

3. Power-Law Transformation

The pixel is normalized first:

r_norm = pixel / 255

Then:

s_norm = r_norm ** gamma

The result is converted back to the range 0–255.

4. Logarithmic Transformation

The scaling constant is calculated as:

c = 255 / manual_ln(1 + max_pixel)

The transformed pixel is calculated using:

s = c * manual_ln(1 + pixel)

The final value is restricted to 0–255.

Part B – Image Processing Using OpenCV

A grayscale image is loaded using:

img = cv2.imread("Lab1/image.jpg", cv2.IMREAD_GRAYSCALE)

The three transformations are then applied to the image.

Negative Transformation Using OpenCV

The negative image is obtained using:

neg_img = cv2.bitwise_not(img)

This reverses the intensity values of all pixels.

Power-Law Transformation Using OpenCV

The Gamma value used is:

gamma = 0.5

A Lookup Table is generated:

lut = np.array(
    [((i / 255.0) ** 0.5) * 255 for i in np.arange(0, 256)]
).astype("uint8")

The LUT is applied using:

gamma_img = cv2.LUT(img, lut)

LUT improves efficiency because the transformation is calculated for all 256 intensity values beforehand.

Logarithmic Transformation Using OpenCV and NumPy

The maximum pixel value is found using:

max_pixel_val = float(np.max(img))

The scaling constant is:

c = 255 / np.log(1 + max_pixel_val)

The transformation is applied using:

log_img = np.array(
    c * np.log1p(img.astype(np.float32)),
    dtype=np.uint8
)

np.log1p() calculates log(1 + x) accurately.

Algorithm / Procedure
Start the program.
Import the required libraries.
Define the pixel matrix or grayscale image.
Enter the Gamma value.
Apply Negative Transformation.
Apply Power-Law Transformation.
Apply Logarithmic Transformation.
Display the transformed matrices.
Load the image using OpenCV.
Apply the three transformations.
Display or save the output images.
Stop the program.
Input

The input consists of:

A grayscale image named image.jpg.
Pixel values between 0 and 255.
A user-defined Gamma value.

The image is loaded from:

Lab1/image.jpg
Result

The Negative, Power-Law, and Logarithmic transformations were successfully implemented using both manual pixel operations and Python libraries.

The negative transformation inverted the image, Gamma transformation with γ = 0.5 increased brightness, and logarithmic transformation enhanced details in darker regions.

Conclusion

The experiment demonstrated three basic intensity transformation techniques: Negative, Power-Law, and Logarithmic Transformation.

Both manual matrix operations and OpenCV/NumPy implementations were performed to understand how pixel intensities can be modified for image enhancement.

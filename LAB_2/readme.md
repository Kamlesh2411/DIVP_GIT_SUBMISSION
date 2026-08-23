Lab 2 – Image Intensity Transformations
Aim

To implement and study Negative, Gamma (Power-Law), and Logarithmic intensity transformations on a grayscale image using manual pixel-level operations with Python, NumPy, and OpenCV.

Objectives

The objectives of this practical are:

To understand image intensity transformations.
To implement Negative Transformation manually.
To implement Gamma (Power-Law) Transformation.
To implement Logarithmic Transformation.
To perform transformations pixel-by-pixel.
To observe the effect of different transformations on an image.
Theory
1. Image Intensity Transformation

Image intensity transformation is a technique used to modify pixel values of an image.

The general transformation is represented as:

s = T(r)

where:

r = input pixel intensity
s = output pixel intensity
T = transformation function

For an 8-bit grayscale image, pixel values range from 0 to 255.

The three transformations used in this practical are:

Negative Transformation
Gamma Transformation
Logarithmic Transformation
2. Negative Transformation

Negative transformation reverses the intensity values of an image.

The transformation is given by:

s = (L - 1) - r

For an 8-bit image:

s = 255 - r

Input Pixel	Negative Pixel
0	255
50	205
100	155
200	55
255	0

Dark pixels become bright and bright pixels become dark.

3. Gamma (Power-Law) Transformation

Gamma transformation is represented by:

s = c × r^γ

The input pixel is first normalized:

r = pixel / 255

The transformation is then applied:

s = r^γ

The result is converted back to the range 0 to 255.

Effect of Gamma
γ < 1 → image becomes brighter.
γ = 1 → image remains approximately unchanged.
γ > 1 → image becomes darker.

The Gamma value is entered by the user during program execution.

4. Logarithmic Transformation

Logarithmic transformation is given by:

s = c × log(1 + r)

For an 8-bit grayscale image:

c = 255 / log(256)

The transformation expands lower intensity values and compresses higher intensity values.

It is useful for enhancing details in darker regions.

Software and Libraries Used

The following technologies and libraries are used:

Python
OpenCV
NumPy
Libraries
import cv2
import numpy as np
Algorithm / Procedure
Start the program.
Import NumPy and OpenCV.
Load the grayscale input image.
Check whether the image is loaded successfully.
Define the Negative Transformation function.
Define the Gamma Transformation function.
Define the Logarithmic Transformation function.
Display the transformation menu.
Select the required transformation.
Enter Gamma value when Gamma transformation is selected.
Apply the selected transformation pixel-by-pixel.
Display the original and transformed images.
Repeat until Exit is selected.
End the program.
Implementation
Step 1 – Load Input Image

The grayscale image is loaded using:

path = "DATASET/LAB_2/lab_2_image.jpg"

img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

If the image cannot be loaded, the program displays an error message.

Step 2 – Negative Transformation

The Negative function processes every pixel using nested loops.

The transformation is:

result[i, j] = 255 - image[i, j]

The resulting pixels are stored in a new image matrix.

Task 1 – Negative Transformation

The input grayscale image is processed using the Negative Transformation.

The operation performed on each pixel is:

Output Pixel = 255 − Input Pixel

The original and negative images are then displayed.

output = negative(img)

cv2.imshow("Original", img)
cv2.imshow("Negative", output)
Task 2 – Gamma (Power-Law) Transformation

The Gamma transformation is applied using a user-defined Gamma value.

First, each pixel is normalized:

r = image[i, j] / 255.0

The Gamma operation is performed:

s = pow(r, gamma)

The result is converted back to the grayscale range:

result[i, j] = np.uint8(s * 255)

The transformed image is then displayed.

gamma = float(input("Enter Gamma Value: "))

output = gamma_transform(img, gamma)

cv2.imshow("Original", img)
cv2.imshow("Gamma", output)
Task 3 – Logarithmic Transformation

The scaling constant is calculated as:

c = 255 / np.log(256)

The logarithmic transformation is applied to each pixel:

result[i, j] = np.uint8(
    c * np.log(1 + image[i, j])
)

The output image is displayed along with the original image.

output = log_transform(img)

cv2.imshow("Original", img)
cv2.imshow("Log", output)
Task 4 – Menu-Based Execution

The program provides a menu to select the required transformation:

========== MENU ==========
1. Negative
2. Gamma (Power Law)
3. Log Transformation
4. Exit

The selected option determines which transformation function is executed.

If an invalid option is entered, the program displays:

Invalid Choice
Results and Observations
Negative Transformation

The Negative Transformation reverses the intensity values of the image.

Dark areas become bright.
Bright areas become dark.
The overall intensity distribution is inverted.
Gamma Transformation

The output brightness depends on the Gamma value.

γ < 1 produces a brighter image.
γ = 1 approximately preserves the original image.
γ > 1 produces a darker image.
Logarithmic Transformation

The logarithmic transformation increases the visibility of darker intensity levels.

Lower intensity values are expanded.
Higher intensity values are compressed.
Dark-region details become more visible.
Output

The practical produces the following major outputs:

Original Image

Input grayscale image.

Negative Image

Image obtained using Negative Transformation.

Gamma Image

Image obtained using the user-defined Gamma value.

Logarithmic Image

Image obtained using Logarithmic Transformation.

Result

The Negative, Gamma (Power-Law), and Logarithmic intensity transformations were successfully implemented using manual pixel-level operations. The transformed images were displayed along with the original grayscale image.

Observations
Negative transformation inverts the intensity values of the image.
Gamma transformation controls image brightness according to the selected Gamma value.
Gamma values less than 1 brighten the image.
Gamma values greater than 1 darken the image.
Logarithmic transformation enhances details in darker regions.
Manual pixel-level processing provides an understanding of how intensity transformations operate internally.
Conclusion

In this practical, three basic image intensity transformations — Negative, Gamma (Power-Law), and Logarithmic Transformation — were implemented using Python, NumPy, and OpenCV.

The experiment demonstrated how individual pixel values can be mathematically modified to invert intensities, control image brightness, and enhance details in darker regions.

Thus, the practical provided an understanding of pixel-level intensity transformation techniques used for image enhancement and analysis.

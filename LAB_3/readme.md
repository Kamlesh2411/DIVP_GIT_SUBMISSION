# Lab 3 – AGV Spatial Filtering and Image Restoration

## Aim

To study and implement **spatial filtering methods for AGV (Automated Guided Vehicle) image restoration and enhancement**, including noise reduction, Laplacian sharpening, unsharp masking, and high-boost filtering.

The practical also includes implementing **2D spatial correlation from scratch** and evaluating the results using **PSNR** and **image sharpness**.

---

# Objectives

The objectives of this practical are:

* To understand spatial filtering in image processing.
* To implement 2D spatial correlation manually.
* To avoid predefined filtering functions such as `cv2.filter2D()`.
* To add Gaussian noise and motion blur to an image.
* To reduce noise using averaging filters.
* To study different averaging filter sizes.
* To enhance edges using Laplacian operators.
* To compare 4-neighbor and 8-neighbor Laplacian filters.
* To implement unsharp masking and high-boost filtering.
* To calculate PSNR and image sharpness.
* To compare the performance of different filters.

---

# Theory

## 1. Spatial Filtering

Spatial filtering operates directly on image pixels using a small matrix called a **kernel**, **mask**, or **filter**.

The kernel moves across the image and combines neighboring pixel values to produce the output.

The general expression is:

**g(x,y) = ΣΣ f(x+i,y+j) h(i,j)**

where:

* `f(x,y)` = input image
* `h(i,j)` = filter kernel
* `g(x,y)` = output image

Spatial filtering is commonly used for:

* Noise removal
* Smoothing
* Edge detection
* Sharpening
* Image enhancement

---

# 2. 2D Spatial Correlation

In this practical, 2D spatial correlation is implemented **manually** without using:

```text
cv2.filter2D()
```

or:

```text
scipy.signal
```

The image is first padded so that filtering can also be performed near the boundaries.

The required padding is calculated using:

```text
pad_h, pad_w = k_h // 2, k_w // 2
```

The image is padded using:

```text
np.pad(
    image,
    ((pad_h, pad_h), (pad_w, pad_w)),
    mode='constant',
    constant_values=0
)
```

For every pixel, the corresponding image region is multiplied with the kernel and summed:

```text
output[i, j] = np.sum(region * kernel)
```

This gives an understanding of how spatial filtering works internally.

---

# 3. Image Degradation

To test restoration methods, the original image is intentionally degraded using:

1. Gaussian noise
2. Motion blur

---

## 3.1 Gaussian Noise

Gaussian noise is random noise that follows a normal distribution.

It can be represented as:

**N ~ N(0, σ²)**

where:

* Mean = `0`
* Standard deviation = `σ`

The noisy image is represented by:

**g(x,y) = f(x,y) + n(x,y)**

In this practical, two noise levels are used:

```text
Sigma = 10
Sigma = 25
```

A larger sigma value produces stronger noise.

The noise is generated using:

```text
noise = np.random.normal(0, sigma, image.shape)
```

---

# 4. Motion Blur

Motion blur occurs when the camera or object moves while capturing an image.

For an AGV, it may be caused by:

* Vehicle movement
* Camera vibration
* Sudden speed changes
* Camera exposure during motion

A horizontal motion blur is simulated using a linear kernel.

For a blur length of 9:

```text
9 × 9 motion blur kernel
```

The center row contains equal values of:

**1 / 9**

The blurred image is generated using the custom spatial correlation function.

---

# 5. Averaging Filter

An averaging filter is a smoothing filter mainly used to reduce noise.

For an `N × N` filter, each kernel element is:

**h(i,j) = 1 / N²**

For example, a 3 × 3 filter is:

```text
1/9  1/9  1/9
1/9  1/9  1/9
1/9  1/9  1/9
```

Each output pixel is obtained from the average of its neighboring pixels.

It reduces noise but may also smooth edges.

---

# 6. Averaging Filter Trade-Off

The following filter sizes are tested:

```text
3 × 3
5 × 5
9 × 9
```

They are applied to images having:

```text
Sigma = 10
Sigma = 25
```

This helps compare the effect of filter size and noise level.

### General observation

A smaller filter provides moderate smoothing and retains more details.

A larger filter removes more noise but may blur edges and fine image details.

---

# 7. Laplacian Sharpening

The Laplacian is a second-order derivative operator used for detecting intensity changes and sharpening images.

It is useful for:

* Edge detection
* Boundary enhancement
* Image sharpening

Two Laplacian kernels are used in this experiment.

---

## 7.1 4-Neighbor Laplacian

The 4-neighbor kernel is:

```text
 0   1   0
 1  -4   1
 0   1   0
```

It considers the four pixels directly connected to the center pixel.

---

## 7.2 8-Neighbor Laplacian

The 8-neighbor kernel is:

```text
 1   1   1
 1  -8   1
 1   1   1
```

It considers all eight surrounding pixels.

Therefore, it detects intensity changes in more directions.

---

# 8. Laplacian Sharpening Equation

The sharpening equation used is:

**g(x,y) = f(x,y) - ∇²f(x,y)**

The implementation is:

```text
sharp_4 = img_blurred.astype(np.float64) - resp_4

sharp_8 = img_blurred.astype(np.float64) - resp_8
```

The output values are restricted to:

```text
0 to 255
```

---

# 9. Unsharp Masking

Unsharp masking is used to increase image sharpness.

The basic steps are:

1. Blur the image.
2. Subtract the blurred image from the original.
3. Obtain the detail mask.
4. Add the mask to the original image.

The mask is:

**mask = original - blurred**

The enhanced image is:

**g = original + k × mask**

where `k` controls the sharpening strength.

---

# 10. High-Boost Filtering

High-boost filtering is an extended form of unsharp masking.

The following values are tested:

```text
k = 1
k = 1.5
k = 2
k = 3
```

The enhanced image is calculated as:

```text
boosted = original + (k * mask)
```

### Effect of k

* `k = 1` → normal unsharp masking.
* `k > 1` → stronger sharpening.
* Higher `k` → more edge enhancement.
* Very high `k` → may increase noise and artifacts.

---

# 11. Peak Signal-to-Noise Ratio (PSNR)

PSNR is used to compare the processed image with the original image.

It is based on Mean Squared Error (MSE).

### Mean Squared Error

**MSE = (1/N) Σ (Original - Processed)²**

PSNR is calculated as:

**PSNR = 20 × log₁₀(MAX / √MSE)**

For an 8-bit image:

**MAX = 255**

Therefore:

**PSNR = 20 × log₁₀(255 / √MSE)**

### Interpretation

A higher PSNR generally indicates better similarity between the processed and original image.

A lower PSNR indicates a larger difference.

---

# 12. Image Sharpness

Image sharpness is measured using the **variance of the Laplacian**.

The Laplacian response is calculated using:

```text
0   1   0
1  -4   1
0   1   0
```

The variance of the response represents the sharpness measure.

A higher value generally indicates stronger edges and more image details.

---

# Software and Libraries Used

The following tools are used:

* **Python**
* **OpenCV**
* **NumPy**
* **Matplotlib**

### Libraries

```text
import numpy as np
import cv2
import matplotlib.pyplot as plt
```

---

# Algorithm / Procedure

1. Start the program.
2. Generate the clean AGV image.
3. Consider it as the reference image.
4. Add Gaussian noise with `σ = 10`.
5. Add Gaussian noise with `σ = 25`.
6. Generate horizontal motion blur.
7. Implement 2D spatial correlation manually.
8. Apply 3 × 3, 5 × 5, and 9 × 9 averaging filters.
9. Calculate PSNR and sharpness.
10. Apply 4-neighbor and 8-neighbor Laplacian filters.
11. Perform Laplacian sharpening.
12. Generate the unsharp mask.
13. Apply high-boost filtering for different `k` values.
14. Calculate PSNR and sharpness for the outputs.
15. Display and compare the results.
16. End the program.

---

# Results and Observations

## Averaging Filter

The averaging filters reduce Gaussian noise by smoothing neighboring pixels.

* 3 × 3 gives moderate smoothing.
* 5 × 5 provides stronger smoothing.
* 9 × 9 gives maximum smoothing but may remove fine details.
* Higher noise requires stronger filtering.

Thus, there is a trade-off between **noise reduction and image sharpness**.

---

## Laplacian Sharpening

Laplacian filtering enhances boundaries and edges in the blurred image.

* The 4-neighbor filter considers horizontal and vertical neighbors.
* The 8-neighbor filter considers all surrounding pixels.
* Sharpening increases the strength of image edges.

---

## High-Boost Filtering

High-boost filtering enhances high-frequency components of the image.

As `k` increases:

```text
1 → 1.5 → 2 → 3
```

the sharpening effect becomes stronger.

However, excessive sharpening may also amplify noise.

---

# Implementation

## Step 1 – Create Ground Truth Image

A synthetic AGV scene is created with dimensions:

```text
200 × 200
```

This image is treated as the clean reference image.

---

## Step 2 – Generate Degraded Images

Three degraded images are generated.

### Gaussian Noise – Sigma 10

```text
img_noisy_10 = add_gaussian_noise(clean_img, sigma=10)
```

### Gaussian Noise – Sigma 25

```text
img_noisy_25 = add_gaussian_noise(clean_img, sigma=25)
```

### Motion Blur

```text
img_blurred = add_motion_blur(clean_img, length=9)
```

These represent different degradation conditions of an AGV camera.

---

# Task 1 – Noise Suppression Using Averaging Filters

The following kernel sizes are tested:

```text
3 × 3
5 × 5
9 × 9
```

The filters are applied to both noisy images.

The averaging kernel is generated using:

```text
box_kernel = np.ones((size, size)) / (size * size)
```

The custom correlation function is used to process the image.

PSNR and sharpness are calculated for each output.

---

# Task 2 – Boundary Recovery Using Laplacian Sharpening

The motion-blurred image is processed using two Laplacian operators.

### 4-Neighbor Laplacian

```text
0   1   0
1  -4   1
0   1   0
```

### 8-Neighbor Laplacian

```text
1   1   1
1  -8   1
1   1   1
```

The Laplacian response is calculated and used to sharpen the blurred image.

The sharpening operation is:

**Sharpened Image = Blurred Image − Laplacian Response**

PSNR and sharpness are then calculated.

---

# Task 3 – Unsharp Masking / High-Boost Filtering

A 5 × 5 averaging filter is first applied to the noisy image.

The blur kernel is:

```text
blur_kernel = np.ones((5, 5)) / 25.0
```

The high-frequency mask is:

**Mask = Original − Blurred**

The following values are tested:

```text
k = 1
k = 1.5
k = 2
k = 3
```

The final image is obtained using:

**g = Original + k × Mask**

PSNR and sharpness are calculated for each value of `k`.

---

# Task 4 – Quantitative Evaluation

The processed images are evaluated using two measures:

### 1. PSNR

Measures the similarity between the processed image and the original image.

### 2. Sharpness

Calculated using the variance of the Laplacian.

The program displays results such as:

```text
Sigma 10, Kernel 3x3 -> PSNR: ... | Sharpness: ...
Sigma 25, Kernel 3x3 -> PSNR: ... | Sharpness: ...
```

Similar values are calculated for all averaging, Laplacian, and high-boost results.

---

# Result

The spatial filtering techniques were successfully applied to degraded AGV images.

Averaging filters reduced Gaussian noise, Laplacian filtering enhanced blurred boundaries, and high-boost filtering improved image sharpness. **PSNR and sharpness** were also calculated for quantitative comparison.

# Observations

* Averaging filters reduce noise but can smooth image details.
* Smaller kernels preserve more edges.
* Larger kernels provide stronger smoothing.
* Laplacian filters improve image boundaries.
* Increasing `k` increases the sharpening effect.
* Excessive sharpening can also enhance unwanted noise.
* PSNR and sharpness help compare the filtering results.

# Output

The practical produces the following outputs:

### Degraded Images

* Clean Ground Truth
* Gaussian Noise with `σ = 10`
* Gaussian Noise with `σ = 25`
* Motion Blurred Image

### Averaging Filter Results

* Sigma 10 with 3 × 3 filter
* Sigma 10 with 5 × 5 filter
* Sigma 10 with 9 × 9 filter
* Sigma 25 with 3 × 3 filter
* Sigma 25 with 5 × 5 filter
* Sigma 25 with 9 × 9 filter

### Laplacian Sharpening Results

* 4-neighbor sharpened image
* 8-neighbor sharpened image

### High-Boost Results

* `k = 1`
* `k = 1.5`
* `k = 2`
* `k = 3`

### Quantitative Results

PSNR and sharpness values are obtained for each processed image.

---

# Conclusion

In this practical, **spatial filtering techniques for AGV image restoration and enhancement** were studied and implemented.

2D spatial correlation was developed from scratch, while Gaussian noise and motion blur were used to simulate image degradation. Averaging filters were used for noise removal, and Laplacian filters were used for edge enhancement.

Unsharp masking and high-boost filtering were also implemented to improve image sharpness. Finally, **PSNR and variance of the Laplacian** were used to evaluate the processed images.

Thus, the practical demonstrated the use of spatial filtering for **noise reduction, edge enhancement, sharpening, and image restoration** in AGV vision applications.


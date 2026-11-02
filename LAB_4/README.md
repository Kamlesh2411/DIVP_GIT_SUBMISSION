# PCC-03: Digital Image and Video Processing
## Lab: Spatial Filtering for an AGV Camera Image

This lab demonstrates spatial-domain image processing techniques that can be used to improve images captured by an **Autonomous Guided Vehicle (AGV) camera**. The program creates a synthetic grayscale road scene, introduces noise and motion blur, applies smoothing and sharpening filters, evaluates the processed images, and saves the resulting images and plots.

## 1. Objectives

- Generate a grayscale AGV/road test image.
- Add Gaussian noise with standard deviations of **10** and **25**.
- Simulate horizontal motion blur using a 9-pixel motion-blur kernel.
- Implement 2D correlation manually, without using `cv2.filter2D()` or `scipy.signal` filtering shortcuts.
- Apply averaging filters of sizes **3×3**, **5×5**, and **9×9**.
- Sharpen a motion-blurred image using 4-neighbour and 8-neighbour Laplacian filters.
- Apply unsharp masking/high-boost filtering with boost factors **k = 1, 1.5, 2, 3**.
- Evaluate image quality using **PSNR** and sharpness using the **variance of the Laplacian**.
- Display and save processed images, comparison figures, and a sharpness graph.

## 2. Technologies and Libraries

The program is written in Python and uses:

| Library | Purpose |
|---|---|
| NumPy | Numerical operations, arrays, noise generation, and kernel calculations |
| OpenCV (`cv2`) | Drawing the synthetic scene, color conversion, and saving images |
| Matplotlib | Displaying and saving image comparisons and graphs |

## 3. Requirements

Install the required libraries if they are not already available:

```bash
pip install numpy opencv-python matplotlib
```

No external input image is required. The program generates its own AGV/road test image.

## 4. How to Run

1. Save the Python program as a `.py` file, or paste it into a Jupyter/Google Colab notebook.
2. Make sure NumPy, OpenCV, and Matplotlib are installed.
3. Run the complete program from top to bottom.
4. The program displays the processed image grids and prints the PSNR and sharpness measurements.
5. The output PNG files are saved in the current working directory. In Google Colab, they appear in the `/content` directory and can be downloaded from the Files panel.

Example command for a local Python environment:

```bash
python spatial_filtering_agv.py
```

## 5. Processing Workflow

```text
Create synthetic AGV road scene
              |
              v
       Clean grayscale image
              |
       +------+------+
       |             |
       v             v
 Add Gaussian     Create 9-pixel
 noise            motion blur
 (sigma 10, 25)       |
       |              v
       v        Laplacian sharpening
 Averaging       (4-neighbour and
 filters          8-neighbour)
 (3x3, 5x5, 9x9)       |
       |              v
       v        Sharpened outputs
 Filtered outputs
       |
       +----------------------+
                              |
                              v
                    PSNR and sharpness
                         evaluation
                              |
                              v
                    Display and save results
```

## 6. Implementation Details

### Task 1 — Gaussian Noise and Averaging Filters

The program adds zero-mean Gaussian noise to the clean image at two noise levels:

- **σ = 10:** lower noise level.
- **σ = 25:** higher noise level.

The noisy images are processed using normalized averaging kernels of three sizes:

- **3×3:** smaller neighbourhood; generally preserves more detail while reducing noise.
- **5×5:** provides stronger smoothing.
- **9×9:** provides stronger smoothing but may blur edges and fine details.

The averaging filter is implemented by applying the program's own `correlate2d()` function to the image and averaging kernel.

### Task 2 — Motion Blur and Laplacian Sharpening

A horizontal motion-blur kernel of length 9 is created. Its centre row contains nine equal values, normalized so that the kernel sums to 1.

The motion-blurred image is sharpened using two Laplacian masks.

**4-neighbour Laplacian:**

```text
 0  -1   0
-1   4  -1
 0  -1   0
```

**8-neighbour Laplacian:**

```text
-1  -1  -1
-1   8  -1
-1  -1  -1
```

The Laplacian response is added to the motion-blurred image, and the result is clipped to the valid grayscale range of 0–255.

### Task 3 — Unsharp Masking / High-Boost Filtering

The program applies a 3×3 averaging filter to the noisy image with σ = 10 to obtain a blurred image.

It then calculates the high-frequency mask:

```text
Mask = Original Image - Blurred Image
```

The high-boost output is calculated as:

```text
Output = Original Image + k × Mask
```

The boost factors used are **1, 1.5, 2, and 3**. Increasing `k` increases the contribution of high-frequency details. A high boost factor can also amplify noise and produce clipping.

### Task 4 — Image Quality Evaluation

Two measurements are calculated for the processed images.

#### Peak Signal-to-Noise Ratio (PSNR)

PSNR measures the difference between a processed image and the clean reference image. It is calculated from the mean squared error (MSE):

\[
MSE = \frac{1}{MN}\sum_{i=1}^{M}\sum_{j=1}^{N}
[I(i,j)-K(i,j)]^2
\]

\[
PSNR = 10\log_{10}\left(\frac{MAX^2}{MSE}\right)
\]

For an 8-bit grayscale image, `MAX = 255`. A higher PSNR generally indicates that the processed image is closer to the clean reference image. If the images are identical, PSNR is infinite.

#### Sharpness — Variance of the Laplacian

The program applies the 4-neighbour Laplacian operator and calculates the variance of its response:

\[
Sharpness = Var(Laplacian(I))
\]

A larger value generally indicates more high-frequency content and stronger edges. However, noise can also increase this value, so sharpness should be interpreted together with PSNR and visual inspection.

## 7. Output Files

The program saves the following results in the current working directory.

### Comparison figures

| Output file | Description |
|---|---|
| `Task_1_Averaging_Grid.png` | Noisy images and their 3×3, 5×5, and 9×9 averaging-filter outputs for both noise levels |
| `Task_2_Laplacian_Grid.png` | Motion-blurred image, Laplacian responses, and sharpened outputs |
| `Task_3_High_Boost_Grid.png` | Noisy input and high-boost outputs for all four `k` values |
| `Task_3_Sharpness_vs_K.png` | Graph of high-boost factor against variance-of-Laplacian sharpness |

### Individual processed images

| Output file | Description |
|---|---|
| `clean_ground_truth.png` | Original generated grayscale scene |
| `noisy_sigma_10.png` | Image with Gaussian noise, σ = 10 |
| `noisy_sigma_25.png` | Image with Gaussian noise, σ = 25 |
| `motion_blurred.png` | Image with 9-pixel horizontal motion blur |
| `average_sigma_10_3x3.png` | σ = 10 image processed with 3×3 averaging |
| `average_sigma_10_5x5.png` | σ = 10 image processed with 5×5 averaging |
| `average_sigma_10_9x9.png` | σ = 10 image processed with 9×9 averaging |
| `average_sigma_25_3x3.png` | σ = 25 image processed with 3×3 averaging |
| `average_sigma_25_5x5.png` | σ = 25 image processed with 5×5 averaging |
| `average_sigma_25_9x9.png` | σ = 25 image processed with 9×9 averaging |
| `laplacian_4_sharpened.png` | Sharpened image using the 4-neighbour Laplacian |
| `laplacian_8_sharpened.png` | Sharpened image using the 8-neighbour Laplacian |
| `high_boost_k_1.png` | High-boost output for k = 1 |
| `high_boost_k_1_5.png` | High-boost output for k = 1.5 |
| `high_boost_k_2.png` | High-boost output for k = 2 |
| `high_boost_k_3.png` | High-boost output for k = 3 |

The program also prints PSNR and sharpness values for the averaging, Laplacian, and high-boost results in the console.

## 8. Important Implementation Notes

- The synthetic scene is generated at **640 × 420 pixels**.
- A fixed random seed (`np.random.seed(42)`) is used so the generated Gaussian noise is repeatable between runs.
- The custom `correlate2d()` function uses edge padding and nested loops to calculate the correlation at each pixel.
- The code intentionally does not use `cv2.filter2D()` or `scipy.signal` for filtering.
- Images are clipped to the 0–255 range before being saved as 8-bit PNG files.
- The PSNR reference is the clean generated image.
- The sharpness metric is an indicator of high-frequency content; it is not, by itself, a measure of image quality.

## 9. Conclusion

This lab demonstrates how spatial filtering can be used to reduce noise and improve image details in an AGV camera scene. Averaging filters reduce Gaussian noise, although larger kernels can remove fine details. Laplacian filtering enhances edges in a motion-blurred image, while unsharp masking and high-boost filtering increase high-frequency detail. PSNR and variance of the Laplacian provide numerical measures that complement visual comparison when evaluating the processed images.

---

**Lab:** PCC-03 — Digital Image and Video Processing  
**Experiment:** Spatial Filtering for an AGV Camera Image

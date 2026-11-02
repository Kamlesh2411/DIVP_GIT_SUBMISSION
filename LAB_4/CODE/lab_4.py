# ============================================================
# PCC-03: DIGITAL IMAGE AND VIDEO PROCESSING
# LAB: SPATIAL FILTERING FOR AN AGV CAMERA IMAGE
#
# This program is self-contained:
# 1. It creates a simple AGV/road grayscale test image.
# 2. Adds Gaussian noise: sigma = 10 and 25.
# 3. Creates 9-pixel motion blur.
# 4. Implements 2D correlation from scratch.
# 5. Applies 3x3, 5x5 and 9x9 averaging filters.
# 6. Applies 4-neighbor and 8-neighbor Laplacian sharpening.
# 7. Applies unsharp/high-boost filtering for k=1,1.5,2,3.
# 8. Calculates PSNR and variance-of-Laplacian sharpness.
# 9. Displays and saves the results.
#
# No cv2.filter2D() or scipy.signal filtering shortcut is used.
# ============================================================

import numpy as np
import cv2
import matplotlib.pyplot as plt


# ============================================================
# 1. CREATE A SELF-CONTAINED AGV/ROAD TEST IMAGE
# ============================================================

def create_agv_scene(width=640, height=420):
    """Create a simple grayscale outdoor road scene."""

    # Create a gray image representing the distant scene.
    scene = np.full((height, width), 120, dtype=np.uint8)

    # Create a drawing object.
    draw = cv2.cvtColor(scene, cv2.COLOR_GRAY2BGR)

    # Draw a brighter sky.
    cv2.rectangle(draw, (0, 0), (width, 210), (155, 155, 155), -1)

    # Draw roadside vegetation as circles.
    for x in range(0, width, 45):
        h = 45 + ((x * 17) % 55)
        cv2.circle(draw, (x, 205 - h // 2), 25, (65, 65, 65), -1)

    # Draw the road as a polygon.
    road = np.array(
        [[210, 210], [430, 210], [620, 420], [20, 420]],
        dtype=np.int32
    )
    cv2.fillPoly(draw, [road], (105, 105, 105))

    # Draw the left road boundary.
    cv2.line(draw, (210, 210), (20, 420), (220, 220, 220), 4)

    # Draw the right road boundary.
    cv2.line(draw, (430, 210), (620, 420), (220, 220, 220), 4)

    # Draw lane markings.
    for y, x1, x2 in [(245, 310, 330), (290, 295, 345), (345, 270, 370)]:
        cv2.line(draw, (x1, y), (x2, y), (235, 235, 235), 5)

    # Draw an obstacle on the left.
    cv2.rectangle(draw, (105, 230), (155, 285), (45, 45, 45), -1)
    cv2.rectangle(draw, (112, 220), (148, 238), (55, 55, 55), -1)

    # Draw an obstacle on the right.
    cv2.rectangle(draw, (480, 225), (530, 285), (50, 50, 50), -1)
    cv2.rectangle(draw, (487, 215), (523, 235), (60, 60, 60), -1)

    # Draw a central obstacle.
    cv2.rectangle(draw, (295, 245), (335, 280), (35, 35, 35), -1)

    # Convert the BGR drawing back to grayscale.
    gray_scene = cv2.cvtColor(draw, cv2.COLOR_BGR2GRAY)

    # Return the generated ground-truth image.
    return gray_scene


# Generate the clean AGV scene.
clean = create_agv_scene().astype(np.float64)


# ============================================================
# 2. ADD GAUSSIAN NOISE
# ============================================================

def add_gaussian_noise(image, sigma):
    """Add zero-mean Gaussian noise to the image."""

    # Generate random Gaussian noise.
    noise = np.random.normal(
        0,
        sigma,
        image.shape
    )

    # Add the noise to the clean image.
    noisy = image + noise

    # Limit pixel values to 0-255.
    noisy = np.clip(noisy, 0, 255)

    # Return the noisy image.
    return noisy


# Make results repeatable between program runs.
np.random.seed(42)

# Create sigma=10 noisy image.
noisy_10 = add_gaussian_noise(clean, 10)

# Create sigma=25 noisy image.
noisy_25 = add_gaussian_noise(clean, 25)


# ============================================================
# 3. CREATE MOTION-BLUR KERNEL
# ============================================================

def motion_blur_kernel(length=9):
    """Create a horizontal linear motion-blur kernel."""

    # Create an all-zero kernel.
    kernel = np.zeros((length, length), dtype=np.float64)

    # Find the middle row.
    center = length // 2

    # Put ones across the middle row.
    kernel[center, :] = 1.0

    # Normalize the kernel so its sum is 1.
    kernel = kernel / np.sum(kernel)

    # Return the kernel.
    return kernel


# Create a 9-pixel motion-blur kernel.
motion_kernel = motion_blur_kernel(9)


# ============================================================
# 4. FROM-SCRATCH 2D CORRELATION
# ============================================================

def correlate2d(image, kernel):
    """Perform 2D correlation without cv2.filter2D()."""

    # Get image height and width.
    image_height, image_width = image.shape

    # Get kernel height and width.
    kernel_height, kernel_width = kernel.shape

    # Calculate required padding.
    pad_h = kernel_height // 2
    pad_w = kernel_width // 2

    # Pad the image using edge pixels.
    padded = np.pad(
        image,
        ((pad_h, pad_h), (pad_w, pad_w)),
        mode="edge"
    )

    # Create an empty output image.
    output = np.zeros_like(image, dtype=np.float64)

    # Visit every image row.
    for i in range(image_height):

        # Visit every image column.
        for j in range(image_width):

            # Extract the local neighborhood.
            region = padded[
                i:i + kernel_height,
                j:j + kernel_width
            ]

            # Multiply the neighborhood and kernel.
            product = region * kernel

            # Sum the products to obtain one output pixel.
            output[i, j] = np.sum(product)

    # Return the correlated image.
    return output


# Apply our own correlation to create motion blur.
motion_blurred = correlate2d(clean, motion_kernel)

# Limit values to the valid image range.
motion_blurred = np.clip(motion_blurred, 0, 255)


# ============================================================
# 5. AVERAGING FILTER
# ============================================================

def averaging_kernel(size):
    """Create a normalized box/averaging kernel."""

    # Create a matrix containing ones.
    kernel = np.ones((size, size), dtype=np.float64)

    # Divide every element by the total number of elements.
    kernel = kernel / (size * size)

    # Return the normalized kernel.
    return kernel


def averaging_filter(image, size):
    """Apply an averaging filter using our own correlation."""

    # Create the averaging kernel.
    kernel = averaging_kernel(size)

    # Apply correlation.
    result = correlate2d(image, kernel)

    # Limit pixel values.
    return np.clip(result, 0, 255)


# Required kernel sizes from the lab.
kernel_sizes = [3, 5, 9]

# Store all averaging outputs.
averaged_results = {}

# Process both noise levels.
for sigma, noisy_image in [(10, noisy_10), (25, noisy_25)]:

    # Create a dictionary for this noise level.
    averaged_results[sigma] = {}

    # Process all three kernel sizes.
    for size in kernel_sizes:

        # Apply averaging.
        averaged_results[sigma][size] = averaging_filter(
            noisy_image,
            size
        )


# ============================================================
# 6. LAPLACIAN FILTERS
# ============================================================

# Four-neighbor Laplacian.
laplacian_4 = np.array([
    [0, -1, 0],
    [-1, 4, -1],
    [0, -1, 0]
], dtype=np.float64)

# Eight-neighbor Laplacian.
laplacian_8 = np.array([
    [-1, -1, -1],
    [-1, 8, -1],
    [-1, -1, -1]
], dtype=np.float64)


def laplacian_sharpen(image, kernel):
    """Sharpen an image using a Laplacian kernel."""

    # Calculate the Laplacian response.
    response = correlate2d(image, kernel)

    # Add the edge response to the original image.
    sharpened = image + response

    # Limit the result to 0-255.
    sharpened = np.clip(sharpened, 0, 255)

    # Return both images.
    return sharpened, response


# Sharpen the motion-blurred image using 4-neighbor Laplacian.
sharp_4, response_4 = laplacian_sharpen(
    motion_blurred,
    laplacian_4
)

# Sharpen using 8-neighbor Laplacian.
sharp_8, response_8 = laplacian_sharpen(
    motion_blurred,
    laplacian_8
)


# ============================================================
# 7. UNSHARP MASKING / HIGH-BOOST FILTERING
# ============================================================

def high_boost_filter(image, k):
    """Apply unsharp masking/high-boost filtering."""

    # Create a 3x3 averaging kernel.
    blur_kernel = averaging_kernel(3)

    # Blur the image.
    blurred = correlate2d(image, blur_kernel)

    # Extract high-frequency detail.
    mask = image - blurred

    # Add k times the detail back to the image.
    output = image + k * mask

    # Keep values in the valid range.
    output = np.clip(output, 0, 255)

    # Return the result.
    return output


# Required boost factors.
boost_values = [1, 1.5, 2, 3]

# Store high-boost results.
boost_results = {}

# Apply each boost factor to sigma=10 image.
for k in boost_values:
    boost_results[k] = high_boost_filter(noisy_10, k)


# ============================================================
# 8. PSNR METRIC
# ============================================================

def calculate_psnr(original, processed):
    """Calculate Peak Signal-to-Noise Ratio."""

    # Calculate mean squared error.
    mse = np.mean((original - processed) ** 2)

    # Identical images have infinite PSNR.
    if mse == 0:
        return float("inf")

    # Maximum grayscale pixel value.
    max_pixel = 255.0

    # Calculate PSNR.
    psnr = 10 * np.log10(
        (max_pixel ** 2) / mse
    )

    # Return PSNR.
    return psnr


# ============================================================
# 9. SHARPNESS METRIC
# ============================================================

def sharpness_metric(image):
    """Use variance of the 4-neighbor Laplacian as sharpness."""

    # Calculate the Laplacian response.
    lap = correlate2d(image, laplacian_4)

    # Calculate its variance.
    value = np.var(lap)

    # Return the sharpness value.
    return value


# ============================================================
# 10. PRINT TASK 4 RESULTS
# ============================================================

print("\n============================================================")
print("TASK 4: AVERAGING FILTER RESULTS")
print("============================================================")

print(
    f"{'Noise':<10}"
    f"{'Kernel':<10}"
    f"{'PSNR(dB)':<15}"
    f"{'Sharpness':<15}"
)

print("-" * 50)

# Evaluate all averaging configurations.
for sigma in [10, 25]:

    # Test each kernel.
    for size in kernel_sizes:

        # Get the processed image.
        result = averaged_results[sigma][size]

        # Calculate PSNR.
        psnr = calculate_psnr(clean, result)

        # Calculate sharpness.
        sharpness = sharpness_metric(result)

        # Print the values.
        print(
            f"{sigma:<10}"
            f"{size}x{size:<10}"
            f"{psnr:<15.2f}"
            f"{sharpness:<15.2f}"
        )


print("\n============================================================")
print("LAPLACIAN RESULTS")
print("============================================================")

# Calculate 4-neighbor metrics.
psnr_4 = calculate_psnr(clean, sharp_4)
sharpness_4 = sharpness_metric(sharp_4)

# Calculate 8-neighbor metrics.
psnr_8 = calculate_psnr(clean, sharp_8)
sharpness_8 = sharpness_metric(sharp_8)

# Print 4-neighbor results.
print("4-Neighbour:")
print("PSNR      =", round(psnr_4, 2), "dB")
print("Sharpness =", round(sharpness_4, 2))

# Print 8-neighbor results.
print("\n8-Neighbour:")
print("PSNR      =", round(psnr_8, 2), "dB")
print("Sharpness =", round(sharpness_8, 2))


print("\n============================================================")
print("HIGH-BOOST RESULTS")
print("============================================================")

print(
    f"{'k':<10}"
    f"{'PSNR(dB)':<15}"
    f"{'Sharpness':<15}"
)

print("-" * 40)

# Store sharpness values for the graph.
k_sharpness = []

# Evaluate every k value.
for k in boost_values:

    # Get high-boost result.
    result = boost_results[k]

    # Calculate PSNR.
    psnr = calculate_psnr(clean, result)

    # Calculate sharpness.
    sharpness = sharpness_metric(result)

    # Save sharpness for plotting.
    k_sharpness.append(sharpness)

    # Print metrics.
    print(
        f"{k:<10}"
        f"{psnr:<15.2f}"
        f"{sharpness:<15.2f}"
    )


# ============================================================
# 11. DISPLAY TASK 1
# ============================================================

fig, axes = plt.subplots(2, 4, figsize=(16, 8))

# Sigma 10 noisy image.
axes[0, 0].imshow(noisy_10, cmap="gray")
axes[0, 0].set_title("Sigma = 10")

# Sigma 10 filtered images.
axes[0, 1].imshow(averaged_results[10][3], cmap="gray")
axes[0, 1].set_title("3x3 Average")

axes[0, 2].imshow(averaged_results[10][5], cmap="gray")
axes[0, 2].set_title("5x5 Average")

axes[0, 3].imshow(averaged_results[10][9], cmap="gray")
axes[0, 3].set_title("9x9 Average")

# Sigma 25 noisy image.
axes[1, 0].imshow(noisy_25, cmap="gray")
axes[1, 0].set_title("Sigma = 25")

# Sigma 25 filtered images.
axes[1, 1].imshow(averaged_results[25][3], cmap="gray")
axes[1, 1].set_title("3x3 Average")

axes[1, 2].imshow(averaged_results[25][5], cmap="gray")
axes[1, 2].set_title("5x5 Average")

axes[1, 3].imshow(averaged_results[25][9], cmap="gray")
axes[1, 3].set_title("9x9 Average")

# Remove axes.
for ax in axes.ravel():
    ax.axis("off")

# Adjust layout.
plt.tight_layout()

# Save Task 1 figure.
plt.savefig("Task_1_Averaging_Grid.png", dpi=200)

# Display the figure.
plt.show()


# ============================================================
# 12. DISPLAY TASK 2
# ============================================================

plt.figure(figsize=(15, 8))

# Show motion blur.
plt.subplot(2, 3, 1)
plt.imshow(motion_blurred, cmap="gray")
plt.title("Motion Blurred")
plt.axis("off")

# Show 4-neighbor response.
plt.subplot(2, 3, 2)
plt.imshow(response_4, cmap="gray")
plt.title("4-Neighbour Laplacian")
plt.axis("off")

# Show 4-neighbor sharpened image.
plt.subplot(2, 3, 3)
plt.imshow(sharp_4, cmap="gray")
plt.title("4-Neighbour Sharpened")
plt.axis("off")

# Show 8-neighbor response.
plt.subplot(2, 3, 5)
plt.imshow(response_8, cmap="gray")
plt.title("8-Neighbour Laplacian")
plt.axis("off")

# Show 8-neighbor sharpened image.
plt.subplot(2, 3, 6)
plt.imshow(sharp_8, cmap="gray")
plt.title("8-Neighbour Sharpened")
plt.axis("off")

# Adjust layout.
plt.tight_layout()

# Save Task 2 figure.
plt.savefig("Task_2_Laplacian_Grid.png", dpi=200)

# Display figure.
plt.show()


# ============================================================
# 13. DISPLAY TASK 3
# ============================================================

plt.figure(figsize=(15, 8))

# Show noisy input.
plt.subplot(2, 3, 1)
plt.imshow(noisy_10, cmap="gray")
plt.title("Noisy Image Sigma=10")
plt.axis("off")

# Show all high-boost results.
for index, k in enumerate(boost_values):

    # Calculate subplot location.
    position = index + 2

    # Select subplot.
    plt.subplot(2, 3, position)

    # Display result.
    plt.imshow(boost_results[k], cmap="gray")

    # Display k.
    plt.title(f"High-Boost k={k}")

    # Remove axes.
    plt.axis("off")

# Adjust layout.
plt.tight_layout()

# Save Task 3 figure.
plt.savefig("Task_3_High_Boost_Grid.png", dpi=200)

# Display figure.
plt.show()


# ============================================================
# 14. SHARPNESS VS K GRAPH
# ============================================================

plt.figure(figsize=(8, 5))

# Plot boost factor against sharpness.
plt.plot(
    boost_values,
    k_sharpness,
    marker="o"
)

# Label the x-axis.
plt.xlabel("Boost Factor k")

# Label the y-axis.
plt.ylabel("Variance of Laplacian")

# Add title.
plt.title("Sharpness vs High-Boost Factor")

# Add grid.
plt.grid(True)

# Save graph.
plt.savefig("Task_3_Sharpness_vs_K.png", dpi=200)

# Display graph.
plt.show()


# ============================================================
# 15. SAVE INDIVIDUAL IMAGES
# ============================================================

def save_image(filename, image):
    """Save a floating-point image as an 8-bit PNG."""

    # Convert image to valid 8-bit range.
    output = np.clip(image, 0, 255).astype(np.uint8)

    # Save the image.
    cv2.imwrite(filename, output)


# Save clean image.
save_image("clean_ground_truth.png", clean)

# Save noisy images.
save_image("noisy_sigma_10.png", noisy_10)
save_image("noisy_sigma_25.png", noisy_25)

# Save motion-blurred image.
save_image("motion_blurred.png", motion_blurred)

# Save averaging outputs.
for sigma in [10, 25]:
    for size in kernel_sizes:
        save_image(
            f"average_sigma_{sigma}_{size}x{size}.png",
            averaged_results[sigma][size]
        )

# Save Laplacian outputs.
save_image("laplacian_4_sharpened.png", sharp_4)
save_image("laplacian_8_sharpened.png", sharp_8)

# Save high-boost outputs.
for k in boost_values:

    # Replace decimal point in filename.
    k_name = str(k).replace(".", "_")

    # Save image.
    save_image(
        f"high_boost_k_{k_name}.png",
        boost_results[k]
    )


# ============================================================
# PROGRAM COMPLETE
# ============================================================

print("\n============================================================")
print("PROGRAM COMPLETED SUCCESSFULLY")
print("============================================================")
print("All Task 1-3 figures and processed images have been saved.")
print("Use the printed PSNR and sharpness values for Task 4.")
print("Use those numbers to justify the final AGV pipeline.")

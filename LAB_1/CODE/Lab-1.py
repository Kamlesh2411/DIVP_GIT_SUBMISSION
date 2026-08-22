import cv2
import numpy as np

# Load image
image = cv2.imread("DATASET/LAB_1/Image_for_Practice.jpg")

if image is None:
    print("Image not found!")
    exit()

current_image = image.copy()

while True:

    print("\n========= IMAGE PROCESSING LAB =========")
    print("1. Display Image")
    print("2. Display Image Properties")
    print("3. Convert to Grayscale")
    print("4. Increase Brightness")
    print("5. Increase Contrast")
    print("6. Resize Image")
    print("7. Rotate Image")
    print("8. Flip Image")
    print("9. Crop Image")
    print("10. Negative Image")
    print("11. Save Image")
    print("0. Exit")

    print("\nEnter your choice: ", end="")
    choice = int(input())

    if choice == 1:
        cv2.imshow("Image", current_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif choice == 2:
        print("\nImage Properties")
        print("------------------------")
        print("Height :", current_image.shape[0])
        print("Width :", current_image.shape[1])
        print("Channels :", current_image.shape[2])
        print("Size :", current_image.size)
        print("Data Type :", current_image.dtype)

    elif choice == 3:
        gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Grayscale", gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif choice == 4:
        value = int(input("Enter Brightness Value (0-100): "))
        bright = cv2.convertScaleAbs(current_image, alpha=1, beta=value)
        cv2.imshow("Brightness Increased", bright)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif choice == 5:
        alpha = float(input("Enter Contrast Value (1.0 - 3.0): "))
        contrast = cv2.convertScaleAbs(current_image, alpha=alpha, beta=0)
        cv2.imshow("Contrast Increased", contrast)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif choice == 6:
        width = int(input("Enter New Width: "))
        height = int(input("Enter New Height: "))
        resized = cv2.resize(current_image, (width, height))
        cv2.imshow("Resized Image", resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif choice == 7:
        angle = float(input("Enter Rotation Angle: "))
        h, w = current_image.shape[:2]
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(current_image, matrix, (w, h))
        cv2.imshow("Rotated Image", rotated)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif choice == 8:
        print("\n1. Horizontal Flip")
        print("2. Vertical Flip")
        print("3. Both")

        flip_choice = int(input("Enter Choice: "))

        if flip_choice == 1:
            flipped = cv2.flip(current_image, 1)
        elif flip_choice == 2:
            flipped = cv2.flip(current_image, 0)
        else:
            flipped = cv2.flip(current_image, -1)

        cv2.imshow("Flipped Image", flipped)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif choice == 9:
        x = int(input("Enter x: "))
        y = int(input("Enter y: "))
        w = int(input("Enter width: "))
        h = int(input("Enter height: "))

        crop = current_image[y:y+h, x:x+w]

        cv2.imshow("Cropped Image", crop)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif choice == 10:
        negative = 255 - current_image
        cv2.imshow("Negative Image", negative)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif choice == 11:
        filename = input("Enter File Name (Example: output.jpg): ")
        cv2.imwrite(filename, current_image)
        print("Image Saved Successfully.")

    elif choice == 0:
        print("Program Ended.")
        break

    else:
        print("Invalid Choice")

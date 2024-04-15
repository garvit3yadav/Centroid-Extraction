import cv2

def remove_gaussian_noise(image_path, kernel_size=(5, 5)):
    # Load the image
    img = cv2.imread(image_path)

    # Apply Gaussian blur to the grayscale image
    blurred = cv2.GaussianBlur(img, kernel_size, 0)

    # Subtract the blurred image from the original
    denoised = cv2.absdiff(img, blurred)

    return denoised

# Path to the image file
image_path = "images/noisy_image.jpg"

# Remove Gaussian noise
denoised_image = remove_gaussian_noise(image_path)

# Display the original and denoised images
cv2.imshow("Original Image", cv2.imread(image_path))
cv2.imshow("Denoised Image", denoised_image)
cv2.imwrite("img_denoised.jpg", denoised_image )
cv2.waitKey(0)
cv2.destroyAllWindows()
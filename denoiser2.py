import cv2

# Load the noisy image
noisy_image = cv2.imread('images/noisy_image.jpg')

# Apply Gaussian blur
blurred_image = cv2.GaussianBlur(noisy_image, (5, 5), 0)

# Apply Median filter
median_filtered_image = cv2.medianBlur(noisy_image, 5)

# Apply Non-Local Means Denoising
denoised_image = cv2.fastNlMeansDenoisingColored(noisy_image, None, 10, 10, 7, 21)

# Apply Bilateral Filter
bilateral_filtered_image = cv2.bilateralFilter(noisy_image, 9, 75, 75)

# Subtract the blurred image from the original
subtracted_image = cv2.absdiff(noisy_image, blurred_image)

# Display or save the denoised images as needed
cv2.imshow("Original Image", noisy_image)
cv2.imshow("Denoised Image", subtracted_image)
cv2.imwrite("img_denoised2.jpg", subtracted_image )
cv2.waitKey(0)
cv2.destroyAllWindows()

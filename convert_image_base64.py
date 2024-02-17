import base64

# Open the image file in binary mode
with open('image-test.jpg', 'rb') as image_file:
    # Read the content of the image file
    image_data = image_file.read()

# Encode the binary data into a Base64 string
base64_image = base64.b64encode(image_data).decode('utf-8')

# Save the Base64 string to a text file
with open('base64_image.txt', 'w') as text_file:
    text_file.write(base64_image)

print(base64_image)

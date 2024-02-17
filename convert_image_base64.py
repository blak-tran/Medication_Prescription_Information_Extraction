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

# print(base64_image)
# import subprocess

# # Run the pip freeze command and capture the output
# pip_freeze_output = subprocess.check_output(['pip', 'freeze']).decode('utf-8')

# # Write the output to a requirements.txt file
# with open('requirements1.txt', 'w') as requirements_file:
#     requirements_file.write(pip_freeze_output)

# print("requirements1.txt file has been generated.")

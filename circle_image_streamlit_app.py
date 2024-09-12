import streamlit as st
from PIL import Image, ImageDraw
import io
import zipfile

def create_circular_image(img):
    img = img.convert("RGBA")
    size = min(img.size)
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    img = img.resize((size, size), Image.LANCZOS)
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    output.paste(img, (0, 0), mask)
    return output

st.title('Circular Image Converter')

uploaded_files = st.file_uploader("Choose image files", accept_multiple_files=True, type=['png', 'jpg', 'jpeg', 'gif', 'bmp'])

if uploaded_files:
    processed_images = []
    
    for uploaded_file in uploaded_files:
        img = Image.open(uploaded_file)
        circular_img = create_circular_image(img)
        processed_images.append((uploaded_file.name, circular_img))
    
    # Create a zip file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for name, img in processed_images:
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            zip_file.writestr(f"circular_{name.split('.')[0]}.png", img_buffer.getvalue())
    
    # Offer the zip file for download
    st.download_button(
        label="Download processed images",
        data=zip_buffer.getvalue(),
        file_name="circular_images.zip",
        mime="application/zip"
    )
    
    # Display processed images
    st.write("Processed Images:")
    for name, img in processed_images:
        st.image(img, caption=f"Circular version of {name}", use_column_width=True)
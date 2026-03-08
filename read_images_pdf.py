import fitz  # PyMuPDF
import PIL.Image
import io

# read the PDF file :
PDF_FILE = fitz.open("Présentations mark zuckerberg.pdf")

for i in range(len(PDF_FILE)) :
    page = PDF_FILE[i]
    images = page.get_images()
    for i in range(len(images)) :
        base_img = PDF_FILE.extract_image(images[i][0])  # type dict
        img_data = base_img["image"]
        ext = base_img["ext"]
        img = PIL.Image.open(io.BytesIO(img_data))
        img.save(open(f"image{i}.{ext}" , "wb"))
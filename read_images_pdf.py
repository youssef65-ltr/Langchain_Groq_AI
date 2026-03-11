import fitz  # PyMuPDF
import PIL.Image
import io

# read the PDF file :
try :
    PDF_FILE = fitz.open("Présentations mark zuckerberg.pdf")
except : 
    print("error in PDF")

def get_text_from_pdf() :
    full_content = ""
    if PDF_FILE is None :
        print("pdf is empty")
        return None
    for i in range(len(PDF_FILE)) :
        text = PDF_FILE[1].get_text()
        full_content += f"\n{text}"
    return full_content


def get_images_from_pdf() :
    for i in range(len(PDF_FILE)) :
        page = PDF_FILE[i]
        images = page.get_images()
        for i in range(len(images)) :
            base_img = PDF_FILE.extract_image(images[i][0])  # type dict
            img_data = base_img["image"]
            ext = base_img["ext"]
            img = PIL.Image.open(io.BytesIO(img_data))
            img.save(open(f"image{i}.{ext}" , "wb"))
import pypdf

read_pdf = pypdf.PdfReader("LATRECHE_YOUSSEF_MOTIVATION.pdf")

# number of pages :
# print(len(read_pdf.pages))

# read context of a specific page :
print(read_pdf.pages[0].extract_text())


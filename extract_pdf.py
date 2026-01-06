from pypdf import PdfReader
import sys

path = r"f:\\2022BCD0028\\final\\Research Scientist Internship_ Take-Home Assignment.pdf"
if len(sys.argv) > 1:
    path = sys.argv[1]

reader = PdfReader(path)
text = []
for page in reader.pages:
    text.append(page.extract_text() or '')

print('\n\n'.join(text))

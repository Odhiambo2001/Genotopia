from googlesearch import search
import PyPDF2

def google_search(query, num_results=5):
    results = search(query, num_results=num_results)
    return results

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text
# Example 1: Google Search
query = "George Mason NLP group"
google_results = google_search(query)
print("Google Search Results:")
for result in google_results:
    print(result)

# Example 2: PDF Reading
pdf_file_path = "example_paper.pdf"
pdf_text = read_pdf(pdf_file_path)
print("PDF Text:")
print(pdf_text)

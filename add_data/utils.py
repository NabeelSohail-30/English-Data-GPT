import os
from docx import Document
import re


def save_uploaded_file(file):
    """Saves the uploaded file to the 'uploads' directory."""
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    file_path = os.path.join('uploads', file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file_path


def extract_headings_and_chunks(doc_path):
    """Extracts headings and chunks from the .docx file, cleans them, and returns the chunks."""

    doc = Document(doc_path)
    chunks = []
    current_heading = None
    current_chunk = []

    heading_font_sizes = {
        'Heading 1': 'Heading 1',
        'Heading 2': 'Heading 2',
        'Heading 3': 'Heading 3',
    }

    for para in doc.paragraphs:
        if is_heading(para, heading_font_sizes):
            if current_heading:
                chunks.append(
                    (current_heading, '\n'.join(current_chunk).strip()))
            current_heading = para.text
            current_chunk = []
        else:
            current_chunk.append(para.text)

    if current_heading:
        chunks.append((current_heading, '\n'.join(current_chunk).strip()))

    return chunks


def is_heading(para, heading_font_sizes):
    """Check if the paragraph is a heading based on its style name or font size."""
    style = para.style.name
    return style in heading_font_sizes


def get_font_size(paragraph):
    """Extract the font size from the paragraph."""
    if paragraph.runs:
        font_size = paragraph.runs[0].font.size
        if font_size:
            return font_size.pt
    return None


def remove_references(text):
    """Removes numbers surrounded by parentheses from the text."""
    return re.sub(r'\(\d+\)', '', text)

"""Multi-format document parser supporting PDF, DOCX, MD, and TXT files."""

import os
from typing import List, Tuple


class DocumentParser:
    SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".md", ".txt"}

    def parse_file(self, filepath: str) -> str:
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        ext = os.path.splitext(filepath)[1].lower()
        if ext not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {ext}. "
                f"Supported types: {', '.join(sorted(self.SUPPORTED_EXTENSIONS))}"
            )

        if ext in (".md", ".txt"):
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                return f.read()

        if ext == ".pdf":
            return self._parse_pdf(filepath)

        if ext == ".docx":
            return self._parse_docx(filepath)

        return ""

    def parse_directory(self, dirpath: str) -> List[Tuple[str, str]]:
        if not os.path.isdir(dirpath):
            raise NotADirectoryError(f"Not a directory: {dirpath}")

        results: List[Tuple[str, str]] = []
        for root, _dirs, files in os.walk(dirpath):
            for filename in files:
                ext = os.path.splitext(filename)[1].lower()
                if ext not in self.SUPPORTED_EXTENSIONS:
                    continue
                filepath = os.path.join(root, filename)
                try:
                    text = self.parse_file(filepath)
                    if text.strip():
                        results.append((filename, text))
                except Exception as e:
                    results.append((filename, f"[ERROR: {e}]"))
        return results

    def _parse_pdf(self, filepath: str) -> str:
        text = self._try_parse_pdf_with_pdfplumber(filepath)
        if text:
            return text
        return self._try_parse_pdf_with_pypdf2(filepath)

    def _try_parse_pdf_with_pdfplumber(self, filepath: str) -> str:
        try:
            import pdfplumber
        except ImportError:
            return ""

        parts = []
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        parts.append(page_text)
        except Exception as e:
            raise RuntimeError(f"pdfplumber failed to parse {filepath}: {e}") from e
        return "\n\n".join(parts)

    def _try_parse_pdf_with_pypdf2(self, filepath: str) -> str:
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            raise ImportError(
                "No PDF parser available. Install pdfplumber or PyPDF2: "
                "pip install pdfplumber PyPDF2"
            )

        parts = []
        try:
            reader = PdfReader(filepath)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    parts.append(page_text)
        except Exception as e:
            raise RuntimeError(f"PyPDF2 failed to parse {filepath}: {e}") from e
        return "\n\n".join(parts)

    def _parse_docx(self, filepath: str) -> str:
        try:
            from docx import Document
        except ImportError:
            raise ImportError(
                "python-docx is not installed. Install it: pip install python-docx"
            )

        try:
            doc = Document(filepath)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n\n".join(paragraphs)
        except Exception as e:
            raise RuntimeError(f"Failed to parse docx file {filepath}: {e}") from e

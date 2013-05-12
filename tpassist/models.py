"""
models.py

contains the data models for the tpassist project. but for an other version.
"""

import markdown as md
import os
import subprocess
from jinja2 import Template

class Document:
    def __init__(self, name=None):
        self.name = name
        self.markdown = None
        if(self.name is not None and os.path.exists(self.name + ".md")):
            with open(self.name + ".md", 'r') as f:
                self.markdown = f.read()
        with open("markdown.html", 'r') as f:
            self.template = Template(f.read())

    def save(self):
        with open(self.name + ".md", 'w') as f:
            f.write(self.markdown)

    def save_to_html(self):
        with open(self.name + ".html", 'w') as f:
            f.write(self._gen_html())
            return f.name

    def _gen_html(self):
        html = md.markdown(self.markdown, ['codehilite', 'extra', 'nl2br', 'toc'])
        return self.template.render(html=html)

    def save_to_pdf(self):
        subprocess.call(["wkhtmltopdf", self.save_to_html(), self.name + ".pdf"])
        return self.name + ".pdf"

    def get_pdf_file_descriptor(self):
        fname = self.save_to_pdf()
        if(os.path.exists(fname)):
            return open(fname, 'r')

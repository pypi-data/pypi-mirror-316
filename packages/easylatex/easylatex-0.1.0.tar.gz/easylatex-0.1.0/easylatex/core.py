class EasyLatexDocument:
    """
    Class to represent a LaTeX document and provide methods to generate it.
    """

    def __init__(self, documentClass="article", options=None):
        """
        Initialize a new LaTeX document.

        Args:
            documentClass (str): The LaTeX document class (default: "article").
            options (list): List of options for the document class (e.g., ["12pt", "a4paper"]).
        """
        self.documentClass = documentClass
        self.options = options or []
        self.content = []

    def addSection(self, title):
        """Add a section to the document."""
        self.content.append(f"\\section{{{title}}}")

    def addParagraph(self, text):
        """Add a paragraph to the document."""
        self.content.append(text)

    def exportToTex(self, filename="output.tex"):
        """
        Export the document to a .tex file.

        Args:
            filename (str): Name of the output file.
        """
        with open(filename, "w") as file:
            file.write(self._generateTex())

    def _generateTex(self):
        """Generate the complete LaTeX document as a string."""
        options = f"[{','.join(self.options)}]" if self.options else ""
        header = (
            f"\\documentclass{options}{{{self.documentClass}}}\n\\begin{{document}}"
        )
        footer = "\\end{document}"
        body = "\n".join(self.content)
        return f"{header}\n{body}\n{footer}"

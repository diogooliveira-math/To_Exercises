# Story 4.1 — Generator preview mode

As an author, I want a preview mode that renders a LaTeX snippet or HTML so that I can verify output before building a PDF.

Acceptance Criteria (BDD):
- Given selected exercise IDs, when preview is run, then a LaTeX snippet or HTML fragment is returned and no pdflatex invocation occurs.
- Given preview output, when author inspects it, then metadata and content are present and accurate.

Technical Notes:
- Implement generator preview flag that returns rendered LaTeX/HTML without invoking full PDF build.

Saved: docs/stories/4-1-generator-preview.md

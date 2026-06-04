import markdown
from weasyprint import HTML

with open("docs/presentazione-cliente.md", "r") as f:
    md_text = f.read()

html_body = markdown.markdown(md_text, extensions=["tables"])

html_full = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<style>
    @page {{
        size: A4;
        margin: 2.5cm;
    }}
    body {{
        font-family: Helvetica, Arial, sans-serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #1a1a1a;
    }}
    h1 {{
        color: #1a3a5c;
        font-size: 22pt;
        margin-bottom: 2px;
        border-bottom: 3px solid #e8a023;
        padding-bottom: 8px;
    }}
    h2 {{
        color: #1a3a5c;
        font-size: 14pt;
        margin-top: 24px;
        border-bottom: 1px solid #ddd;
        padding-bottom: 4px;
    }}
    h3 {{
        color: #2d5a8c;
        font-size: 12pt;
        margin-top: 16px;
    }}
    strong {{
        color: #1a3a5c;
    }}
    hr {{
        border: none;
        border-top: 1px solid #e0e0e0;
        margin: 20px 0;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0;
        font-size: 10pt;
    }}
    th {{
        background-color: #1a3a5c;
        color: white;
        text-align: left;
        padding: 8px 12px;
    }}
    td {{
        padding: 8px 12px;
        border-bottom: 1px solid #e0e0e0;
    }}
    tr:nth-child(even) td {{
        background-color: #f7f9fc;
    }}
    p {{
        margin: 6px 0;
    }}
    ul {{
        margin: 6px 0;
    }}
    li {{
        margin: 3px 0;
    }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

HTML(string=html_full).write_pdf("docs/presentazione-globalink-security.pdf")
print("PDF generato: docs/presentazione-globalink-security.pdf")

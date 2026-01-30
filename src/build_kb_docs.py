import os

RAW_DOCS = "../raw_docs"
KB_DIR = "../kb"

os.makedirs(KB_DIR, exist_ok=True)

converter = DocumentConverter()

def build_kb_from_docs():
    for fname in os.listdir(RAW_DOCS):
        if not fname.lower().endswith((".pdf", ".docx", ".html")):
            continue 

        fpath = os.path.join(RAW_DOCS, fname)
        print(f"Processing document: {fname}")

        result = converter.convert(fpath)
        text = result.document.export_to_text()

        out_name = os.path.splitext(fname)[0] + ".txt"
        out_path = os.path.join(KB_DIR, out_name)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)

    print("Document-based KB built")

if __name__ == "__main__":
    build_kb_from_docs()

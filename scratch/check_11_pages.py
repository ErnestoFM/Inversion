import pypdf

reader = pypdf.PdfReader('scratch/test_single.pdf')
print(f"Total pages: {len(reader.pages)}")

for i, page in enumerate(reader.pages):
    txt = page.extract_text().strip().split('\n')
    lines = [l.strip() for l in txt if l.strip()]
    top = " ".join(lines[:2]) if len(lines) >= 2 else " ".join(lines)
    bottom = " ".join(lines[-2:]) if len(lines) >= 2 else " ".join(lines)
    print(f"Page {i+1} ({len(lines)} lines)")
    print(f"   Top:    {top[:70]}")
    print(f"   Bottom: {bottom[:70]}")

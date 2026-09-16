from __future__ import annotations

import zipfile
from copy import copy
from pathlib import Path

import lxml.etree as ET

ROOT = Path(__file__).resolve().parent
ORIGINALS = ROOT / "originals"
FINAL = ROOT / "final"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}
Q = lambda name: f"{{{W}}}{name}"

DEEP_GREEN = "315C3B"
BRAND_GREEN = "4F7D3A"
PALE_GREEN = "EAF2E3"
PALE_GOLD = "FFF1C7"
WARM_CREAM = "FFF9E8"
MUTED = "6B675F"
BORDER = "B8C4B1"

TITLE_PHRASES = (
    "Service Agreement",
    "Veterinary Release Agreement",
    "Pet Lodging Addendum",
    "Key Handling Agreement",
    "Contact Information",
    "Pet Information Form",
    "Service Request",
)
MAJOR_HEADINGS = {
    "New Client Packet",
    "Suggested Leave-Out Checklist",
    "Paw Prints Pet Services LLC",
    "Service Agreement",
    "Veterinary Release Agreement",
    "Pet Lodging Addendum",
    "Key Handling Agreement",
    "Contact Information",
    "Pet Information Form",
    "Service Request",
    "Important Terms",
}
MINOR_HEADINGS = {
    "The New Client Packet Includes:",
    "At the initial interview (meet and greet):",
    "If applicable:",
    "Keys:",
    "Contact Us:",
    "Key Returns",
    "Emergency contacts",
    "Things to bring for pet lodging or daycare:",
    "Schedule",
    "Tasks",
    "Additional Comments:",
}


def normalized(text: str) -> str:
    return " ".join(text.replace("\u00a0", " ").split())


def node_text(node) -> str:
    return normalized("".join(node.xpath(".//w:t/text()", namespaces=NS)))


def ensure(parent, tag: str):
    child = parent.find(Q(tag))
    if child is None:
        child = ET.Element(Q(tag))
        parent.append(child)
    return child


def set_paragraph_color_bold(paragraph, color: str, bold: bool = True) -> None:
    for run in paragraph.xpath(".//w:r", namespaces=NS):
        rpr = run.find(Q("rPr"))
        if rpr is None:
            rpr = ET.Element(Q("rPr"))
            run.insert(0, rpr)
        color_node = ensure(rpr, "color")
        color_node.set(Q("val"), color)
        if bold:
            bold_node = ensure(rpr, "b")
            bold_node.set(Q("val"), "1")


def map_fill(fill: str, text: str) -> str:
    fill = fill.upper().replace("#", "")
    lower = normalized(text).lower()
    if "owner" in lower:
        return PALE_GREEN
    if lower == "pet" or lower.startswith("pet "):
        return PALE_GOLD
    if fill in {"00FF00", "92D050", "70AD47", "C6E0B4", "A9D18E"}:
        return PALE_GREEN
    if fill in {"FFFF00", "FFF2CC", "FFE699", "FFD966"}:
        return PALE_GOLD
    if fill in {"F4B183", "F8CBAD", "FCE4D6", "E2F0D9", "DDEBF7", "D9EAD3", "E4DFEC", "EADCF8"}:
        return WARM_CREAM
    return fill


def polish_document_xml(data: bytes, muted_only: bool = False) -> bytes:
    parser = ET.XMLParser(remove_blank_text=False)
    root = ET.fromstring(data, parser)
    if muted_only:
        for paragraph in root.xpath(".//w:p", namespaces=NS):
            if node_text(paragraph):
                set_paragraph_color_bold(paragraph, MUTED, False)
        return ET.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)

    for highlight in root.xpath(".//w:highlight", namespaces=NS):
        if highlight.get(Q("val")) == "green":
            rpr = highlight.getparent()
            rpr.remove(highlight)
            shade = rpr.find(Q("shd"))
            if shade is None:
                shade = ET.Element(Q("shd"))
                rpr.append(shade)
            shade.set(Q("fill"), PALE_GREEN)
            shade.set(Q("val"), "clear")

    for element in root.iter():
        fillcolor = element.get("fillcolor", "").lower()
        if fillcolor in {"#cfc", "#ccffcc", "#00ff00"}:
            element.set("fillcolor", f"#{PALE_GREEN}")
        elif fillcolor in {"#ff9", "#ffff99", "#ffff00"}:
            element.set("fillcolor", f"#{PALE_GOLD}")

    for table in root.xpath(".//w:tbl", namespaces=NS):
        text = node_text(table)
        upper = text.upper()
        if "VISIT TYPE" in upper and "RATE" in upper:
            continue
        is_title = any(phrase in text for phrase in TITLE_PHRASES)
        cells = table.xpath("./w:tr/w:tc", namespaces=NS)
        for index, cell in enumerate(cells):
            tc_pr = cell.find(Q("tcPr"))
            if tc_pr is None:
                tc_pr = ET.Element(Q("tcPr"))
                cell.insert(0, tc_pr)
            shade = tc_pr.find(Q("shd"))
            if shade is not None:
                shade.set(Q("fill"), map_fill(shade.get(Q("fill"), "FFFFFF"), node_text(cell)))
                shade.set(Q("val"), "clear")
            for border in tc_pr.xpath(".//w:tcBorders/*", namespaces=NS):
                border.set(Q("color"), BORDER)
            if is_title and index == 0:
                if shade is None:
                    shade = ET.Element(Q("shd"))
                    tc_pr.append(shade)
                shade.set(Q("fill"), PALE_GREEN)
                shade.set(Q("val"), "clear")
                for paragraph in cell.xpath(".//w:p", namespaces=NS):
                    set_paragraph_color_bold(paragraph, DEEP_GREEN)

    for paragraph in root.xpath(".//w:p", namespaces=NS):
        text = node_text(paragraph)
        if not text:
            continue
        if text in MAJOR_HEADINGS:
            set_paragraph_color_bold(paragraph, DEEP_GREEN)
        elif text in MINOR_HEADINGS or (len(text) <= 55 and text.endswith(":")):
            set_paragraph_color_bold(paragraph, BRAND_GREEN)
        elif text.startswith(("A. ", "B. ", "C. ", "D. ", "E. ", "F. ", "G. ", "H. ")):
            set_paragraph_color_bold(paragraph, DEEP_GREEN, False)
        elif "Thank you for choosing Paw Prints Pet Services" in text or "We look forward to providing" in text:
            set_paragraph_color_bold(paragraph, BRAND_GREEN)

    return ET.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def text_inventory(data: bytes) -> list[str]:
    root = ET.fromstring(data)
    return root.xpath("//w:t/text()", namespaces=NS)


def polish(source: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source, "r") as zin, zipfile.ZipFile(output, "w") as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            before = text_inventory(data) if info.filename.startswith("word/") and info.filename.endswith(".xml") else None
            if info.filename == "word/document.xml":
                data = polish_document_xml(data)
            elif info.filename.startswith("word/header") and info.filename.endswith(".xml"):
                data = polish_document_xml(data, muted_only=True)
            elif info.filename.startswith("word/footer") and info.filename.endswith(".xml"):
                data = polish_document_xml(data, muted_only=True)
            if before is not None and text_inventory(data) != before:
                raise RuntimeError(f"Text changed in {info.filename}")
            zout.writestr(copy(info), data)
    with zipfile.ZipFile(output, "r") as check:
        bad = check.testzip()
        if bad:
            raise RuntimeError(f"Corrupt ZIP entry: {bad}")


def main() -> None:
    for source_name in (
        "Paw Prints-Welcome packet.docx",
        "Paw Prints-Welcome packet with Pet Lodging.docx",
    ):
        source = ORIGINALS / source_name
        output = FINAL / source_name.replace(".docx", " - Professional Refresh.docx")
        polish(source, output)
        print(output)


if __name__ == "__main__":
    main()

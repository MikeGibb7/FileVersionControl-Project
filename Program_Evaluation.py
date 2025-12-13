import os
import xml.etree.ElementTree as ET
import csv

# ------------------------
# Folders
# ------------------------
saved_dir = "Program_Outputs"   # GUI outputs (.txt)
xml_dir = "File_Mappings"       # XML mappings (.xml)

# ------------------------
# Parsing functions
# ------------------------
def parse_txt(txt_file):
    """
    Parse GUI output in {orig new} format
    """
    mappings = []
    with open(txt_file, "r") as f:
        content = f.read()
        parts = content.split("}")
        for p in parts:
            p = p.strip().replace("{", "").strip()
            if not p:
                continue
            nums = p.split()
            if len(nums) == 2:
                try:
                    mappings.append((int(nums[0]), int(nums[1])))
                except ValueError:
                    pass
    return mappings


def parse_xml(xml_file):
    """
    Parse XML and return mappings from the latest VERSION
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    versions = root.findall("VERSION")
    if not versions:
        return []

    # Choose latest version by NUMBER
    latest_version = max(versions, key=lambda v: int(v.attrib["NUMBER"]))

    mappings = []
    for loc in latest_version.findall("LOCATION"):
        orig = int(loc.attrib["ORIG"])
        new = int(loc.attrib["NEW"])
        if new != -1:  # skip eliminated mappings
            mappings.append((orig, new))

    return mappings


# ------------------------
# Evaluation
# ------------------------
def evaluate(txt_mappings, xml_mappings):
    correct = sum(1 for m in txt_mappings if m in xml_mappings)
    spurious = sum(1 for m in txt_mappings if m not in xml_mappings)
    eliminated = sum(1 for m in xml_mappings if m not in txt_mappings)

    total_xml = len(xml_mappings)

    correct_pct = (correct / total_xml * 100) if total_xml else 0
    spurious_pct = (spurious / total_xml * 100) if total_xml else 0
    eliminated_pct = (eliminated / total_xml * 100) if total_xml else 0

    return correct_pct, spurious_pct, eliminated_pct


# ------------------------
# Main
# ------------------------
results = []

for txt_file in sorted(os.listdir(saved_dir)):
    if not txt_file.endswith(".txt"):
        continue

    base_name = txt_file.replace("_New.txt", "").replace(".txt", "")
    txt_path = os.path.join(saved_dir, txt_file)

    # ---- FIX: support BOTH XML naming styles ----
    xml_candidates = [
        os.path.join(xml_dir, f"{base_name}_Mapping.xml"),  # student tests
        os.path.join(xml_dir, f"{base_name}.xml")           # professor files
    ]

    xml_file = None
    for candidate in xml_candidates:
        if os.path.exists(candidate):
            xml_file = candidate
            break

    if xml_file is None:
        print(f"Skipping {base_name}, missing XML mapping file")
        continue

    print(f"Evaluating {base_name} using {os.path.basename(xml_file)}")

    try:
        txt_mappings = parse_txt(txt_path)
        xml_mappings = parse_xml(xml_file)
    except ET.ParseError as e:
        print(f"XML parse error in {xml_file}: {e}")
        continue

    correct, spurious, eliminated = evaluate(txt_mappings, xml_mappings)
    results.append((base_name, correct, spurious, eliminated))


# ------------------------
# Print summary table
# ------------------------
print("\nEvaluation Results")
print(f"{'Test':<25} | {'Correct%':<10} | {'Spurious%':<10} | {'Eliminated%':<12}")
print("-" * 65)

for r in results:
    print(f"{r[0]:<25} | {r[1]:<10.1f} | {r[2]:<10.1f} | {r[3]:<12.1f}")


# ------------------------
# Save CSV
# ------------------------
with open("evaluation_results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Test", "Correct%", "Spurious%", "Eliminated%"])
    for r in results:
        writer.writerow(r)

print("\nResults saved to evaluation_results.csv")

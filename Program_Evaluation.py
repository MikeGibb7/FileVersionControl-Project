import os
import xml.etree.ElementTree as ET

# Folders
saved_dir = "Program_Outputs"   # GUI outputs
xml_dir = "File_Mappings"       # XML mappings

# --- Parsing functions ---
def parse_txt(txt_file):
    """Parse GUI output in {orig new} format"""
    mappings = []
    with open(txt_file, "r") as f:
        content = f.read()
        parts = content.split("}")
        for p in parts:
            p = p.strip().replace("{","").strip()
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
    """Parse XML and return mappings from latest version"""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    versions = root.findall("VERSION")
    if not versions:
        return []

    # Pick the latest version by NUMBER
    latest_version = max(versions, key=lambda v: int(v.attrib["NUMBER"]))
    mappings = []
    for loc in latest_version.findall("LOCATION"):
        orig = int(loc.attrib["ORIG"])
        new = int(loc.attrib["NEW"])
        if new != -1:  # skip eliminated mappings
            mappings.append((orig, new))
    return mappings

# --- Evaluation ---
def evaluate(txt_mappings, xml_mappings):
    correct = sum(1 for m in txt_mappings if m in xml_mappings)
    spurious = sum(1 for m in txt_mappings if m not in xml_mappings)
    eliminate = sum(1 for m in xml_mappings if m not in txt_mappings)
    total_xml = len(xml_mappings)
    correct_pct = (correct / total_xml * 100) if total_xml else 0
    spurious_pct = (spurious / total_xml * 100) if total_xml else 0
    eliminate_pct = (eliminate / total_xml * 100) if total_xml else 0
    return correct_pct, spurious_pct, eliminate_pct

# --- Main ---
results = []

# Loop through all GUI outputs
for txt_file in sorted(os.listdir(saved_dir)):
    if not txt_file.endswith(".txt"):
        continue
    base_name = txt_file.replace("_New.txt", "").replace(".txt", "")
    xml_file = os.path.join(xml_dir, f"{base_name}_Mapping.xml")
    txt_path = os.path.join(saved_dir, txt_file)

    if not os.path.exists(xml_file):
        print(f"Skipping {base_name}, missing XML mapping file")
        continue

    txt_mappings = parse_txt(txt_path)
    xml_mappings = parse_xml(xml_file)
    correct, spurious, eliminate = evaluate(txt_mappings, xml_mappings)
    results.append((base_name, correct, spurious, eliminate))

# --- Print summary table ---
print(f"{'Test':<10} | {'Correct%':<10} | {'Spurious%':<10} | {'Eliminate%':<10}")
print("-"*50)
for r in results:
    print(f"{r[0]:<10} | {r[1]:<10.1f} | {r[2]:<10.1f} | {r[3]:<10.1f}")

# --- Optional: save CSV ---
try:
    import csv
    with open("evaluation_results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Test", "Correct%", "Spurious%", "Eliminate%"])
        for r in results:
            writer.writerow(r)
    print("\nResults saved to evaluation_results.csv")
except Exception:
    pass

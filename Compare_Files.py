import os

def read_file(path):
    try:
        with open(path, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"Error: file '{path}' not found.")
        return None

def main():
    old_path_base = input("Enter path to old file: ").strip()
    new_path_base = input("Enter path to new file: ").strip()

    old_path = os.path.join("Old_File_Versions", old_path_base + ".txt")
    new_path = os.path.join("New_File_Versions", new_path_base + ".txt")

    old_lines = read_file(old_path)
    new_lines = read_file(new_path)

    if old_lines is None or new_lines is None:
        print("Exiting due to file error.")
        return
    
    print(f"Old file: {old_path} — {len(old_lines)} lines")
    print(f"New file: {new_path} — {len(new_lines)} lines")

if __name__ == "__main__":
    main()

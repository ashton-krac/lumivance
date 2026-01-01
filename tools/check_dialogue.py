
import glob
import re

def check_chapters():
    files = glob.glob('chapters/*.md')
    non_compliant = []
    
    for file_path in sorted(files):
        with open(file_path, 'r') as f:
            lines = f.readlines()
            
        found_header = False
        next_line_checked = False
        
        for i, line in enumerate(lines):
            # Check for header, allowing for subtitles like "I. CALL TO ORDER: THE ARCHITECTURE"
            if line.strip().startswith('**I. CALL TO ORDER'):
                found_header = True
                # Check subsequent lines
                for j in range(i + 1, len(lines)):
                    next_line = lines[j].strip()
                    if next_line: # Found first non-empty line
                        # Check if it starts with a quote
                        if not (next_line.startswith('"') or next_line.startswith('“')):
                            non_compliant.append(file_path)
                            print(f"[FAIL] {file_path}")
                            print(f"       Found: {next_line[:50]}...")
                        else:
                            print(f"[PASS] {file_path}")
                        next_line_checked = True
                        break
                break
        
        if not found_header:
            print(f"[WARN] {file_path}: Header not found")
            non_compliant.append(file_path)

    print("\nNon-compliant files:")
    for f in non_compliant:
        print(f" - {f}")

if __name__ == "__main__":
    check_chapters()

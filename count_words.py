import glob
import os

files = sorted(glob.glob("chapters/*.md"))
with open('chapter_word_counts.md', 'w') as report:
    report.write("| Chapter | Word Count | Status |\n")
    report.write("| :--- | :--- | :--- |\n")
    for f in files:
        with open(f, 'r') as file:
            content = file.read()
            word_count = len(content.split())
            basename = os.path.basename(f)
            status = "✅ Complete (>3000)" if word_count >= 3000 else "⚠️  In Progress"
            report.write(f"| {basename} | {word_count:,} | {status} |\n")
    print("Report generated at chapter_word_counts.md")

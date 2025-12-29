import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Local imports
sys.path.append(str(Path(__file__).resolve().parent.parent))
from tools.utils import BIBLE_PATH

# Load environment variables
load_dotenv()

LUMIS_LIST = [
    "Dorothy Dandridge", "Eartha Kitt", "Josephine Baker", "Bob Marley", "Jimi Hendrix", "Prince",
    "Mariah Carey", "Halle Berry", "Alicia Keys", "Barack Obama",
    "Kamala Harris", "Trevor Noah", "Drake", "J. Cole",
    "Logic", "Slash", "Lenny Kravitz", "Lisa Bonet",
    "Zoe Kravitz", "Rashida Jones", "Maya Rudolph", "Tracee Ellis Ross",
    "Jordan Peele", "Keegan-Michael Key", "Wentworth Miller", "Jesse Williams",
    "Thandie Newton", "Ruth Negga", "Tessa Thompson", "Doja Cat",
    "H.E.R.", "Sade", "Meghan Markle", "Misty Copeland"
]

def slugify(name):
    """Converts a name to a filename-friendly slug."""
    return name.lower().replace(" ", "_").replace(".", "").replace("-", "_")

def generate_bio(name):
    """Generates a biography using OpenAI."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment.")
        sys.exit(1)

    # disable auto-retries to handle 429 quota errors manually and gracefully
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7, max_retries=0)
    
    prompt = ChatPromptTemplate.from_template(
        "Write a 250-word narrative biography of {name}, focusing on their dual heritage "
        "and their impact on culture and society. Write in the style of a 'Lumivance' dossier: "
        "elegant, insightful, respectful, and highlighting their role as a bridge between worlds. "
        "Do not use markdown bolding for the name at the start, just the narrative text."
    )
    
    chain = prompt | llm
    try:
        response = chain.invoke({"name": name})
        return response.content
    except Exception as e:
        error_str = str(e)
        if "insufficient_quota" in error_str:
            print(f"\nCRITICAL ERROR: OpenAI API Quota Exceeded for {name}.")
            print("Action: Please check your billing details at platform.openai.com/account/billing/overview.")
            sys.exit(1)
        elif "429" in error_str:
             print(f"\nWarning: Rate limit hit for {name}. Taking a breather...")
             raise e
        else:
            raise e

def archive_lumis(args):
    """Generates and saves biographies for the Lumis list."""
    output_dir = BIBLE_PATH / "lumis"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    target_list = [args.name] if args.name else LUMIS_LIST
    
    for i, name in enumerate(target_list, 1):
        slug = slugify(name)
        file_path = output_dir / f"{slug}.md"
        
        if file_path.exists() and not args.force:
            print(f"[{i}/{len(target_list)}] Skipped {name} (File exists)")
            continue
            
        print(f"[{i}/{len(target_list)}] Generating dossier for {name}...")
        try:
            bio_content = generate_bio(name)
            
            # Add Frontmatter
            full_content = f"# {name}\n\n{bio_content}\n"
            
            file_path.write_text(full_content)
            print(f"   -> Saved to {file_path.name}")
        except Exception as e:
            print(f"   -> Error generating {name}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate biographies for Lumis.")
    parser.add_argument("--name", help="Generate for a specific person only.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    
    args = parser.parse_args()
    archive_lumis(args)

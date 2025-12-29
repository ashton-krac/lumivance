import argparse
import sys
from pathlib import Path
from datetime import datetime

# Local imports
# Adjust path to find tools if necessary, though running as script usually requires module setup
# For simplicity in this script, we'll assume relative imports or direct execution
sys.path.append(str(Path(__file__).resolve().parent.parent))
from tools.utils import SRC_PATH

TEMPLATE = """**Date:** {date}
**Location:** {location}
**Chair:** {chair}
**Secretary:** {secretary}

The meeting was called to order at {time} by the Chair.

**Order of Business:** {agenda}

{body}

It was thereby **Resolved** that {resolution}

**Further Discussion:** {discussion}

There being no further business, the meeting adjourned at {adjournment}.

Respectfully submitted,
{secretary}, Secretary
"""

def create_minutes(args):
    """Generates a new chapter file based on the Meeting Minutes template."""
    
    # Format Date
    try:
        dt = datetime.strptime(args.date, "%Y-%m-%d")
        formatted_date = dt.strftime("%B %d, %Y")
    except ValueError:
        formatted_date = args.date

    content = TEMPLATE.format(
        date=formatted_date,
        location=args.location,
        chair=args.chair,
        secretary=args.secretary,
        time=args.time,
        agenda=args.agenda,
        body=args.body,
        resolution=args.resolution,
        discussion=args.discussion,
        adjournment=args.adjournment
    )
    
    # Determine Output Path
    # Auto-generate filename from date if specific output name not provided
    # Attempt to parse ISO date for filename
    try:
        dt = datetime.strptime(args.date, "%Y-%m-%d")
        filename_date = dt.strftime("%Y-%m-%d")
    except ValueError:
        # If date is free text (e.g. "July 1, 1892"), try to parse or just use it cleaned
        try:
             dt = datetime.strptime(args.date, "%B %d, %Y")
             filename_date = dt.strftime("%Y-%m-%d")
        except ValueError:
             # Fallback: slugify the text date
             filename_date = args.date.replace(" ", "_").replace(",", "")

    if args.out:
        filename = args.out
    else:
        filename = filename_date

    if not filename.endswith(".md"):
        filename += ".md"
        
    output_path = SRC_PATH / "draft" / filename
    
    # Ensure directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if output_path.exists() and not args.force:
        print(f"Error: File '{filename}' already exists. Use --force to overwrite.")
        sys.exit(1)
        
    output_path.write_text(content)
    print(f"Success: Created '{output_path}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a new Lumivance Chapter (Meeting Minutes).")
    
    parser.add_argument("--date", required=True, help="Date of meeting (YYYY-MM-DD or 'Month DD, YYYY')")
    parser.add_argument("--location", default="1411 W Street SE, Washington, D.C.", help="Meeting location")
    parser.add_argument("--chair", default="Mr. Douglass", help="Chairperson")
    parser.add_argument("--secretary", default="Mr. Herriman", help="Secretary")
    parser.add_argument("--time", default="six o'clock in the evening", help="Start time")
    parser.add_argument("--agenda", default="General Business", help="Order of Business")
    parser.add_argument("--body", default="[Body of the meeting minutes goes here...]", help="Main content")
    parser.add_argument("--resolution", default="[Resolution details...]", help="Resolution text")
    parser.add_argument("--discussion", default="None.", help="Further discussion")
    parser.add_argument("--adjournment", default="half past six in the evening", help="Adjournment time")
    parser.add_argument("--out", required=False, help="Optional output filename. Defaults to YYYY-MM-DD.md")
    parser.add_argument("--force", action="store_true", help="Overwrite existing file")

    args = parser.parse_args()
    create_minutes(args)

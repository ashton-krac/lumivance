# Lumivance: Digital Nervous System

## Overview
This repository serves as the computational backbone for the novel **Lumivance**. It seamlessly integrates narrative data ("The Bible"), active drafts, and generative AI tools to ensure narrative consistency, automate world-building checks, and facilitate "Agent-First" interactions.

## Architecture
- **`src/`**: The core narrative text (Markdown).
    - `draft/`: Active writing workspace.
    - `archive/`: Versioned history.
- **`bible/`**: Source of Truth for world-building (Entities, Spells, Locations).
- **`memory/`**: Persistent Vector Store (ChromaDB) for RAG interactions.
- **`tools/`**: Python scripts designed as clean APIs for AI Agents.

## Usage
Tools are designed to be run silently or via CLI.
```bash
# Example: Check for narrative consistency
python tools/character_tracker.py --chapter src/draft/chapter_01.md
```

## Philosophy
* **Quiet Luxury Code**: Minimalist, robust, and invisible.
* **Agent-First**: Outputs are machine-readable (JSON/Markdown).
* **Narrative Logic**: Code serves the story, not the other way around.

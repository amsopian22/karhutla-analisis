#!/usr/bin/env python3
"""
Test proper BibTeX parsing and validation.
"""
from pathlib import Path
import re

BIB_FILE = Path("/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/manuscript/references.bib")

with open(BIB_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Tokenize and parse entries
entries = []
pos = 0
length = len(content)

while pos < length:
    at_idx = content.find("@", pos)
    if at_idx == -1:
        break
    # find open brace
    open_brace_idx = content.find("{", at_idx)
    if open_brace_idx == -1:
        break
    entry_type = content[at_idx+1:open_brace_idx].strip().lower()
    
    # now match balanced braces from open_brace_idx
    brace_count = 1
    curr = open_brace_idx + 1
    in_quote = False
    while curr < length and brace_count > 0:
        c = content[curr]
        if c == '"' and content[curr-1] != '\\':
            in_quote = not in_quote
        elif not in_quote:
            if c == '{':
                brace_count += 1
            elif c == '}':
                brace_count -= 1
        curr += 1
    
    if brace_count != 0:
        print(f"Error: Unbalanced braces in entry starting at {at_idx} ({entry_type})")
        pos = curr
        continue
    
    entry_text = content[at_idx:curr]
    inside_text = content[open_brace_idx+1:curr-1]
    # first comma separates key from fields
    comma_idx = inside_text.find(",")
    if comma_idx == -1:
        print(f"Error: No comma after key in entry {entry_type}")
        pos = curr
        continue
    
    key = inside_text[:comma_idx].strip()
    fields_str = inside_text[comma_idx+1:].strip()
    entries.append((entry_type, key, fields_str))
    pos = curr

print(f"Parsed {len(entries)} BibTeX entries perfectly.")
for t, k, fld in entries:
    # check required fields: author, title, year
    has_author = "author" in fld.lower()
    has_title = "title" in fld.lower()
    has_year = "year" in fld.lower()
    if not (has_author and has_title and has_year):
        print(f"Warning: Entry '{k}' missing one of (author, title, year)")

print("All entries checked.")

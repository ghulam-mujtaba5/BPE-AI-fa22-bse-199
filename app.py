#!/usr/bin/env python3
"""
BPE AI - Business Process Element Analysis
Classifies process labels from draw.io diagrams based on grammatical structure.
"""

import sys
from xml_extractor import get_labels
from worldList import type_of_word, ensure_nltk_data

FILENAME = 'file.xml'

def classify_labels(labels):
    """Classify labels into categories based on first word type."""
    verb_phrases = []  # Actions: "Send Email", "Process Payment"
    noun_phrases = []  # Objects/States: "Payment Gateway", "Customer Account"
    others = []  # Unclassified or uncertain
    
    skipped = []
    
    for label in labels:
        label = label.strip()
        
        # Skip empty labels
        if not label:
            continue
            
        # Split and get first word
        words = label.split()
        if not words:
            skipped.append(label)
            continue
            
        first_word = words[0]
        word_type = type_of_word(first_word)
        
        # Classify based on first word type
        if word_type == 'verb':
            verb_phrases.append((label, first_word))
        elif word_type == 'noun':
            noun_phrases.append((label, first_word))
        else:
            others.append((label, first_word, word_type))
    
    return verb_phrases, noun_phrases, others, skipped

def print_results(verb_phrases, noun_phrases, others, skipped):
    """Print classification results with statistics."""
    total = len(verb_phrases) + len(noun_phrases) + len(others) + len(skipped)
    
    print("=" * 70)
    print("BUSINESS PROCESS ELEMENT CLASSIFICATION RESULTS")
    print("=" * 70)
    print(f"Total Labels Processed: {total}\n")
    
    # Verb Phrases (Action-oriented)
    print(f"\n{'='*70}")
    print(f"ACTION PHRASES (Verb-led) - {len(verb_phrases)} items")
    print(f"{'='*70}")
    if verb_phrases:
        for label, first_word in verb_phrases:
            print(f"  • {label:<50} [starts with: {first_word}]")
    else:
        print("  (None found)")
    
    # Noun Phrases (Object/State-oriented)
    print(f"\n{'='*70}")
    print(f"OBJECT/STATE PHRASES (Noun-led) - {len(noun_phrases)} items")
    print(f"{'='*70}")
    if noun_phrases:
        for label, first_word in noun_phrases:
            print(f"  • {label:<50} [starts with: {first_word}]")
    else:
        print("  (None found)")
    
    # Other/Unclassified
    if others:
        print(f"\n{'='*70}")
        print(f"UNCLASSIFIED/OTHER - {len(others)} items")
        print(f"{'='*70}")
        for label, first_word, word_type in others:
            print(f"  • {label:<50} [starts with: {first_word} ({word_type})]")
    
    # Skipped
    if skipped:
        print(f"\n{'='*70}")
        print(f"SKIPPED (Empty/Invalid) - {len(skipped)} items")
        print(f"{'='*70}")
        for label in skipped:
            print(f"  • '{label}'")
    
    # Statistics Summary
    print(f"\n{'='*70}")
    print("SUMMARY STATISTICS")
    print(f"{'='*70}")
    print(f"  Action Phrases (Verb-led):     {len(verb_phrases):>3} ({len(verb_phrases)/total*100:.1f}%)")
    print(f"  Object/State Phrases (Noun):   {len(noun_phrases):>3} ({len(noun_phrases)/total*100:.1f}%)")
    print(f"  Unclassified:                  {len(others):>3} ({len(others)/total*100:.1f}%)")
    if skipped:
        print(f"  Skipped:                       {len(skipped):>3} ({len(skipped)/total*100:.1f}%)")
    print(f"  {'─'*68}")
    print(f"  Total:                         {total:>3}")
    print(f"{'='*70}\n")

def main():
    """Main execution function."""
    try:
        # Ensure NLTK data is available
        print("Initializing NLTK resources...")
        if not ensure_nltk_data():
            print("Warning: NLTK data not fully available. Results may be less accurate.")
            print()
        
        # Extract labels from XML
        print(f"Extracting labels from '{FILENAME}'...")
        labels = get_labels(FILENAME)
        
        if not labels:
            print(f"\nNo labels found in {FILENAME}")
            return 1
        
        print(f"Found {len(labels)} labels with spaces.\n")
        
        # Classify labels
        print("Classifying labels...\n")
        verb_phrases, noun_phrases, others, skipped = classify_labels(labels)
        
        # Print results
        print_results(verb_phrases, noun_phrases, others, skipped)
        
        return 0
        
    except FileNotFoundError:
        print(f"\nError: File '{FILENAME}' not found!")
        print("Please ensure the XML file exists in the current directory.")
        return 1
    except Exception as e:
        print(f"\nError: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
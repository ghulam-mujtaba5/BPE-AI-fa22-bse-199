#!/usr/bin/env python3
"""
Word Type Classification Module
Determines if words are verbs, nouns, or other parts of speech using NLTK.
"""

import sys

def ensure_nltk_data():
    """Ensure required NLTK data is downloaded."""
    try:
        import nltk
        required_data = [
            ('corpora/wordnet', 'wordnet'),
            ('taggers/averaged_perceptron_tagger', 'averaged_perceptron_tagger'),
            ('corpora/omw-1.4', 'omw-1.4')
        ]
        
        all_available = True
        for path, name in required_data:
            try:
                nltk.data.find(path)
            except LookupError:
                print(f"Downloading NLTK data: {name}...")
                try:
                    nltk.download(name, quiet=True)
                except:
                    all_available = False
                    print(f"Warning: Could not download {name}")
        
        return all_available
    except ImportError:
        print("Error: NLTK not installed. Install with: pip install nltk")
        return False

def is_noun_or_verb(word):
    """
    Determine if a word is a noun, verb, or other part of speech.
    
    Uses WordNet for semantic analysis and POS tagging as fallback.
    
    Args:
        word (str): Word to analyze
        
    Returns:
        str: 'verb', 'noun', or 'other'
    """
    try:
        from nltk.corpus import wordnet
        from nltk.tag import pos_tag
    except ImportError:
        print("Error: NLTK not available")
        return 'other'
    
    # Normalize word
    word = word.lower().strip()
    
    if not word:
        return 'other'
    
    try:
        # First check WordNet for all possible parts of speech
        synsets = wordnet.synsets(word)
        pos_found = set()
        
        for synset in synsets:
            if synset.pos() == 'v':  # verb
                pos_found.add('verb')
            elif synset.pos() == 'n':  # noun
                pos_found.add('noun')
        
        # If we found both noun and verb, prioritize based on more common usage
        if 'verb' in pos_found and 'noun' in pos_found:
            # Count synsets for each type to determine primary usage
            verb_count = len([s for s in synsets if s.pos() == 'v'])
            noun_count = len([s for s in synsets if s.pos() == 'n'])
            return 'verb' if verb_count > noun_count else 'noun'
        
        # Return the found type
        if 'verb' in pos_found:
            return 'verb'
        if 'noun' in pos_found:
            return 'noun'
        
        # Fallback to POS tagging if WordNet doesn't help
        pos_tags = pos_tag([word])
        if pos_tags:
            tag = pos_tags[0][1]
            
            # Verb tags: VB, VBD, VBG, VBN, VBP, VBZ
            if tag.startswith('VB'):
                return 'verb'
            # Noun tags: NN, NNS, NNP, NNPS
            if tag.startswith('NN'):
                return 'noun'
        
        return 'other'
        
    except Exception as e:
        print(f"Error analyzing word '{word}': {e}", file=sys.stderr)
        return 'other'

def check_word_type(word):
    """
    Main function to check if word is noun or verb.
    
    Args:
        word (str): Word to analyze
        
    Returns:
        dict: Result with word type and boolean flags
    """
    result = is_noun_or_verb(word)
    
    return {
        'word': word,
        'type': result,
        'is_noun': result == 'noun',
        'is_verb': result == 'verb',
        'is_other': result == 'other'
    }

def type_of_word(word):
    """
    Simple interface to get word type.
    
    Args:
        word (str): Word to analyze
        
    Returns:
        str: 'verb', 'noun', or 'other'
    """
    result = check_word_type(word)
    return result['type']

def analyze_phrase(phrase):
    """
    Analyze a multi-word phrase.
    
    Args:
        phrase (str): Phrase to analyze
        
    Returns:
        dict: Analysis of the phrase structure
    """
    words = phrase.strip().split()
    if not words:
        return {'type': 'empty', 'words': []}
    
    word_analysis = []
    for word in words:
        word_type = type_of_word(word)
        word_analysis.append({
            'word': word,
            'type': word_type
        })
    
    first_word_type = word_analysis[0]['type'] if word_analysis else 'other'
    
    return {
        'phrase': phrase,
        'first_word_type': first_word_type,
        'word_count': len(words),
        'words': word_analysis
    }

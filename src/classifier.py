import re

# Classificate using regular expressions
def classify_sentence(sentence):
    """
    Classifies a sentence based on predefined regular expression patterns.
    Returns the first matching category or "99" if no match.
    """
    patterns = {
        # TEAM LEADERSHIP Subcategories need to be matched with priority
        'ASP': [
            # Task assignment
            r"\b(?:assign|reassign|allocat(?:ing|e)|requesting|priorit(?:y|ize|ise|izing)|take|work\s+on)\b.*\b(?:F|S|TMA)\d+\b",
            # Direct command
            r"\b(?:do|focus\s+on|temporarily\s+on|switch\s+to)\s+(?:F|S|TMA)\d+\b",
            # Priority declaration
            r"\b(?:F|S|TMA)\d+\s+(?:takes?\s+priority|first|next|now)\b",
            # Compound request
            r"\b(?:can\s+(?:you|we|I)|please)\s+(?:get|take|assign|work\s+on)\b.*\b(?:F|S|TMA)\d+\b"
        ],
        'ORD': [
            # Global command
            r"\b(?:down\s+all\s+masts|assign\s+the\s+solution|cut\s+that\s+through)\b",
            # Equipment operation command
            r"\b(?:raise\s+the\s+masts|capture\s+image|cut\s+through)\b",
            # Reinforcement command
            r"\b(?:immediate\s+action\b|execute\s+now\b|you\s+must\b)"
        ],
        'DUP': [
            # Status change
            r"\b(?:has\s+been\s+identified|disregard\s+(?:F|S|TMA)\d+|updated\s+solution\s+for)\b",
            # Global notification
            r"\b(?:all\s+positions\b.*\b(?:disregard|contact|update))\b",
            # Tracking status
            r"\b(?:lost\s+track(?:er|ing)|visual\s+contact|new\s+contact\s+detected)\b"
        ],
        'FB': [
            # Performance feedback
            r"\b(?:solution\s+is\s+lagging|check\s+(?:for|the)|(?:speed|range)\s+should\s+be)\b.*\b(?:F|S|TMA)\d+\b",
            # Numerical correction
            r"\b\d+\s*(?:knots?|kiloyards?)\b.*\b(?:over|under)\s+the\s+solution\b"
        ],
        'MV': [
            r"\b(?:looking\s+good\s+team|well\s+done\b|let'?s\s+go\s+team)\b",
            r"\b(?:great\s+work|excellent\s+job|keep\s+it\s+up)\b"
        ],
        'PUSHED': [
            # Proactive report
            r"\b(?:just\s+monitoring|updated\s+(?:solution|range)|new\s+contact\s+at)\b",
            # Technical parameters
            r"\b(?:bearing\s+\d+|range\s+\d+\.?\d*\s*(?:kiloyards)?|ATB\s+\d+)\b",
            # Status update
            r"\b(?:possible\s+rendezvous|visual\s+range|still\s+in\s+visual)\b"
        ],
        'PULLED': [
            # Explicit request
            r"\b(?:can\s+I\s+get|can\s+you\s+please|please\s+give\s+me|what'?s?\s+happening\s+to)\b",
            # Asking for suggestion
            r"\b(?:would\s+you\s+like\s+me\s+to|should\s+I|do\s+you\s+want\s+me\s+to)\b",
            # Compound question
            r"\b(?:any\s+report\?|no\s+report\b|confirm\s+again)\b"
        ],
        'RESPONSE': [
            # Data response
            r"\b(?:is\s+at\s+\d+\s*ATB|range\s+is\s+\d+\.?\d*\s*kiloyards)\b",
            # Status confirmation
            r"\b(?:confirmed|detected|still\s+there)\b.*\b(?:F|S|TMA)\d+\b"
        ],
        'CLC': [
            # Basic confirmation phrases
            r"\b(?:roger\b\.?|thank\s+you|standby|confirm|copy\s+that|acknowledged|understood)\b",
            # Polite response
            r"\b(?:yep|yeah|okay|yes|go)\b[,.!]?\s*(?:please|ahead)?\b",
            # Short sentences
            r"^\s*(?:yes|no|okay|roger|got\s+it)\s*[,.!]?\s*$",
            # Confirmation request
            r"\b(?:affirmative|negative)\b",
            # Polite confirmation
            r"\b(?:yes\s+please|no\s+thank\s+you)\b"
        ],
        'MISCOM': [
            r"\b(?:stop[\.,!]*\b.*\bnot\s+(?:correct|right)|disregard\s+previous|apologies|make\s+that)\b",
            r"^(?:disregard|abort|error)\b"
        ],
        'WL': [
            r"\b(?:watch(?:leader)?\b.*\b(?:update|check|system))\b",
            r"\b(?:monitoring\s+station|WL\s+update)\b"
        ]
    }

    matches = []
    for label, regex_list in patterns.items():
        for pattern in regex_list:
            if re.search(pattern, sentence, re.IGNORECASE):
                matches.append(label)
    return matches

# label mapping logic
def get_b5t_and_subcategories(categories):
    b5t, sub1, sub2 = '99', '', ''    

    tl_subcategories = {'ASSIGN','ORDER','UPDATE','FEEDBACK','MOTIVATE'}
    tl_matches = [c for c in categories if c in tl_subcategories]
    other_matches = [c for c in categories if c not in tl_subcategories] 
  
    # TL logic processing
    if tl_matches:
        b5t = 'TL'
        sub1 = tl_matches[0] if len(tl_matches) > 0 else ''
        # Handle multiple subcategories
        sub2 = ','.join(tl_matches[1:3]) if len(tl_matches) > 1 else ''
    
    # Non-TL logic
    elif other_matches:
        b5t = other_matches[0]
        # Handle multiple labels
        sub2 = ','.join(other_matches[1:3]) if len(other_matches) > 1 else ''

    # WATCHLEADER logic
    if 'WL' in categories and b5t == '99':
        b5t = 'WL'

    subcategories = [c for c in categories if c != b5t]
    sub1 = subcategories[0] if len(subcategories) > 0 else ""
    sub2 = subcategories[1] if len(subcategories) > 1 else ""

    return b5t, sub1, sub2
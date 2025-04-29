import re
import csv

def load_dictionaries(file_path):
    """
    Loads the dictionary.csv file from the specified path and builds a mapping dictionary for B5T and Keywords.
    
    Args:
    file_path (str): The path to the CSV file.
    
    Returns:
    dict: A dictionary with B5T as keys and Keywords as values.
    """
    b5t_dict = {}
    try:
        # Open the CSV file
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            header = next(csv_reader, None)
            for row in csv_reader:
                # If the row has at least two columns
                if len(row) >= 2:
                    b5t = row[0].strip()
                    keyword = row[1].strip()
                    b5t_dict[b5t] = keyword        
        return b5t_dict

    except Exception as e:
        print(f"Error loading file: {e}")
        return {}

def find_b5t_labels(b5t_dict, sentence):
    """
    Scans the sentence, finds all matching B5T labels based on keywords:
      b5t   - the main category (e.g. 'TL' or other label)
      sub1  - first subcategory (if any)
      sub2  - second subcategory (if any)
    """

    # Find all possible labels
    matched = []
    for label, keywords_str in b5t_dict.items():
        # split keywords string
        keywords = [kw.strip() for kw in keywords_str.split(',') if kw.strip()]
        for kw in keywords:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, sentence, re.IGNORECASE):
                matched.append(label)
                break  # match one keyword and jump to next label

    # TL subcategory logic
    def find_tl_subcategory(categories):
        # Initialize defaults
        b5t, sub1, sub2 = '99', '', ''

        # Define TL subcategories
        tl_subcategories = {'ASSIGN', 'ORDER', 'UPDATE', 'FEEDBACK', 'MOTIVATE'}
        tl_matches   = [c for c in categories if c in tl_subcategories]
        other_matches= [c for c in categories if c not in tl_subcategories]

        # TL
        if tl_matches:
            b5t  = 'TL'
            sub1 = tl_matches[0]
            sub2 = ','.join(tl_matches[1:3]) if len(tl_matches) > 1 else ''
        # Non-TL
        elif other_matches:
            b5t  = other_matches[0]
            sub2 = ','.join(other_matches[1:3]) if len(other_matches) > 1 else ''
        # Special rule: WATCHLEADER override
        if 'WL' in categories and b5t == '99':
            b5t = 'WL'

        # Retry sub1/sub2 from whatever remains
        subcats = [c for c in categories if c != b5t]
        sub1 = subcats[0] if len(subcats) > 0 else ''
        sub2 = subcats[1] if len(subcats) > 1 else ''
        return b5t, sub1, sub2

    b5t, sub1, sub2 = find_tl_subcategory(matched)
    return b5t, sub1, sub2
import csv, re

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
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
             # header = next(csv_reader, None)
            for row in csv_reader:
                # If the row has at least two columns
                if len(row) >= 2:
                    b5t = row[0].strip()
                    keyword = row[1].strip()
                    b5t_dict[b5t] = keyword   
        # debug line
        print(b5t_dict)     
        return b5t_dict

    except Exception as e:
        print(f"Error loading file: {e}")
        return {}

def find_b5t_labels(b5t_dict, text):
    """
    Scans text, finds all matching B5T labels based on keywords
    """
    # Find all possible labels
    matched = []
    for label, keywords_str in b5t_dict.items():
        # split keywords string
        keywords = [kw.strip() for kw in keywords_str.split(',') if kw.strip()]
        for kw in keywords:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                matched.append(label)
                break  # match one keyword and jump to next label

    # Print matched labels for debugging
    print(f"Matched labels: {matched}")

    # TL subcategory logic
    def find_tl_subcategory(categories):
        # Initialize defaults
        b5t, sub1, sub2 = '99', '', ''

        # Define TL subcategories
        tl_subcategories = {'ASP', 'ORD', 'DUP', 'FB', 'MV'}
        tl_matches = [c for c in categories if c in tl_subcategories]
        other_matches = [c for c in categories if c not in tl_subcategories]

        # If TL subcategory matches are found
        if tl_matches:
            b5t = 'TL'  # Set main category to TL
            sub1 = tl_matches[0]  # First subcategory
            sub2 = ','.join(tl_matches[1:3]) if len(tl_matches) > 1 else ''  # Subsequent subcategories
        # Non-TL is found
        elif other_matches:
            b5t = other_matches[0]
            sub1 = other_matches[1] if len(other_matches) > 1 else ''
            sub2 = ','.join(other_matches[2:4]) if len(other_matches) > 2 else ''

        # Special rule: WATCHLEADER priority
        if 'WL' in categories:
            b5t = 'WL'
            # Recalculate subcategories, excluding WL
            subcats = [c for c in categories if c != 'WL']
            sub1 = subcats[0] if subcats else ''
            sub2 = ','.join(subcats[1:3]) if len(subcats) > 1 else ''

        return b5t, sub1, sub2

    b5t, sub1, sub2 = find_tl_subcategory(matched)
    return b5t, sub1, sub2
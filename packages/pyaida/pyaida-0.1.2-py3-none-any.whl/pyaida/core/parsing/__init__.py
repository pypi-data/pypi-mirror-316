
import re

def parse_bibtex(bibtex_entry:str):
    """parse a bix text ref"""
    pattern = r"@(\w+)\s*{\s*(.*?)\s*}$"
    match = re.match(pattern, bibtex_entry, re.DOTALL)
    
    if match:
        content = match.group(2)
        
        field_pattern = re.compile(r'(\w+)\s*=\s*{([^}]+)}', re.DOTALL)
        d = {}
        for field_match in field_pattern.finditer(content):
            field_name = field_match.group(1).strip()
            field_value = field_match.group(2).strip()
            d[field_name] = field_value

        return {
            "type": match.group(1),     
            "content": d
        }
    else:
        return None
import numbers
from functions.chr import CHR 

def make_string(text: str) -> str:
    requires_uppercase = text.lower() != text
    requires_lowercase = text.upper() != text

    gh = f"gh:={numbers.SEVENTY_EIGHT}," if requires_uppercase else ""
    aaz = f"aaz:={numbers.HUNDERED_TEN}," if requires_lowercase else ""

    results = []
    for char in text:
        if char == ' ':
            results.append(f"({numbers.TWO}).__pow__({numbers.FIVE})")
            continue

        num = ord(char)
        if abs(num - 78) < abs(num - 110):
            base = 'gh' 
            offset = num - 78
        else:
            base = 'aaz' 
            offset = num - 110

        if offset != 0:
            method = '__add__' if offset >= 0 else '__sub__'
            offset = abs(offset)
            offset_str = numbers.OFFSETS[offset - 1]

            results.append(f"({base}).{method}({offset_str})")
        else:
            results.append(f"({base})")
    
    result = f"({CHR}({results[0]}))"
    for res in results[1:]:
        result = f"{result}.__add__({CHR}({res}))"

    return f"({gh}{aaz}{result})[({numbers.ONE}).__neg__()]"

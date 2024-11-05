from B_000_globalDependecies import typing, re
divBy2: typing.Callable[[int], bool] = lambda x: x % 2 == 0


NoneOrBool: typing.Callable[[any], bool] = lambda x: (x is None) or (isinstance(x, bool))

def convertString(ipt: str) -> None|bool|float|str:
    iptMod =ipt.lower().strip()
    if len(iptMod) == 0: return None
    
    if iptMod == "none": return None
    
    if iptMod == "false": return False
    elif iptMod == "true": return True
    
    try:
        returnVal = float(iptMod)
        return returnVal
    except:
        return ipt.strip()

def jsonQuotes(text:str)->str:
    # Remove the outer single quotes
    text = text.strip("'")
    
    # Use regex to find keys and string values
    def replace(match):
        key_or_value = match.group(0)
        # Check if it's a number or boolean
        if re.match(r'^\d+$', key_or_value):  # Check for integers
            return key_or_value
        elif key_or_value in ['true', 'false']:  # Check for booleans
            return key_or_value
        else:
            return f'"{key_or_value}"'  # Add quotes for strings

    # Replace keys and string values
    modified_text = re.sub(r'\b\w+\b', replace, text)
    
    # Return the modified string with outer double quotes
    return f'{modified_text}'

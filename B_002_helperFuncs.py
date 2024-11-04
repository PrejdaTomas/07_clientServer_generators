from B_000_globalDependecies import typing
divBy2: typing.Callable[[int], bool] = lambda x: x % 2 == 0


NoneOrBool: typing.Callable[[any], bool] = lambda x: (x is None) or (isinstance(x, bool))

def convertString(ipt: str) -> any:
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
    
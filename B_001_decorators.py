def info(func: callable) -> callable:
    def inner(*args, **kwargs):
        printStatement: str = f"Executing {func.__name__} with:\n"
        printStatement += "\tthe following args:\n"
        for i, arg in enumerate(args):
            printStatement += f"\t\t{i}: {arg}, {type(arg)}"
            if i < len(args)-1 and len(args) >= 1: printStatement += "\n"
        
        printStatement += "\tthe following kwargs:\n"
        for i, kwarg in enumerate(kwargs):
            printStatement += f"\t\t{i}: {kwarg}, {type(kwarg)}"
            if i < len(kwargs)-1 and len(args) >= 1: printStatement += "\n"
            
        printStatement = printStatement[:-1]
        print(printStatement)
        value: any = func(*args, **kwargs)
        print(f"Done executing {func.__name__} with the return value {value}: {type(value)}\n")
        
        return value
    return inner


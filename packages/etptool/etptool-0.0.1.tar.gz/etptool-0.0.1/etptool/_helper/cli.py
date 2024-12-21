import argparse
import typing

def parse_args(arg_types, args):
    """Generic function to parse arguments.
    
    Args:
        arg_types (dict): Dictionary where keys are argument names, and values are their types.
        args (list): List of arguments to parse.

    Returns:
        dict: Parsed arguments as key-value pairs.

    Example:
    >>> parse_args({"bus": int, "addr": int, "data": list[int]}, ["--bus", "1", "--addr", "0x50", "--data", "0x12", "0x34"])
    """
    parser = argparse.ArgumentParser()

    # Add optional arguments based on the arg_types dictionary
    for arg, arg_type in arg_types.items():
        if arg_type is bool:
            parser.add_argument(f"--{arg}", action="store_true", help=f"{arg} (optional argument)")
        elif typing.get_args(arg_type) == typing.get_args(list[int]):
            parser.add_argument(f"--{arg}", nargs="+", type=int, help=f"{arg} (optional argument)")
        elif arg_type is list:
            parser.add_argument(f"--{arg}", nargs="+", help=f"{arg} (optional argument)")
        else:
            parser.add_argument(f"--{arg}", type=arg_type, help=f"{arg} (optional argument)")

    # Add positional arguments group for compatibility with both named and unnamed arguments
    parser.add_argument("parameters", nargs="*", type=int, help="Positional arguments")

    # Parse the arguments
    parsed_args = parser.parse_args(args)

    # Resolve positional arguments (if any) by combining them with the optional arguments
    result = {}
    if parsed_args.parameters:
        pos_args = parsed_args.parameters + [None] * (len(arg_types) - len(parsed_args.parameters))
        for idx, (arg, arg_type) in enumerate(arg_types.items()):
            if typing.get_args(arg_type) == typing.get_args(list[int]):
                result[arg] = pos_args[idx:]
            else:
                result[arg] = pos_args[idx]

    # Combine results from optional and positional arguments, giving priority to optional
    for arg, arg_type in arg_types.items():
        # Check if 'arg' is not already set by positional arguments
        if result.get(arg) is None:
            result[arg] = parsed_args.__dict__.get(arg, result.get(arg))

    # Ensure that all necessary arguments have been provided
    for arg in arg_types:
        if result[arg] is None:
            parser.error(f"Argument '{arg}' must be specified either as a positional or optional argument.")

    return result

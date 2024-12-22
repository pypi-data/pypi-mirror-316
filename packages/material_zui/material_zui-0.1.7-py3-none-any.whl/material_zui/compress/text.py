from typing import Any, TypeVar

T = TypeVar('T')


def encode(lines: list[str]) -> list[str]:
    """
    INPUT:  A line of ASCII String.
    OUTPUT: A List of Run-Length Encoded of the input string.
    """
    if not lines:
        return [""]
    else:
        last_char = lines[0]
        length = len(lines)
        i = 1
        while i < length and last_char == lines[i]:
            i += 1
        return [str(i), last_char] + encode(lines[i:])


def decode(parsed_string: Any) -> str:
    """
    INPUT:  A List of List parsed from encoded string
    OUTPUT: A String of Decoded line
    """
    decoded = ""
    for item in parsed_string:
        try:
            decoded += item[0] * item[1]
        except IndexError:
            pass
    return decoded


def flatten(encoded_list):
    """
    INPUT:  A list of encoded ASCII String
    OUPUT:  A String of encoded ASCII String
    """
    return "".join(encoded_list)


def parse(string):
    """
    This function parses the encoded string for the decoding phase.
    This is especially userful when a character shows up
    more than nine times in a row.

    INPUT:  An Encoded String
    OUTPUT: A List of List // Parsed Encoded String
    """
    if not string or len(string) == 1:
        return [""]
    if string[1].isdigit():
        return [[int(string[:2]), string[2]]] + parse(string[3:])
    else:
        return [[int(string[0]), string[1]]] + parse(string[2:])


def save_text_encode(file_path: str, output_path: str):
    '''
    @file_path: `abc/def.txt`
    @output_path: `ghk/ilm.txt`
    - Only apply for `text file (*.txt)`
    - Use `lossless compression algorithm`
    - Text file after encode will reduce volume size
    '''
    with open(file_path, 'r') as f:
        with open(output_path, 'w+') as o:
            for line in f:
                encoded_string = flatten((encode(line)))
                o.write(encoded_string)


def save_text_decode(file_path: str, output_path: str):
    '''
    Only apply for text file (*.txt)
    '''
    with open(file_path, 'r') as f:
        with open(output_path, 'w+') as o:
            for line in f:
                parsed_string = parse(line)
                o.write(decode(parsed_string))

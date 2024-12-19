import os
import argparse
import pandem.io

known_input_types = ["mercury", "nddem", "nddem_vtk", "yade", "liggghts"]


def guess_type(filename):
    """
    Guess the type of file based on its extension.

    Parameters:
    filename (str): The name of the file whose type is to be guessed.

    Returns:
    str: The guessed type of the file. Possible return values are:
         - "mercury" for files with a ".data" extension
         - "nddem" for files with a ".csv" extension
         - "yade" for files with a ".bz2" or ".gz" extension
         - None if the file extension does not match any known types
    """
    extension = filename.split(".")[-1]
    if extension == "data":
        return "mercury"
    elif extension == "csv":
        return "nddem"
    elif extension == "vtk":
        return "nddem_vtk"
    elif extension == "bz2" or extension == "gz":
        return "yade"
    elif extension == "dump":
        return "liggghts"
    else:
        None


def conversion_script():
    """
    Parses command-line arguments and performs a file conversion.

    This script takes an input file and converts it to an output file, with optional
    specifications for the input and output file types.

    Command-line arguments:
    input_file (str): The path to the input file.
    output_file (str): The path to the output file.
    --input-type (str, optional): The type of file for the input. Default is None.
    --output-type (str, optional): The type of file for the output. Default is None.

    Example usage:
    python pipeline.py input.csv output.data --input-type nddem --output-type mercury
    """
    parser = argparse.ArgumentParser(description="Perform a full analysis of a sand sample.")
    parser.add_argument("input_file", type=str, help="The path to the input file")
    parser.add_argument("output_file", type=str, help="The path to the output file")
    parser.add_argument("--input-type", type=str, help="The type of file for the input.", default=None)
    parser.add_argument("--output-type", type=str, help="The type of file for the output", default=None)

    args = parser.parse_args()

    convert(args.input_file, args.output_file, input_type=args.input_type, output_type=args.output_type)


def convert(input_file, output_file, input_type=None, output_type=None):
    """
    Convert a file from one DEM format to another.

    Parameters:
    input_file (str): Path to the input file.
    output_file (str): Path to the output file.
    input_type (str, optional): Type of the input file. If None, the type will be guessed from the file extension.
    output_type (str, optional): Type of the output file. If None, the type will be guessed from the file extension.

    Raises:
    FileNotFoundError: If the input file does not exist.
    ValueError: If the input type or output type cannot be determined, or if they are unknown, or if they are the same.

    Returns:
    None
    """

    if not os.path.exists(input_file):
        raise FileNotFoundError("The input file does not exist.")

    if input_type is None:
        input_type = guess_type(input_file)
        if input_type is None:
            raise ValueError("Could not determine input type from file extension. Please specify the input type.")

    if output_type is None:
        output_type = guess_type(output_file)
        if output_type is None:
            raise ValueError("Could not determine output type from file extension. Please specify the output type.")

    if input_type not in known_input_types:
        raise ValueError(f"Unknown input type: {input_type}. Known types are: {', '.join(known_input_types)}")

    if output_type not in known_input_types:
        raise ValueError(f"Unknown output type: {output_type}. Known types are: {', '.join(known_input_types)}")

    if input_type == output_type:
        raise ValueError("Input and output types are the same. No conversion needed.")

    print(f"Converting {input_file} ({input_type}) to {output_file} ({output_type})")

    data, headers, metadata = getattr(pandem.io, input_type).load(input_file)
    getattr(pandem.io, output_type).save(data, headers, metadata, output_file)

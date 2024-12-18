import os
import numpy
import argparse
import subprocess
import pandas as pd
from tqdm import tqdm
import pandem.io.mercury


def conversion_script():
    parser = argparse.ArgumentParser(description="Perform a full analysis of a sand sample.")
    parser.add_argument("input_file", type=str, help="The path to the input file")
    parser.add_argument("output_file", type=str, help="The path to the output file")
    parser.add_argument("--input-type", type=str, help="The type of file for the input.", default=None)
    parser.add_argument("--output-type", type=str, help="The type of file for the output", default=None)

    args = parser.parse_args()

    convert(args.input_file, args.output_file, input_type=args.input_type, output_type=args.output_type)


def convert(input_file, output_file, input_type=None, output_type=None):

    if not os.path.exists(input_file):
        print("The input file does not exist.")
        return
    else:
        pass

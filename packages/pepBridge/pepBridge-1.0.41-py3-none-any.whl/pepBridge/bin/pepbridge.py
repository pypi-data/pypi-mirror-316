#!/usr/bin/env python3
import sys
import argparse
import os
import pkg_resources
from pepBridge import MatchingMZ

def positive_number(value):
    # Convert to float and check if the number is positive
    ivalue = float(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is not a positive number.")
    return ivalue

def read_options(args=sys.argv[1:]):

    # construct the argument parser
    parser = argparse.ArgumentParser(
        description="Easy way to match MALDI-MSI (m/z) peaks to the peptides (m/z) from LC-MS/MS",
        epilog='Written by Carlos Madrid-Aliste.'
    )
    
    # add the positional arguments to the Argument Parser
    parser.add_argument("--maldi", type=str, default='maldi.ini', help="location of the MALDI INI file.")
    parser.add_argument("--lcms" , type=str, default='lcms.ini', help="location of the LCMS INI file.")
    
    # type=float ensures that the argument is converted to a float.
    # If the user enters a non-numeric value, argparse will automatically raise an error.
    #parser.add_argument("--mass",  type=float, default='1.0', help="Mass tolerance in Da (float number) (default=1.0 Da)")
    parser.add_argument("--mass",   type=positive_number, default='1.0', help="Mass tolerance in Da (float number) (default=1.0 Da)")
    parser.add_argument("--output", type=str, default='matched_results_1.0.csv', help="Output file in CSV format.")
    
    # Add a --version argument
    # The action="version" automatically handles displaying the version when the 
    # user specifies the --version argument. The version argument uses pkg_resources.get_distribution('pepBridge').version 
    # to dynamically fetch the version of the package as defined in setup.py
    parser.add_argument("--version", action="version",
        version=f"pepBridge {pkg_resources.get_distribution('pepBridge').version}",
        help="Show the version of pepBridge."
    )

    # parse arguments from terminal
    opts = parser.parse_args(args)
    
    # manually catching mistakes
    if not opts.maldi:  
        parser.error("MALDI INI file is required\nPlease type pepBridge --help")
    if not opts.lcms:   
        parser.error("LCMS INI file is required\nPlease type pepBridge --help")

    return opts
        
def main():
    # call the function to read the argument values
    opts = read_options(sys.argv[1:])
    
    m_file = opts.maldi
    l_file = opts.lcms
    delta  = opts.mass       # Mass tolerance in Daltons
    output_filename = opts.output  # Name of the output file
    #output_filename = f"matched_results_{delta}.csv"
    
    if not os.path.exists(m_file):
        sys.exit(f"{m_file} does not exists in current directory.\n")
    if not os.path.exists(l_file):
        sys.exit(f"{l_file} does not exists in current directory.\n")
        
    # Initialize the MatchingMZ object with the provided INI files
    matcher = MatchingMZ(maldi_ini_file=m_file, lcms_ini_file=l_file, debug=False)
    
    # Perform the matching
    matches = matcher.match_maldi_in_lcms(delta=delta)
    
    # Write the results to a CSV file
    matcher.write(matches, output_filename)
    
if __name__ == "__main__":
    main()

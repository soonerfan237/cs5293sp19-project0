# -*- coding: utf-8 -*-
# Example main.py
import argparse

import project0

def main(url):
    print("test")

    # Download data
    print(url)
    project0.fetchincidents(url)

    # Extract Data
    project0.extractincidents()
	
    # Create Dataase
    project0.createdb()

    # Insert Data
    project0.populatedb()
	
    # Print Status
    project0.status()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--arrests", type=str, required=True, 
                         help="The arrest summary url.")
     
    args = parser.parse_args()
    if args.arrests:
        main(args.arrests)

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
    incidents = project0.extractincidents()
	
    # Create Dataase
    #db = project0.createdb()
	
    # Insert Data
    #project0.populatedb(db, incidents)
	
    # Print Status
    #project0.status(db)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--arrests", type=str, required=True, 
                         help="The arrest summary url.")
     
    args = parser.parse_args()
    if args.arrests:
        main(args.arrests)

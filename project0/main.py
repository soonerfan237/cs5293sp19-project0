# -*- coding: utf-8 -*-
# Example main.py
import argparse
import project0

def main(url):

    # Download data
    project0.fetchincidents(url) #calling method to download pdf to tmp folder

    # Extract Data
    incidents = project0.extractincidents() #extracting incidents from pdf
	
    # Create Dataase
    db = project0.createdb() #creating norman pd database

    # Insert Data
    project0.populatedb(db, incidents) #populating database with incidents
	
    # Print Status
    project0.status(db) #printing random record


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--arrests", type=str, required=True, 
                         help="The arrest summary url.")
     
    args = parser.parse_args()
    if args.arrests:
        main(args.arrests)

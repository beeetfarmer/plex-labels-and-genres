#!/usr/bin/env python3
import argparse
import sys

from plex_labels_and_genres.plex_connect import connect_to_plex, get_tv_library
from plex_labels_and_genres.metadata import update_from_csv
from plex_labels_and_genres.export import export_tv_shows_to_csv

def main():
    # Set up CLI arguments
    parser = argparse.ArgumentParser(description='Manage Plex TV Show labels and genres')
    parser.add_argument('--export', action='store_true', 
                        help='Export TV shows to CSV')
    parser.add_argument('--output', default='plex_tv_shows.csv', 
                        help='Output CSV filename')
    parser.add_argument('--csv-file', 
                        help='Import metadata from CSV file')
    parser.add_argument('--update-labels', action='store_true', 
                        help='Update labels from CSV')
    parser.add_argument('--update-genres', action='store_true', 
                        help='Update genres from CSV')
    parser.add_argument('--update-all', action='store_true', 
                        help='Update both labels and genres')
    
    args = parser.parse_args()
    
    # Connect to Plex
    server = connect_to_plex()
    tv_library = get_tv_library(server)
    
    # Handle update-all flag
    if args.update_all:
        args.update_labels = True
        args.update_genres = True
    
    # Process based on arguments
    if args.csv_file:
        # Default to updating both if nothing specified
        if not args.update_labels and not args.update_genres:
            args.update_labels = True
            args.update_genres = True
            
        update_from_csv(tv_library, args.csv_file, args.update_labels, args.update_genres)
    elif args.export:
        export_tv_shows_to_csv(tv_library, args.output)
    else:
        # No action specified, just print basic usage
        parser.print_help()

if __name__ == "__main__":
    main()
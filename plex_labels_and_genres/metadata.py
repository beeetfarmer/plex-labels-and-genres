import csv
import sys
from . import config

def add_labels_to_show(show, labels, update_labels=True):
    """Add labels to a show if they don't already exist."""
    if not update_labels:
        return 0
        
    # Skip duplicates
    existing_labels = show.labels
    new_labels = [label for label in labels if label not in existing_labels]
    
    if new_labels:
        show.addLabel(new_labels)
        print(f"  Added labels: {', '.join(new_labels)}")
        return len(new_labels)
    else:
        print(f"  No new labels to add. Existing: {', '.join(existing_labels)}")
        return 0

def add_genres_to_show(show, genres, update_genres=True):
    """Add genres to a show if they don't already exist."""
    if not update_genres:
        return 0
        
    # Skip duplicates
    existing_genres = [genre.tag for genre in show.genres] if show.genres else []
    new_genres = [genre for genre in genres if genre not in existing_genres]
    
    if new_genres:
        for genre in new_genres:
            show.addGenre(genre)
        print(f"  Added genres: {', '.join(new_genres)}")
        return len(new_genres)
    else:
        print(f"  No new genres to add. Existing: {', '.join(existing_genres)}")
        return 0

def update_from_csv(library, csv_file, update_labels=True, update_genres=True):
    """Update TV shows metadata from a CSV file."""
    if not update_labels and not update_genres:
        print("Error: At least one of --update-labels or --update-genres must be specified.")
        return
        
    operations = []
    if update_labels:
        operations.append("labels")
    if update_genres:
        operations.append("genres")
    
    print(f"Updating {' and '.join(operations)} from CSV: {csv_file}")
    
    not_found_shows = []
    processed_count = 0
    skipped_count = 0
    labels_added_count = 0
    genres_added_count = 0
    
    # Try different encodings
    for encoding in config.CSV_ENCODINGS:
        try:
            print(f"Trying encoding: {encoding}")
            with open(csv_file, 'r', encoding=encoding) as file:
                reader = csv.DictReader(file)
                
                # Check for required column
                headers = reader.fieldnames
                if 'Title' not in headers:
                    print("Error: CSV file is missing the required 'Title' column.")
                    return
                
                # Warnings about missing columns
                if update_labels and 'Labels' not in headers:
                    print("Warning: 'Labels' column not found but --update-labels was specified.")
                if update_genres and 'addGenre' not in headers:
                    print("Warning: 'addGenre' column not found but --update-genres was specified.")
                
                # Process each row
                for row in reader:
                    title = row['Title'].strip()
                    year = row.get('Year', '').strip()
                    
                    # Skip if no data to update
                    labels_text = row.get('Labels', '').strip() if update_labels else ''
                    genres_text = row.get('addGenre', '').strip() if update_genres else ''
                    
                    if not labels_text and not genres_text:
                        print(f"Skipping '{title}' - no labels or genres specified")
                        skipped_count += 1
                        continue
                    
                    # Parse comma-separated values
                    labels = [label.strip() for label in labels_text.split(',') if label.strip()] if labels_text else []
                    genres = [genre.strip() for genre in genres_text.split(',') if genre.strip()] if genres_text else []
                    
                    # Find the show
                    results = []
                    if year and year.isdigit():
                        # Try with year first
                        results = library.search(title=title, year=int(year), libtype='show')
                        if not results:
                            # Fall back to title-only search
                            results = library.search(title=title, libtype='show')
                    else:
                        results = library.search(title=title, libtype='show')
                    
                    if not results:
                        print(f"Show not found: '{title}'{f' ({year})' if year else ''}")
                        not_found_shows.append(title)
                        continue
                    
                    # Get first match
                    show = results[0]
                    print(f"Processing: {show.title}{f' ({show.year})' if hasattr(show, 'year') else ''}")
                    
                    # Add metadata
                    labels_added = add_labels_to_show(show, labels, update_labels)
                    genres_added = add_genres_to_show(show, genres, update_genres)
                    
                    if labels_added > 0 or genres_added > 0:
                        processed_count += 1
                        labels_added_count += labels_added
                        genres_added_count += genres_added
                
                # If we got here, the encoding worked
                break
                
        except UnicodeDecodeError:
            # Try next encoding
            continue
        except FileNotFoundError:
            print(f"Error: CSV file '{csv_file}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error processing CSV: {e}")
            sys.exit(1)
    
    # Print summary
    print(f"\nSummary:")
    print(f"  Shows processed: {processed_count}")
    print(f"  Shows skipped (no data): {skipped_count}")
    print(f"  Shows not found: {len(not_found_shows)}")
    if update_labels:
        print(f"  Labels added: {labels_added_count}")
    if update_genres:
        print(f"  Genres added: {genres_added_count}")
    
    if not_found_shows:
        print("\nShows not found in Plex library:")
        for show in not_found_shows:
            print(f"  - {show}")
    
    # Sanity check
    if processed_count == 0 and skipped_count == 0 and len(not_found_shows) == 0:
        print("\nNo shows processed. Check your CSV format.")
        print("CSV should have 'Title' column and either 'Labels' or 'addGenre' columns.")
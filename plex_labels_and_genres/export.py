import csv

def export_tv_shows_to_csv(library, filename='plex_tv_shows.csv'):
    """Export all TV shows to a CSV file."""
    print(f"Exporting TV shows to {filename}...")
    
    # Get all shows
    shows = library.all(libtype='show')
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Year', 'Genres', 'Labels']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for show in shows:
            # Get genres
            genres = ', '.join([genre.tag for genre in show.genres]) if show.genres else ''
            
            # Get labels - handle Label objects correctly
            try:
                if hasattr(show.labels[0], 'tag') if show.labels else False:
                    # If labels are objects with tag attribute
                    labels = ', '.join([label.tag for label in show.labels]) if show.labels else ''
                else:
                    # If labels are strings
                    labels = ', '.join(show.labels) if show.labels else ''
            except (IndexError, AttributeError):
                # Fall back to empty string if any issues
                labels = ''
            
            writer.writerow({
                'Title': show.title,
                'Year': show.year if hasattr(show, 'year') else '',
                'Genres': genres,
                'Labels': labels
            })
            
    print(f"Exported {len(shows)} TV shows to {filename}")
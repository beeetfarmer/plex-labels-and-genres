# Plex Labels and Genres update tool

A utility for managing TV show labels and genres in Plex Media Server. This tool allows you to export existing metadata to CSV and import/update labels and genres from CSV files.

## Features

- Export all TV shows to CSV with titles, years, genres, and labels
- Import metadata from CSV to update your Plex library
- Add labels and genres to shows based on CSV data
- Automatic matching of shows by title and year

## Installation

```bash
# Clone the repository
git clone https://github.com/beeetfarmer/plex-labels-and-genres.git
cd plex-labels-and-genres

# Install the package
pip install -e .
```

## Configuration

Edit the `plex_labels_and_genres/config.py` file to set your Plex server URL, token, and library name.

```python
# Example configuration
PLEX_URL = 'http://localhost:32400'
PLEX_TOKEN = 'your-plex-token-here'
LIBRARY_NAME = 'TV Shows'
```

## Usage

### Export TV Shows to CSV

```bash
plex-metadata --export --output my_shows.csv
```

### Update Labels and Genres from CSV

```bash
plex-metadata --csv-file my_shows.csv --update-labels --update-genres
```

Or use `--update-all` to update both labels and genres:

```bash
plex-metadata --csv-file my_shows.csv --update-all
```

### CSV Format

Your CSV file should have the following columns:
- `Title` (required): Show title
- `Year` (optional): Show year for better matching
- `Labels` (optional): Comma-separated list of labels to add
- `addGenre` (optional): Comma-separated list of new genres to add
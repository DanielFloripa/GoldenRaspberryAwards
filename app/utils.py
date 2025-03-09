import csv
import os

def read_movielist_csv(file_path):
    movies = []
    if os.path.exists(file_path):
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                movies.append({
                    'year': row['year'],
                    'title': row['title'],
                    'studios': row['studios'],
                    'producers': row['producers'],
                    'winner': row['winner'] == 'yes'
                })
    return movies
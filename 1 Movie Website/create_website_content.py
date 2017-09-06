import media
import movie_trailer_viewer
import urllib2
import json
from bs4 import BeautifulSoup
import pickle
import os


# Change these to what you want
MOVIE_LIST_URL = "https://en.wikipedia.org/wiki/List_of_zombie_films"
NUM_MOVIES = 10


def get_wikidata_label(wikidata_id):
    """
    Given a Wikidata ID, gets the corresponding label for that ID.
    """
    curr_wikidata_url = "https://www.wikidata.org/wiki/Special:EntityData/%s.json" % wikidata_id
    curr_wikidata_resp = urllib2.urlopen(curr_wikidata_url)
    curr_wikidata = json.load(curr_wikidata_resp)
    label = curr_wikidata['entities'][wikidata_id]['labels']['en']['value']
    return label


def create_movie_objects():
    """
    Given a list of movies from Wikipedia and a total number of movies to
    display, create movie objects for the webpage. Skips movies it can't find
    either an image, trailer, or title for.
    """
    movies = []
    wikipedia_list_url = MOVIE_LIST_URL
    wiki_page = urllib2.urlopen(wikipedia_list_url)
    soup = BeautifulSoup(wiki_page, "lxml")
    movie_urls = []
    movie_table = soup.find('table', class_='wikitable')
    for row in movie_table.select('tr'):
        for link in row.select('a[href]'):
            wikipedia_url = "https://en.wikipedia.org" + link['href']
            movie_urls.append(wikipedia_url)
            break  # only need first link in table

    # get movie image from Wikipedia page
    count = 0
    trailers = {}
    for movie_url in movie_urls:
        if count < NUM_MOVIES:
            # get movie image from Wikipedia page
            try:
                img_url = ''
                wiki_movie_page = urllib2.urlopen(movie_url)
                soup = BeautifulSoup(wiki_movie_page, "lxml")
                for potential_image in soup.select('a.image img[src]'):
                    if potential_image['src'].endswith('.svg.png') or potential_image['src'].endswith('.svg.png 2x'):
                        continue  # skip these images - they're part of the Wikipedia header/footer
                    else:
                        img_url = "http:" + str(potential_image['src'])
                        break
                if not img_url:
                    continue
            except:
                continue

            title = movie_url.split('/')[-1]

            # check if movie trailer URL is saved from a previous run with the same settings
            trailer_url = ''
            if os.path.isfile('trailer_urls.pkl'):
                with open('trailer_urls.pkl', 'rb') as f:
                    trailer_urls = pickle.load(f)
                    if len(trailer_urls) == NUM_MOVIES:
                        trailer_url = trailer_urls[title]
            # if not, get movie trailer URL by searching YouTube
            if not trailer_url:
                try:
                    youtube_search = 'https://www.youtube.com/results?search_query=' + title.replace('_', '+') + '+trailer'
                    youtube_page = urllib2.urlopen(youtube_search)
                    soup = BeautifulSoup(youtube_page, "lxml")
                    trailer_url = soup.select('h3 a[href]')[0]
                    trailer_url = "http://www.youtube.com" + str(trailer_url['href'])
                    # store the trailer URL so you don't have to keep accessing YouTube
                    trailers[title] = trailer_url
                except:
                    continue

            # get movie metadata from Wikidata
            wikidata_url = "https://www.wikidata.org/w/api.php?action=wbgetentities&sites=enwiki&format=json&titles=" + title.replace('_', '%20')
            response = urllib2.urlopen(wikidata_url)
            wikidata = json.load(response)
            for key, value in wikidata['entities'].iteritems():
                wikidata_id = key

            # get clean movie title from Wikidata
            if 'labels' in wikidata['entities'][wikidata_id]:
                if 'en' in wikidata['entities'][wikidata_id]['labels']:
                    clean_title = wikidata['entities'][wikidata_id]['labels']['en']['value']
                else:
                    continue
            else:
                continue

            # get movie description from Wikidata
            if 'en' in wikidata['entities'][wikidata_id]['descriptions']:
                description = wikidata['entities'][wikidata_id]['descriptions']['en']['value']
            else:
                description = ''

            # get movie genres from Wikidata
            if 'P136' in wikidata['entities'][wikidata_id]['claims']:
                genre_ids = []
                for item in wikidata['entities'][wikidata_id]['claims']['P136']:
                    genre_id = item['mainsnak']['datavalue']['value']['id']
                    genre_ids.append(genre_id)
                # get genre names from Wikidata genre IDs
                genre_list = []
                for genre_id in genre_ids:
                    genre = get_wikidata_label(genre_id)
                    if genre.endswith(' film'):
                        genre = genre[:-5]
                    genre_list.append(genre)
                genres = ', '.join(genre_list)
            else:
                genres = ''

            # get movie subjects from Wikidata
            if 'P921' in wikidata['entities'][wikidata_id]['claims']:
                main_subject_ids = []
                for item in wikidata['entities'][wikidata_id]['claims']['P921']:
                    main_subject_id = item['mainsnak']['datavalue']['value']['id']
                    main_subject_ids.append(main_subject_id)
                # get subject names from Wikidata subject IDs
                subject_list = []
                for main_subject_id in main_subject_ids:
                    subjects = get_wikidata_label(main_subject_id)
                    subject_list.append(subjects)
                subjects = ', '.join(subject_list)
            else:
                subjects = ''

            # get movie publication year from Wikidata
            if 'P577' in wikidata['entities'][wikidata_id]['claims']:
                pub_date = wikidata['entities'][wikidata_id]['claims']['P577'][0]['mainsnak']['datavalue']['value']['time']
                pub_date = pub_date[1:-16]
            else:
                pub_date = ''

            # get movie directors from Wikidata
            if 'P57' in wikidata['entities'][wikidata_id]['claims']:
                director_ids = []
                for item in wikidata['entities'][wikidata_id]['claims']['P57']:
                    director = item['mainsnak']['datavalue']['value']['id']
                    director_ids.append(director)
                # get director names from Wikidata director IDs
                director_list = []
                for director_id in director_ids:
                    directors = get_wikidata_label(director_id)
                    director_list.append(directors)
                directors = ', '.join(director_list)
            else:
                directors = ''

            # get movie duration from Wikidata
            if 'P2047' in wikidata['entities'][wikidata_id]['claims']:
                duration = wikidata['entities'][wikidata_id]['claims']['P2047'][0]['mainsnak']['datavalue']['value']['amount']
                if '.' in duration:  # remove any decimal values
                    duration = duration.split('.')[0]
                duration = duration[1:] + ' minutes'
            else:
                duration = ''

            # create movie objects with metadata
            movies.append(media.Movie(clean_title,
                                      description,
                                      img_url,
                                      trailer_url,
                                      genres,
                                      subjects,
                                      pub_date,
                                      director,
                                      duration))
            count += 1
        else:
            break

    # if this is the first run, save trailer URLs for next time
    if not os.path.isfile('trailer_urls.pkl'):
        with open('trailer_urls.pkl', 'wb') as f:
            pickle.dump(trailers, f)

    return movies

movies = create_movie_objects()

# Create Movie Trailer Viewer HTML page to show the movies.
movie_trailer_viewer.open_movies_page(movies)

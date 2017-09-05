# Movie Website
This site grabs movies from any Wikipedia list (for example, [zombie films](https://en.wikipedia.org/wiki/List_of_zombie_films)) and displays them on a static webpage, where you can see its subject, genre, and duration, and click to view its trailer.

I created this site as part of the Udacity [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## Requirements
* [Python 2.7](https://www.python.org/downloads/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)

## Running the Website
1. Download the files `create_website_content.py`, `media.py`, and `movie_trailer_viewer_py` and save them in the same directory.
2. Edit the two variables at the beginning of `create_website_content.py` to your desired settings: the Wikipedia movie list you'd like to see (`MOVIE_LIST_URL`), and the number of movies from that list you'd like to include (`NUM_MOVIES`).
3. Run `create_website_content.py`. The program will create two files: `movie_trailer_viewer.html` (the static site) and `trailer_urls.pkl` (a file that stores YouTube URLs so you don't have to keep accessing the site). You only need to re-run `create_website_content.py` when you want to change what the site displays using the variables at the beginning of the file.

## Preview of the Site
To see what the site will look like, download and open `movie_trailer_viewer.html`.

Here's a quick preview:

![Preview of the movie website](http://github.com/ahegel/udacity-full-stack-nanodegree/blob/master/1%20Movie%20Website/images/site.png?raw=true)

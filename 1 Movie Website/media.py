import webbrowser

class Movie():
    """This class provides a way to store movie-related information"""

    def __init__(self, movie_title, movie_storyline, poster_image, trailer_youtube, movie_genre, movie_subject, movie_pub_year, movie_director, movie_duration):
        self.title = movie_title
        self.storyline = movie_storyline
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube
        self.genre = movie_genre
        self.subject = movie_subject
        self.pub_year = movie_pub_year
        self.director = movie_director
        self.duration = movie_duration

    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)

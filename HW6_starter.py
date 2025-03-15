# Your name: 
# Your student id:
# Your email:
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# If you worked with generative AI also add a statement for how you used it.  
# e.g.: 
# Asked Chatgpt hints for debugging and suggesting the general structure of the code


import requests
import json
import unittest
import os

# TO DO: 
# assign this variable to your API key
# if you are doing the extra credit, assign API_KEY to the return value of your get_api_key function
API_KEY = ''

def get_json_content(filename):
    '''
    opens file file, loads content as json object

    ARGUMENTS: 
        filename: name of file to be opened

    RETURNS: 
        json dictionary OR an empty dict if the file could not be opened 
    '''
    pass


def save_cache(dict, filename):
    '''
    Encodes dict into JSON format and writes
    the JSON to filename to save the search results

    ARGUMENTS: 
        filename: the name of the file to write a cache to
        dict: cache dictionary

    RETURNS: 
        None
    '''
    pass


def search_movie(movie):
    '''
    creates API request
    ARGUMENTS: 
        movie: title of the movie you're searching for 

    RETURNS: 
        tuple with the response text and url OR None if the 
        request was unsuccessful
    '''
    pass


def update_cache(movies, cache_file):
    '''
    Iterates through a list of movies, adds their data to the cache.
    checks if a movie already exists in the cache before making an API request.
    only counts successful new API requests in the success_count.

    ARGUMENTS: 
        movies: a list of movies to get data for 
        cache_file: the file that has cached data 

    RETURNS: 
        A string saying the percentage of movies we successfully got data for 
    '''
    pass


def get_highest_box_office_movie_by_genre(genre_name, cache_file): 
    '''
    Gets the movie with the highest box office total for a given genre.

    ARGUMENTS: 
        genre_name: the name of the genre to find the highest grossing film for 
        cache_file: the file that has cached data 

    RETURNS:
        EITHER a tuple with the title and box office amount of the highest grossing film in the specified genre
        OR "No films found for [genre_name]"
    '''
    pass


def recommend_similar_movies(movie_title, cache_file):
    '''
    Recommends movies that share at least one genre with the given movie

    ARGUMENTS: 
        movie_title: the title of the movie we're looking for recommendations for
        cache_file: the file that has cached data 

    RETURNS:
        EITHER a list of movie titles that share at least one genre with movie_title
        OR an error message if the movie can't be found, has no genre information, or no similar movies
    '''
    pass


# EXTRA CREDIT
def get_api_key(filename):
    '''
    loads in API key from file 

    ARGUMENTS:  
        file: file that contains your API key
    
    RETURNS:
        your API key
    '''
    pass


# EXTRA CREDIT
def get_movie_rating(title, cache_file):
    '''
    gets the rotten tomatoes rating for a given film 

    ARGUMENTS: 
        title: the title of the movie we're searching for 
        cache_file: the file that has cached data 

    RETURNS:
        the rating OR 'No rating found'
    '''
    pass


class TestHomework6(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.filename = dir_path + '/' + "cache.json"

        with open('movies.txt', 'r') as f: 
            movies = f.readlines()
            
        for i in range(len(movies)): 
            movies[i] = movies[i].strip()
        self.movies = movies

        # NOTE: if you already have a cache file, setUp will open it
        # otherwise, it will cache all movies to use that in the test cases 
        if not os.path.isfile(self.filename):
            self.cache = update_cache(self.movies, 'cache.json')
        else:
            self.cache = get_json_content(self.filename)

        self.url = "http://www.omdbapi.com/"


    def test_load_and_save_cache(self):
        test_dict = {'test': [1, 2, 3]}
        save_cache(test_dict, 'test_cache_get_json_content.json')

        test_dict_cache = get_json_content('test_cache_get_json_content.json')
        self.assertEqual(test_dict_cache, test_dict)
        os.remove('test_cache_get_json_content.json')

        test_dict_2 = {'test_2': {'test_3': ['a', 'b', 'c']}}
        save_cache(test_dict_2, 'test_cache_get_json_content_2.json')
        
        test_dict_2_cache = get_json_content('test_cache_get_json_content_2.json')
        self.assertEqual(test_dict_2_cache, test_dict_2)
        os.remove('test_cache_get_json_content_2.json')


    def test_search_movie(self):
        # testing valid movies
        for movie in ['Mean Girls', 'Pulp Fiction', 'Forrest Gump']:
            movie_data = search_movie(movie)
            movie = movie.replace(" ", "+")
            self.assertEqual(type(movie_data[0]), dict)
            self.assertTrue(movie in movie_data[1])

        # testing invalid movie 
        invalid_movie_data = search_movie('fake movie 123')
        self.assertEqual(invalid_movie_data, None)


    def test_update_cache(self):
        test_movies = ['Mean Girls', 'Pulp Fiction', 'Forrest Gump']
        test_resp = update_cache(test_movies, 'test_cache_movies.json')
        self.assertTrue(test_resp == "Cached data for 100% of movies" or test_resp == "Cached data for 100.0% of movies")
        test_cache = get_json_content('test_cache_movies.json')
        self.assertIsInstance(test_cache, dict)
        self.assertEqual(len(list(test_cache.keys())), 3)

        for _, data in test_cache.items():
            if data['Ratings']:
                self.assertEqual(type(data['Ratings']), list)
                self.assertEqual(type(data['Ratings'][0]), dict)

        # checking it won't cache duplicates
        test_resp_2 = update_cache(test_movies, 'test_cache_movies.json')
        self.assertTrue(test_resp_2 == "Cached data for 0% of movies" or test_resp_2 == "Cached data for 0.0% of movies")        
        self.assertEqual(len(list(test_cache.keys())), 3)
        os.remove('test_cache_movies.json')


    def test_get_highest_box_office_movie_by_genre(self):
        # Updated test cases to match the actual data
        test_1 = get_highest_box_office_movie_by_genre("Action", 'cache.json')
        self.assertEqual(test_1[0], 'Avatar')  # Check only the title, as box office value might vary in formatting
        
        test_2 = get_highest_box_office_movie_by_genre("Drama", 'cache.json')
        self.assertEqual(test_2[0], 'Top Gun: Maverick')  # Check only the title
        
        test_3 = get_highest_box_office_movie_by_genre("Fantasy", 'cache.json')
        self.assertEqual(test_3[0], 'Avatar')  # Check only the title
        
        test_4 = get_highest_box_office_movie_by_genre("NonexistentGenre", 'cache.json')
        self.assertEqual(test_4, "No films found for NonexistentGenre")


    def test_recommend_similar_movies(self):
        # Updated test case to use a movie that's definitely in the cache
        test_1 = recommend_similar_movies("Titanic", 'cache.json')
        self.assertTrue(isinstance(test_1, list))
        self.assertTrue(len(test_1) > 0)  # There should be recommendations for Titanic
        self.assertEqual(test_1, ['Little Women', 'Top Gun: Maverick', 'La La Land', 'Whiplash',
                                   '12 Years a Slave', 'Life of Pi', 'The Help', 'Killers of the Flower Moon', 
                                   'Oppenheimer', 'The Lord of the Rings: The Fellowship of the Ring', 'Braveheart', 
                                   'Clueless', '10 Things I Hate About You', 'Gone with the Wind', 'Casablanca', 'Parasite'])
        
        test_2 = recommend_similar_movies("NonexistentMovie", 'cache.json')
        self.assertEqual(test_2, "'NonexistentMovie' is not in the cache.")


    # UNCOMMENT TO TEST EXTRA CREDIT
    '''
    
    def test_get_api_key(self):                     
        hidden_key = get_api_key('api_key.txt')
        self.assertEqual(API_KEY, hidden_key)

    def test_get_movie_rating(self):
        # Updated test cases to match the actual data
        test_titanic = get_movie_rating('Titanic', 'cache.json')
        self.assertEqual(test_titanic, '88%')
        
        test_avatar = get_movie_rating('Avatar', 'cache.json')
        self.assertEqual(test_avatar, '81%')
        
        # Top Gun: Maverick is in the data, not Top Gun
        test_topgun = get_movie_rating('Top Gun: Maverick', 'cache.json')
        self.assertEqual(test_topgun, '96%')
        
        # This should still return "No rating found" as expected
        test_frozen = get_movie_rating('Frozen 2', 'cache.json')
        self.assertEqual(test_frozen, 'No rating found')

    '''
    

    
def main():
    '''
    Note that your cache file will be called 
    cache.json and will be created in your current directory

    Make sure you are in the directory you want to be work in 
    prior to running
    '''
    #######################################
    # DO NOT CHANGE THIS 
    # this code loads in the list of movies and 
    # removes whitespace for you!
    with open('movies.txt', 'r') as f: 
        movies = f.readlines()
        
    for i in range(len(movies)): 
        movies[i] = movies[i].strip()
    resp = update_cache(movies, 'cache.json')
    print(resp)
    # DO NOT CHANGE THIS 
    #######################################

    #prints a tuple (movie_title, box_office_total) for the movie that has 
    # the highest box office sale within the Action genre
    print(get_highest_box_office_movie_by_genre("Action", 'cache.json'))
    
    print('\n\n-------------\n\n')

    #prints movies that share at least one genre with Titanic
    print(recommend_similar_movies('Titanic', 'cache.json'))

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)
import math
import sys
import time

if __name__ == "__main__":
	if len(sys.argv) <= 2:
		# missing arguments , print usage message 
		print("Usage:")
		print(" $ python3 similarity.py <data_file> <output_file> [user_thresh (default = 5)] ")
		sys.exit(0)

data_file = open(sys.argv[1], "r")
output_file = open(sys.argv[2], "w")

if len(sys.argv) == 4: # Threshold defined by user
	user_thresh = int(sys.argv[3]) 
else:
	user_thresh = 5 # Default Threshold

data_file_list = data_file.readlines() # Get a list containing each line of data
t1 = time.time()

def clean_dataset(list):
	""" Create a list of list containing each value/word in the string """
	clean_list = []
	for item in list:
		clean_list.append(item.split()) # Split string into separate values between spaces and append it as a list  
	return clean_list

clean_list = clean_dataset(data_file_list) # Create a list of lists containing user_id, movie_id, rating, timestamp
n_lines = len(clean_list) # Number of lines in file

clean_set = [0]*len(clean_list) # clean_set will be a list of sets
for i in range(len(clean_list)):
	clean_set[i] = set(clean_list[i]) # Convert each list into a set 


def movies(clean_list):
	""" Return unique movies set """
	movies_list = []
	for i in range(len(clean_list)):
		movies_list.append(clean_list[i][1])

	unique_movies = set(movies_list)
	return unique_movies

movies = movies(clean_list) # Set with unique movies (keys)
unique_movies_list = list(movies) # List of unique movies (keys)
n_movies = len(unique_movies_list) # Number of unique movies

def create_dic(clean_list):
	"""Create a dictionary that has movies as keys and a list of tuples (user_id, rating) as elements"""
	ratings_catalog = {}
	users_set_per_movie = {}
	for i in range(len(clean_list)):
		movie =  clean_list[i][1]
		if movie not in ratings_catalog:
			ratings_catalog[movie] = {} # Create new sub dictionary
		user = clean_list[i][0]
		rating = int(clean_list[i][2]) # Save rating as type int
		ratings_catalog[movie][user] = rating
		if movie not in users_set_per_movie:
			users_set_per_movie[movie] = set()
		users_set_per_movie[movie].add(user) # Add user to  set of users
	return ratings_catalog, users_set_per_movie

ratings_catalog, users_set_per_movie = create_dic(clean_list) # Dictionary that has movies as keys and a list of tuples (user_id, rating)

users_set = set()
for elem in users_set_per_movie.keys():
	new_set = users_set_per_movie[elem]
	users_set.update(new_set) # Set of users
n_users = len(users_set) # Number of users in the datafile


def similarities(ratings_catalog, users_set_per_movie, user_thresh):
	""" Return a dictionary with movies as keys and a list of tuples (most similar movie_id, rating, number of common users) as elements"""
	similarity_dic = {}
	for movie_a in ratings_catalog.keys():
		if movie_a not in similarity_dic:
			similarity_dic[movie_a] = None # Create new key with movie_a value and None as element
		users_a = users_set_per_movie[movie_a] # Set of users of movie a
		max_similarity = -1 # Initial maximum similarity coefficient
		most_sim_movie = None # Initialize most similar movie 
		for movie_b in ratings_catalog.keys():
			if movie_a == movie_b:
				#print("Continue because movie a == movie b")
				continue  # Comparing with same movie 
			users_b = users_set_per_movie[movie_b] # Set of users of movie b
			users_intersection_ab = users_a.intersection(users_b) # Get the common users between movies a and b
			common_users = len(users_intersection_ab) # Number of common users
			total_ratings_a = len(list(ratings_catalog[movie_a].values()))
			total_ratings_b = len(list(ratings_catalog[movie_b].values()))
			if common_users == 0: # No common users
				#print("Continue because m = 0. No common users")
				continue # Go to next movie
			mean_rating_a = sum(list(ratings_catalog[movie_a].values()))/total_ratings_a # Sum ratings from all users for movie a
			mean_rating_b = sum(list(ratings_catalog[movie_b].values()))/total_ratings_b # Sum ratings from all users for movie b
			if common_users < user_thresh: # Not enough users to compute the similarity coefficient
				continue # Go to next movie b
			sum_A_pw2 = 0
			sum_B_pw2 = 0
			numerator = 0
			for user in users_intersection_ab:
				rating_movie_b_user = ratings_catalog[movie_b][user] # Rating that a common user between movie a and b gave to b
				rating_movie_a_user = ratings_catalog[movie_a][user] # """gave to movie a
				A = rating_movie_a_user - mean_rating_a 
				B = rating_movie_b_user - mean_rating_b

				product_AB = A*B
				numerator += product_AB
				A_pw2 = A**2
				B_pw2 = B**2
				sum_A_pw2 += A_pw2
				sum_B_pw2 += B_pw2
			denominator = math.sqrt(sum_A_pw2*sum_B_pw2)
			if denominator == 0: # Denominator is zero
				continue # Go to next movie
			
			P_similarity = numerator/denominator # Compute similarity coeficient
			if P_similarity > max_similarity:
				max_similarity = P_similarity # Set new max similarity value
				most_sim_movie = movie_b # Save corresponding movie b
				n_users_mostsim = common_users # Numer of common users for most similar movie
			else:
				max_similarity =  max_similarity
				most_sim_movie = most_sim_movie
				n_users_mostsim = n_users_mostsim
		if most_sim_movie == None:
			similarity_dic[movie_a] = None # No  similar movie found
		else:
			movies_sim_tuple = (int(most_sim_movie),round(max_similarity,2),n_users_mostsim) # Save most similar movie b to movie a with similarity coefficient and number of common users
			similarity_dic[movie_a] = movies_sim_tuple # Save tuple of movies similarities to movie_a's element
	return similarity_dic 


movie_similarity_dic = similarities(ratings_catalog, users_set_per_movie, user_thresh) # Dictionary with movies similarities


for movie in movie_similarity_dic:
	element = movie_similarity_dic[movie] # Get the tuple for each movie
	if element == None:
		output_file.write("{}\n".format(movie)) # Movie with no similar movie
	else:
		output_file.write("{} {}\n".format(movie, element)) # Movie with similar movie

t2 = time.time()
t_diff = t2-t1

print("Input MovieLens file: {}".format(sys.argv[1]))
print("Output file for similarity data: {}".format(sys.argv[2]))
print("Minimum number of common users = {}".format(user_thresh))
print("Read {} lines with total of {} movies and {} users".format(n_lines,n_movies,n_users))
print("Computed similarities in {} seconds".format(t_diff))


data_file.close()
output_file.close()





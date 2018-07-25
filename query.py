import os  
import json
import psycopg2
from operator import itemgetter
from datetime import datetime
import numpy as np
import scipy.spatial.distance
from sklearn.metrics.pairwise import cosine_similarity

from rosette.api import API, DocumentParameters, RosetteException


# range for distance:
	# 0 to =>.4
	# < .4 to >.8
	# > .8 


def get_input():
	search = raw_input('Input your search term: ')
	#distance = input('Select similarity distance from 0 to 10 (0=close, 10=far): ')

	api = API(user_key="", service_url="http://localhost:8181/rest/v1/")
	params = DocumentParameters()
	params["content"] = search

	try:
		vector = api.text_embedding(params)
		vector = vector.get("embedding")
		return vector
	except RosetteException as exception:
		print(exception)
	except:
		print('unkown error in get vector')


def get_docs():
	try:
		conn = psycopg2.connect("dbname='textvals' user='ec2-user' password='MikeBasis2'")
		cur = conn.cursor()

		cur.execute("SELECT * FROM documents WHERE doc_type = 'doc'")
		#cur.execute("SELECT * FROM documents")
		return cur.fetchall()

		cur.close()
	except psycopg2.DatabaseError as error:
		print(error)
	except:
		print('unkown error')
	finally:
		if conn is not None:
			conn.close()

def get_similarity(data, search_vector):
	#print("search_vector"+str(search_vector))
	results = []

	for row in data:
		#print(row[3])
		search_vector = np.asarray(search_vector)
		search_vector = search_vector.reshape(1,-1)

		doc_val = json.loads(row[3])
		doc_val = np.asarray(doc_val)
		doc_val = doc_val.reshape(1,-1)

		#print(search_vector)
		#print(doc_val)

		distance = scipy.spatial.distance.cdist(doc_val, search_vector, 'cosine')
		cosine_similarity(doc_val,search_vector)
		#distance_list.append(float(distance[0][0]))
		#print(distance[0][0])
		rlist = [row[0], row[1], row[2], distance[0][0], row[4]]
		results.append(rlist)


	return results
	#for elem in results:
		#print(elem)

def display_results(results):
	results = sorted(results, key=itemgetter(3))

	print("\n##############")
	print("### Top 5 results: ###\n")
	count = 0
	for elem in results:
		count += 1
		print("\t"+str(elem))
		if(count == 4):
			break

	results = sorted(results, key=itemgetter(3), reverse=True)

	print("\n##############")
	print("### Bottom 5 results: ###\n")
	count = 0
	for elem in results:
		count += 1
		print("\t"+str(elem))
		if(count == 4):
			break


search_vector = get_input()
startTime = datetime.now()
data = get_docs()
results = get_similarity(data,search_vector)
display_results(results)

#print datetime.now() - startTime 


import os  
import json
import psycopg2
from rosette.api import API, DocumentParameters, RosetteException

def save_vector(filepath, vector, filetype, sentence):
	try:
		conn = psycopg2.connect("dbname='textvals' user='ec2-user' password='MikeBasis2'")
		cur = conn.cursor()
		
		lang = vector.get('responseHeaders').get('X-RosetteAPI-ProcessedLanguage')
		vectors = str(vector.get("embedding"))

		print("file path is: "+filepath)
		print("vector is: "+vectors)
		print("lang is: "+lang)
		print("filetype is: "+filetype)
		print("sentences is: "+sentence)

		sentence = sentence.replace("'","''")

		cur.execute("INSERT INTO documents(doc_type, lang, file_path, vectors, sentence_native) VALUES('%s', '%s', '%s', '%s', '%s')" % (filetype, lang, filepath, vectors, sentence))
		conn.commit()
	except psycopg2.DatabaseError as error:
		print(error)
	except:
		print('unkown error')
	finally:
		if conn is not None:
			conn.close()

def get_vector(folder,file):
	f=open(folder+file, "r")
	embeddings_data =f.read()

	api = API(user_key="", service_url="http://localhost:8181/rest/v1/")
	params = DocumentParameters()
	params["content"] = embeddings_data
	
	try:
		vector = api.text_embedding(params)
		save_vector(file, vector, "doc", "")
	except RosetteException as exception:
		print(exception)
	except:
		print('unkown error in get vector')

	try:
		sentences = api.sentences(params)
		sentences = sentences.get('sentences')
		for x in sentences:
			params["content"]=x
			sentence_vector = api.text_embedding(params)
			save_vector(file, sentence_vector, "sen", x)
	except RosetteException as exception:
		print(exception)
	except:
		print('unkown sentence error')


def get_file(folder):
	for fn in os.listdir(folder):
		#print(fn)
		if os.path.isfile(folder+fn):
			#print (fn)
			get_vector(folder,fn)

folder = "/home/ec2-user/textembeddings/files/"
get_file(folder)
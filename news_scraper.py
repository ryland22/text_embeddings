import re
import newspaper
from newspaper import Article
from newspaper import fulltext

LIMIT = 1000

cnn_paper = newspaper.build('http://www.quo.es/')

count = 0
for article in cnn_paper.articles:
    
    article.download()
    article.parse()
    
    title = article.title
    #title = re.sub("[^a-zA-Z\s]+", "", title)
    title = title.replace(' ','-').lower()

    file = open("files/spa/"+title+".txt", 'w')
    file.write(article.text)
    file.close

    count += 1
    if count == LIMIT:
    	break
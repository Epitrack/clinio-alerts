FROM python:3.6
MAINTAINER João Gabriel Lima "joao.gabriel@epitrack.tech"

#
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
ENV PYTHONPATH $PYTHONPATH:/code

# INSTALL NLTK
RUN pip install -U nltk
ENV CORPORA punkt
ENV NEO4J_URL neo4j
ENV REDIS_URL redis

# INSTALL NLTK DEPENDENCES
CMD python -m nltk.downloader all;
CMD python -m nltk.downloader all-corpora;
#RUN python -m nltk.downloader brown
#RUN python -m nltk.downloader punkt
#RUN python -m nltk.downloader treebank
#RUN python -m nltk.downloader sinica_treebank
#RUN python -m nltk.downloader hmm_treebank_pos_tagger
#RUN python -m nltk.downloader maxent_treebank_pos_tagger
#RUN python -m nltk.downloader words
#RUN python -m nltk.downloader stopwords
#RUN python -m nltk.downloader names
#RUN python -m nltk.downloader wordnet
#RUN python -m nltk.downloader averaged_perceptron_tagger
#RUN python -m nltk.downloader popular
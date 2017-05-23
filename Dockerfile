FROM python:3.6
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
ENV PYTHONPATH $PYTHONPATH:/code

RUN pip install -U nltk
ENV CORPORA punkt
CMD python -m nltk.downloader punkt;
# Some corpus for nltk
RUN python -m nltk.downloader brown
RUN python -m nltk.downloader punkt
#
#RUN python3 -m nltk.downloader -d /usr/share/nltk_data treebank
#RUN python3 -m nltk.downloader -d /usr/share/nltk_data sinica_treebank
RUN python -m nltk.downloader hmm_treebank_pos_tagger
RUN python -m nltk.downloader maxent_treebank_pos_tagger
#
RUN python -m nltk.downloader words
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader names
RUN python -m nltk.downloader wordnet

FROM catenae/link:develop
COPY instagram_scraper.py /opt/catenae
RUN pip install pygram

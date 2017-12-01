#!/usr/bin/env python2.7

import psycopg2
from datetime import datetime
import sys

DBNAME = 'news'


def executeQuery(query, param=None):
    '''
    Take a string query and execute the query.
    Return a list of tuples.
    '''
    try:
        db = psycopg2.connect(database=DBNAME)
    except psycopg2.OperationalError as e:
        print 'Unable to connect to database.'
        print e
        sys.exit(1)
    c = db.cursor()
    if param:
        c.execute(query, (param,))
    else:
        c.execute(query)
    rows = c.fetchall()
    db.close()
    return rows


def top_n_articles(n=3):
    '''
    Return the top n articles by number of views.
    '''
    query = """SELECT articles.title, COUNT(*) as views
               FROM articles INNER JOIN log
               ON log.path = '/article/' || articles.slug
               WHERE log.status like '200%'
               GROUP BY articles.title
               ORDER BY views DESC
               LIMIT (%s)"""
    top_n_articles = executeQuery(query, int(n))
    return top_n_articles


def popular_authors():
    '''
    Return the most popular authors by number of views.
    '''
    query = """SELECT authors.name, COUNT(*) as views
               FROM articles
               INNER JOIN authors ON articles.author = authors.id
               INNER JOIN log ON log.path = '/article/' || articles.slug
               WHERE log.status like '200%'
               GROUP BY authors.name
               ORDER BY views DESC"""
    popular_authors = executeQuery(query)
    return popular_authors


def days_with_error(n=1):
    '''
    Return days when more than n% of requests were errors.
    '''
    query = """SELECT day, perc FROM (
                 SELECT day, ROUND(
                   (SUM(requests)/(SELECT COUNT(*) FROM log
               WHERE time::date = day) * 100), 2)
                 AS perc FROM (
                   SELECT time::date AS day,
                     COUNT(*) AS requests
                   FROM log
                   WHERE status LIKE '%404%'
                   GROUP BY day)
                 AS log_percentage
                 GROUP BY day
                 ORDER BY perc DESC)
               AS result
               WHERE perc >= (%s)"""
    errors = executeQuery(query, int(n))
    return errors

if __name__ == '__main__':
    n_articles = 3
    error_perc = 1

    top_3_articles = top_n_articles(n_articles)
    top_authors = popular_authors()
    error_days = days_with_error(error_perc)
    with open('output.txt', 'w') as f:
        s1 = '1. What are the most popular {} articles of all time?\n'
        f.write(s1.format(n_articles))
        for article in top_3_articles:
            f.write(article[0] + ', ' + str(article[1]) + ' views\n')
        f.write('\n2. Who are the most popular article authors of all time?\n')
        for author in top_authors:
            f.write(author[0] + ', ' + str(author[1]) + ' views\n')
        s3 = ('\n3. On which days did more than '
              '{}% of requests lead to errors?\n')
        f.write(s3.format(error_perc))
        for error in error_days:
            clean_date = datetime.strptime(error[0], '%Y-%m-%d')
            f.write(clean_date.strftime('%B %-d, %Y') +
                    ', ' + str(error[1]) + '% errors')

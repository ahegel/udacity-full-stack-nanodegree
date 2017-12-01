# Logs Analysis with SQL

In this project, I build an internal reporting tool for a newspaper website that determines what kinds of articles the site's readers like. I use SQL to analyze a database with over a million rows and answer three queries with the data:

1. What are the most popular three articles?
2. Who are the most popular article authors?
3. On which days did more than 1% of requests lead to errors?

This project is part of the Udacity [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## Technologies Used

* SQL
* Python
* [Vagrant](https://www.vagrantup.com/)
* [VirtualBox](https://www.virtualbox.org/)

## Setup

1. Ensure that Python, the python package [psycopg2](https://pypi.python.org/pypi/psycopg2), [Vagrant](https://www.vagrantup.com/), and [VirtualBox](https://www.virtualbox.org/) are installed. (The vagrantfile I used is [here](https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile).)
2. Download or clone the [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository.
3. Download the [SQL database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip), unzip, and save `newsdata.sql` in the vagrant directory.
4. Navigate to the vagrant folder in the terminal and enter `vagrant up` to bring the server online, followed by `vagrant ssh` to log in.
5. To run the SQL queries directly, navigate to the vagrant directory with `cd /vagrant`, then enter `psql -d news -f newsdata.sql` to connect to and run the project database.
6. To execute the program in this repo, run `python logs_analysis.py`.

## Database

The SQL script to create the data (downloadable [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)) results in a database called 'news' with three tables:

* The `articles` table includes information about news articles and their contents.
* The `authors` table includes information about the authors of articles.
* The `log` table includes one entry for each time a user has accessed the news site.

## SQL Queries

You can view the output of the SQL commands below in the [output.txt](https://github.com/ahegel/udacity-full-stack-nanodegree/blob/master/3%20Logs%20Analysis/output.txt) file in this repo.

1. What are the most popular three articles of all time?

    ```sql
    SELECT articles.title, COUNT(*) as views
    FROM articles INNER JOIN log
    ON log.path = '/article/' || articles.slug
    WHERE log.status like '200%'
    GROUP BY articles.title
    ORDER BY views DESC
    LIMIT 3
    ```

2. Who are the most popular article authors of all time?

    ```sql
    SELECT authors.name, COUNT(*) as views
    FROM articles
    INNER JOIN authors ON articles.author = authors.id
    INNER JOIN log ON log.path = '/article/' || articles.slug
    WHERE log.status like '200%'
    GROUP BY authors.name
    ORDER BY views DESC
    ```

3. On which days did more than 1% of requests lead to errors?

    ```sql
    SELECT day, perc FROM (
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
    WHERE perc >= 1
    ```
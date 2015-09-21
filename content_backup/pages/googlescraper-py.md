Title: GoogleScraper.py
Date: 2013-12-27 14:25
Author: admin
Slug: googlescraper-py
Status: published

GoogleScraper - A simple module to scrape and extract links from Google. {#googlescraperasimplemoduletoscrapeandextractlinksfromgoogle}
========================================================================

### What does GoogleScraper? {#whatdoesgooglescraper}

GoogleScraper parses Google search engine results easily and in a
performant way. It allows you to extract all found links/link titles/
link descriptions and the total results for you query problematically
and your application can do whatever it want with them (Probably some
SEO related research)

There are unlimited use cases:

-   Quickly harvest masses of [google
    dorks](http://www.webvivant.com/google-hacking.html "Google Dorks").
-   Use it as a SEO tool.
-   Discover trends.
-   Compile lists of sites to feed your own database.
-   Many more use cases...

GoogleScraper is implemented with the following techniques/software:

-   Written in Python 3.3
-   Uses multihreading/asynchronous IO (Uses
    [twisted](http://twistedmatrix.com/trac/ "twisted framework")).
-   Supports parallel google scraping with multiple IP addresses.
-   Provides proxy support using
    [socksipy](https://code.google.com/p/socksipy-branch/ "Socksipy Branch"):
    -   Socks5
    -   Socks4
    -   HttpProxy
-   Support for additional google search futures.
-   Includes exhaustive research of similar projects!

### Example Usage {#exampleusage}

    import GoogleScraper
    import urllib.parse

    if __name__ == '__main__':

        results = GoogleScraper.scrape('HOly shit', number_pages=1)
        for link_title, link_snippet, link_url in results['results']:
            # You can access all parts of the search results like that
            # link_url.scheme => URL scheme specifier (Ex: 'http')
            # link_url.netloc => Network location part (Ex: 'www.python.org')
            # link_url.path => URL scheme specifier (Ex: ''help/Python.html'')
            # link_url.params => Parameters for last path element
            # link_url.query => Query component
            try:
                print(urllib.parse.unquote(link_url.geturl())) # This reassembles the parts of the url to the whole thing
            except:
                pass

    # How many urls did we get?
    print(len(results['results']))

    # How many hits has google found with our keyword?
    print(results['num_results_for_kw'])

### Example Output {#exampleoutput}

This is a [example
output](http://incolumitas.com/wp-content/uploads/2013/12/links.txt "example output of search query")
of the above *use.py*:

### Direct command line usage {#directcommandlineusage}

In case you want to use GoogleScraper.py as a CLI tool, use it somehow
like this:

    python GoogleScraper.py -p 1 -n 25 -q 'inurl:".php?id=555"'

But be aware that google might recognize you pretty fast as a abuser if
you use such google dorks.

Maybe try a socks proxy then (But don't bet on TOR) [This is just a
example, this socks will probably not work anymore when *you are here*]

    python GoogleScraper.py -p 1 -n 25 -q 'i hate google' --proxy="221.132.35.5:2214"

### Contact

If you feel like contacting me, do so and send me a mail. You can find
my contact information on my
[blog](http://incolumitas.com/about/contact/ "Contact with author").

### To-do list (As of 25.12.2013) {#todolistasof25122013}

-   Figure out whether to use threads or asynchronous I/O for multiple
    connections.
-   Determine if is is possible to use one google search session with
    multiple connections that are independent of each other (They have
    different IP's)

### Stable version {#stableversion}

This is a development repository. But you can always find a [working
GoogleScraper.py script
here](http://incolumitas.com/2013/01/06/googlesearch-a-rapid-python-class-to-get-search-results/).

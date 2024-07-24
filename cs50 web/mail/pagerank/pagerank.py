import os
import random
import re
import sys
import numpy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # this is a dict which keys link the page to its probability that it will be selected
    visit_next = {}
    for link in corpus:
        visit_next[link] = 0

    # check if page has any outgoing links
    if len(corpus[page]) == 0:
        # add a equal probability that the next page will be any rondom one in the corpus
        for link in corpus:
            visit_next[link] = 1/len(corpus)
        return visit_next

    # set the probobility of all the outgoing links to the division of len(outgoinglinks)/0.85
    for link in corpus[page]:
        visit_next[link] =  visit_next[link] + damping_factor/len(corpus[page])

    # add the dampning factor to all the links
    for link in corpus:
        visit_next[link] = visit_next[link] + (1-DAMPING)/len(corpus)

    return visit_next

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # set the current page to a random one
    page = random.choice(list(corpus.keys()))

    # iniatalize a dict for the amount of times a page was picked
    times_page_picked = {key: 0 for key in corpus.keys()}

    # call the transition_model n times
    for i in range(n):
        # get the probability for each page given the current page
        next_page_distro = transition_model(corpus, page, damping_factor)

        # get all the pages and there corresponding pick probabilitys
        pages = list(next_page_distro.keys())
        probability = list(next_page_distro.values())

        # pick a new page based on the probabilitys
        page = numpy.random.choice(pages, p=probability)

        # update the times_page_picked dict
        times_page_picked[page] = times_page_picked[page] + 1

    # create a new dict to store the pr(p) in decimal form
    pr_of_p = {key: 0 for key in corpus.keys()}

    # get the percentage of times a page was chosen
    for k, v in times_page_picked.items():
        times_in_decimal = int(v)/n
        pr_of_p[k] = times_in_decimal

    return pr_of_p

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # setting some vars
    d = damping_factor
    N = len(corpus)

    # create a dict to store the probability and set the probability of all pages to the same value
    PR = {key: 1/N for key in corpus.keys()}

    # make a temp pr for iterations
    temp_PR = {key: 1/N for key in corpus.keys()}

    # make a while loop to iterate over the corpes
    while True:
        # get all the keys in the corpus
        for k in corpus:
            # set the summation to 0
            summation = 0
            # get all the pages in the corpus
            for page in corpus:
                # check if the a page links to the current key
                if k in corpus[page]:
                    # if yes add to the summation the PR of the page that links to the key and divide it by the number of pages that page links to
                    summation += PR[page]/ len(corpus[page])

            # set the temp_PR of the page to the probability we will get on that page by picking it at random or from being on a page and choosing the link to the page
            temp_PR[k] = (1-d)/N + d * summation

        # set a flag for convergence
        convergence = 0

        # check if all the values in temp_PR did not change more than 0.001 and set convergence if thats the case
        for k, v in temp_PR.items():
            if abs(PR[k] - temp_PR[k]) >= 0.001:
                convergence = convergence + 1

        if convergence == 0:
            return PR

        # set whats in temp_pr to PR
        for k, v in temp_PR.items():
            PR[k] = temp_PR[k]


if __name__ == "__main__":
    main()

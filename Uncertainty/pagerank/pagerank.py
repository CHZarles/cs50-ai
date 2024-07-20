import os
import random
import re
import sys

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
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.



    cropus is represented by a dict
    {
        "3.html": {"2.html", "4.html"},
        "4.html": {"2.html"},
        "2.html": {"1.html", "3.html"},
        "1.html": {"2.html"},
    }
    """

    d = damping_factor
    # probability of choosing a link at random
    trans_probability = {}  # get links inside page
    links = corpus[page]
    # apportion portion of probability to each link, and they should sum up to 1 - d
    nums = len(links)
    # if there are no links, return a probability distribution that's evenly distributed
    if nums == 0:
        for page_ in corpus:
            trans_probability[page_] = 1 / len(corpus)
    else:
        # calculate the probability for each link
        prob = d / nums

        # create a probability distribution for the links
        for link in links:
            trans_probability[link] = prob

        # add the remaining probability to the pages without links
        for page_ in corpus:
            if page_ not in trans_probability:
                trans_probability[page_] = (1 - d) / len(corpus)
            else:
                trans_probability[page_] += (1 - d) / len(corpus)
    # print(corpus)
    # print(page)
    # print(trans_probability)
    return trans_probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    d = damping_factor

    # define a function that returns the next page base on the probability distribution
    def choose_page_randomly(probability: dict) -> str:
        # return a random page based on the probability distribution
        return random.choices(
            population=list(probability.keys()),
            weights=list(
                probability.values()
            ),  # attention, it must be weitghts=, not cum_weights=
            k=1,
        )[0]

    # begin sampling
    trans_probability = {page: 1 / len(corpus) for page in corpus}
    # a dict record sampling result for each page
    records = {page: 0.0 for page in corpus}
    sampling_times = n
    while n > 0:
        # choose a page at random
        page = choose_page_randomly(trans_probability)
        # calc page_rank according to formulation
        records[page] += 1
        # generate a new trans_probability
        trans_probability = transition_model(corpus, page, d)
        # next iteration
        n -= 1
    # calc the pangrank for each page
    for page in records:
        records[page] /= sampling_times

    return records


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    d = damping_factor
    # set initial page rank
    page_rank = {page: 1 / len(corpus) for page in corpus}

    # if the page doesn't link to any page, it shoudl be interpretd as linking to all pages, includeing itself
    backup_corpus = corpus.copy()
    for page in corpus:
        if len(corpus[page]) == 0:
            corpus[page] = set(corpus.keys())

    # a data structure records pages that link to the page
    links_to_page = {page: set() for page in corpus}
    for page in corpus:
        for link in corpus[page]:
            links_to_page[link].add(page)

    # do iterations algorithm until convergence ( PageRank value change no more than 0.001 )
    flag = True
    while flag:
        # copy the current page_rank
        new_page_rank = page_rank.copy()
        # update the page rank
        for page in corpus:
            new_page_rank[page] = (1 - d) / len(corpus)
            # iterate partent page
            for link in links_to_page[page]:
                new_page_rank[page] += d * page_rank[link] / len(corpus[link])
        # check convergence
        max_change = max(abs(new_page_rank[page] - page_rank[page]) for page in corpus)
        page_rank = new_page_rank

        if max_change < 0.001:
            flag = False

    # recover the corpus
    corpus = backup_corpus

    return page_rank


if __name__ == "__main__":
    main()

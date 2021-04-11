import gzip, json
import re
import random
import pronouncing
import markovify
from collections import defaultdict
from typing import List


## Helper functions (largely from aparrish's examples)

def generate_poetry_corpus_lines() -> List:
    """Returns a list of all lines from Gutenberg poetry corpus"""
    # TODO: do this quicker -- hm
    all_lines = []
    for line in gzip.open("gutenberg-poetry-v001.ndjson.gz"):
        all_lines.append(json.loads(line.strip()))
    return all_lines

def generate_rhyming_part_defaultdict() -> defaultdict:
    """Returns a default dict structure of 
    keys: Rhyming parts (strs)
    values: defaultdicts,
    of words corresponding to that rhyming part (strs)
    : lists of lines that end with those words (lists of strs)"""
    all_lines = generate_poetry_corpus_lines()
    by_rhyming_part = defaultdict(lambda: defaultdict(list))
    for line in all_lines:
        text = line['s']
        if not(32 < len(text) < 48): # only use lines of uniform lengths
            continue
        match = re.search(r'(\b\w+\b)\W*$', text)
        if match:
            last_word = match.group()
            pronunciations = pronouncing.phones_for_word(last_word)
            if len(pronunciations) > 0:
                rhyming_part = pronouncing.rhyming_part(pronunciations[0])
                # group by rhyming phones (for rhymes) and words (to avoid duplicate words)
                by_rhyming_part[rhyming_part][last_word.lower()].append(text)
    return by_rhyming_part

def get_random_line() -> str:
    """Returns a random line from the poetry corpus"""
    all_lines = generate_poetry_corpus_lines()
    lines = [line['s'] for line in all_lines]
    return random.choice(lines) # For example, a string: "And his nerves thrilled like throbbing violins"

#####

# get defaultdict of rhymes
by_rhyming_part = generate_rhyming_part_defaultdict()

# TODO: get a random word, or a word from user input
# For now: input word with typing
selected_word = "other" #"grandmother"
phones = pronouncing.phones_for_word(selected_word)[0]
rhyming_part_for_word = pronouncing.rhyming_part(phones)

# TODO: maybe 1 selected word for non rhyming? and 1 for rhymes?
# So like, get couplets from selected word and then get random things about another word for lines between the couplets?

# TODO: shuffle the rhymes so it's not always in the same order

# Check whether seletcted word's rhyme part has > 1 word
# if rhyming_part_for_word in by_rhyming_part.keys():
# print("check!!", type(by_rhyming_part[rhyming_part_for_word]))

    


####

# Poetry generation

def generate_stanza():
    # If there are at least 2 different words to rhyme from this word,
    if len(by_rhyming_part[rhyming_part_for_word].keys()) > 2:
        
        for k in by_rhyming_part[rhyming_part_for_word]:
            # print(k) # word in rhyme group - a string
            # print(by_rhyming_part[rhyming_part_for_word][k]) # list of sentences that each end in word k
            print(random.choice(by_rhyming_part[rhyming_part_for_word][k]))
        # TODO: Do this ^ two or three times (for 3 words k) but not more
        # Then follow with a (random) other line.
        # TODO generate random line here.
        random_line = get_random_line()
        print(random_line + ".") # TODO: only add . when it isn't already a period or -,
        # TODO: if it's a comma, remove the comma at end and replace with period (?)

    # But if there aren't, 
    else:
    # use the selected word to grab the non-rhyming line.
        pass


def generate_poem():
    # TODO: shouldn't be the _same_ word or lines intially
    # should just be like...seeded by it? Have to decide now to 'choose' next stanza material
    generate_stanza()
    generate_stanza()
    generate_stanza()

# TODO: if the stanzas are long, they get fewer


generate_poem()

#### Expts

# lines_with_word = [line['s'] for line in all_lines if re.search(fr"\b{selected_word}\b", line['s'], re.I)]
# print(random.sample(lines_with_word,12))
# # note: important that the sample amount not be longer than how many exist so can't just have a number if getting user input -- or have to handle that properly
# # or could just pick from a selected set of words, tbd


# set the amount of repetition -- like some value and determine what that means
# and use that to determine whether 

# could have some specification of rhyme schemes (AABB)
# or surprise me
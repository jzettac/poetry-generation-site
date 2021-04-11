import gzip, json
import re
import random
import pronouncing
import markovify
from collections import defaultdict


## Helper functions (largely from aparrish's examples)

def generate_poetry_corpus_lines():
    # TODO: do this quicker -- hm
    all_lines = []
    for line in gzip.open("gutenberg-poetry-v001.ndjson.gz"):
        all_lines.append(json.loads(line.strip()))
    return all_lines

def generate_rhyming_part_defaultdict():
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

#####

# get defaultdict of rhymes
by_rhyming_part = generate_rhyming_part_defaultdict()

# TODO: get a random word, or a word from user input
# For now: input word with typing
selected_word = "grandmother"
phones = pronouncing.phones_for_word(selected_word)[0]
rhyming_part_for_word = pronouncing.rhyming_part(phones)

# TODO: maybe 1 selected word for non rhyming? and 1 for rhymes?
# So like, get couplets from selected word and then get random things about another word for lines between the couplets?

# Check whether seletcted word's rhyme part has > 1 word
# if rhyming_part_for_word in by_rhyming_part.keys():
# print("check!!", type(by_rhyming_part[rhyming_part_for_word]))

def get_random_line():
    # Select a random rhyming part
    random_rhyming_part = random.choice(list([x for x in by_rhyming_part.keys() if len(by_rhyming_part[x]) >= 1]))
    # random_rhyming_part, by_rhyming_part[random_rhyming_part]
    
# test
get_random_line()

####

# If there are at least 2 different words to rhyme from this word,
if len(by_rhyming_part[rhyming_part_for_word].keys()) > 2:
    # print(by_rhyming_part[rhyming_part_for_word])
    for k in by_rhyming_part[rhyming_part_for_word]:
        print(k) # word in rhyme group - a string
        # print(by_rhyming_part[rhyming_part_for_word][k]) # list of sentences that each end in word k
        print(random.choice(by_rhyming_part[rhyming_part_for_word][k]))
    # TODO: Do this ^ two or three times (for 3 words k) but not more
    # Then follow with a (random) other line.
    # TODO generate random line here.

# But if there aren't, 
else:
   # use the selected word to grab the non-rhyming line.
    pass


# Get a random number -- 3, and/or a random number less than or equal to ((the # of words in the sentence >= 5 chars) - 1)
# So that we're selecting a random "important" word in the sentence, UNLESS it's a sentence without clearly useful words






#### Expts

# lines_with_word = [line['s'] for line in all_lines if re.search(fr"\b{selected_word}\b", line['s'], re.I)]
# print(random.sample(lines_with_word,12))
# # note: important that the sample amount not be longer than how many exist so can't just have a number if getting user input -- or have to handle that properly
# # or could just pick from a selected set of words, tbd
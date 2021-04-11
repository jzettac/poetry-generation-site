import gzip, json
import re
import random
import pronouncing
import markovify
from collections import defaultdict
from typing import List

# TODO: major refactor lol lol

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

# # get defaultdict of rhymes
# by_rhyming_part = generate_rhyming_part_defaultdict()

# # TODO: get a random word, or a word from user input
# # For now: input word with typing
# selected_word = "other" #"grandmother"
# phones = pronouncing.phones_for_word(selected_word)[0]
# rhyming_part_for_word = pronouncing.rhyming_part(phones)

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
        rhyming_options = list(by_rhyming_part[rhyming_part_for_word].keys())
        random.shuffle(rhyming_options)
        for k in rhyming_options:
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


# def generate_poem():
#     # TODO: shouldn't be the _same_ word or lines intially
#     # should just be like...seeded by it? Have to decide now to 'choose' next stanza material
#     generate_stanza()
#     generate_stanza()
#     generate_stanza()

# # TODO: if the stanzas are long, they get fewer


# generate_poem()



class Poem:
    def __init__(self, seed_word):
        self.all_lines = generate_poetry_corpus_lines()
        self.by_rhyming_part = self.generate_rhyming_part_defaultdict()
        # Set up ability to seed by word, TODO neaten
        self.seed_word = seed_word
        phones = pronouncing.phones_for_word(self.seed_word)[0]
        self.rhyming_part_for_word = pronouncing.rhyming_part(phones)

    def generate_rhyming_part_defaultdict(self) -> defaultdict:
        """Returns a default dict structure of 
        keys: Rhyming parts (strs)
        values: defaultdicts,
        of words corresponding to that rhyming part (strs)
        : lists of lines that end with those words (lists of strs)
        Code borrowed directly from Allison Parrish's examples."""
        by_rhyming_part = defaultdict(lambda: defaultdict(list))
        for line in self.all_lines:
            text = line['s']
            # TODO: potentially - select line length input options
            # Uniform lengths original: if not(32 < len(text) < 48)
            if not(32 < len(text) < 100): # only use lines of uniform lengths
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

    def get_random_line(self) -> str:
        """Returns a random line from the poetry corpus"""
        lines = [line['s'] for line in self.all_lines]
        return random.choice(lines) # For example, a string: "And his nerves thrilled like throbbing violins"

    def handle_line_punctuation(self):
        pass

    def generate_stanza(self):
        stanza_list = []

        # If there are at least 2 different words to rhyme from this word,
        if len(self.by_rhyming_part[self.rhyming_part_for_word].keys()) >= 2:
            rhyme_options_source = self.by_rhyming_part[self.rhyming_part_for_word]
            rhyming_options = list(rhyme_options_source.keys())
            random.shuffle(rhyming_options) # Don't always have the words that rhyme in the same order in each stanza
            if len(rhyming_options) > 8: # Don't have it do more than # rhymes, too many
                # TODO: select number here, maybe vary from 3 to 8 or something where possible - as limit, not actual count, using this if stmt
                # TODO: some randomness in how many per stanza or something???
                rhyming_options = rhyming_options[:8] # TODO variation here?
            for k in rhyming_options:
                # print(k) # word in rhyme group - a string
                # print(by_rhyming_part[rhyming_part_for_word][k]) # list of sentences that each end in word k
                # print(random.choice(rhyme_options_source[k]))
                stanza_list.append(random.choice(rhyme_options_source[k]))
            # Then follow with a (random) other line.
            random_line = get_random_line()
            # print(random_line + ".") # TODO: only add . when it isn't already a period or -,
            # TODO: if it's a comma, remove the comma at end and replace with period (?)
            stanza_list.append(random_line + ".")

        # TODO TODO TODO
        # But if there aren't, 
        else:
        # use the selected word to grab the non-rhyming line.
        # get a totally random word for the rhyming stanza and do that thing. 
        # or a couplets thing!
            pass

        return stanza_list

    def generate_poem(self):
        # TODO checks in generate stanza could potentially go _here_ instead
        # TODO add in certainty that there won't be too much repetition that's silly
        # TODO maybe add in check in stanza that we don't use every single rhyme each time if there are > 5, but make sure to use a random set for each stanza !!
        # TODO full idea here is that there can be input to the stanza generator that happens here (in the poem generator) -- break up the machine

        # TODO clean up all the silly additional newline char concats

        self.full_poem = ""
        # If each stanza using all the rhymes will be 
        # if len(self.by_rhyming_part[self.rhyming_part_for_word].keys()) <= 3:

        # Now: controlling len of stanza and such, but always doing 3
        self.full_poem += "\n".join(self.generate_stanza())
        self.full_poem += "\n\n"
        self.full_poem += "\n".join(self.generate_stanza())
        self.full_poem += "\n\n"
        self.full_poem += "\n".join(self.generate_stanza())

        # if len(self.by_rhyming_part[self.rhyming_part_for_word].keys()) > 3:
        #     self.full_poem += "\n".join(self.generate_stanza())
        #     self.full_poem += "\n"
        #     self.full_poem += "\n".join(self.generate_stanza())
        return self.full_poem


    def __str__(self):
        return self.generate_poem()


# TODO: indicate why a word doesn't generate a poem if it doesn't?
# TODO the else
p = Poem("bird")
print(p)








#### Expts

# lines_with_word = [line['s'] for line in all_lines if re.search(fr"\b{selected_word}\b", line['s'], re.I)]
# print(random.sample(lines_with_word,12))
# # note: important that the sample amount not be longer than how many exist so can't just have a number if getting user input -- or have to handle that properly
# # or could just pick from a selected set of words, tbd


# set the amount of repetition -- like some value and determine what that means
# and use that to determine whether 

# could have some specification of rhyme schemes (AABB)
# or surprise me


# IDEAS:
# Random lines could be a couplet OR a random line
# Variation in numbers of rhymes per stanza > 3 and < say 8, up to limit of what there is

# End with a couplet? Stanza, stanza, stanza-with-couplet. (Would help last lines feel final?) Or sometimes?
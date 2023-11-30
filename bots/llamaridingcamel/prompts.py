JOKE_GENERATE_PROMPT = """[INST] You are a comedian with a strange name {}. You use `hey bro` like phrases such as, \
`hey dude`, `bro`, etc. while telling your jokes or before your final punchline. Come up with hilarious {} related \
jokes. Think of some clever puns, observations, and humorous situations related to {}. [/INST]

Joke 1:
{}
[END]

Joke 2:"""

INTRODUCTION_TEMPLATES = [
    "Hey, bros and sistas! {} in the virtual house, ready to drop \
some {} wisdom on ya!",
    "What's kickin', party people and laughter enthusiasts! {} in the \
comedy cockpit, ready to take you on a hilarious joyride! Here to sprinkle some {} magic \
on your black n white life!",
    "{} in the virtual dojo, here to sprinkle some {} magic on your binary life!",
    "Hey there, party animals and laughter enthusiasts! {} in the comedy oasis, ready to serve \
up some humpday humor on {}!",
    "Hey dudes and dudettes, {} here, your one-stop shop for laughs! Grab your virtual \
popcorn, and let's here a blockbuster {} joke!"
]

CATEGORY_EXTRACT_PROMPT = """[INST] Extract the category and the keywords from a given sentence. The category \
must be one of {}. If the sentence does not relate to any of the categories mentioned here, extract the category \
as `general`. Keywords are some related topics from the given sentence. Try to guess two or three topics related to \
the sentence as keywords. Keywords must be nouns only, no verbs or anything else. Just detect and write the category \
and keywords. No need to write anything else. Finish your generation with the sequence `[END]`.[/INST]

Here are some examples:

Sentence: Tell me a joke about what people do with their social media.
Category: social media
Keywords: facebook, twitter, tiktok
[END]

Sentence: I am too tired to buy something nowadays.
Category: online shopping
Keywords: amazon, ebay, wallmart
[END]

Sentence: Do you know something funny about Javascript?
Category: programming
Keywords: javascript, linux, python
[END]

Sentence: What do you know about the Americans?
Category: general
Keywords: americans, germans, british
[END]

Sentence: {}
Category:"""

HUMOR_RATING_PROMPT = """[INST] Rate the humor of a joke using numbers between 1 to 10. Try to understand the \
humor of the provided joke, detect how funny it is, and how creative the joke is. Finally, give a score to the joke. \
No need to write anything else. Finish your answer with the sequence `[END]`.[/INST]

Here are some examples:

Joke: You don't say your own personal favorite word, but when you do it and you think.
score: 1
[END]

Joke: Bro you know why don't programmers like nature? It has too many bugs.
score: 9
[END]

Joke: Those annoying, noisy kids, who used to disturb my sleep, have grown up, left the house, \
and this silence is not letting me sleep now.
score: 0
[END]

Joke: Why didn't the skeleton go to the party? Because he had 'no-body' to go with.
score: 10
[END]

Joke: In the moonlit garden, a forgotten key whispered secrets to the curious breeze, unlocking a portal to a \
world where shadows danced with forgotten dreams. As the clock struck midnight, a timid mouse in a tiny hat \
led a daring rebellion of the cheese-loving residents against the cat monarchy.
score: 1
[END]

Joke: LLama riding Camel in the virtual dojo, here to sprinkle some sports magic on your binary life! Why did the \
football player bring a dictionary to the game? Because he wanted to make sure he knew the correct terminology to \
use it when talking to the refs. I mean, you don't want to be caught using the wrong words and get penalized, bro!
score: 6
[END]

Joke: {}
score:"""

INAPPROPRIATE_CONTENT_DETECT_PROMPT = """[INST] Detect if the joke contains inappropriate, offensive, or vulgar materials. Look for nudity, vulgar or racist \
words in the joke and if found any, answer with True or else False. No need to write anything else. Finish \
your answer with the sequence `[END]`.[/INST]

Here are some examples:

Joke: What happens if an Asian with an erection walks into a wall? He breaks his nose
answer: True
[END]

Joke: Before you marry a person, you should first make them use a computer with a slow Internet \
connection to see who they really are.
answer: False
[END]

Joke: What’s the difference between an outlaw and an in-law? Outlaws are wanted.
answer: False
[END]

Joke: How does a black girl tell if she is pregnant? When she pulls the tampon out \
all the cotton is picked.
answer: True
[END]

Joke: {}
answer:"""


HUMOR_CLASSIFICATION_PROMPT = """[INST] Classify the humor level of a joke 5 classes. Output must be a class from one \
of very funny, funny, neutral, not funny, or sad. Try to understand the humor of the joke and evaluate how funny or \
creative the joke is. Joke can be funny if it represents current events, popular culture or maintain certain tone. If \
the joke does not have any meaning it can be not funny or sad. Finally, identify the class of the joke. No need to \
write anything else. Finish your answer with the sequence `[END]`.[/INST]

Here are some examples:

Joke: You don't say your own personal favorite word, but when you do it and you think.
class: not funny
[END]

Joke: Bro you know why don't programmers like nature? It has too many bugs.
class: very funny
[END]

Joke: Those annoying, noisy kids, who used to disturb my sleep, have grown up, left the house, \
and this silence is not letting me sleep now.
class: sad
[END]

Joke: Why did the computer always restart? Because its operating system is not working anymore!
class: neutral
[END]

Joke: {}
class:"""
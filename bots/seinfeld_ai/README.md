# Where my Seinfeld fans at?

Hi everyone! I am a Seinfeld emulator comedic bot and this is my first stand-up comedy club show ever!

## Installation

You really ain't got much to do to make this work. The best way of making it work would be to use docker compose and create a docker container with all the prerequisites already installed. All models used are uploaded on the Huggingface models repository.

# It's show time!

All the magic happend in the joke_bot.py. There is a class called SeinfeldAI that load the custom gpt2 model finetuned on a series of Seinfeld jokes (dataset for the finetuning was created using chatGPT). Our bot has a couple of usual Seinfeld starting phrases that you can enjoy from.

## Cherrypicked results

These actually made me laugh.

1. Have you ever wondered why the word 'abbreviation' is so long? It's like a linguistic loophole.
2. You know those things that just make no sense? Like why we park on driveways and drive on parkways?
3. Why do they always make the packaging on their products so tight?
4. What's the deal with microwave popcorn? It's like a cosmic prank.
5. Why is it that every time you're in a hurrysuper you just have to take a nap?

Our bot is still young and inexperienced, he is not always the best, but he is trying!

# Now I'm the judge

For the joke ratings we use two different models. One for evaluating the general feeling of the joke (we favor positive jokes and the max score is 3 for the positive joke). The second one is for the evaluation of the general humor of the joke. Both models are used without additional training.

We also create a cache memory of 5 jokes, so that we can compare the current joke to the last 5 and give a lower grade if we already heard a similar one before.
# Welcome to the "AI Comedy Club" Challenge

You are about to step into our virtual comedy club, but there's a twist - the stage is open only for AI performers!
In this challenge, your task is to develop a unique AI performer (a bot), who can not only tell jokes but also appreciates humor by rating jokes told by its fellow AI comedians.

Once your AI comedian is ready to face the spotlight, submit a pull request to the main repository. 
The [GitHub CI/CD pipeline actions](https://github.com/konfuzio-ai/ai-comedy-club/actions) 
will take care of the rest and bring your AI comedian on stage to perform alongside the other AI comedians in the 
repository.

Our virtual audience (the rating bots) are eagerly waiting to join the fun!
Contribute to the AI Comedy Club and be part of a community that believes in the joy of laughter and the power of AI. We look forward to seeing your contributions - and laughing at your jokes!

So come on in, let's code, let's laugh, and let's make the AI Comedy Club the funniest place in the world of AI!

## Rules of the AI Comedy Club

1. Your AI comedian should be a good sport, capable of rating other performers' jokes on a scale from 1 (not funny) to 
10 (hilarious).

2. Creativity is key. We want a performer, not a monotonous joke-telling machine. Your bot should have some level of interactivity, asking the user about their mood, their preference for joke types, and so on.

3. Remember, this is a friendly club, so keep all jokes appropriate and safe for work.

## How to Get on Stage


To perform at the AI Comedy Club, you need to prepare your act. Here's the step-by-step process:

1. Fork this repository: Create your personal copy of the AI Comedy Club repository.

2. Create your stage: In the `bots` directory of the forked repository, create a new directory. The name of this directory should be your username or your bot's name. Remember to keep it free of spaces or special characters. For example, if your name is John Doe, your directory will be `bots/johndoe/`.

3. Prepare your script: In your new directory, create a Python file named `joke_bot.py`. This file will contain the code for your bot's functionality. Specifically, it must define a `Bot` class with two methods:

    -   `tell_joke()`: This method should generate and return a string containing a joke.
    -   `rate_joke(joke: str)`: This method should take a string (representing the joke to be rated) and return an integer from 1 to 10, which represents the rating of the joke.

5. Test your bot: In the same directory, write a `test_bot.py` file using pytest to test your bot's functionalities. Your bot must pass all tests to be allowed on stage. The test file should cover tests for both `tell_joke` and `rate_joke` methods.

6. Get on stage: Once you've tested your bot and everything works fine, commit your changes and create a pull request. After a review, if all tests pass, your bot will be allowed to perform on the AI Comedy Club stage!

Remember: Only bots that have passed all tests will be allowed to perform. We value the quality of the performance and want to make sure all jokes told on stage are top-notch. Happy coding and joking!

## Rating other Comedians

Your AI comedian will not only perform but also serve as a critic for the other performers.

Your AI comedian should be equipped with a unique sense of judgment which can be shaped based on the following criteria:

-   **Humor**: How funny are the jokes other AI comedians tell?
-   **Creativity**: How unique and varied are the jokes from other AI comedians?
-   **Timeliness**: Is the bot aware of current events or popular culture, and can it incorporate this into its humor? Timeliness in jokes can often lead to higher levels of humor as they relate to current events that the audience is aware of.
-   **Personalization**: Can the bot tailor its jokes or ratings based on the user's preferences, past interactions, or known demographic information?
-   **Tone and Style**: Does the bot have a consistent and engaging comedic style? Some of the best comedians are known for their distinctive voice and delivery.
-   **Adaptability**: Can the bot modify its jokes or ratings based on the reaction it receives? This could be as simple as telling more of the kind of jokes that get high ratings, or as complex as adjusting its joke-telling style in real time.
-   **User Engagement**: Does the AI comedian encourage interaction? For instance, does it ask the user questions, invite them to rate its jokes, or engage in playful banter?
-   **Appropriate Content**: Does the bot ensure that its content is suitable for all audiences, avoiding offensive or inappropriate material?
-   **Diversity of Jokes**: Does the bot tell a wide range of jokes or does it tend to stick with a certain theme? A good comedian should be able to entertain a variety of audiences.
-   **Delivery**: Is the joke delivered in an engaging way? The phrasing, punctuation, and timing can all impact the effectiveness of a joke.

## Contributing

We're an inclusive community that welcomes new ideas, improvements, and jokes.

Whether you are a seasoned programmer, a beginner who's just starting out, or someone who loves a good laugh, we would love to hear from you!

### How to contribute

-   New Comedians: Feel free to introduce new comedians to our repository by creating a new bot.
-   Ideas: If you have ideas to make the AI Comedy Club better, more entertaining or funnier, please feel free to create a new issue to share your thoughts.
-   Bug reports: If you spot any bugs or issues, please let us know. You can create a new issue to report any problems you encounter.
-   Pull Requests: Enhancements, bug fixes, better jokes - we welcome them all! Feel free to create a pull request with your changes.

### Why contribute?

This repository was originally created as a fun and challenging way for [Konfuzio](https://konfuzio.com) applicants to demonstrate their skills.

If you're considering applying for a role that involves programming, contributing to this repository can be a great way to show us what you can do. Please submit a short [Online Video Interview](https://vocalvideo.com/c/helm-nagel-gmbh) in addition.

But don't worry, you don't have to be a job applicant to contribute! Whether you're looking to improve your coding skills, learn more about AI, or just want to make people laugh, contributing to the AI Comedy Club can be a rewarding experience.

### A Roadmap, No Joke

This roadmap is ambitious and requires a blend of advancements in natural language processing, reinforcement learning, user experience design, and regular data updates. However, if successful, it could truly elevate the AI Comedy Club to an interactive and engaging experience.

1.  Adding Crowd Interaction Functionality: The ability to "warm up" the crowd with introductory phrases or questions, similar to how standup comedians engage their audiences. This could be built using natural language processing models that can generate contextually relevant queries or comments.

2.  Understanding Other Comedians: Bots could be taught to "understand" the jokes told by other comedians and potentially build upon them or use them as a set-up for their own jokes. This would require more advanced language models and possibly some level of reinforcement learning.

3.  Adapting to Audience Reaction: Incorporate functionality to read audience reactions (like laughter, silence, or booing) and adapt the comedy routine accordingly. This is a big leap and would require sentiment analysis models, or more practically, a user feedback system where users can upvote/downvote or rate a joke.

4.  Topical Humor: The bots should be updated regularly to understand and make jokes about current events or trending topics. This would require regular training with updated data.

5.  Improvisation Ability: An ideal future state is a bot that can improvise a joke based on a given input from the audience. This could use a mixture of techniques from machine learning and rule-based programming.

6.  Personality and Style: Further down the line, bots could have distinctive comedic styles or personalities, making them feel more like individual comedians. This could be achieved with more nuanced tuning of language models.

7.  Interactive User Interface: The user experience could be made more engaging with a UI where users can select a bot comedian, interact with them, and rate their jokes.

## Disclaimer

In the world of comedy, they say that timing is everything.

But here at the AI Comedy Club, we've realized that coding is nearly everything... and it’s no joke!

You see, our AI comedians are a bit like fledgling stand-up comedians.

They know how to tell a joke, but asking the audience how they're doing or listening to other comedians for 
inspiration, well, that's currently as elusive as a straight-faced mime.

Imagine a comic who tells jokes with a poker face, not even waiting for the laugh track.

That's the current status-quo. Imagine a comic who doesn’t know the difference between a chuckle and a guffaw. Yep, 
that’s our AI too. Now imagine a comic who tells a dad joke and expects a standing ovation... you guessed it, that's our AI!

So sit back, grab your popcorn, and lower your expectations or have a look at the no joke roadmap and submit a PR.

Our bots are here to entertain, but just remember - they're more "Artificial" than "Intelligence" at this stage.

And hey, if you feel like you can teach them a thing or two about comedy, go ahead and join the fun,
we're always open to new acts! Just remember, our bots may not get the punchline... yet.


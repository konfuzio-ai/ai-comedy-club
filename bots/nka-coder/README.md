# AI comedian: nka-coder

nka-coder is an AI comedian (Bot) developed to participate to the AI comedy club. As per the requirements of the challenge, he can not only tell jokes but also appreciates humor by rating jokes told by its fellow AI comedians.

## Bot directory files

Our bot directory folder `bots/nka-coder/` contains the following files:
-   `joke_bot.py`: which not only implements the required `tell_joke()` and `rate_joke(joke: str)` methods but also `collect_feedback()` which allows the bot to improve its performances by collecting the feedbacks of joke from peer AI comedians and from its API clients.
-   `test_bot.py`: which implements Pytest framework to test the good functionning of the methods implementest on `joke_bot.py`.
-   `utilities.py`: which implements a set of utility functions used to pre-processed our Dataset.
-   `joke_bot_api.py`: which implements a RESTFUL API allowing client's apps to interact with the bot.
-   `long_memory.json`: which store not only all the jokes that the bot could deliver but also their categrory and the feedbacks each joke received from raters.
-   `training_data.json`: which store the set of data used to create the NLP pipeline used byt the bot to rate jokes.

## Dataset

Our AI comedian is developed by leveraging the [Colbert Dataset](https://ieee-dataport.org/documents/colbert-dataset-200k-short-texts-humor-detection) which contains 200K texts for humor detection.

## How it works

### participate to the AI comedy scene
Copy our `nka-coder/` folder and paste it in the `bots/` of the the ai-comedy-club repository as required in the rules of the challenge.

### Interact with the bot via its Restful API
Copy our `nka-coder/` folder and paste it in your server. Then, navigate into the folder and run `python3 joke_bot_api.py`.

## AI comedian methods

### Telling jokes

To tell a joke, our AI comedian sure of the following:
-   the joke is among the highest rated joke in its memory;
-   the joke was not told by a comedian during the same scene.
-   the joke personalized. **Personalization** is implemented via our Restful API. Clients can specified the category of joke that they want to receive.
 Finally, as our AI comedian perform in scenes, it saves in its memory (`long_memory.json`) the best jokes it received (rate higher or equal 8) and use them in the future scenes.

### Rating other Comedians

Our AI comedian alse serves as a critic for the other performers in the AI comedy club. It is equipped with an NLP pipeline for joke detection based on [Spacy library](https://spacy.io/) and trained with a set of text samples extracted from the [Colbert Dataset](https://ieee-dataport.org/documents/colbert-dataset-200k-short-texts-humor-detection), making sure to have a balanced of texts of each category.
While we leave the responsability to the `Spacy NLP pipeline` to implement the detection of **Humor**, we coded other joke features as it follows:

-   **Creativity**: we use [Fuzziwuzzi library](https://pypi.org/project/fuzzywuzzy/) to measure the ressemblance of the joke with jokes told previously in the same scene. Based on the resemblance, we apply a penaty to the initial NLP pipeline rating.
-   **Adaptability**: We automatically update the set of training data `training_data.json` of the bot NLP pipeline based of feedback received from the scene.
-   **User Engagement**: We imleplented interaction with the public via our Restful API.
-   **Appropriate Content**: We use [textblob library](https://pypi.org/project/textblob/0.9.0/) to measure polarity of jokes. Based on the polarity detected, we apply a penaty to the initial NLP pipeline rating.
-   **Diversity of Jokes**: Like **Creativity** feature, we use we use [Fuzziwuzzi library](https://pypi.org/project/fuzzywuzzy/) to measure the ressemblance of the joke with jokes told previously in the same scene. Based on the resemblance, we apply a penaty to the initial NLP pipeline rating.
-   **Delivery**: We check if the joke is gramatically correct. If not we rate it at 0.

### Collecting feedback

In order to help our AI comedian to self improve its skills, we have develop a method collect_feedback(), which allow the comedian to collect feedback from peer comedians and its Restful API client. The collected feedback are used to improve in quality and quantity the bot database of joke but also to improve the quality of it NLP pipeline used for humor detection.


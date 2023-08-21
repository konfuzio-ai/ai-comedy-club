import random
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from textblob import TextBlob
import pyttsx3 as t2s

class JokeBot:
    def __init__(self):
        self.name = "etexaco123"
        # self.jokes_by_type = ["Animal", "Puns", "Knock-Knock", "Lightbulb", "Lawyer", "Animal", "Tech"]
        # self.jokes_by_type = ["Animal", "Dad", "College", "Children", "Sports", "Religious", "Tech", "Bar", "Lightbulb"]
        self.jokes_by_type = {
            "Animal": [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the chicken go to the seance? To talk to the other side!",
                "Q: Where do cows go on Saturday nights? \r\nA:  To the moovies",
                "Did you hear about the scientists who crossed a porcupine with a sheep?  They got an animal that knits its own sweaters.",
                "Thats a bunch of cows.\r\nFarmer: No, a herd.\r\nGuy1: Of course I've heard of cows.\r\nFarmer:.No, I mean the cow herd\r\nGuy1: I have no secrets from cows",
                "Why did the chicken cross the playground?\r\n\r\nTo get to the other slide!",
                "I found a way to make a horse stand perfectly still. Place a bet on him.",
                "What does the lion say to his friends before they go out hunting for food? \r\n\r\n\"Let us prey.\"",
                "What do you call a pig who knows karate? \r\n\r\n A Pork-Chop!",
                "What's the difference between a Scot and Mick Jagger?\r\n\r\nMick Jagger sang \"Hey, you, get offa my cloud.\"\r\n\r\nThe Scot says \"Hey, McCloud, get offa my ewe.\"",
                "Where does Batman's goldfish live ?\r\n\r\n\r\nIn the BAT-TUB!! ahahaha...",
                "Q. What happens when you cross a Bulldog with a Shih tzu? \r\nA. You get Bullshit.",
                "Q: What do you get when you cross a kangaroo and a sheep?\r\n\r\nA:  A sweater with pockets",
                "Q: What do you get when you cross a snake and a kangaroo?\r\n\r\nA:  A jump rope",
                "How do you know that carrots are good for your eyesight?\r\nHave YOU ever seen a rabbit with glasses?",
                "Q: What's invisible and smells like carrots?\r\n \r\nA: Bunny farts!",
                "What is the difference between a BMW & a porcupine? \r\nA porcupine has pricks on the outside.",
                "Did you hear about the scientists who crossed a porcupine with a sheep?  They got an animal that knits its own sweaters.",
                "If a rabbit were racing cabbage, who would win?\r\n\r\nThe cabbage, because it's a head.",
                "Why do ducks have webbed feet? \r\nTo stamp out fires. \r\nWhy do elephants have flat feet? \r\nTo stamp out burning ducks.",
                "Q: What does a fish use to get high?\r\n\r\nA: Seaweed!",
                "How do you keep a Rhino from charging?\r\n\r\nTake away its credit card.",
                "A horse walked into a bar.\r\nThe barman said,\r\n\"Why the long face?\"",
                "Two fish swim into a concrete wall. One turns to the other and says \"Dam\".",
                "Did you hear the one about the Polish wolf?\r\n\r\nHe chewed off three legs and was still caught in the trap.",
                "What do you call a cow jumping over a barbed wire fence?\r\n\r\nUtter destruction.",
                "What do you call a cow with no legs?\r\n\r\nGround Beef!",
                "A waiter on a ship said to a boarding lion \"sir, do you want anything of the chef's special?\" The lion said \"nah..I'll look at the passenger list,though!\"",
                "Mik: \"Do skunks have a good sense of smell?\"\r\nMak: \"No! If they did, they'd jump off a cliff!\"",
                "Why did the chicken cross the road? To get away from the butcher",
                "What is it called when your pet snake doesn't feel right?\r\n\r\n-reptile dysfunction.",
                "What do you get if you cross a dinosaur, a tiger, a crocodile, a spider, and a elephant?\r\n I don't know but you better get out of it's way!",
                "My wife and I were at an outdoor shopping mall, and I came across what I thought was a 'life-sized' chess board. So I began playing chess solo. Ten moves in, my wife comes by and says, \"Honey, that's a cr\u00c3\u00a8che!\"",
                "My dog Minton has eaten my shuttle cock.  Bad Minton!",
                "Paddy tells Mick he's thinking of buying a Labrador dog.\r\n\r\n\"Oh, I wouldn't if I were you!\", says Mick. \"Have you seen how many of their owners go blind?\"",
                "What did the father buffalo say to his son when he dropped him off at school?\r\n\r\n- Bison!",
                "What s green and hangs from a tree???\r\nGiraffe Boogers",
                "Why did the chicken cross the road?\r\nBecause the chicken and the road can't agree on anything.",
                "When was the price of milk the highest?\r\n\r\nWhen the cow jumped over the moon.",
                "Why did the chicken cross the road?\r\nBecause it had no frontal lobe.",
                "Why didn't the chicken cross the road?\r\nBecause he's \"chicken\".",
                "Why did the duck cross the road?\r\nBecause the chicken was on holiday.",
                "Why didn't the duck cross the road?\r\nTo prove he's no chicken.",
                "Why does a duck cross the street?\r\nBecause it was the chicken's and turkey's day off.",
                "Q: What did Jane say to Tarzan when she saw the elephants coming? \r\nA: Here come the plums; she was color blind.",
                "Q: What has eight legs, two trunks, four eyes, and two tails? \r\nA: Two elephants.",
                "Q: What is brown, has four legs, and a trunk? \r\nA: A mouse coming back from vacation.",


                # Add more jokes of type 'Animal'
            ],
            "Puns": [
                "I went to a wedding the other day. Two antennas were getting married. It wasn't much of a wedding ceremony, but it was one heck of a reception!",
                "Did you know diarhea is part of your inheritence?\r\n\r\nYa, it flows in our genes.",
                "Two buzzards were eating a dead clown. One said to the other, \"Does this taste funny to you?\"",
                "How do you praise a computer?\r\nSay \"Data Boy\"!",
                "Mind Over Matter \r\n\r\nIf you don't mind, \r\nit doesn't matter.",
                "Hey, have any of you heard of the kidnapping in the woods?\r\n\r\nYeah, well, it all turns out OK, though, since he woke up...",
                "What happens when the smog clears over southern California?\r\n\r\nUCLA",
                "Wanna hear a dirty joke? A boy fell in a mud puddle.",
                "Two Eskimos sitting in their boat were chilly; but when they lit a fire in the boat, it sank, proving once and for all that you can't have your kayak and heat it too.",
                "Did you hear about the woman who poured margaritas in her birdbath?  Enough tequila mockingbird.",
                "What do you call a bear who's into gardening?\r\n\r\nA Hairy Potter!",
                "When ice skating, never judge a brook by its cover.",
                "There was a man who entered a local paper's pun contest. He sent in ten different puns, in the hope that at least one of the puns would win. Unfortunately, no pun in ten did.",
                "There were 3 tomatoes.  A momma tomato, a papa tomato, and a baby tomato.  The baby tomato started to fall behind and the papa tomato called over to him and said, \"Ketchup!\"",
                "A test-tube baby has a womb with a view.",
                "If a lawyer can be disbarred can a musician be denoted or a model deposed?",
                "What's black and white and played all over?\r\n\r\n\r\nBlack and White (the computer game)",
                "If a rabbit were racing cabbage, who would win?\r\n\r\nThe cabbage, because it's a head.",
                "One woman to another woman\r\n\r\nWoman- Those firemen are hot.\r\nOther Woman- Yeah they are nice looking.\r\nWoman- No. I mean they just came out of that burning building. They're hot.",
                "What did the dog say to the driver who was driving behind him?\r\nGet off my tail!",
                "Band Class is the only class where you can blow it.",
                "Mik and mak are having a pillow fight. Mak whacks mik hard. Mik yells \"are you jamaican because ja maican me crazy!\"",
                "The other day, I heard that a good friend of mine was outside during a thunderstorm and got struck by lightning.\r\n\r\nI was a bit shocked, but not as much as he was.",
                "Have you heard about the sauna that serves food?\r\n\r\nTheir specialty is steamed mussels.",
                "Child: Mum, can I wear those really nice jeans with the hole in the knee to church?\r\nMother: No honey, you can't wear holy jeans to church!",
                "Q: Why did the witch buy a computer?\r\n\r\nA: She needed the spellcheck",
                "Since workaholics are people addicted to work and chocaholics are people addicted to chocolate, are catholics people addicted to cats?",
                "You probably know for a fact that Adolf Hitler had only one testicle.\r\n \r\nAnd here we say ''You got to have balls to become a leader''",
                "I tried for years to snap my thumb and finger together - and suddenly it clicked!",
                "Little Brother: How long is a strong?\r\nBig Sister: Huh?\r\nLittle Brother: Well, I've heard of a week...",
                "There was a nearly-new television for sale the other day. It has a 42-inch plasma screen, and I bought it for $50.\r\n\r\nThe only thing wrong was that there was no volume control - but at that price, I couldn't turn it down!",
                "How did the aliens hurt the farmer? \r\n\r\nThey trod on his corn.",
                "Why do melons get married in church?\r\n\r\n\r\n- Because they cantaloupe.",
                "If I travelled to the end of the rainbow,\r\nAs Dame Fortune did intend,\r\nMurphy would be there to tell me,\r\nThe pot's at the other end.",
                "How does a sperm bank treat its donors?\r\n\r\nOn a first come, first serve basis.",

                # Add more jokes of type 'Puns'
            ],
            "Other / Misc": [
               "What is the world's sharpest thing?\r\n\r\nA fart! It goes through your pants without leaving a hole!",
               "An actual sign outside a house:\r\nThe dog is okay. Beware of the owner",
               "A fact of life:\r\nAfter Monday and Tuesday, even the calendar says W T F",
               "Teenager: Dad, did you hear that Jake broke up with Taylor?\r\n\r\nDad:  Oh no, another album.",
               "I had a great memory once, but I don't know where I left it.  You haven't seen it lying around anywhere have you?\r\nNo?  No what?",
               "An Irishman, a Scotsman, and an American walk into a bar.\r\nThe beginning of a cheesy joke?\r\nYou betcha.",
               "The devil is the father of lies, but he neglected to patent the idea, and the business now suffers from competition.",
               "What has four legs and ticks?\r\nA walking clock!",
               "Why are golf balls small and white?\r\n\r\nBecause if they were big and grey they would be elephants.",
               "Did you know they have Knight Rider in the GDR? It's a Trabant with a pocket calculator!",
               "A man was fishing. After a while another angler came to join him. \"Have you had any bites?\" asked the second man.\r\n\r\n\"Yes, lots,\" replied the first one, \"but they were all mosquitoes.\"",
               "What's the difference between an HO-sausage and Sputnik?\r\nThey've officially confirmed that Sputnik 2 had a dog in it.",
               "How can you tell that the Stasi has bugged your apartment?\r\nThere's a new cabinet in it.",
               "\"What I saw, it was burned into my mind forever.\"\r\n\r\n\"Well, that explains the red markings on your scalp.\"",
               "Q:Why can peter pan fly?\r\nA:Because if you got hit in the peter with a pan you'd fly too.",
               "Why did the limping man sit on a scorpion?\r\n \r\nHe thought that it would be \"pinched\"!",
               "A Kerryman emigrated from Ireland to England, thereby increasing the average IQ of both countries.",
               "How do you keep an idiot in suspense?\r\n\r\nI'll tell you tomorrow!",
               "\"Daddy, there's a man knocking on the door with a beard!\"\r\n\r\n\"No wonder I didn't hear him!\"",
               "Q. Why do people wear shamrocks on St. Patrick's day?\r\n\r\nA. Regular Rocks are too heavy!",
               "Little Willy, full of hell,\r\nThrew his sister in the well.\r\nTheir mother said when drawing water,\r\n\"It's so hard to raise a daughter.\"",
               "What color is red? True or false?",
               "What starts with an E, ends with an E and usually contains only one letter? \r\n\r\nENVELOPE!",
               "What's round and hard and sticks so far out of a man's pajamas you can hang a hat on it?\r\n\r\nHis head!",
               "Larry: Why did Humpty Dumpty have a great Fall?\r\n\r\nMary: Because he had a bad summer.",
               "What's invisible and very frightened?\r\n\r\nA ghost with the sheet scared out of him.",
               "What do call a crying alien baby?\r\nAn Unidentifyed Crying Object!",
               "Some useless inventions:\r\n1) A waterproof teabag\r\n2) A swimsuit store in the North Pole\r\n3) Sugar free, fat free, taste free chocolate\r\n4) A parachute that opens on impact\r\n5) An ejector seat in a helicopter",
               "I once heard a cretin tell his friend that all cretins are liars! \r\n\r\nDid he lie though?",
               "Q: Where are the brave French soldiers buried?\r\nA: There aren't any so they had to bury some of ours on their soil.",
               "Why was Jesus not born in France?\r\n\r\nBecause they couldn't find three wise men or a virgin.",
               "Q: Why don't they have fireworks at Euro Disney?\r\nA: Because every time they shoot them off, the French try to surrender."
               "Q. Why was the Chunnel built under the English Channel?\r\nA.  So the French government could to flee to London.",
               "Q. What do you call 100,000 Frenchmen with their hands up?\r\nA. The French Army.",
               "What sits on a window sill, hums, and dies mysteriously 91 days after you bring it home?\r\n\r\n\r\n- An air conditioner with a 90 day warranty.",
                # Add more jokes of type 'Miscellenous'
            ],
            "Knock-Knock": [
               "A bachelor asked his friend to find him the perfect mate: \"I want a companion who is small and cute, loves water sports and enjoys group activities.\"\r\n\r\nWithout thinking, his friend replied: \"Marry a penguin.\"",
               "Knock, Knock \r\n\r\nWho's there? \r\n\r\nCows go. \r\n\r\nCows go who? \r\n\r\nNo, silly! Cows go moo!",
               "Knock, knock!\r\nWho's there?\r\nDelores.\r\nDelores who?\r\nDelores my shepherd...",
               "Knock Knock.\r\nWho's there?\r\nAnita.\r\nAnita who?\r\nAnita really warm place to sleep tonight, it's cold out here.",
               "Knock, knock.\r\nWho's there?\r\nDwayne\r\nDwayne who?\r\nDwayne the bathtub mommy, I'm dwowning.",
               "Knock Knock\r\n\r\nWho's there?\r\n\r\nMadam\r\n\r\nMadam who?\r\n\r\nMadam foot's caught in the door!",
                # Add more jokes of type 'Miscellenous'
            ],
            # "Blond": [
            #    "What do you call a blond who can change a lightbulb?\r\n\r\nTalented",
            #    "Q: Whats the difference between a blonde and a mosquito?\r\n\r\nA:  A mosquito will stop sucking when you smack it!",
            #    "body": "Q:  A blonde, a brunette, and a redhead are all in the 3rd grade.  Who has the biggest tits?\r\n\r\nA:  The blonde because she is 18.",
            #    "Q: How can you tell when a blonde has been driving your car?\r\n\r\nA: There is lipstick on the steering wheel from her blowing the horn.",
            #    "Q: What are the worst six years in a blonde's life? \r\n\r\nA: Fourth grade.",
            #    "A blonde missed a 44 bus so she took the 22 bus twice!",
            #    "Why doesn't a blonde talk during mating? \r\nBecause her mother told her never to talk to strangers.",
            #    "What are the blonde's first words after 4 years of college? \r\n\"Would you like fries with that?\"",
            #    "Why did the blonde keep a picture of herself in her room?\r\n\r\nSo she could use it as a mirror!",
            #    "Q: Why did the blonde keep taking off and putting the Pepsi bottle cap back on? \r\nA: Because it said, ''Sorry, try again.''",
            #    "How do you tell that a blonde has been at a computer?\r\n\r\nThere is lipstick on the joy stick!",
            #    "Q: Why does a blonde nurse carry around a red pen? \r\nA: To draw blood.",
            #    "How do you get a one-armed blonde out of a tree? \r\nWave!",
            #    "Two blondes are walking down the road when one says ''Look at that dog with one eye!'' \r\nThe other blonde covers one of her eyes and says ''Where?''",
            #    "On her way home from a long trip, a blonde drove past a sign that said \"CLEAN RESTROOMS 8 MILES\". By the time she drove eight miles, she had cleaned 43 restrooms.",
                # Add more jokes of type 'Miscellenous'
            # ],
            "Lawyer": [
               "Why do they bury lawyers 10 feet below ground instead of the usual 6?\r\n\r\nBecause deep down, they're not so bad!",
               "What do you call 100 lawyers jumping out of an airplane?\r\n\r\nSkeet",
               "How can you tell when a lawyer is lying?\r\nHis lips are moving.",
               "If a lawyer and an IRS agent were both drowning, and you could only save one of them, would you go to lunch or read the paper?",
               "Q: What's the difference between a lawyer and a herd of buffalo?\r\n\r\nA: The lawyer charges more.",
               "Q:What is the difference between a leech and a lawyer? \r\n\r\n\r\nA:The leech stops sucking you dry after you're dead.",
               "Why do lawyers always wear a tie?\r\n\r\nTo keep back the foreskin.",
               "Not all lawyers are bad.\r\nI've seen some graveyards full of  good ones!",
               "What do a circus and congress have in common?\r\n\r\nThey are both full of CLOWNS",
               "what do you get when you cross a LAWYER and a LIBRARIAN?\r\n\r\n\r\nAll the information you want, but you can't understand it!",
               "What's the difference between a bad lawyer and a good lawyer?\r\n\r\nA bad lawyer can have a case drag on for several years.\r\n\r\nA good lawyer can make it last even longer.",
               "What's the difference between a lawyer and a vampire?\r\n \r\nA vampire only sucks blood at night.",
               "How do you tell when a lawyer is well-hung?\r\nWhen you can't fit your fingers between the rope and his throat.",
               "Lawyers are safe from the threat of automation taking over their professions. No one would build a robot to do nothing.",
               "Lawyer: \"Now that you have been acquitted, will you tell me truly? Did you steal the car?\"\r\n\r\nClient: \"After hearing your amazing argument in court this morning, I'm beginning to think I didn't.\"",


                # Add more jokes of type 'Miscellenous'
            ],
            # Define more types of jokes and their corresponding jokes
        }
        
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        # if self.tell_joke.pad_token_id is None:
        #     self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

        self.model = GPT2LMHeadModel.from_pretrained("gpt2")

        # self.model2 = GPT2LMHeadModel.from_pretrained("gpt2")

    def get_mood_response(self, mood):
        mood_responses = {
            "happy": f"{self.name}: 😄 Awesome! I'm here to brighten your day with some jokes!",
            "neutral": f"{self.name}: 😐 Alright, let's have some fun with jokes!",
            "sad": f"{self.name}: 😢 I'm here to cheer you up with some humor!",
            # Add more mood responses
        }
        return mood_responses.get(mood, f"{self.name}: 😊 Let's share some laughs with jokes!")

    def get_joke_type_prompt(self):
        # joke_types = self.jokes_by_type
        joke_types = list(self.jokes_by_type.keys())
        joke_prompt = f"{self.name}: Which type of joke would you like to hear?\n"
        for i, joke_type in enumerate(joke_types, start=1):
            joke_prompt += f"{i}. {joke_type}\n"
        joke_prompt += "Please select a number: "
        return joke_prompt

    def prompt_user_mood(self):
        user_mood = input(f"{self.name}: What is your mood today (happy, neutral, sad)? ").lower()
        return user_mood
    
    def tell_joke(self, prompt):
        # Just tell a random joke from our list
        return prompt

    # def tell_joke(self, prompt):
    #     input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
    #     with torch.no_grad():
    #         output = self.model.generate(input_ids, 
    #                                     #  max_length=100, 
    #                                      num_return_sequences=3, 
    #                                      max_new_tokens = 50,
    #                                      do_sample=True, 
    #                                     #  pad_token_id = self.tokenizer.pad_token_id,
    #                                      pad_token_id = self.tokenizer.eos_token_id,
    #                                      eos_token_id = self.tokenizer.eos_token_id,
    #                                      temperature= 1000.0, 
    #                                     #  no_repeat_ngram_size = 2,
    #                                     #  top_k =50,
    #                                     typical_p = 1000.0,
    #                                      top_p = 0.95)
    #     response = self.tokenizer.decode(output[0], skip_special_tokens=True)
    #     return response
    
    def rate_joke(self, joke):
        # Rate the joke based on its sentiment polarity
        # This is a simple example and doesn't actually reflect humor
        blob = TextBlob(joke)
        polarity = blob.sentiment.polarity
        rating = int((polarity + 1) * 5)  # convert polarity from [-1, 1] to [0, 10]
        return rating

    def run(self):
        print(f"Hi I am the {self.name} welcome to the Joke Bot!")
        t2s.speak(f"Hi I am the {self.name} welcome to the Joke Bot!")
        print(f"{self.name} What is your name? \nUser:")
        t2s.speak("What is your name?")
        user = input("")
        print(f"{self.name}: Hello {user}, nice to meet you  !")
        t2s.speak(f"Hello {user}, nice to meet you !")
        
        while True:
            user_mood = self.prompt_user_mood()
            mood_response = self.get_mood_response(user_mood)
            print(mood_response)
            t2s.speak(mood_response)
            
            joke_type_prompt = self.get_joke_type_prompt()
            selected_type_idx = int(input(joke_type_prompt)) - 1
            # selected_joke_type = self.jokes_by_type[selected_type_idx]
            selected_joke_type = list(self.jokes_by_type.keys())[selected_type_idx]
            # selected_type = input(joke_type_prompt)  # Get user input as a string
            # joke_types = list(self.jokes_by_type.keys())
            # if selected_type in joke_types:
            #     selected_type_idx = joke_types.index(selected_type)
            #     selected_joke_type = joke_types[selected_type_idx]
            
            joke = random.choice(self.jokes_by_type[selected_joke_type])
            joke_prompt = f"{self.name}: I will tell a funny {selected_joke_type.lower()} joke:"
            # joke_prompt = f"{self.name}: You will tell a funny {selected_joke_type.lower()} joke in only English: "
            # joke = self.tell_joke(joke_prompt)
            print(joke_prompt)
            t2s.speak(f"I will tell a funny {selected_joke_type.lower()} joke")
            joke = self.tell_joke(joke)
            print(f"{self.name}: Here's a joke for you:")
            t2s.speak("Here's a joke for you:")
            print(joke)
            t2s.speak(joke)
            
            user_rating = int(input(f"{self.name}: On a scale of 1 to 10, how funny was the joke?\n{user}:  "))
            print(f"{self.name}: Thank you for your feedback!")
            t2s.speak("Thank you for your feedback!")
            
            tell_own_joke = input(f"{self.name}: Would you like to tell me a joke? (yes/no)\n{user}: ").lower()
            t2s.speak("Would you like to tell me a joke? yes or no")
            
            if tell_own_joke == "yes":
                user_joke = input(f"{self.name}: Sure, go ahead and tell me your joke:\n{user}:  ")
                t2s.speak("Sure, go ahead and tell me your joke:")
                user_joke_rating = self.rate_joke(user_joke)
                # user_joke_rating = int(input("On a scale of 1 to 10, how funny is your joke? "))
                # print(f"User: {user_joke}")
                print(f"{self.name}: I rated your joke as {user_joke_rating} out of 10.")
                t2s.speak(f"I rated your joke as {user_joke_rating} out of 10.")
                print(f"{self.name}: Thank you for sharing your joke!")
                t2s.speak("Thank you for sharing your joke!")
            
            another_joke = input(f"{self.name}: Would you like to hear another joke? (yes/no) ").lower()
            if another_joke == "no":
                print(f"{self.name}: Thank you for joking with me. Have a great day!")
                t2s.speak("Thank you for joking with me. Have a great day!")
                break

bot = JokeBot()
bot.run()
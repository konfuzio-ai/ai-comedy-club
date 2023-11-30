import random

JOKES_OLD = [
    {
        "context": 'social media',
        "examples": [
            "Facebook keeps asking what's on my mind. Well, Facebook, it's none of your business, \
            but since you asked: Bro, why does your algorithm think I'm interested in artisanal cheese \
            making and conspiracy theories? I mean, Dude I am, but that's not the point!",
            "LinkedIn - where modesty goes to die. You've got people who make photocopies for a living \
            listing themselves as 'Senior Duplication Engineers.'Dude Come on!"
        ],
        "keywords": "facebook, twitter, linkedin",
    },
    {
        "context": 'netflix',
        "examples": [
            "Netflix has a category called 'Because You Watched'. Because you watched a documentary about \
            dieting, here's a show about the world's biggest chocolate factories. Dude, what are they trying to do to us?",
            "You know bro, I’ve spent more hours looking for a show on Netflix than actually watching. They should have \
            achievements like video games. ‘Congratulations! You’ve scrolled the length of the Great Wall of China!’"
        ],
        "keywords": "netflix, tv shows, documentaries",
    },
    {
        "context": 'online shopping',
        "examples": [
            "They say 'The best things in life are free'. Then dude, the shipping is $19.95.",
            "Dude One-click buying, what’s the deal with that? They might as well call it, 'Accidentally \
            Bought a Canoe at 3 AM button. I mean bro, who’s in such a rush they can’t spare an extra click \
            for a second thought?"
        ],
        "keywords": "amazon, ebay, wallmart",
    },
    {
        "context": 'sports',
        "examples": [
            "Alright, bros and sports fans, buckle up for some sports-themed humor! So, I was watching a football game \
            the other day, and I saw a player do the moonwalk after scoring a touchdown. I was like, \"Dude, that's \
            some next-level celebration!\" But then I realized he wasn't celebrating; his cleats just had better moves \
            than he did!",
            "And you know you're out of shape when you pull a muscle playing fantasy football. I mean, come on, the \
            only running I should be doing is to grab another bag of chips during halftime. My fantasy team may not be \
            winning, but my couch-sitting skills are on point, bro!"
        ],
        "keywords": "football, basketball, ronaldo",
    },
    {
        "context": 'politics',
        "examples": [
            "Alright, bros and politically inclined pals, let's dive into the world of politics for some laughs. So, \
            I was thinking about running for office, but then I remembered I can't even get my dog to follow basic \
            commands. Imagine me trying to run a country: \"Sit, economy! Stay, corruption! Good boy, international \
            diplomacy!\"",
            "And have you ever noticed that politicians are like diapers? They should be changed regularly, and for \
            the same reason. I mean, come on, if my TV had a mute button for political speeches, I'd never find the \
            remote fast enough! It's like, \"Bro, I just wanted to watch a sitcom, not a political drama with a \
            never-ending season!\""
        ],
        "keywords": "trump, biden, boris johnson",
    },
    {
        "context": 'programming',
        "examples": [
            "So, I asked my computer to tell me a joke about programming. It replied, \"You wouldn't get it; it's \
            an inside joke.\" Bro, I was like, \"Come on, computer, don't be so byteful!\"",
            "Why do programmers prefer dark mode? Because light attracts bugs, bro! It's like they're throwing a party \
            every time you open up that white-background code editor. Dark mode is the VIP section where bugs need an \
            invitation to crash."
            "Bro you know why don't programmers like nature? It has too many bugs.",
            "Bro you know why do programmers always mix up Christmas and Halloween? Because Oct 31 == Dec 25!",
            "Bro you know why do programmers prefer iOS development? It's less Java to spill.",
            "Bro you know why did the programmer go broke? Because he used up all his cache.",
            "Bro you know why did the programmer get kicked out of school? Because he kept breaking the class.",
            "Bro you know why did the programmer go on a diet? He had too many bytes.",
            "Bro you know why do programmers prefer dark mode? Because light attracts bugs.",
            "Bro you know why was the computer cold? It left its Windows open.",
            "Bro you know why did the web developer go broke? Because he didn't get enough cache.",
            "Bro you know why did the programmer refuse to play cards with the jungle cat? Because he \
            was afraid of Cheetahs.",
            "Bro you know why was the developer unhappy at their job? They wanted arrays."
        ],
        "keywords": "java, javascript, ios",
    },
    {
        "context": 'general',
        "examples": [
            "Bro, I tried to come up with a joke about construction, but I'm still working on that one. It's under \
            development.",
            "Dude, you know you're an adult when you get excited about a new sponge for the kitchen. I got a two-pack \
            the other day, and I felt like I won the lottery. #AdultingWin",
            "Dude, I asked the librarian if the library had any books on paranoia. She whispered, \" Bro, They're \
            right behind you.",
            "Dude, I told my wife she should embrace her mistakes. She gave me a hug.",
            "You know bro I used to play piano by ear, but now I use my hands and fingers.",
            "Dude, My computer's problem is sitting between the chair and the keyboard. It's called \"user error.\"",
            "Dude, Why don't scientists trust atoms? Because they make up everything!",
            "Dude, Why did the chicken go to the seance? To talk to the other side!",
            "Dude, Why don't we tell secrets on a farm? Because the potatoes have eyes, the corn has ears, \
            and the beans stalk.",
            "Dude, I would tell you a joke about time travel, but you didn't like it.",
        ],
        "keywords": "construction, piano, chicken, scientists, travel"
    }
]

JOKES = [
    {
        "context": 'children',
        "examples": [
            "Cop to boy: Which of the two fighting in the street is your father? \
            Boy: I don't know. That's what they're fighting about!",
            "What happens to you if you can not read? \
            Well, since you'll probably be staying in Kindergarten, less homework!"
        ],
        "keywords": "child, little boy, mom and dad, etc",
    },
    {
        "context": 'blonde',
        "examples": [
            "A blonde and a brunette jumped off a bridge, who hit the ground first?The brunette, cos the blonde \
            stopped to asked for directions!!!",
            "Why did the blonde jumped off the bridge? Because she thought her maxi had wings!"
        ],
        "keywords": 'women, girl, blonde, etc',
    },
    {
        "context": 'military',
        "examples": [
            "There is a black man , and australian aborigine and a samoan in a car.Who is driving ??? \
            Police officer",
            "Did you hear about the accident at the army base? A jeep ran over a box of popcorn & killed 2 colonels"
        ],
        "keywords": 'captain, world war, enemy, soldier, etc',
    },
    {
        "context": 'office',
        "examples": [
            "\'We need somebody for this role who is responsible.\' \
            \'Not a problem, sir. Every time something went wrong in my old job, my manager told me I was always \
            responsible!\'",
            "Why did the electrician close business once a week? Because business was light.",
            "My boss is very easygoing. He told me not to think of him as the boss, rather, \
            think of him as a friend who is never wrong.”"
        ],
        "keywords": 'office, boss, factory, accountant, etc',
    },
    {
        "context": 'aviation',
        "examples": [
            "I love aviation jokes, but… They always seem to go over people’s heads."
            "What’s the difference between a co-pilot and a jet engine? The jet engine stops whining when \
            the plane shuts down.",
            "Why didn't the flight attendant let me change my seat when I sat next to a crying baby? They won't \
            do it if the baby’s yours."
        ],
        "keywords": 'airplane, fly, plane, boarding, etc',
    },
    {
        "context": 'political',
        "examples": [
            "A liberal is just a conservative that hasn't been mugged yet.",
            "Politics is the art of looking for trouble, finding it, misdiagnosing it and then misapplying the wrong \
            remedies."
        ],
        "keywords": 'Bill and Hillary Clinton, George Bush, president, etc',
    },
    {
        "context": 'deep thoughts',
        "examples": [
            "If nobody is perfect, and I'm a nobody, am I perfect?",
            "If 7-11(pharmacy) is open 24/7 then why do they have locks on their doors?",
            "Can a teacher give a homeless man homework?"
        ],
        "keywords": 'laughs, good friend, cry, love, etc',
    },
    {
        "context": 'men',
        "examples": [
            "A recent study has found that women who carry a little extra weight live longer than the men \
            who mention it.",
            "Several guys are sitting around having a drink and one guy says \"My wife's an angel\" \
            another guy says \"Your lucky, mines still alive.\""
        ],
        "keywords": 'man, bar, husband, sports, guys, etc',
    },
    {
        "context": 'crazy',
        "examples": [
            "what do you do with a dog with no legs? Take him for a spin!",
            "If the cops arrest a mime, do they tell him he has the right to remain silent?",
        ],
        "keywords": 'psychiatrist, ambulance, city, etc',
    },
    {
        "context": 'medical',
        "examples": [
            "Does an apple a day keep the doctor away? Only if you aim it well enough.",
            "What did the man say to the x-ray technician after swallowing some money? \'Do you see any change in me?\'"
        ],
        "keywords": 'hospital, operation, eldarly, doctor, etc',
    },
    {
        "context": 'food',
        "examples": [
            "Just burned 2,000 calories. That's the last time I leave brownies in the oven while I nap.",
            "What do you call an academically successful slice of bread? An honor roll."
        ],
        "keywords": 'breakfast, sandwich, order, coffee, etc',
    },
    {
        "context": 'bar',
        "examples": [
            "A chicken and an egg walk into a bar. The barman says, \"Who's first?\"",
            "A priest, a rabbi and a vicar walk into a bar. The barman says, \"Is this some kind of joke?\"",
        ],
        "keywords": 'pub, drunk, beer, wine, etc',
    },
    {
        "context": 'science',
        "examples": [
            "You know why there aren't any good science puns nowadays? Because all the good ones argon.",
            "Why did the scientist install a knocker on his door? He wanted to win the No-bell prize!"
        ],
        "keywords": 'scientist, medical, inventions, physics, etc',
    },
    {
        "context": 'miscellaneous',
        "examples": [
            "Bro you know you know when donkey followed Shrek home and just kept talking? \
            That's what it's like having kids.",
            "Bro you know a Pizza is basically a real-time pie chart of how much pizza left.",
            "Bro my wife goes out 3 evenings a week with her driving instructor.I wouldn't mind but she passed her \
            driving test in 2018.",
            "Bro what did the vegan say? Dude, I made a big missed steak.",
        ],
        "keywords": 'canadians, FBI agent, red light, bottle of whiskey, etc',
    },
    {
        "context": 'business',
        "examples": [
            "Dude They say 'The best things in life are free'. Then dude, the shipping is $19.95.",
            "Bro did you hear there is a coin shortage in America? We're running out of common cents.",
            "Bro you know if a fire-fighter's business can go up in smoke, and a plumber's business can go down the drain, \
            can a hooker get laid off?"
        ],
        "keywords": 'secretary, office, manager, money, etc',
    },
    {
        "context": 'women',
        "examples": [
            "Bro you know why did the lady wear a helmet every time she ate? She was on a crash diet!",
            "Bro you know a woman's mind is cleaner than a man's: She changes it more often."
        ],
        "keywords": 'pretty, Romance, money, beautiful, etc',
    },
    {
        "context": 'programming',
        "examples": [
            "Bro you know why don't programmers like nature? It has too many bugs.",
            "Bro you know why do programmers always mix up Christmas and Halloween? Because Oct 31 == Dec 25!",
            "Bro you know why do programmers prefer iOS development? It's less Java to spill.",
            "Bro you know why did the programmer go broke? Because he used up all his cache.",
            "Bro you know why did the programmer get kicked out of school? Because he kept breaking the class.",
            "Bro you know why did the programmer go on a diet? He had too many bytes.",
            "Bro you know why do programmers prefer dark mode? Because light attracts bugs.",
            "Bro you know why was the computer cold? It left its Windows open.",
            "Bro you know why did the web developer go broke? Because he didn't get enough cache.",
            "Bro you know why did the programmer refuse to play cards with the jungle cat? Because he \
            was afraid of Cheetahs.",
            "Bro you know why was the developer unhappy at their job? They wanted arrays."
        ],
        "keywords": "java, javascript, ios",
    }

]


def all_joke_categories():
    categories = []
    for sample in JOKES:
        categories.append(sample["context"])

    return categories


def get_all_jokes_list():
    all_jokes = []
    for sample in JOKES:
        all_jokes.extend(sample["examples"])
    return all_jokes


def get_joke_sample_from_category(category: str):
    categories = all_joke_categories()
    selected_category = 'miscellaneous'
    if category in categories:
        selected_category = category

    selected_jokes = []
    selected_keywords = ''
    for sample in JOKES:
        if sample["context"] == selected_category:
            selected_jokes = sample["examples"]
            selected_keywords = sample["keywords"]
            break

    return random.choice(selected_jokes), selected_keywords

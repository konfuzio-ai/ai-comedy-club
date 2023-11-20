import random

JOKES = [
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
    selected_category = 'general'
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

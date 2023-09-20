import pyjokes
import random
import emoji
from textblob import TextBlob

class Bot:
    '''Class Bot having methods to generate random joke and rate the jokes'''

    def __init__(self):
         '''Constructor to give introduction'''
         self.greetings = ["Hello! I'm KSD", "Hi!, My name is KSD", "Hey there! I'm KSD", "Greetings!...Howdy! I'm KSD.."]
         self.random_index = random.randint(0, len(self.greetings) - 1)
         self.random_greeting = self.greetings[self.random_index]
    
    def intro(self):
         '''This method will get the user name'''
         try:
              print(self.random_greeting,emoji.emojize(":grinning_face_with_big_eyes:"),"\n\nI'll be telling few jokes for you... Hope u enjoys it...\n\nHey... What is your name?")
              self.aud_name = input()
              print("\nHello ",self.aud_name, ".. So, How u doing??")
              self.feel = input()
         except Exception as e:
            print(f"An error occurred: {e}")

    def get_language(self):
         '''This method will get the user language to generate joke in the preferred language'''
         print("\nSo ",self.aud_name,", Which language do you prefre for joke??\nplease select any of these lamguages:")
         self.language = {1:["English","en"],2:["German","de"],3:["Spanish","es"],4:["Italian","it"],5:["Galician","gl"],6:["Basque","eu"]}
         for self.l in self.language:
              print("Press ", self.l," for ",self.language[self.l][0])
         try:
              self.language_choice = 0 #Making English as default
              for j in range(0,3):
                   self.language_choice = int(input())
                   if self.language_choice in [1,2,3,4,5,6]:
                        self.l_choice = self.language[self.language_choice][1]
                        break
                   else:
                        print("Oops... Invalid language. Choose between 1 to 6.",emoji.emojize(":zipper-mouth_face:"))
                        j = j+1
              #print(self.l_choice)#remove, for testing only  
         except Exception as e:
              print(f"An error occurred in getting the user language for joke:{e} \nMaking English as default..") 
              self.l_choice = 'en' #making English as default    
         
    def tell_joke(self):
        '''This method will generate random jokes'''
        try:
             self.joke = pyjokes.get_joke(language=self.l_choice, category="neutral")
        except pyjokes.pyjokes.LanguageNotFoundError as e:
            print(f"Invalid language choice: {e}")
        except pyjokes.pyjokes.CategoryNotFoundError as e:
            print(f"Invalid Category: {e}")
        except Exception as e:
              print(f"An error occurred :{e}")  
      #  print(self.joke)
        return self.joke

    def rate_joke(self,get_joke):
        '''Rate the joke based on its sentiment polarity'''
        try:
             self.blob = TextBlob(get_joke)
             print("before..\n")
             self.polarity = self.blob.sentiment.polarity
             print("after...\n")
             if self.polarity > 0 :
                  self.rating = random.randrange(6,10)
             else :
                  self.rating = random.randrange(1,6)     
                  print(self.rating) # testing purpose
        except Exception as e:
              print(f"An error occurred while rating the joke :{e}") 
        return self.rating
    
'''Main starts from here'''
if __name__ == '__main__':
     obj = Bot()
     obj.intro()
     obj.get_language()
     i=0 # to remove the while loop for testing
     count = 0
     print("ready to hear a joke... Y or N")
     while(1):       
        #This loop will not break if the condition does not meet
        try:
             input1=input()   
             #If the input is yes, Call for joke generate function
             if input1 in ['Y','y','Yes','YES','yes','1'] :   
                   joke=obj.tell_joke()
                   punchline = ["I thought it would be fun!","Hope you like it","Isn't it funny!!","Ha Ha Ha...","LOL!!"]
                   print("joke is : \n",joke,punchline[random.randrange(0,5)])
                   i=i+1
             elif input1 in ['n','N','no','NO','No','2']:
             #if user don't want to hear a joke, ask if they want to tell a joke
                  if input1 == '2':
                       input2 = '2'
                  else:
                       print("Do you wanna tell a joke??\nY or N")
                       input2=input()
                  if input2 in ['Y','y','Yes','YES','yes','2']:
                            i = i+1
                            # if the user want to tell a joke, call the rating function for that joke
                            print("Great!!! Let's hear it then..\nTell the joke...")
                            get_joke = input()
                            print("claaing... rate")
                            rate = obj.rate_joke(get_joke)
                            print("Ha Ha.. Good try.\nI would give...\nahhh..",rate,"out of 10",emoji.emojize(":face_with_tongue:"))
                            if rate <= 5:
                                 print("Not bad, You could try better..",emoji.emojize(":relieved_face:"))
                            elif rate > 5:
                                 print("Good joke...",emoji.emojize(":rolling_on_the_floor_laughing:"))
                  else :
                       print("I guess You are tired to tell nor hear a joke... \nSo Do you wanna end??\nY or N ",emoji.emojize(":thinking_face:"))
                       end = input()
                       if end in ['Y','y','Yes','YES','yes'] :
                            print("BYE BYE",obj.aud_name,emoji.emojize(":sleeping_face:"))
                            break
                       else :
                           print("Okay.. Do you wanna hear a joke? or tell joke? \n1 - hear a joke\n2 - Tell a joke")
                           i = 0
                           continue
             
        except Exception as e:
             print(f"An erroe occurred while calling the tell joke method and rating joke methods: {e}")
        if(i == 5):     
             # To check the user mood, if the user needs to end or continue the program        
             print("\nahh.. Kind of getting tired??\n\nDo you wanna end this show?? Press Y or N")
             input3 = input()
             if input3 in ['Y','y','Yes','YES','yes']:
                  print("Sure... It was a fun time. Will meet soon again for few more comedies.. \nBYE BYE for now",emoji.emojize(":sleeping_face:"))
                  break
             else:
                  print("Great!!!")
                  print("wanna hear one more joke??? or tell a joke??",emoji.emojize(":thinking_face:"), "Press: \n1 - hear a joke\n2 - Tell a joke")
                  i = 0
        else:
             print("wanna hear one more joke?? or tell a joke??",emoji.emojize(":thinking_face:"),"Press: \n1 - hear a joke\n2 - Tell a joke")

        

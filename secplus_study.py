import random
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import sys
import time
import os

translator = Translator()
card = ['a', 'b', 'c','d','e', 'f', 'g','h','i']
lang = "pt"

class Study:
    def __init__(self, number_question):
        self.number_question = number_question
        self.url = "https://passcomptia.com/comptia-security/comptia-security-question-"
    
    def get_questions(self, random_card):
        valid_tags = ["p"]
        ps = []
        r = requests.get(self.url+random_card+"-"+self.number_question)

        self.soup = BeautifulSoup(r.text, "html.parser")
        for tag in self.soup.find_all('p'):
            if tag.name in valid_tags:
                ps.append(tag)
        try:
            #quest = ps[1]
            #answers = ps[2]
            self.quest = str(ps[1]).replace("<br/></b></p>", "").replace("<p><b>", "")
            self.answers = str(ps[2]).replace("<p>", "").replace("</p>", "").replace("<br/>", "\n")
        except Exception as e:
            print(e)

        return self.soup, self.quest, self.answers
    
    #def __str__(self):
    #   return self.quest+"\n"+self.answers


    def get_quest_answer(self, soup):
        list_to_parsed = []
        VALID_TAGS = ["b"]
        for i in soup.find_all('b'):
            if i.name in VALID_TAGS:
                list_to_parsed.append(i)
        questions_answer = open("questions_answer.txt", "a")
        questions_answer.write(str(list_to_parsed[1]).replace("<b>Answer: ", "").replace(" </b>", "")+"\n")
        questions_answer.close()
    

    def get_user_answer(self):
        answer = input("Answer: ").upper()
        user_answer = open("user_answer.txt", "a")
        user_answer.write(str(answer)+"\n")
        user_answer.close()

    def check_hits(self):
        correctly_answers = 0
        user_answers = open("user_answer.txt", "r")
        question_answer = open("questions_answer.txt", "r")
        for i in user_answers.readlines():
            for j in question_answer.readlines():
                if i == j:
                    correctly_answers += 1

        return correctly_answers



     
if __name__ == "__main__":
    number_of_questions = 0
    list_of_questions = []
    start = time.time()
    while number_of_questions < 90:
        number_quest = random.randint(0, 100)
        letter_quest = random.choice(card)
        quest_identify = str(number_of_questions)+letter_quest
        if quest_identify not in list_of_questions:
            list_of_questions.append(quest_identify)
            study = Study(str(number_quest))
            soup, quest, answers = study.get_questions(letter_quest)
            perg_pt = translator.translate(quest, src="en", dest=lang)
            alters = translator.translate(answers, src="en", dest=lang)
            print(perg_pt.text)
            print("")
            print(alters.text)
            print("")
            study.get_user_answer()
            study.get_quest_answer(soup)
            number_of_questions += 1
        
    
    end = time.time()
    trial_time = end - start
    
    print("\x1b[6;30;42m"+"Quantidade de acertos -> "+str(study.check_hits())+"\x1b[0m")
    print("\x1b[6;30;42m"+"Tempo de duração -> "+str(trial_time)[:2]+" segundos!"+"\x1b[0m")
    os.remove("questions_answer.txt")
    os.remove("user_answer.txt")
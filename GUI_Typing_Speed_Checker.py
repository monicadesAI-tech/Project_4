#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
from tkinter import *
import bs4
import requests

#this will generate a random sentence for the user to type
#the time taken to type the sentence will be recorded and the wpm, accuracy and cps will be calculated and displayed to the user

root = Tk()
root.title("Typing Speed Tester")
root.geometry("730x450")
root.configure(bg = "blue")

class Game():
    
    def  __init__(self,master):
        
        #set up welcome screen
        #print welcome messages
        self.welcomeLabel = Label(master,text = "Welcome to typing speed tester !", bg = "blue", fg = "white", 
                                  font = ("Helvetica", 20))
        self.welcomeLabel.grid(row = 0 , column = 0, columnspan = 2, padx = 10, pady = 10)

        self.welcomeLabel1 = Label(master,text = "Enter the following sentence as quickly as you can and then click the enter key :", 
                              bg = "blue",fg = "white", font = ("Helvetica", 15))
        self.welcomeLabel1.grid(row = 1, column = 0, columnspan = 2,padx = 10, pady = 10)

        #print sentence for user to type, sentence is generated from get_sentence() method
        self.sentenceLabel2 = Label(master, text = self.get_sentence(),  bg = "blue",fg = "red", font = ("Helvetica", 15) )  
        self.sentenceLabel2.grid(row = 2, column = 0, columnspan = 2,padx = 10, pady = 10)

        #entry box for user
        self.entryBox = Entry(master,width = 50,fg = 'black', bg = 'white', borderwidth = 5, font = ("Helvetica", 15) )
        self.entryBox.grid(row = 3, column = 0, columnspan = 2,padx = 10, pady = 10)

        #start timer when user clicks on input box and end timer when user enters text
        #this is only for the first try as text box is deselected by default at start
        #once player wants to get a new word the timer will reset using the reset method
        self.entryBox.bind("<Button-1>",self.start_record_time) and self.entryBox.bind("<Return>", self.end_record_time)

        #button to play again
        self.play_again = Button(master, text = "New Phrase",command = self.reset, bg = 'green', fg = 'white', 
                            borderwidth = 5,width = 15, font = ("Helvetica", 15))
        self.play_again.grid(row = 8 , column = 0, columnspan = 2, padx = 15, pady = 15)
        
        
        
    def get_sentence(self):
        #scrape this website to get random sentences for user to type
        self.res = requests.get("http://www.englishinuse.net/")
        self.soup = bs4.BeautifulSoup(self.res.text, "lxml")
        #store these sentences in a list
        self.sentences = []
        for item in self.soup.select(".font1"):
            self.sentences.append(item.text)

        self.sentence = '"' + self.sentences[0][2:-1] + '"' 
        return self.sentence
        
    def reset(self):
        #clear the text box, print new phrase and reset timer
        self.entryBox.delete(0, END)
        self.sentenceLabel2.config(text = self.get_sentence())
        self.start = time.time()
        
    
    #this function starts the timer when entry box is clicked
    def start_record_time(self,event):
        self.start = time.time()

    #this will stop the timer and calculate wpm, time and charpm and accuracy of typing
    def end_record_time(self,event):
        #stop timer
        self.end = time.time()

        #display time taken
        self.time_taken = "{:.2f}".format(self.end - self.start)
        self.timeLabel = Label(root, text =  "Time Taken =  " + self.time_taken + " s " , 
                               bg = "blue",fg = "red", font = ("Helvetica", 15))
        self.timeLabel.grid(row = 4,column = 0, columnspan = 2,padx = 5, pady = 5)

        #calculate words per minute
        self.enteredText = self.entryBox.get()
        
        #wpm = no.words / time (minutes)
        self.wpm = "{:.2f}".format(len(self.enteredText.split()) / ((self.end - self.start) / 60))
        self.wpmLabel = Label(root, text =  "Wpm =  " + self.wpm , bg = "blue",fg = "red", font = ("Helvetica", 15))
        self.wpmLabel.grid(row = 5,column = 0, columnspan = 2,padx = 5, pady = 5)

        #characters per second
        self.cps = "{:.2f}".format(len(self.enteredText) / (self.end-self.start))
        self.cpsLabel = Label(root, text =  "Cps =  " + self.cps , bg = "blue",fg = "red", font = ("Helvetica", 15))
        self.cpsLabel.grid(row = 6,column = 0, columnspan = 2,padx = 5, pady = 5)

        #calculate accuracy
        self.count = 0;
        for char in self.enteredText:
# the reason it is 1:-1 and not :: is because the first and last characters of the sentence are quotation marks 
# this is not needed for user to enter
            if char in self.sentence[1:-1]:
                self.count += 1
        
        #len(sentence) -2 this is to discount for the quotation marks
        if self.count > len(self.sentence)-2:
            self.accuracyLabel = Label(root, text =  "Character limit exceeded, cannot calculate accuracy " , 
                                                       bg = "blue",fg = "red", font = ("Helvetica", 15))
            self.accuracyLabel.grid(row = 7, column = 0, columnspan = 2, padx = 5, pady = 5)
        else:
            self.accuracy = "{:.2f}".format(self.count/(len(self.sentence)-2)*100)

            self.accuracyLabel = Label(root, text =  "Accuracy =  " + self.accuracy + " % " , 
                                                           bg = "blue",fg = "red", font = ("Helvetica", 15))
            self.accuracyLabel.grid(row = 7, column = 0, columnspan = 2, padx = 5, pady = 5)
           

test = Game(root)
#note this is just to ensure that the app does not close straight away after running it on python
k = input("Type q to quit") 

root.mainloop()


# In[ ]:





# 

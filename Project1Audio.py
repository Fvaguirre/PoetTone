import pygame;
import win32com.client as wincl;
from time import sleep; 

#TODO: write up the architecture documentation
#Start ReadMe (dependencies and such)
#Find Songs

#Global variables
tones = {"Sad": "StillAlive.mp3", "Anger": "StillAlive.mp3"};
poem = [(\
"Nature's first green is gold, \
Her hardest hue to hold.", "Sad"),("\
Her early leaf's a flower; \
But only so an hour.", "Sad"),("\
Then leaf subsides to leaf,", "Anger"),(" \
So Eden sank to grief, \
So dawn goes down to day. \
Nothing gold can stay.", "Sad")];

#tone_id can be either: anger, fear, joy, and sadness (emotional tones); analytical, confident, and tentative (language tones)

globalPause = False;

#Stanza - the text to be read
#Tone - the tone of music to be played
#cont - Whether the tone of music is the same as the previous one that was played (will always be false for first tone)
#end - whether this is the last stanza to be read and the music should fadeout afterwards. 
def playStanza(stanza, tone, cont, end): 
    speak = wincl.Dispatch("SAPI.SpVoice");
    if (cont == False): #New tone from the previous one
        if (pygame.mixer_music.get_busy()): #check if there is currently music playing
            pygame.mixer_music.fadeout(2000);
            sleep(2);
        pygame.mixer_music.load(tone); #load the new tone, set the volume and then play it. 
        pygame.mixer_music.set_volume(.5);
        pygame.mixer_music.play();
        sleep(3);
    else: #The tone is the same as the previous one.
        if (False == pygame.mixer_music.get_busy()):
            pygame.mixer_music.rewind(); #Check to make sure the music is still playing and hasn't run out, if it has, replay it. 

    if (globalPause == False): #Check to make sure that next line should be spoken.
        speakLine(stanza, speak);
    else: 
        pygame.mixer_music.pause(); #Pause the music

    if (end):
        pygame.mixer_music.fadeout(2000); #If it's the end of the poem then fadeout the music before stopping.
        sleep(2);

#Takes a SAPI.SpVoice object and the line that it will say
def speakLine(line, speak):
    speak.Speak(line);

def playPoem(poem): #expected that poem is an array in the form [(stanza, id), (stanza id), ...]. 
    for i in range(len(poem)): #Loops through the poem stanza by stanza. 
         stanza = poem[i][0];
         tone = poem[i][1];
         if (i == 0): #Figures out whether the music should continue or not and passes the correct arguments to play the Stanza
             playStanza(stanza, tones[tone], False, False);
         elif (i == (len(poem)-1)):
               playStanza(stanza, tones[tone], (poem[i-1][1] == poem[i][1]), True);
         elif (poem[i][1] == poem[i-1][1]):
             playStanza(stanza, tones[tone], True, False);
         else:
             playStanza(stanza, tones[tone], False, False);

#Driver function to start the application
def run(poem):
    pygame.mixer.init();
    playPoem(poem);

run(poem);
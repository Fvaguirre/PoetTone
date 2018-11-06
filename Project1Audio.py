import pygame;
import win32com.client as wincl;
from time import sleep; 



def playStanza(stanza, tone, cont): 
    speak = wincl.Dispatch("SAPI.SpVoice");
    if (cont == False):
        pygame.mixer_music.load(tone);
        pygame.mixer_music.set_volume(.5);
        pygame.mixer_music.play();
        sleep(3);
    speak.Speak(stanza);

    if (cont):
        pygame.mixer_music.fadeout(2000);
        sleep(2);


tones = {"Sad": "StillAlive.mp3"};

poem = [(\
"Nature's first green is gold, \
Her hardest hue to hold. \
Her early leaf's a flower; \
But only so an hour.", "Sad"),("\
Then leaf subsides to leaf, \
So Eden sank to grief, \
So dawn goes down to day, \
Nothing gold can stay.", "Sad")];

def playPoem(poem): #expected that poem is an array in the form [(stanza, id), (stanza id), ...]. 
    for i in range(len(poem)):
         stanza = poem[i][0];
         tone = poem[i][1];
         if (i == 0):
             playStanza(stanza, tones[tone], False);
         elif (i == (len(poem)-1)):
               playStanza(stanza, tones[tone], (poem[i-1][1] == poem[i][1]));
         elif (poem[i][1] == poem[i+1][1]):
             playStanza(stanza, tones[tone], True);
         else:
             playStanza(stanza, tones[tone], False);

def run(poem):
    pygame.mixer.init();
    playPoem(poem);

run(poem);
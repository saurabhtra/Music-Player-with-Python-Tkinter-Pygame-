import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from ttkthemes import themed_tk as tk
from mutagen.mp3 import MP3
from pygame import mixer

# Tk() represents for our window and we are storing its value in root variable
# and to make it run in a loop we use root.mainloop() so that our main window appears contineousliy
root = tk.ThemedTk()
root.get_themes()
root.set_theme('radiance')


statusbar = ttk.Label(root, text="This is Pyhton coded Music Player ",
                      relief=SUNKEN, anchor=W)  # the SUNKEN make our widget(text) as it is sunked in our main window
statusbar.pack(side=BOTTOM, fill=X)

# creating menu bar
menubar = Menu(root)
root.config(menu=menubar)  # it has mainly two functions 1.it fix the menu bar at the top

# 2. make the menu bar ready to have sub menu

playlist = []


# playlist -contain the full path +filename
# playlistbox- online filename
# fullpath+ filename is required for mixer.music.load()

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()

    add_to_playlist(filename_path)
    mixer.music.queue(filename_path)

def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index,filename_path)
    index += 1

# create the submenu
submenu = Menu(menubar, tearoff=0)  # tearoff is used to remove the dash sign from the our submenus's cascade
menubar.add_cascade(label="file", menu=submenu)
submenu.add_command(label="new file", command=browse_file)
submenu.add_command(label="Exit", command=root.destroy)


def about_me():
    tkinter.messagebox.showinfo("about me",
                                'hey this is saurabh gangwar,im a pyhton developer follow me on insta @_artuto_gangwar')


submenu = Menu(menubar, tearoff=0)  # tearoff is used to remove the dash sign from the our submenus's cascade
menubar.add_cascade(label="playlist", menu=submenu)
submenu.add_command(label="fav")
submenu.add_command(label="about me", command=about_me)

mixer.init()  # initialize the mixer to make it work

# root.geometry('800x500')  # define the geometry if the window

root.title("Arturo")  # title of main window

root.iconbitmap(r'images/headphones.ico')  # adding ico on main window(tk supports only .ico not .png file so convert the .png to .ico(online ))
# about blueprint of the code
# root window-statusbar,rightframe,leftframe
# leftframe-playlist,addbutton,deletebutton
# rightframe-topframe,middleframe,bottomframe

# CREATING THE FRAME FOR OUR WINDOW WHICH IS DIVIDE THE WHOLE WINDOW
# IN PARTS E.G. middle ,top,bottom frame and we will be able to control each part seprately
# e.g arranging buttton in in middle frame without distorbing all the others frame
# or we can say that it isolate the portion which we want from the other frames

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=20)

rightframe = Frame(root)
rightframe.pack(pady=30)

topframe = Frame(rightframe)
topframe.pack()
middleframe = Frame(rightframe)
middleframe.pack()
lowerframe = Frame(rightframe)
lowerframe.pack()
bottomframe = Frame(rightframe)
bottomframe.pack()

# note: every single thing inside our window is a widget even the text which we make to appear inside it
# so lets make a label widget for text
# it will required two parameters first root(where has to appear),second
# text(what has to appear)

# text label for the length of the track
length_label = ttk.Label(topframe, text="Total Length --:--")
length_label.pack(pady=25)

current_time_label = ttk.Label(topframe, text="Curent Time --:--", relief=GROOVE)
current_time_label.pack()

# frameleft work
playlistbox = Listbox(leftframe)
playlistbox.pack()

addbtn = ttk.Button(leftframe, text="+ add", command=browse_file)
addbtn.pack(side=LEFT)

def del_song():
    selected_song = playlistbox.curselection()
    selected_song= int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)

delbtn = ttk.Button(leftframe, text="- del",command=del_song)
delbtn.pack(side=LEFT)


def set_vol(vall):  # this function is called by scale fun. bt this function
    # set_vol accepts only integer values so first we will convert the string (from scale)to int
    # and this procees is called as type casting
    volume = int(vall) / 100  # type casting and we devided by 100 as it accepts the values from 0-1
    mixer.music.set_volume(volume)


def show_details(play_song):
    file_data = os.path.splitext(play_song)
    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length

    else:

        a = mixer.Sound(play_song)
        total_length = a.get_length()
    # to get the lenth in minute and seconds
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)

    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    length_label['text'] = 'TOtal Length:' + ' - ' + timeformat
    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    # mixer.music.get_busy() -return the value false when music stops
    # and while loop ended
    global x
    while t and mixer.music.get_busy():
        if paused:
            continue

        else:
            mins, secs = divmod(t, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            current_time_label['text'] = 'Time remaining:' + ' - ' + timeformat
            time.sleep(1)
            t -= 1

   # if t==0:
       # next_song=playlist(x)
       # mixer.music.play(next_song)
# adding image as a button
# but first define there functions


def play_music():
    global paused
    global paused
    if paused:
        mixer.music.unpause()
        paused=FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            print(play_it)
            #x=selected_song[1]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showinfo("NO Track Found", "opps !!! please select the song ")


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Is Stoped"

paused =FALSE

def rewindMusic():
    play_music()

def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()

muted = False


def mute_music():
    global muted

    if muted:  # to unmute the music
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = False
    else:  # to mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = True

# we can't use grid and pack method together except in the frame
# grid gives us more complex gui which pack cant
playPhoto = PhotoImage(file='images/video.png')
playBtn = ttk.Button(middleframe, image=playPhoto, command=play_music)  # this command variable used to call a fun.
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file='images/stop-button.png')
stopBtn = ttk.Button(middleframe, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=2, padx=10)

pausePhoto = PhotoImage(file='images/pause.png')
pauseBtn=ttk.Button(middleframe,image=pausePhoto,command=pause_music)
pauseBtn.grid(row=0,column=2,padx=10)


rewindPhoto = PhotoImage(file="images/rewind.png")
rewindBtn = ttk.Button(bottomframe, image=rewindPhoto, command=rewindMusic)
rewindBtn.grid(row=1, column=0)

mutePhoto = PhotoImage(file="images/no-sound.png")
volumePhoto = PhotoImage(file="images/speaker.png")
volumeBtn = ttk.Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=2, column=2, pady=25)

# creating a scale widget to control the volume of the music
scale = Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)
mixer.music.set_volume(0.7)
scale.grid(row=2, column=3, pady=25)


def on_closing():
    pause_music()
    tkinter.messagebox.showinfo("HAVE A NICE DAY", "HOPING THAT YOU LIKE OUR WORK "
                                                   "YOU CAN GIVE YOUR SUGGESATION @ saurabhtra1997@gmail.com"
                                                   "  follow me on insta @ _arturo_gangwar")

    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

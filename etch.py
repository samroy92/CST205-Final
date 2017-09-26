# CST 205 - Final Project
# Team: Byte Bistro
# Members: Michael Goss, Jan Patrick Camaclang, Keith Groves, Oswaldo Minez, Samuel Roy
# April 19, 2016
# Project: Etch-A-Sketch

import random
import datetime
import java.awt.Font as Font

# Initialize variables
canvas = 0
frame = 0
point = {'x': 0, 'y': 0}
introSong = ""

# Initializes the canvas, and adds the frame.
def init():
  global point, canvas
  
  # Project directory that all visual/audio resources will be pulled from
  setMediaFolder("C:\Users\Papa Casper\Desktop\ByteBistro_FinalProject\\")
  
  # Create the empty canvas for the frame to be placed onto
  canvas = makeEmptyPicture(701,501)
  frame = makePicture("frame.png")
  
  # Place frame.png onto the canvas
  copyInto(frame, canvas, 0 ,0 )
  
  # Starting coordinates for the cursor
  point['x'] = getWidth(canvas)/2;
  point['y'] = getHeight(canvas)/2;
  
  # Display initial canvas
  show(canvas)
  
# Simulates the dials on an Etch-A-Sketch by moving drawing coordinates.
def dial(x, y):
  # Ensures the cursor remains within the white frame's boundaries
  if (point['x'] + x > 80) and (point['x'] + x <= 620) and (point['y'] + y > 70) and (point['y'] + y <= 425):
    # Adds a line with coordinates based on the direction provided by the user
    addLine(canvas, point['x'], point['y'], point['x']+ x, point['y']+ y )
    
    # Set the new coordinates of the cursor
    point['x'] += x
    point['y'] += y
    
    # Update the canvas with the new line
    repaint(canvas)
  
  #The shake function is used to clear the screen.
def shake(shakecount, canvas):
  soundShake = makeSound("rattle.wav")
  
  # If shake() has already been called 3 times, reset the canvas
  if shakecount >= 3:
    frame = makePicture("frame.png")
    copyInto(frame, canvas, 0 ,0 )
    repaint(canvas)
    play(soundShake)
    return 0
  
  # Iterate through the white canvas only (80 < x < 620) skipping every 1st, 2nd, 3rd, or 4th
  for x in range(80, 620, random.randint(1, 4)):
    # Iterate through the white canvas only (73 < y < 425) skipping every 1st, 2nd, 3rd, or 4th
    for y in range(73, 425, random.randint(1, 4)):
      p = getPixel(canvas, x, y)
      # 50/50 chance for changing or keeping the pixel as is
      r = random.randint(1, 2)
      if r == 1:
        # Set the pixel to white
        setColor(p, makeColor(255, 255, 255))
  repaint(canvas)
  play(soundShake)
  
  # Increase shakecount and inform main() of its new value
  return (shakecount + 1)

# Determines the length of the line based on the number of directional keys that were entered
def getChars(char, str, len):
  press = 0
  for key in str:
    if key == char:
      press += len  
  return press

#Code used to display the help menu
def displayHelp():
  showInformation("Welcome to Etch-A-Sketch\nTo play, use the following command reference:\n\n\
  w - moves the cursor up\n\
  s - moves the cursor down\n\
  a - moves the cursor to the left\n\
  d - moves the cursor to the right\n\
  aw - moves the cursor up to the left, diagonally\n\
  wd - moves the cursor up to the right, diagonally\n\
  sw - moves the cursor down to the left, diagonally\n\
  sd - moves the cursor down to the right, diagonally\n\n\
  These keys can be inputted multiple times to repeat the action\n\
  www - moves the cursor up three times\n\
  awawaw - moves the cursor up to the left three times\n\
  Other commands:\n\
  shake - distorts the picture; clears the picture completely after 4 shakes\n\
  help - displays this window\n\
  save - saves your drawing with the desired filename")
     
def main():
  # Setup the canvas and initialize the starting point
  init()
  draw = true
  
  # Length of pixels to draw for every directional command
  len = 20
  
  # Maintain the number of times that shake() was called
  shakecount = 0
  
  # Begin playing background music
  introSong = makeSound("music.wav")
  play(introSong)
  
  # Show help before prompting for the first command
  displayHelp()

  while(draw):
    str = requestString("Enter a command (or type 'help' to show possible commands):")
    x = 0
    y = 0
    if(str == 'shake'):
      shakecount = shake(shakecount, canvas)
      continue;
    elif(str == 'save'):
      while(True):
        filename = requestString("Enter the filename you would like to save your picture as without any extension:")
        if not filename:
          # If invalid filename, prompt again
          continue;
        else:
          # Create a new canvas to add the date to
          outputcanvas = makeEmptyPicture(701,501)
          pyCopy(canvas, outputcanvas, 0 ,0 )
          
          # Get the current date/time
          now = datetime.datetime.now()
          # Set the current date/time; format as Year Month Date Hour:Minutes AM/PM
          addTextWithStyle(outputcanvas, 130, 465, "This masterpiece was created at: " + 
          now.strftime("%Y-%m-%d %I:%M %p"), makeStyle("Comic Sans", Font.ITALIC, 16))
          
          # Append .png to the filename and save
          writePictureTo(outputcanvas, filename + ".png")
          
          # Indicate that the file was saved
          showInformation("File saved!\n" + filename + ".png")
          break;
    elif(str == 'help'):
      displayHelp()
      continue;
    else:
      y += getChars('s', str, len)
      y -= getChars('w', str, len)
      x += getChars( 'd', str, len)
      x -= getChars( 'a', str, len)
    dial(x,y)
    if(str == "exit"):
      stopPlaying(introSong)
      draw = false

# Used to create a copy of the canvas before saving to PNG            
def pyCopy(source, target, targetX, targetY):
  for x in range(0, getWidth(source)):
    for y in range(0, getHeight(source)):
      setColor(getPixel(target, x + targetX, y + targetY), getColor(getPixel(source, x, y)))
  return target

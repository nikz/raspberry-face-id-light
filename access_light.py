# This is a demo of running face recognition on a Raspberry Pi.
# This program will print out the names of anyone it recognizes to the console.

# To run this, you need a Raspberry Pi 2 (or greater) with face_recognition and
# the picamera[array] module installed.
# You can follow this installation instructions to get your RPi set up:
# https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65


import face_recognition
import picamera
import numpy as np
import unicornhat
from time import sleep

unicornhat.brightness(0.5)

def turn_on_green_light():
    print("GREEN")
    unicornhat.set_all(0,255,0)
    unicornhat.show()

def turn_on_red_light():
    print("RED")
    unicornhat.set_all(255,0,0)
    unicornhat.show()

# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.
camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

# Load a sample picture and learn how to recognize it.
unicornhat.set_all(0, 0, 255)
unicornhat.show()

print("Loading known face image(s)")
allowed_image = face_recognition.load_image_file("allowed.jpg")
allowed_face_encoding = face_recognition.face_encodings(allowed_image)[0]

unicornhat.off()

# Initialize some variables
face_locations = []
face_encodings = []

while True:
    unicornhat.off()

    print("Capturing image.")
    unicornhat.set_all(255, 255, 255)
    unicornhat.show()

    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(output)
    print("Found {} faces in image.".format(len(face_locations)))
    face_encodings = face_recognition.face_encodings(output, face_locations)

    unicornhat.off()

    # Loop over each face found in the frame to see if it's someone we know.
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(
            [allowed_face_encoding], face_encoding)
        name = "<Unknown Person>"

        if match[0]:
            name = "Matty the Patty"
            # turn on the green light!
            turn_on_green_light()
            sleep(3.5)
        else:
            # turn on the red light!
            turn_on_red_light()
            sleep(3.5)
            

        print("I see someone named {}!".format(name))

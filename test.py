import sys, threading, time, random, string
#Change your path !
sys.path.insert(0,"C:\\Users\\ajith\\Desktop\\LeapSDK")
import Leap
#PIL or Pillow should be installed
from PIL import Image
import ctypes

n = 0

count = 1
def increment():
        global count
        count = count+1

class SampleListener(Leap.Listener):
    
    def on_connect(self, controller):
        print ("Connected")

    def on_frame(self, controller):
        print ("Frame available")
        time.sleep(0.5)#2 second sleep
        frame = controller.frame()
        increment()
        if frame.is_valid:
            leap_image = frame.images[0]            
            print(leap_image)
            imagedata = ctypes.cast(leap_image.data.cast().__long__(), ctypes.POINTER(leap_image.width*leap_image.height*ctypes.c_ubyte)).contents
            image = Image.frombuffer("L", (leap_image.width, leap_image.height), imagedata, "raw", "L", 0, 1)
            #Do whatever you want with the PIL image          
            #image_path = "C:\\Users\\ajith\\Desktop\\Capstone Project\\pyparrot\\handpicture"
            image.save(str(count)+'.png')
            print(count)
    def on_exit(self, controller):
        print ("Exited")

listener = SampleListener()
controller = Leap.Controller()

#You need to unable the image policy in Leap Motion app settings
controller.set_policy_flags(Leap.Controller.POLICY_IMAGES)

# Sample listener receive events from the controller
controller.add_listener(listener)

# Keep this process running until Enter is pressed
print ("Press Enter to quit...")
try:
    sys.stdin.readline()
except KeyboardInterrupt:
    pass
finally:
    # Remove the sample listener when done
    controller.remove_listener(listener)
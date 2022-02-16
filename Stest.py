import socket
import Leap, sys, time
count =0
d=0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #this is the client
s.connect((socket.gethostname(), 1234))
def tkoff():
  global d
  d=d+1
  return d

class senddata:
    def __init__(self,data=""):
        self.data=data
    def get_data(self):
        return self._data
    def set_data(self,x):
        self._data=x
datacon=senddata()

class SampleListener(Leap.Listener):
    time.sleep(1)
    def on_init(self, controller):
        pass

    def on_connect(self, controller):
        pass

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        pass

    def on_exit(self, controller):
        pass

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()   
        print("Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (frame.id, frame.timestamp, len(frame.hands), len(frame.fingers)))
        handnum=len(frame.hands)
        if(handnum==0 and d>=2):
            
            print("4 0 0 0 0\n")
            f=open("demo.txt","a")
            f.write("4 0 0 0 0\n")
            x = "4 0 0 0 0"

            datacon.set_data(x)
            msg = datacon.get_data() #this sends data to server
            time.sleep(1)
            s.send(msg.encode())
            
            f.close()

        # Get hands     
        for hand in frame.hands:
            handType = "Left hand" if hand.is_left else "Right hand"

            if(handnum==2):
                f=open("demo.txt","a")
                f.write("3 landing\n")
                x = "3 landing"

                datacon.set_data(x)
                msg = datacon.get_data() #this sends data to server
                s.send(msg.encode())
                
                print("4")
                f.close()
                exit()
            elif(handType=="Right hand"):
                if(d>=1):
                    print("4 0 0 0 0\n")
                    f=open("demo.txt","a")
                    f.write("4 0 0 0 0\n")
                    x = "4 0 0 0 0"

                    datacon.set_data(x)
                    msg = datacon.get_data() #this sends data to server
                    time.sleep(1)
                    s.send(msg.encode())

                    f.close()
                else:
                    f=open("demo.txt","a")
                    f.write("1 takeoff\n")
                    print("1")
                    sd="1 takeoff"
                    

                    datacon.set_data(sd)
                    msg = datacon.get_data() #this sends data to server
                    s.send(msg.encode())
                    time.sleep(5)
                    x=tkoff()
                    f.close()
                
            elif(handType=="Left hand"):                
                print("2")
                x=tkoff()                                         
                print("  %s, id %d, position: %s" % (
                handType, hand.id, hand.palm_position.y))

                # Get the hand's normal vector and direction
                normal = hand.palm_normal
                direction = hand.direction

                # Calculate the hand's pitch, roll, and yaw angles
                print("  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                    direction.pitch * Leap.RAD_TO_DEG,
                    normal.roll * Leap.RAD_TO_DEG,
                    direction.yaw * Leap.RAD_TO_DEG))
                f=open("demo.txt","a")    
                f.write("2 "+str(int(direction.pitch * Leap.RAD_TO_DEG))+" "+str(int(normal.roll * Leap.RAD_TO_DEG))+" "+str(int(direction.yaw * Leap.RAD_TO_DEG))+" "+str(int(hand.palm_position.y))+"\n")
                #x ="2 "+str(int(direction.pitch * Leap.RAD_TO_DEG))+" "+str(int(normal.roll * Leap.RAD_TO_DEG))+" "+str(int(direction.yaw * Leap.RAD_TO_DEG))+" "+str(int(hand.palm_position.y))
                x ="2 "+str(int(normal.roll * Leap.RAD_TO_DEG))+" "+str(int(direction.pitch * Leap.RAD_TO_DEG))+" "+str(int(direction.yaw * Leap.RAD_TO_DEG))+" "+str(int(hand.palm_position.y))
                print(x)
                datacon.set_data(x)
                msg = datacon.get_data() #this sends data to server
                time.sleep(1)
                s.send(msg.encode())
                f.close() 

                
def main():
    if(d==0):
        f=open("demo.txt","w")
        f.write("")
        
        
    
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print("Press Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
import cv2
import mediapipe as mp
import time
from directkeys import right_pressed,left_pressed,enter_pressed,up_arrow_pressed,down_arrow_pressed
from directkeys import PressKey, ReleaseKey  


break_key_pressed=left_pressed
accelerato_key_pressed=right_pressed
enter_key_pressed=enter_pressed
up_arrow_key_pressed = up_arrow_pressed
down_arrow_key_pressed = down_arrow_pressed

game_started=0
last_general_time=time.time()
last_left_time=last_general_time
last_game_time=last_general_time
last_right_time=last_general_time
# time.sleep(2.0)
current_key_pressed = set()
last_enter_time = time.time()
last_up_time = time.time()
last_down_time = time.time()
mp_draw=mp.solutions.drawing_utils
mp_hand=mp.solutions.hands


tipIds=[4,8,12,16,20]

video=cv2.VideoCapture(0)

with mp_hand.Hands(min_detection_confidence=0.4,
               min_tracking_confidence=0.5) as hands:
    while True:
        keyPressed = False
        break_pressed=False
        accelerator_pressed=False
        key_count=0
        key_pressed=0
        ret,image=video.read()
        image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable=False
        results=hands.process(image)
        image.flags.writeable=True
        image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmList=[]
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands=results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h,w,c=image.shape
                    cx,cy= int(lm.x*w), int(lm.y*h)
                    lmList.append([id,cx,cy])
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)
        fingers=[]
        if len(lmList)!=0:
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1,5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total=fingers.count(1)
            if total==0:
                if game_started==1:
                    cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                    cv2.putText(image, "BRAKE", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (255, 0, 0), 5)
                    PressKey(break_key_pressed)
                    break_pressed=True
                    current_key_pressed.add(break_key_pressed)
                    key_pressed=break_key_pressed
                    keyPressed = True
                    key_count=key_count+1
                else:
                    if time.time() - last_general_time > 1.0:  # Check if 2 seconds have passed since the last enter press
                        cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                        cv2.putText(image, "Left", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255, 0, 0), 5)
                        PressKey(break_key_pressed)
                        break_pressed=True
                        current_key_pressed.add(break_key_pressed)
                        key_pressed=break_key_pressed
                        keyPressed = True
                        key_count=key_count+1
                        last_general_time = time.time()
            elif fingers[1]==1 and fingers[2]==1 and fingers[0]==0 and fingers[3]==0 and fingers[4]==0:
                if time.time() - last_game_time > 1.0:
                    if game_started==0:
                        game_started=1
                    else:
                        game_started=0
                if game_started==0:
                        cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                        cv2.putText(image, "General", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255, 0, 0), 5)
                else:
                    cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                    cv2.putText(image, "Gaming", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (255, 0, 0), 5)
                last_game_time=time.time()
            elif total==5:
                if game_started==1:
                    cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                    cv2.putText(image, " GAS", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (255, 0, 0), 5)
                    PressKey(accelerato_key_pressed)
                    key_pressed=accelerato_key_pressed
                    accelerator_pressed=True
                    keyPressed = True
                    current_key_pressed.add(accelerato_key_pressed)
                    key_count=key_count+1
                else:
                    if time.time() - last_general_time > 1.0:
                        cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                        cv2.putText(image, " Right", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255, 0, 0), 5)
                        PressKey(accelerato_key_pressed)
                        key_pressed=accelerato_key_pressed
                        accelerator_pressed=True
                        keyPressed = True
                        current_key_pressed.add(accelerato_key_pressed)
                        key_count=key_count+1
                        last_general_time=time.time()
            elif total==1 and fingers[0] != 1 and fingers[4] != 1:
                if time.time() - last_general_time > 2.0:  # Check if 2 seconds have passed since the last enter press
                    cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                    cv2.putText(image, " Enter", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                    PressKey(enter_key_pressed)
                    key_pressed = enter_key_pressed
                    enter_pressed = True
                    keyPressed = True
                    current_key_pressed.add(enter_key_pressed)
                    key_count += 1
                    last_general_time = time.time()
            else:
                if fingers[0] == 1 and fingers[4]==0 and time.time() - last_general_time > 1.0: 
                    cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                    cv2.putText(image, " Up Arrow", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                    PressKey(up_arrow_key_pressed)
                    key_pressed = up_arrow_key_pressed
                    keyPressed = True
                    current_key_pressed.add(up_arrow_key_pressed)
                    key_count = key_count + 1
                    last_general_time = time.time()
                elif fingers[4] == 1 and fingers[0]==0 and time.time() - last_general_time > 1.0:
                     cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                     cv2.putText(image, " Down Arrow", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                     PressKey(down_arrow_key_pressed)
                     key_pressed = down_arrow_key_pressed
                     keyPressed = True
                     current_key_pressed.add(down_arrow_key_pressed)
                     key_count = key_count + 1
                     last_general_time = time.time()
        if not keyPressed and len(current_key_pressed) != 0:
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed = set()
        elif key_count==1 and len(current_key_pressed)==2:    
            for key in current_key_pressed:             
                if key_pressed!=key:
                    ReleaseKey(key)
            current_key_pressed = set()
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed = set()


            # if lmList[8][2] < lmList[6][2]:
            #     print("Open")
            # else:
            #     print("Close")
        cv2.imshow("Frame",image)
        k=cv2.waitKey(1)
        if k==ord('q'):
            break
video.release()
cv2.destroyAllWindows()

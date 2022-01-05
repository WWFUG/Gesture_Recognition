import mediapipe as mp
import cv2

DIR = "./dataset/"
CATEGORY = ['A', 'B', 'C','D','E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O'
            , 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'space' ]
DNUM = 3000
mp_hands = mp.solutions.hands

OUT_FILE = "./train.csv"
fout = open(OUT_FILE, 'w')
with mp_hands.Hands( model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    for cl, sub_dir in enumerate(CATEGORY[:]):
        for i in range(DNUM):
            print("{}{}".format(sub_dir, i+1))
            img = cv2.imread( DIR + sub_dir + "/" + sub_dir + str(i+1) + ".jpg")
            results = hands.process(img)
            if results.multi_hand_landmarks:
                line = str()
                for hand_landmarks in results.multi_hand_landmarks:
                    if len(hand_landmarks.landmark)!=21: continue
                    for lm in hand_landmarks.landmark:
                        line += (str(lm.x) + ',' + str(lm.y) + ',' + str(lm.z))
                        #print(lm.x, lm.y, lm.z)
                        line += ','
                    line += str(cl)  
                    fout.write(line)
                    fout.write('\n')
            
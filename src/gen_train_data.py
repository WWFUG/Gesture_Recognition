import mediapipe as mp
import cv2
import os

DIR = "./dataset/"
# CATEGORY = ['A', 'B', 'C','D','E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O'
# 			 , 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'space' ]
CATEGORY = ['G']
OUT_FILE = "./train2.csv"


fout = open(OUT_FILE, 'w')
mp_hands = mp.solutions.hands

with mp_hands.Hands( model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1, static_image_mode = False ) as hands:
	for cl, ch in enumerate(CATEGORY):

		full_dir = DIR + ch + '/'
		nFiles = len( os.listdir(full_dir) )

		for i, fname in enumerate(os.listdir(full_dir)):
			fpath = full_dir + fname
			print("%5s %4d/%d %s" % (ch, i+1, nFiles, fname) )
			img = cv2.imread( fpath )
			results = hands.process(img)
			if results.multi_hand_landmarks:
				for hand_landmarks in results.multi_hand_landmarks:
					if len(hand_landmarks.landmark)!=21: 
						continue
					line = str()
					for lm in hand_landmarks.landmark:
						line += (str(lm.x) + ',' + str(lm.y) + ',' + str(lm.z))
						line += ','
					line += str(cl)  
					fout.write(line)
					fout.write('\n')
			else:
				# os.remove(fpath)
				print( 'not found' )
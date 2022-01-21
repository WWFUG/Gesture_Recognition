import cv2
import mediapipe as mp
import sys

from enum import Enum
from collections import Counter
from sound import speech
from server_MQTT.publisher import send, connect
from settings import DEFAULT_TOPIC

mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles
mp_drawing = mp.solutions.drawing_utils

class State(Enum):
	READ = 0
	INPUT = 1

from predict import Predictor
p = Predictor()
connect()


use_webcam = False
# vcap = cv2.VideoCapture("rtmp://172.20.10.7/rtmp/live")		# rtmp
vcap = cv2.VideoCapture("rtmp://192.168.55.1/rtmp/live")		# rtmp

# vcap = cv2.VideoCapture(0) 										# webcam
# use_webcam = True

vcap.set(cv2.CAP_PROP_BUFFERSIZE, 1)


DRAW_INTERVAL = 4
PRED_INTERVAL = 6
SWITCH_INTERVAL = 5
CLEAR_INTERVAL = 3

if len(sys.argv) < 2: 
	TOPIC = DEFAULT_TOPIC
else:
	TOPIC = sys.argv[1]
print( "Publish to topic \"", TOPIC, "\"" )



##
i=0
predict_buf = []
word_buf = ""
cur_state = State.READ
prev_ret_ch = ""
no_hand_cnt = CLEAR_INTERVAL

display_str = ""
result = None


with mp_hands.Hands( model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1, static_image_mode=False ) as hands:

	while True:
		ret, image = vcap.read()
		image = cv2.resize(image, (540, 360))
		if ( not use_webcam ):
			image = cv2.flip(image, 0)
			image = cv2.flip(image, 1)

		# To improve performance, optionally mark the image as not writeable to
		# pass by reference.
		image.flags.writeable = False
		image_pred = cv2.cvtColor( image, cv2.COLOR_BGR2RGB )

		if i%DRAW_INTERVAL==0:

			results = hands.process(image_pred)

			# Draw the hand annotations on the image.
			if no_hand_cnt >= CLEAR_INTERVAL:
				#print("Clear buffer")
				predict_buf = []
				cur_state = State.READ
				prev_ret_cn = ""

			if results.multi_hand_landmarks:
				no_hand_cnt = 0
				for hand_landmarks in results.multi_hand_landmarks:

					# predict 
					ch = p.predict( hand_landmarks.landmark )
					# send( TOPIC, ch )

					predict_buf.append(ch)
					if cur_state == State.READ:
						if len(predict_buf)==PRED_INTERVAL:
							occur = Counter(predict_buf)
							ret_ch, cnt = occur.most_common()[0]
							if cnt > PRED_INTERVAL/2:
								if ret_ch == 'del':
									print('\b \b', flush=True, end='')
									if ( len(word_buf) > 0 ):
										word_buf = word_buf[:-1]
										display_str = display_str[:-1]
								elif ret_ch == 'wait':
									pass
								elif ret_ch == 'space':
									print(" ", flush=True, end='')
									send( TOPIC, word_buf )
									word_buf = ""
									display_str += " "
								else:
									print(ret_ch, flush=True, end='')
									word_buf += ret_ch
									display_str += ret_ch
								# print(ret_ch, flush=True, end='')
								cur_state = State.INPUT
								prev_ret_ch = ret_ch
								predict_buf = []
							else:
								predict_buf.pop(0)
					elif cur_state == State.INPUT:
						if len(predict_buf) == SWITCH_INTERVAL:
							occur = Counter(predict_buf)
							if occur[prev_ret_ch] < SWITCH_INTERVAL/2:
								#print("Change Character")
								cur_state = State.READ
							else:
								predict_buf.pop(0)
			else:
				no_hand_cnt += 1
			i=0

		if results != None and results.multi_hand_landmarks:

			for hand_landmarks in results.multi_hand_landmarks:

				# draw
				mp_drawing.draw_landmarks(
					image,
					hand_landmarks,
					mp_hands.HAND_CONNECTIONS,
					mp_drawing_styles.get_default_hand_landmarks_style(),
					mp_drawing_styles.get_default_hand_connections_style())

		# display_str = "AAAAABBBBBCC"
		image = cv2.flip(image, 1)
		image = cv2.resize(image, (1080, 720))
		short_display_str = display_str[-12:]
		cv2.rectangle(image, (0, 700), (1080, 590), (0, 0, 0, 0.5), -1)
		pos = (5, 670)
		cv2.putText(image, short_display_str+"_", pos, cv2.FONT_HERSHEY_COMPLEX_SMALL, 4, (255, 255, 255), 1, cv2.LINE_AA)
		cv2.imshow('American Sign Language Recognition', image)
		if cv2.waitKey(1)  & 0xFF==ord('4'):
			break
		i += 1 
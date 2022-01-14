import cv2
import mediapipe as mp
import timeit
import time
from enum import Enum
from collections import Counter
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles
mp_drawing = mp.solutions.drawing_utils

from sound import speech
from server_MQTT.publisher import send

class State(Enum):
	READ = 0
	INPUT = 1

# vcap = cv2.VideoCapture("rtmp://192.168.55.1/rtmp/live")		# rtmp
vcap = cv2.VideoCapture(0) 										# webcam
vcap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

DRAW_INTERVAL = 2
PRED_INTERVAL = 6
SWITCH_INTERVAL = 4
CLEAR_INTERVAL = 10
i=0

##
predict_buf = []
pred_i = 0
switch_i = 0
cur_state = State.READ
prev_ret_ch = ""
no_hand_cnt = CLEAR_INTERVAL


from predict import Predictor
p = Predictor()


with mp_hands.Hands( model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1, static_image_mode=False ) as hands:

	while True:
		mep = timeit.default_timer()
		ret, image = vcap.read()
		#image = cv2.resize(frame, (1080, 560))

		# To improve performance, optionally mark the image as not writeable to
		# pass by reference.
		if i%DRAW_INTERVAL==0:
			image.flags.writeable = False
			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			results = hands.process(image)

			# Draw the hand annotations on the image.
			image.flags.writeable = True
			image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
			start = timeit.default_timer()

			if no_hand_cnt >= CLEAR_INTERVAL:
				#print("Clear buffer")
				predict_buf = []
				cur_state = State.READ
				prev_ret_cn = ""

			if results.multi_hand_landmarks:
				no_hand_cnt = 0
				for hand_landmarks in results.multi_hand_landmarks:
					# draw
					mp_drawing.draw_landmarks(
						image,
						hand_landmarks,
						mp_hands.HAND_CONNECTIONS,
						mp_drawing_styles.get_default_hand_landmarks_style(),
						mp_drawing_styles.get_default_hand_connections_style())

					# predict 
					ch = p.predict( hand_landmarks.landmark )
					# speech("mep")
					#send("mep")
					predict_buf.append(ch)
					# print(cur_state.name)
					if cur_state == State.READ:
						if len(predict_buf)==PRED_INTERVAL:
							occur = Counter(predict_buf)
							ret_ch, cnt = occur.most_common()[0]
							if cnt > PRED_INTERVAL/2:
								if ret_ch == 'del':
									print('\b \b', flush=True, end='')
								elif ret_ch == 'wait':
									pass
								elif ret_ch == 'space':
									print(" ", flush=True, end='')
								else:
									print(ret_ch, flush=True, end='')
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

		cv2.imshow('MediaPipe Hands', image)
		if cv2.waitKey(1)  & 0xFF==ord('4'):
			break
		i += 1 
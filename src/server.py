import cv2
import mediapipe as mp
import timeit
import time
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles
mp_drawing = mp.solutions.drawing_utils

from sound import speech
# from server_MQTT.publisher import send


# vcap = cv2.VideoCapture("rtmp://192.168.43.196/rtmp/live")		# rtmp
vcap = cv2.VideoCapture(0) 										# webcam
vcap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

interval = 2
i=0
from predict import Predictor
p = Predictor()

with mp_hands.Hands( model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1, static_image_mode=False ) as hands:

	while True:
		mep = timeit.default_timer()
		ret, image = vcap.read()
		image = cv2.resize(image, (1080, 720))


		# To improve performance, optionally mark the image as not writeable to
		# pass by reference.
		if i%interval==0:
			image.flags.writeable = False
			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			# results = hands.process(image)

			# Draw the hand annotations on the image.
			image.flags.writeable = True
			image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
			start = timeit.default_timer()

			# if results.multi_hand_landmarks:

			# 	for hand_landmarks in results.multi_hand_landmarks:
			# 		# draw
			# 		mp_drawing.draw_landmarks(
			# 			image,
			# 			hand_landmarks,
			# 			mp_hands.HAND_CONNECTIONS,
			# 			mp_drawing_styles.get_default_hand_landmarks_style(),
			# 			mp_drawing_styles.get_default_hand_connections_style())

			# 		# predict 
			# 		ch = p.predict( hand_landmarks.landmark )
			# 		# speech("mep")
			# 		# send("mep")

			i=0
		cv2.imshow('MediaPipe Hands', image)
		if cv2.waitKey(1)  & 0xFF==ord('4'):
			break
		i += 1 
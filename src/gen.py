import cv2
import mediapipe as mp
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles
mp_drawing = mp.solutions.drawing_utils

vcap = cv2.VideoCapture(0) 										# webcam
vcap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

interval = 2
chars = ['A', 'B', 'C','D','E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O' ,
	'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'space', 'empty' ]
keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 
	'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3' ]
fname = './data/tmp.csv'

from pynput import keyboard

def on_press(key):
	try:
		global pressed
		pressed = '%s' % key.char
		# print('alphanumeric key {0} pressed'.format( key.char))
	except AttributeError:
		print('special key {0} pressed'.format(
			key))

def on_release(key):
	global pressed
	pressed = None
	# print('{0} released'.format(key))
	if key == keyboard.Key.esc:
		# Stop listener
		return False

# Collect events until released
listener = keyboard.Listener(
	on_press=on_press,
	on_release=on_release)
listener.start()

fout = open(fname, 'w')
char_label = { ch:i for i, ch in enumerate(chars) }
key_label = { key:i for i, key in enumerate(keys) }
data_count = {}
pressed = None
interval_cnt = 0
enable = False

from predict import Predictor
p = Predictor()
 
with mp_hands.Hands( model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1 ) as hands:

	while True:
		ret, image = vcap.read()
		#image = cv2.resize(frame, (1080, 560))


		# To improve performance, optionally mark the image as not writeable to
		# pass by reference.
		image.flags.writeable = False
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		results = hands.process(image)

		# Draw the hand annotations on the image.
		image.flags.writeable = True
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
		if results.multi_hand_landmarks:
			for hand_landmarks in results.multi_hand_landmarks:
				ch = p.predict(hand_landmarks.landmark)
				print(ch)
				# draw
				mp_drawing.draw_landmarks(
					image,
					hand_landmarks,
					mp_hands.HAND_CONNECTIONS,
					mp_drawing_styles.get_default_hand_landmarks_style(),
					mp_drawing_styles.get_default_hand_connections_style())

		image = cv2.flip( image, 1 )
		cv2.imshow('MediaPipe Hands', image)
		if cv2.waitKey(1)  & 0xFF==ord('4'):
			break

		# add to csv
		if interval_cnt % interval == 0:

			if (pressed != None) and (pressed in key_label):

				interval_cnt = 1

				if results.multi_hand_landmarks:
					for hand_landmarks in results.multi_hand_landmarks:
						if len(hand_landmarks.landmark)!=21: 
							continue
						data_count[pressed] = data_count.get(pressed, 0) + 1
						print( pressed, data_count[pressed] )
						line = str()
						for lm in hand_landmarks.landmark:
							line += (str(lm.x) + ',' + str(lm.y) + ',' + str(lm.z))
							line += ','
						line += str(key_label[pressed])  
						fout.write(line)
						fout.write('\n')


		else:
			interval_cnt += 1

		
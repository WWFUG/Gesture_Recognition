from pycaret.classification import *
import pandas as pd

char = ['A', 'B', 'C','D','E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O'
			 , 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'space', 'wait' ]
mapping = { i:ch for i, ch in enumerate(char) }

class Predictor:

	def __init__( self ):

		self.model = load_model( './model/model')
	
	def predict( self, landmark ):

		if len(landmark) != 21: 
			return None

		feature = []
		for lm in landmark:
			feature += [ lm.x, lm.y, lm.z ]
		feature = pd.DataFrame( [feature] ) 

		# result, score = predict_model( self.model, feature )[['Label', 'Score']].iloc[0]
		# print( '%5s %5.3f' % (mapping[result], score) )
		result = predict_model( self.model, feature )['Label'].iloc[0]
		#print( '%5s' % (mapping[result]) )

		return mapping[result]


		

		
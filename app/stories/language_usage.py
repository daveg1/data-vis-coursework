from pandas import DataFrame
from altair import *

class LanguageUsage:

	@staticmethod
	def format_data(data: DataFrame) -> DataFrame:
		subset = data[['language', 'theme']]
		return subset.value_counts().reset_index(name='occurrence')

	@staticmethod
	def create_pie(data) -> Chart:
		return Chart(data).mark_arc().encode(
			theta=Theta(field='occurrence', type='quantitative'),
			color=Color(field='language', type='nominal', title='Languages'),
		)
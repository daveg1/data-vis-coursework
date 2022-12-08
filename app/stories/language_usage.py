from pandas import DataFrame
from plotly.graph_objects import Figure
from plotly.express import *

class LanguageUsage:

	@staticmethod
	def format_data(data: DataFrame) -> DataFrame:
		subset = data[['language', 'theme']]
		return subset.value_counts().reset_index(name='occurrence')

	@staticmethod
	def create_pie(data) -> Figure:
		fig = pie(data,
			values='occurrence',
			names='language',
			color_discrete_sequence=data['theme'],
			height=600)

		fig.update_traces(textposition='inside', textinfo='percent+label')

		return fig
from plotly.graph_objects import *
from pandas import DataFrame

class GeoPlot:

	@staticmethod
	def create_map(data: DataFrame) -> Figure:
		choro = Choropleth(
			locations = data['country'],
			locationmode = 'country names',
			z = data['users'],
			text = data['framework'],
			reversescale=True,
			marker_line_color='darkgray',
			marker_line_width=0.5
		)

		return Figure(data=choro, layout={ 'height': 700 })

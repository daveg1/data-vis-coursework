from pandas import DataFrame
from altair import *

class StackOverflowQnA:

	@staticmethod
	def create_bar_gt(data: DataFrame, stacked: str) -> Chart:
		subset = data[['framework', 'total posts', stacked]]
		subset = subset[subset['total posts'] >= 200_000]
		return Chart(subset).mark_bar().encode(
			x='framework',
			y='total posts',
			color=stacked
		).properties(width=1000)

	@staticmethod
	def create_bar_lt(data: DataFrame, stacked: str) -> Chart:
		subset = data[['framework', 'total posts', stacked]]
		subset = subset[subset['total posts'] <= 200_000]

		return Chart(subset).mark_bar().encode(
			x='framework',
			y='total posts',
			color=stacked
		)

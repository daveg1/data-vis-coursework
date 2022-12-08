from altair import *
from pandas import DataFrame

class FrameworkUsage:

	@staticmethod
	def format_data(data: DataFrame) -> tuple[DataFrame, DataFrame]:
		# Have Used
		used = data[['framework', 'have used']]
		used.insert(2, 'type', 'have used')
		used.columns = ['framework', 'occurrence', 'type']

		# Want to Use
		want = data[['framework', 'want to use']]
		want.insert(2, 'type', 'want to use')
		want.columns = ['framework', 'occurrence', 'type']

		return (used, want)

	@staticmethod
	def graph_data(data: DataFrame) -> Chart:
		return Chart(data).mark_bar().encode(
			x='occurrence',
			y=Y('framework', sort='-x')
		).properties(width=700)

	@staticmethod
	def graph_pyramid(datasets: list[DataFrame, DataFrame]) -> ConcatChart:
		base = Chart(pd.concat(datasets))

		left = base.transform_filter(
			datum.type == 'have used'
		).encode(
			y=Y('framework:O', sort='-x', axis=None),
			x=X('occurrence:Q',sort=SortOrder('descending')),
		).mark_bar()

		middle = base.encode(
			y=Y('framework:O', axis=None, sort=None),
			text=Text('framework')
		).mark_text(color='white', opacity=0.75).properties(width=100)

		right = base.transform_filter(
			datum.type == 'want to use'
		).encode(
			y=Y('framework:O', sort='-x', axis=None),
				x=X('occurrence:Q',sort=SortOrder('ascending')),
		).mark_bar()

		return concat(left, middle, right, spacing=10)
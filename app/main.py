import streamlit as st
import pandas as pd
import os
from stories.framework_usage import FrameworkUsage
from stories.info_bubbles import InfoBubbles
from stories.language_usage import LanguageUsage
from stories.stack_overflow_qna import StackOverflowQnA
from stories.geoplot import GeoPlot

title = 'Frameworks of the Web'
st.set_page_config(page_title=title, layout="wide")

# Datasets
frameworks = pd.read_csv(os.path.abspath('app/data/frameworks.csv'), index_col=0)
langs_used = LanguageUsage.format_data(pd.read_csv(os.path.abspath('app/data/languages.csv')))
tags = pd.read_csv(os.path.abspath('app/data/tags.csv'))
countries = pd.read_csv(os.path.abspath('app/data/countries.csv'))
top_used, top_want = FrameworkUsage.format_data(frameworks)

# Apply custom styles
with open(os.path.abspath('app/style.css')) as css:
	st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

# Create main container
with st.container() as header:
	st.title(title)

	bar_col, pie_col = st.columns(2)

	# ==========
	# Story 1
	# ==========
	with st.container():
		st.header('At a Glance')

		top_framework_used = top_used.sort_values(by='occurrence', ascending=False).iloc[0]
		top_framework_want = top_want.sort_values(by='occurrence', ascending=False).iloc[0]

		bubbles = InfoBubbles.container([
			InfoBubbles.bubble(
				top_framework_used['framework'],
				f'Most used technology in 2022',
				f'used by <strong>{top_framework_used["occurrence"]:,}</strong> respondents'
			),
			InfoBubbles.bubble(
				top_framework_want['framework'],
				f'Most desired technology for 2023',
				f'as expressed by <strong>{top_framework_want["occurrence"]:,}</strong> respondents'
			),
		])

		st.markdown(bubbles, unsafe_allow_html=True)

	# ==========
	# Story 2
	# ==========
	with st.container():
		st.header('Top Frameworks by Current Usage')

		tab1, tab2 = st.tabs(['Split Graphs', 'Side-by-Side'])

		with tab1:
			col1, col2 = st.columns(2)

			with col1:
				st.subheader('Frameworks Used in 2022')
				st.altair_chart(FrameworkUsage.graph_data(top_used))
			with col2:
				st.subheader('Desired Frameworks for 2023')
				st.altair_chart(FrameworkUsage.graph_data(top_want))

		with tab2:
			st.subheader('Frameworks Used in 2022 vs Frameworks Desired for 2023')
			st.altair_chart(FrameworkUsage.graph_pyramid([top_used, top_want]), use_container_width=True)

	# ==========
	# Story 3
	# ==========
	with st.container():
		st.header('Languages Used by Frameworks')
		st.altair_chart(LanguageUsage.create_pie(langs_used))

	# ==========
	# Story 4
	# ==========
	with st.container():
		st.header('Stack Overflow Questions')
		tab1, tab2 = st.tabs(['Unanswered Posts', 'Unsolved Posts'])

		with tab1:
			st.altair_chart(StackOverflowQnA.create_bar(tags, 'unanswered posts'))

		with tab2:
			st.altair_chart(StackOverflowQnA.create_bar(tags, 'unsolved posts'))


	# ==========
	# Story 5
	# ==========
	with st.container():
		st.subheader('Framework Usage Around the Globe')

		df = pd.DataFrame([['United Kingdom of Great Britain and Northern I', 123]], columns=['country', 'value'])

		st.plotly_chart(GeoPlot.create_map(countries), use_container_width=True)

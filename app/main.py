import streamlit as st
import pandas as pd
import plotly.express as px
import os
from stories.framework_usage import FrameworkUsage
from stories.info_bubbles import InfoBubbles
from stories.language_usage import LanguageUsage
from stories.stack_overflow_qna import StackOverflowQnA
from stories.geoplot import GeoPlot

title = 'Frameworks of the Web'
st.set_page_config(page_title=title, layout="wide")

# Datasets
base_path = ''

if (os.getenv('PROD')):
	base_path = os.path.abspath('app')
else:
	base_path = os.path.abspath('.')

frameworks = pd.read_csv(os.path.join(base_path, 'data/frameworks.csv'), index_col=0)
langs_used = LanguageUsage.format_data(pd.read_csv(os.path.join(base_path, 'data/languages.csv')))
tags = pd.read_csv(os.path.join(base_path, 'data/tags.csv'))
countries = pd.read_csv(os.path.join(base_path, 'data/countries.csv'), index_col=0)
top_used, top_want = FrameworkUsage.format_data(frameworks)

# Apply custom styles
with open(os.path.join(base_path, 'style.css')) as css:
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

	with st.container():
		st.header('Top Frameworks by Current Usage')

		tab1, tab2 = st.tabs(['Split Graphs', 'Side-by-Side'])

		# ==========
		# Story 2
		# ==========

		with tab1:
			col1, col2 = st.columns(2)

			with col1:
				st.subheader('Frameworks Used in 2022')
				st.markdown('These were the frameworks respondents reported using in 2022')
				st.altair_chart(FrameworkUsage.graph_data(top_used))
			with col2:
				st.subheader('Desired Frameworks for 2023')
				st.markdown('These were the frameworks respondents wanted to use in 2023')
				st.altair_chart(FrameworkUsage.graph_data(top_want))

		# ==========
		# Story 3
		# ==========
		with tab2:
			st.subheader('Frameworks Used in 2022 vs Frameworks Desired for 2023')
			st.altair_chart(FrameworkUsage.graph_pyramid([top_used, top_want]), use_container_width=True)

	# ==========
	# Story 4
	# ==========
	with st.container():
		st.header('Languages Used by Frameworks')
		st.markdown('These are the languages the web frameworks are written in')
		st.plotly_chart(LanguageUsage.create_pie(langs_used), theme='streamlit')

	# ==========
	# Story 5
	# ==========
	with st.container():
		st.header('Stack Overflow Question Responses')
		st.markdown('Note: a post receiving a response does not necessarily mean it was solved.')
		tab1, tab2 = st.tabs(['Unanswered Posts', 'Answered Posts'])

		with tab1:
			st.subheader('Unanswered Posts')
			st.markdown('The number of posts that went unanswered')
			st.markdown('### Less than 200,000 Posts')
			st.altair_chart(StackOverflowQnA.create_bar_lt(tags, 'unanswered posts'))
			st.markdown('### greater than 200,000 Posts')
			st.altair_chart(StackOverflowQnA.create_bar_gt(tags, 'unanswered posts'))

		with tab2:
			st.subheader('Answered Posts')
			st.markdown('The number of posts that received an answer')
			st.markdown('### Less than 200,000 Posts')
			st.altair_chart(StackOverflowQnA.create_bar_lt(tags, 'answered posts'))
			st.markdown('### Greater than 200,000 Posts')
			st.altair_chart(StackOverflowQnA.create_bar_gt(tags, 'answered posts'))

	# ==========
	# Story 6
	# ==========
	with st.container():
		st.header('Stack Overflow Questions Solutions')
		st.markdown('The number of questions that were marked as solved')
		tab1, tab2 = st.tabs(['Unsolved Posts', 'Solved Posts'])

		with tab1:
			st.subheader('Unsolved Posts')
			st.markdown('The number of posts that went unsolved')
			st.markdown('### Less than 200,000 Posts')
			st.altair_chart(StackOverflowQnA.create_bar_lt(tags, 'unsolved posts'))
			st.markdown('### Greater than 200,000 Posts')
			st.altair_chart(StackOverflowQnA.create_bar_gt(tags, 'unsolved posts'))

		with tab2:
			st.subheader('Solved Posts')
			st.markdown('The number of posts that were marked as solved by the author')
			st.markdown('### Less than 200,000 Posts')
			st.altair_chart(StackOverflowQnA.create_bar_lt(tags, 'solved posts'))
			st.altair_chart(StackOverflowQnA.create_bar_gt(tags, 'solved posts'))


	# ==========
	# Story 7
	# ==========
	with st.container():
		st.subheader('Framework Usage Around the Globe')
		st.markdown('Hover over each country to see its most use framework')

		world_have_used = countries[countries['type'] == 'have used']

		st.plotly_chart(GeoPlot.create_map(world_have_used), use_container_width=True)
		# st.plotly_chart(GeoPlot.create_map(world_want_to_use), use_container_width=True)

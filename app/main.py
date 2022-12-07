import streamlit as st
import pandas as pd
from stories.framework_usage import FrameworkUsage
from stories.info_bubbles import InfoBubbles
from stories.language_usage import LanguageUsage

title = 'Frameworks of the Web'
# st.set_page_config(page_title=title, layout="wide")

# Read Data
frameworks = pd.read_csv('./data/frameworks.csv', index_col=0)
top_used, top_want = FrameworkUsage.format_data(frameworks)
langs_used = LanguageUsage.format_data(frameworks)

# Apply custom styles
with open('./style.css') as css:
	st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

# Create main container
with st.container() as header:
	st.title(title)

	# ==========
	# Story 1
	# ==========

	with st.expander('Story 1'):

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
	with st.expander('Story 2'):

		with st.container():
			st.header('Top Frameworks by Current Usage')
			st.altair_chart(FrameworkUsage.graph_data(top_used))

		with st.container():
			st.header('Top Frameworks by Desire to Use')
			st.altair_chart(FrameworkUsage.graph_data(top_want))

		with st.container():
			st.header('Comparison of Framework Usage')
			st.altair_chart(FrameworkUsage.graph_pyramid([top_used, top_want]), use_container_width=True)

	# ==========
	# Story 3
	# ==========
	with st.container():
		st.header('Language Share')
		st.altair_chart(langs_used)
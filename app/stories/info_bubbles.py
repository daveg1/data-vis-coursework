import streamlit as st
from altair import *

class InfoBubbles:

	@staticmethod
	def container(bubbles: list[str]) -> str:
		return f'''
		<div class="bubble-container">
			{' '.join(bubbles)}
		</div>
		'''


	@staticmethod
	def bubble(value: int, line1: str, line2: str) -> str:
		return f'''
		<div class="bubble">
			<span class="bubble__value">{value}</span>
			<span class="bubble__description">{line1}<br>{line2}</span>
		</div>
		'''

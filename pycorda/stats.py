from pycorda import Node
from datetime import datetime
import matplotlib
from matplotlib import pyplot
import pandas as pd
import chart_studio, chart_studio.plotly as py, plotly.graph_objs as go
from sklearn import linear_model as lm

# Format for timestamp string is YYYY-MM-DD HH:MM:SS.FFF

def plot_time_series(timestamp_column, title=None):
	"""Plots time series for a given sequence of timestamps

	Parameters
    ----------
    timestamp_column : iterable object
        iterable of timestamp strings in the %Y-%m-%d %H:%M:%S.%f format
    title : str, optional
    	figure title
	"""
	dt_list = [datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f') for timestamp in timestamp_column]
	dates = matplotlib.dates.date2num(dt_list)
	fig, ax = pyplot.subplots()
	if title is not None:
		ax.set_title(title)
	ax.plot_date(dates, [0]*len(dates))
	ax.fmt_xdata = matplotlib.dates.DateFormatter('%Y-%m-%d %H:%M:%S.%f')
	fig.autofmt_xdate()

def plot_ids(ids, fontsize, title=None):
	"""Plots IDs as labelled equally spaced points

	Parameters
    ----------
    ids : iterable object
        iterable of ID strings
    fontsize : int
    	font size of point labels
    title : str, optional
    	figure title
	"""
	sorted_ids = sorted(ids)
	n = len(ids)
	points = range(n)
	fig, ax = pyplot.subplots()
	if title is not None:
		ax.set_title(title)
	ax.scatter(points, [0]*n)
	for i, txt in enumerate(sorted_ids):
		ax.annotate(txt, (points[i], 0.001), ha='center', fontsize=fontsize)
	ax.set_xlim(-0.5, min(5, n))

class Plotter(object):
	"""Plotter object for plotting data obtained from a database node

	tbname_ts methods will plot time series for table TBNAME. After choosing which plots
	to create by calling the relevant methods, use the show method to
	display the plots.
	"""

	def __init__(self, node):
		"""
        Parameters
        ----------
        node: pycorda.Node
        	node used to gather data for display
        """
		self.node = node

	def publish_timeseries_fungible_qty_plotly(self, contract, user,api_key):
		chart_studio.tools.set_credentials_file(username=user,api_key=api_key)
		vault_states = self.node.get_vault_states()
		vault_states = vault_states[vault_states.CONTRACT_STATE_CLASS_NAME==contract]
		vault_fungible_states = self.node.get_vault_fungible_states()
		df = vault_states.merge(vault_fungible_states)[['RECORDED_TIMESTAMP','QUANTITY']]
		df['RECORDED_TIMESTAMP'] = pd.to_datetime(df['RECORDED_TIMESTAMP'])
		series = go.Scatter(
			x=df['RECORDED_TIMESTAMP'].tolist(),
			y=df['QUANTITY'].tolist()
		)
		data = [series]
		url = py.plot(data,filename='Coda - ' + contract)
		print('Link to your Plotly chart is',url)

	def plot_timeseries_node_attachments(self):
		df = self.node.get_node_attachments()
		plot_time_series(df['INSERTION_DATE'], 'Node attachments time series')

	def plot_timeseries_node_message_ids(self):
		df = self.node.get_node_message_ids()
		plot_time_series(df['INSERTION_TIME'], 'Node message IDs time series')

	def plot_timeseries_vault_states_consumed(self):
		df = self.node.get_vault_states()
		plot_time_series(df['CONSUMED_TIMESTAMP'].dropna(), 'Vault states consumed times')

	def plot_timeseries_fungible_qty(self,contract):
		vault_states = self.node.get_vault_states()
		vault_states = vault_states[vault_states.CONTRACT_STATE_CLASS_NAME==contract]
		vault_fungible_states = self.node.get_vault_fungible_states()
		df = vault_states.merge(vault_fungible_states)[['RECORDED_TIMESTAMP','QUANTITY']]
		df['RECORDED_TIMESTAMP'] = pd.to_datetime(df['RECORDED_TIMESTAMP'])
		df.plot(kind='line',x='RECORDED_TIMESTAMP',y='QUANTITY',color='red')
		print(df)

	# def vault_states_recorded_ts(self):
	# 	df = self.node.get_vault_states()[]
	# 	pyplot.plot()
	# def vault_states_recorded_ts(self):
	# 	df = self.node.get_vault_states()
	# 	plot_time_series(df['RECORDED_TIMESTAMP'].dropna(), 'Vault states recorded times')		

	def node_checkpoints_ids(self):
		df = self.node.get_node_checkpoints()
		plot_ids(df['CHECKPOINT_ID'], 9, 'Checkpoint IDs')

	def vault_states_status(self):
		"""Plots pie chart of the relative frequencies of vault state status"""
		df = self.node.get_vault_states()
		df['STATE_STATUS'].value_counts().plot.pie()

	def show(self):
		"""Displays all plots"""
		pyplot.show()

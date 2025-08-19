import pandas as pd
import numpy as np
import plotly.graph_objects as go

class binomialTree:
	def __init__(self, S0: float, u: float, d: float, p: float, n: int):
		"""
        Initializes a binomial tree object.

        Args:
            S0 (float): Initial stock price.
            u (float): Up factor.
            d (float): Down factor.
			p (float): Probability of upward movement.
			n (int): Number of periods.
        """
		if S0 < 0:
			raise ValueError("The stock price must be a positive number.")
		else:
			self.S0 = S0	# Asset price at t = 0
		
		if u < 1:
			raise ValueError("The up factor must be greater than 1.")
		else:
			self.u = u # Up factor

		if  (d < 0 or d > 1):
			raise ValueError("The down factor must lie in the open interval (0, 1).")
		else:
			self.d = d # Down factor

		if (p < 0 or p > 1):
			raise ValueError("The probability of an upward movement must lie in the open interval (0, 1).")
		
		if (isinstance(n, int) == False or n < 0):
			raise ValueError("The number of periods n must be a non-negative integer!")
		else:
			self.n = n # Number of periods
	
	def generate(self) -> pd.DataFrame:
		matrix = [[0] * (self.n + 1) for _ in range(self.n + 1)]
		for j in range(0, self.n + 1):
			for i in range(0, j + 1):
				matrix[i][j] = self.S0*(self.u**(j - i))*(self.d**i)
		return pd.DataFrame(matrix)


	# This plots the binomial tree. 
	def plot(self):
		df = self.generate()
		nodes_x = []
		nodes_y = []
		node_values = []
		edges_x = []
		edges_y = []

		n_periods = df.shape[1]
		for t in range(n_periods):
			for i in range(t + 1):
				price = df.iloc[i, t]
				if price != 0:
					nodes_x.append(t)
					nodes_y.append(price)
					node_values.append(price)
					if t < n_periods - 1:
						if i <= t and df.iloc[i, t + 1] != 0:
							edges_x.extend([t, t + 1, None])
							edges_y.extend([price, df.iloc[i, t + 1], None])
						if i + 1 <= t + 1 and df.iloc[i + 1, t + 1] != 0:
							edges_x.extend([t, t + 1, None])
							edges_y.extend([price, df.iloc[i + 1, t + 1], None])

		fig = go.Figure()
		fig.add_trace(go.Scatter(
			x=edges_x, y=edges_y,
			mode='lines',
			line=dict(color='black', width=1),
			hoverinfo='none'
		))
		fig.add_trace(go.Scatter(
			x=nodes_x, y=nodes_y,
			mode='markers+text',
			text=[f'${v:.2f}' for v in node_values],
			textposition='middle right',
			marker=dict(size=10, color='blue'),
			hoverinfo='text'
		))
		fig.update_layout(
			title='Binomial Stock Price Tree',
			xaxis_title='Period',
			yaxis_title='Stock Price ($)',
			showlegend=False,
			xaxis=dict(tickmode='linear', tick0=0, dtick=1),
			yaxis=dict(tickformat='.2f')
		)
		fig.show()



t = binomialTree(4, 2, 0.5, 0.25, 50)
print(t.generate())
t.plot()


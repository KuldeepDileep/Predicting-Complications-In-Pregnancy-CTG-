import numpy as np
import random

# it could be bad because in reality our cluster could be bigger, 
# if a doctor could give us ranges I could inc that into this code and our data could be more holistic

class data_for_cluster:
	def __init__(self, cluster):
		self.cluster = cluster
		self.centres = []
		self.radius = 0
		# set radius and centre
		self.ass_centre_rad()

	def check_cluster_validity(self, data_point, z):
		for i in range(self.cluster.shape[1]):
			if not self.check_circle(data_point, self.centres, self.radius):
				return False
		return True

	def check_datapoint_presence(self, data_point):
		for i in self.cluster:
			if np.array_equal(i, data_point):
				print("Datapoint already present.")
				return True
		return False

	def check_circle(self, points, centres, radius):
		sum_ = 0
		for i in range(len(centres)):
			sum_ += (points[i]-centres[i])**2
		if sum_ <= radius**2:
			return True
		return False

	def ass_centre_rad(self):
		radii = []
		for i in range(self.cluster.shape[1] - 1):
			col = self.cluster[:,i]

			col_max = np.max(col)
			col_min = np.min(col)
			centre = (col_max + col_min)/2
			radius = col_max - centre

			radii.append(radius)
			self.centres.append(centre)

		# create a point within hypersphere of cluster
		self.radius = np.max(radii)

	def create_row(self):
		row = []

		radii = []
		pts = []

		for i in range(self.cluster.shape[1] - 1):
			col = self.cluster[:,i]

			col_max = np.max(col)
			col_min = np.min(col)

			newp = random.uniform(col_min, col_max)
			pts.append(newp)
		row = pts
		tendency = [-1, 0, 1]
		row.append(tendency[np.random.randint(0,3)])
		return np.array(row)

	def from_cluster_get_feature(self, feature_no):
		return self.cluster[:,feature_no]

class cluster_extract:
	def __init__(self, features, labels):
		self.labels = labels
		self.features = features

	def get_cluster_from_data(self, label):
		idxs = np.array([i for i, x in enumerate(self.labels) if x == label])
		return np.array([x for i, x in enumerate(self.features) if i in idxs])


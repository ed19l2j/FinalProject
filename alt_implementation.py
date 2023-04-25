# 2-3 Tree
# balanced tree data structure with up to 2 data items per node

class Node:
	def __init__(self, data, par = None):
		self.data = list([data])
		self.parent = par
		self.child = list()

	def __str__(self):
		if self.parent:
			return str(self.parent.data) + ' : ' + str(self.data)
		return 'Root : ' + str(self.data)

	# less than function that does a comparison between two nodes
	def __lt__(self, node):
		return self.data[0] < node.data[0]

	# checks the length of the child nodes
	def _isLeaf(self):
		return len(self.child) == 0

	# merge new_node sub-tree into self node
	def _add(self, new_node):
		for child in new_node.child:
			child.parent = self
		self.data.extend(new_node.data)
		self.data.sort()
		self.child.extend(new_node.child)
		if len(self.child) > 1:
			self.child.sort()
		if len(self.data) > 2:
			self._split()

	# find correct node to insert new node into tree
	def _insert(self, new_node):
		# leaf node - add data to leaf and rebalance tree
		if self._isLeaf():
			self._add(new_node)

		# not leaf - find correct child to descend, and do recursive insert
		elif new_node.data[0] > self.data[-1]:
			self.child[-1]._insert(new_node)
		else:
			for i in range(0, len(self.data)):
				if new_node.data[0] < self.data[i]:
					self.child[i]._insert(new_node)
					break

	# 3 items in node, split into new sub-tree and add to parent
	def _split(self):
		left_child = Node(self.data[0], self)
		right_child = Node(self.data[2], self)
		if self.child:
			self.child[0].parent = left_child
			self.child[1].parent = left_child
			self.child[2].parent = right_child
			self.child[3].parent = right_child
			left_child.child = [self.child[0], self.child[1]]
			right_child.child = [self.child[2], self.child[3]]

		self.child = [left_child]
		self.child.append(right_child)
		self.data = [self.data[1]]

		# now have new sub-tree, self. need to add self to its parent node
		if self.parent:
			if self in self.parent.child:
				self.parent.child.remove(self)
			self.parent._add(self)
		else:
			left_child.parent = self
			right_child.parent = self

	# find an item in the tree; return item, or False if not found
	def _find(self, item):
		if item in self.data:
			return self.data
		elif self._isLeaf():
			return False
		elif item > self.data[-1]:
			return self.child[-1]._find(item)
		else:
			for i in range(len(self.data)):
				if item < self.data[i]:
					return self.child[i]._find(item)

	def removeAndFindSuccessor(self, item):
		# Checks which location in the node the data item is
		if self.data[0] == item:
			loc = 0
		elif self.data[1] == item:
			loc = 1
		# Removes the item thats being deleted
		self.data.remove(item)
		# If the item being deleted was in the left position in the 3-node
		# then goes into here
		if loc == 0:
			# Left data has been deleted so go down middle route for successor
			node = self.child[1]
			while(node._isLeaf() == False):
				node = node.child[0]
			# Check if the successor code has a spare piece of data
			if len(node.data) == 2:
				# Has a spare and can take the successor
				self.data.append(node.data[0])
				node.data.remove(node.data[0])
				self.data.sort()
			else:
				 # Doesn't have a spare piece of data
				 pass
		# If the item being deleted was in the right position in the 3-node
		# then goes into here
		elif loc == 1:
			# Right data has been deleted so go down right route for successor
			node = self.child[2]
			while(node._isLeaf() == False):
				node = node.child[0]
			# Check if the successor code has a spare piece of data
			if len(node.data) == 2:
				# Has a spare and can take the successor
				self.data.append(node.data[0])
				node.data.remove(node.data[0])
				self.data.sort()
			else:
				 # Doesn't have a spare piece of data
				 pass
	# For this case no other action must be taken
	def case11(self, item):
		pass

	def case12(self, item):
		# Node is empty so check sibling for extra key
		# Checks whether parent is a 2-node or 3-node
		if len(self.parent.child) == 3:
			for x in range(len(self.parent.child)):
				if self.parent.child[x].data == []:
					i = x
			if i == 0:
				# Left child
				# Check if middle child has a spare
				if len(self.parent.child[1].data) == 2:
					# Has a spare key
					# Copies the left key from the parent into the deleted node
					self.parent.child[0].data.append(self.parent.data[0])
					# Overwrites the left data node in the parent with the data from the middle child
					self.parent.data[0] = self.parent.child[1].data[0]
					# Sort parent node to ensure its in correct order
					self.parent.data.sort()
					# Delete duplicate data in middle child
					self.parent.child[1].data.remove(self.parent.child[1].data[0])
					# Sort the children just to make sure they are in the correct order
					self.parent.child[1].data.sort()
					self.parent.child[0].data.sort()
				else:
					# Merge one value from parent and one from middle node
					self.parent.child[1].data.append(self.parent.data[0])
					self.parent.data.remove(self.parent.data[0])
					del self.parent.child[0]
					self.parent.data.sort()
					self.parent.child[0].data.sort()
			elif i == 1:
				# Middle child
				# Check if Left child has a spare
				if len(self.parent.child[0].data) == 2:
					# Has a spare key
					# Copies the left key from the parent into the deleted node
					self.parent.child[1].data.append(self.parent.data[0])
					# Overwrites the left data node in the parent with the data from the left child
					self.parent.data[0] = self.parent.child[0].data[1]
					# Sort parent node to ensure its in correct order
					self.parent.data.sort()
					# Delete duplicate data in left child
					self.parent.child[0].data.remove(self.parent.child[0].data[1])
					# Sort the children just to make sure they are in the correct order
					self.parent.child[1].data.sort()
					self.parent.child[0].data.sort()
				# Check if right child has a spare
				elif len(self.parent.child[2].data) == 2:
					# Has a spare key
					# Copies the right key from the parent into the deleted node
					self.parent.child[1].data.append(self.parent.data[1])
					# Overwrites the right data node in the parent with the data from the right child
					self.parent.data[1] = self.parent.child[2].data[0]
					# Sort parent node to ensure its in correct order
					self.parent.data.sort()
					# Delete duplicate data in right child
					self.parent.child[2].data.remove(self.parent.child[2].data[0])
					# Sort the children just to make sure they are in the correct order
					self.parent.child[1].data.sort()
					self.parent.child[2].data.sort()
				else:
					# Merge one value from parent and one from left node
					self.parent.child[0].data.append(self.parent.data[0])
					self.parent.data.remove(self.parent.data[0])
					del self.parent.child[1]
					self.parent.data.sort()
					self.parent.child[0].data.sort()
			elif i == 2:
				# Right child
				# Check if middle child has a spare
				if len(self.parent.child[1].data) == 2:
					# Has a spare key
					# Copies the right key from the parent into the deleted node
					self.parent.child[2].data.append(self.parent.data[1])
					# Overwrites the right data node in the parent with the data from the middle child
					self.parent.data[1] = self.parent.child[1].data[1]
					# Sort parent node to ensure its in correct order
					self.parent.data.sort()
					# Delete duplicate data in middle child
					self.parent.child[1].data.remove(self.parent.child[1].data[1])
					# Sort the children just to make sure they are in the correct order
					self.parent.child[1].data.sort()
					self.parent.child[2].data.sort()
				else:
					# Merge one value from parent and one from middle node
					self.parent.child[1].data.append(self.parent.data[1])
					self.parent.data.remove(self.parent.data[1])
					del self.parent.child[2]
					self.parent.data.sort()
					self.parent.child[1].data.sort()
		elif len(self.parent.child) == 2:
			#It is a 2-node
			for i in range(2):
				if self.parent.child[i].data == []:
					if i == 0:
						# Deleted node is a left child
						# Check right child to see if it can share
						if len(self.parent.child[1].data) == 2:
							# Can share as its a 3-node by sending data to the parent
							self.parent.data.append(self.parent.child[1].data[0])
							# Sort the list
							self.parent.data.sort()
							# Delete data in sibling that was shared so it isnt duplicated
							self.parent.child[1].data.remove(self.parent.child[1].data[0])
							# Parent passes down smallest key to fill node
							self.data.append(self.parent.data[0])
							#Delete data from parent that was shared so it isnt duplicated
							self.parent.data.remove(self.parent.data[0])
						else:
							# Cant share so must merge with parent
							# We already know which child it is
							self.parent.data.append(self.parent.child[1].data[0])
							self.parent.data.sort()
							self.parent.child[1].data.remove(self.parent.child[1].data[0])
							del self.parent.child[0]
							del self.parent.child[0]
					if i == 1:
						# Deleted node is a right child
						# Check left child to see if it can share
						if len(self.parent.child[0].data) == 2:
							# Can share as its a 3-node by sending data to the parent
							self.parent.data.append(self.parent.child[0].data[1])
							# Sort the list
							self.parent.data.sort()
							# Delete data in sibling that was shared so it isnt duplicated
							self.parent.child[0].data.remove(self.parent.child[0].data[1])
							# Parent passes down smallest key to fill node
							self.data.append(self.parent.data[1])
							#Delete data from parent that was shared so it isnt duplicated
							self.parent.data.remove(self.parent.data[1])
						else:
							# Cant share so must merge with parent
							# We already know which child it is
							self.parent.data.append(self.parent.child[0].data[0])
							self.parent.data.sort()
							self.parent.child[0].data.remove(self.parent.child[0].data[0])
							# deletes both children because after the first
							# deletion the other child becomes child[0]
							del self.parent.child[0]
							del self.parent.child[0]

	def case1(self, item):
		# As its a leaf, delete the key
		self.data.remove(item)
		if len(self.data) >= 1 or self.parent == None:
			self.case11(item)
		# If that node is now empty check its sibling to see if it has extra keys to offer
		elif len(self.data) < 1:
			self.case12(item)

	def _remove(self, item):
		if item in self.data:
			# Check what case we are in
			# Check to see if its a leaf. If its child is a NULL node then its a leaf
			if self._isLeaf():
				self.case1(item)
			else:
				# As it isn't a leaf node then the deletion is slightly more complicated
				# So it must find the inorder successor
				self.removeAndFindSuccessor(item)
			return self.data
		elif self._isLeaf():
			return False
		elif item > self.data[-1]:
			return self.child[-1]._remove(item)
		else:
			for i in range(len(self.data)):
				if item < self.data[i]:
					return self.child[i]._remove(item)

	def _findTightFit(self, item):
		# Finds the best bin for the package to be stored into
		current_lowest = None
		node = self
		while(node._isLeaf() == False):
			if len(node.data) == 1:
				# 2-node
				if item <= node.data[0]:
					current_lowest = node.data[0]
					# As it fits, try find an even smaller fit so go left
					node = node.child[0]
				else:
					# As package didnt fit, we need a larger residual capacity
					# So take the right subtree
					node = node.child[1]
			elif len(node.data) == 2:
				# 3-node
				if item == node.data[0] or item == node.data[1]:
					# Check to see if either bins are of perfect size
					if item == node.data[0]:
						current_lowest = node.data[0]
					else:
						current_lowest = node.data[1]
				elif item < node.data[0]:
					current_lowest = node.data[0]
					# As it fits try find an even tighter fit
					node = node.child[0]
				elif item < node.data[1]:
					current_lowest = node.data[1]
					# As it fits try find an even tighter fit
					node = node.child[1]
				else:
					# Can't fit in either bins so takes the right subtree
					node = node.child[2]
		if node._isLeaf():
			if item <= node.data[0]:
				current_lowest = node.data[0]
			if len(node.data) == 2:
				if item <= node.data[1]:
					current_lowest = node.data[1]
		return current_lowest

	def _preorder(self):
		print (self)
		for child in self.child:
			child._preorder()

# All the functions used by the user on the Tree
class Tree:
	def __init__(self):
		print("Tree __init__")
		self.root = None

	def insert(self, item):
		print("Tree insert: " + str(item))
		if self.root is None:
			self.root = Node(item)
		else:
			self.root._insert(Node(item))
			while self.root.parent:
				self.root = self.root.parent
		return True

	def find(self, item):
		return self.root._find(item)

	def remove(self, item):
		print("Tree remove: " + str(item))
		return self.root._remove(item)

	def printTop2Tiers(self):
		print ('----Top 2 Tiers----')
		print (str(self.root.data))
		for child in self.root.child:
			print (str(child.data), end = ' ')
		print(' ')

	def findTightFit(self, item):
		print("Finding tighest fit for " + str(item))
		if self.root is None:
			return None
		return self.root._findTightFit(item)

	def preorder(self):
		print ('----Preorder----')
		if self.root != None:
			self.root._preorder()

# Initialises the Tree
tree = Tree()

# List of packages that will be packed into bins
lst_of_packages = [34, 3, 72, 46, 44, 29, 89, 74, 22]
# Counter to store how many bins have been initialised
amm_of_bins_used = 0
# Loops through all the packages one-by-one and stores them in a bin
for package in lst_of_packages:
	# Finds the best bin for the package
	bestFitBin = tree.findTightFit(package)
	# If it couldn't find a bin then initialise a new bin
	if bestFitBin == None:
		tree.insert(100 - package)
		amm_of_bins_used += 1
	# If it did find a suitable bin, remove the old data item and insert the
	# new residual capacity of the bin
	else:
		tree.remove(bestFitBin)
		tree.insert(bestFitBin - package)
	tree.preorder()

# Prints the total amount of bins that were initialised to store the packages
print("Total amount of bins initialised for this example: " + str(amm_of_bins_used))

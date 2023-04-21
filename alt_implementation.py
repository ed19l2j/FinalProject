# 2-3 Tree
# balanced tree data structure with up to 2 data items per node

class Node:
	def __init__(self, data, par = None):
		#print ("Node __init__: " + str(data))
		self.data = list([data])
		self.parent = par
		self.child = list()

	def __str__(self):
		if self.parent:
			return str(self.parent.data) + ' : ' + str(self.data)
		return 'Root : ' + str(self.data)

	# def __del__(self):
	# 	print ("Object gets destroyed");

	# less than function that does a comparison between two nodes
	def __lt__(self, node):
		return self.data[0] < node.data[0]

	# checks the length of the child nodes
	def _isLeaf(self):
		return len(self.child) == 0

	# merge new_node sub-tree into self node
	def _add(self, new_node):
		# print ("Node _add: " + str(new_node.data) + ' to ' + str(self.data))
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
		# print ('Node _insert: ' + str(new_node.data) + ' into ' + str(self.data))
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
		# print("Node _split: " + str(self.data))
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
		# print ("Find " + str(item))
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


	def case11(self, item):
		pass

	def case12(self, item):
		# Node is empty so check sibling for extra key
		# Checks whether parent is a 2-node or 3-node
		if len(self.parent.child) == 3:
			print("parent is a 3-node")
			for i in range(3):
				if self.parent.child[i].data == []:
					print("child found at location " + str(i))
					if i == 0:
						# Left child
						# Check if middle child has a spare
						if len(self.parent.child[1].data) == 2:
							# Has a spare key
							# Copies the left key from the parent into the deleted node
							self.parent.child[0].data[0].append(self.parent[0])
							# Overwrites the left data node in the parent with the data from the middle child
							self.parent.data[0] = self.parent.child[1].data[0]
							# Sort parent node to ensure its in correct order
							self.parent.data.sort()
							# Delete duplicate data in middle child
							self.parent.child[1].data[0].remove()
					elif i == 1:
						#middle child
						pass
					elif i == 2:
						#right child
						pass
		elif len(self.parent.child) == 2:
			#It is a 2-node
			print("parent is a 2-node")
			for i in range(2):
				if self.parent.child[i].data == []:
					print("child found at location " + str(i))
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
		# If that node is now empty check its sibling to see if it has extra keys to offer
		if len(self.data) < 1:
			self.case12(item)
		else:
			self.case11(item)

	def _remove(self, item):
		# print ("Find " + str(item))
		if item in self.data:
			print("time to die number: " + str(self.data))
			# Check what case we are in
			# Check to see if its a leaf. If its child is a NULL node then its a leaf
			if self._isLeaf():
				print("Leaf detected")
				self.case1(item)

			return self.data
		elif self._isLeaf():
			return False
		elif item > self.data[-1]:
			return self.child[-1]._remove(item)
		else:
			for i in range(len(self.data)):
				if item < self.data[i]:
					return self.child[i]._remove(item)

	# print preorder traversal
	def _preorder(self):
		print (self)
		for child in self.child:
			child._preorder()

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

	def preorder(self):
		print ('----Preorder----')
		self.root._preorder()

tree = Tree()

#lst = [13, 7, 24, 15, 4, 29, 20, 16, 19, 1, 5, 22, 17]
lst = [16,12,18]#,22,19]
for item in lst:
	tree.insert(item)
tree.preorder()

tree.preorder()

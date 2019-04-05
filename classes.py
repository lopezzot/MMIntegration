class rootdategraph_plusatten:
	'''class with all elements to create 
	root date graph plus atten'''
	def __init__(self, name, new_rootdates, newvalues, atten_newvalues, filename, xtitle, ytitle, rootdirectory):
		self.name = name
		self.new_rootdates = new_rootdates
		self.newvalues = newvalues
		self.atten_newvalues = atten_newvalues
		self.filename = filename
		self.xtitle = xtitle
		self.ytitle = ytitle
		self.rootdirectory = rootdirectory

class attenuationrootgraph:

	def __init__(self, name, setattenvalues, normalizedsetmeancurrents, filename, xtitle, ytitle, dir_summary):
		self.name = name
		self.setattenvalues = setattenvalues
		self.normalizedsetmeancurrents = normalizedsetmeancurrents
		self.filename = filename
		self.xtitle = xtitle
		self.ytitle = ytitle
		self.dir_summary = dir_summary

class currentgraph:

	def __init__(self, name, rootdates, newvalues, filename, xtitle, ytitle, rootdirectory):
		self.name = name
		self.rootdates = rootdates
		self.newvalues = newvalues
		self.filename = filename
		self.xtitle = xtitle
		self.ytitle = ytitle
		self.rootdirectory = rootdirectory
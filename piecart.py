import matplotlib.pyplot as plt


def create_pie(sizes, name):
	labels = ["In spec", "Out spec"]
	#sizes = [30,10]
	colors = ['green','red']
	explode = (0,0)

	piechart = plt.pie(sizes,explode=explode,labels=labels,colors=colors,
		autopct='%1.1f%%', shadow=True, startangle=140)
	plt.axis('equal')
	#plt.show()
	plt.savefig(str(name), bbox_inches='tight')
	plt.close()

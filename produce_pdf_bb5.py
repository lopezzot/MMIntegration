import os
import datetime
import MMPlots
import MMPlots_attenuation
import glob
import piecart
from termcolor import colored
import production_site

from pylatex import Document, PageStyle, Head, Foot, MiniPage, \
	StandAloneGraphic, MultiColumn, Tabu, LongTabu, LargeText, MediumText, \
	LineBreak, NewPage, Tabularx, TextColor, simple_page_number, Section, TextBlock
from pylatex.utils import bold, NoEscape

now = datetime.datetime.now()
chambername = raw_input("Insert chamber name (e.g. SM1_M6): ")
ps = raw_input("Do you have production site data? (yes or no) " )

#--------------------------------------------------------------------------------
def generate_unique_ps(sectors_notirradiated, hv_notirradiated, spark_notirradiated, ps_hv, ps_spike):
	geometry_options = {
		"head": "40pt",
		"margin": "0.5in",
		"bottom": "1.0in",
		"includeheadfoot": True
	}
	doc = Document(indent=False,geometry_options=geometry_options)

	# Generating first page style
	first_page = PageStyle("firstpage")

	# Header image
	with first_page.create(Head("L")) as header_left:
		with header_left.create(MiniPage(width=NoEscape(r"0.49\textwidth"),
										 pos='c')) as logo_wrapper:
			logo_file = os.path.join(os.path.dirname(__file__),
									 '../cernlogo.png')
			logo_wrapper.append(StandAloneGraphic(image_options="width=80px",
								filename=logo_file))

	# Add document title
	with first_page.create(Head("R")) as right_header:
		with right_header.create(MiniPage(width=NoEscape(r"0.49\textwidth"),
								 pos='c', align='r')) as title_wrapper:
			title_wrapper.append(LargeText(bold("ATLAS New Small Wheel")))
			title_wrapper.append(LineBreak())
			title_wrapper.append(bold("Integration Tests"))
			title_wrapper.append(LineBreak())
			title_wrapper.append(bold(now.strftime("%d-%m-%Y")))
			title_wrapper.append(LineBreak())
			title_wrapper.append("\n")
			title_wrapper.append(LargeText(bold("Chamber: "+str(chambername))))
			title_wrapper.append(LineBreak())
			title_wrapper.append("ID: "+str(ID))
			title_wrapper.append(LineBreak())

	# Add footer
	with first_page.create(Foot("C")) as footer:

		with footer.create(Tabularx(
				"X X X ",
				width_argument=NoEscape(r"\textwidth"))) as footer_table:

			footer_table.add_empty_row()

			footer_table.add_hline(color="blue")

			branch_address1 = MiniPage(
				width=NoEscape(r"0.25\textwidth"),
				pos='t')
			branch_address1.append("Lorenzo Pezzotti")
			branch_address1.append("\n")
			branch_address1.append("lorenzo.pezzotti@cern.ch")

			branch_address2 = MiniPage(
				width=NoEscape(r"0.25\textwidth"),
				pos='t')
			branch_address2.append("Alan Peyaud")
			branch_address2.append("\n")
			branch_address2.append("alan.peyaud@cern.ch")

			branch_address3 = MiniPage(
				width=NoEscape(r"0.25\textwidth"),
				pos='t')
			branch_address3.append("Ivan Gnesi")
			branch_address3.append("\n")
			branch_address3.append("ivan.gnesi@cern.ch")

			document_details = MiniPage(width=NoEscape(r"0.2\textwidth"),
										pos='t', align='r')
			document_details.append(" ")
			document_details.append(LineBreak())
			document_details.append(simple_page_number())

			footer_table.add_row([branch_address1, branch_address2,
								  branch_address3])

	doc.append(first_page)
	# End first page style
	redcircle = glob.glob("redcircle.png")
	redcircle = StandAloneGraphic(redcircle, image_options="width=220px")

	# Add customer information
	with doc.create(Tabu("X[r]")) as first_page_table:
		'''
		# Add branch information
		branch = MiniPage(width=NoEscape(r"0.49\textwidth"), pos='t!',
						  align='r')
		branch.append("Chamber name: ")
		branch.append(LineBreak())
		branch.append("ID: ")
		branch.append(LineBreak())

		first_page_table.add_row([branch])
		'''
		first_page_table.add_empty_row()

	doc.change_document_style("firstpage")
	doc.add_color(name="lightgray", model="gray", description="0.80")

	#doc.append(NoEscape(r'\vspace{17.634mm}'))
	#doc.append(LargeText(bold("Gas leak (mL/h) "))+str(gas_leak))

	with doc.create(Section('HV not irradiated', numbering=False)):
	   # Add statement table
		doc.append("\n")
		doc.append(timeslot)
		doc.append(LineBreak())
		doc.append(str(deltatime/60)+str("_min"))
		doc.append(LineBreak())
		doc.append("Spike_treshold_0.2_uA")
		doc.append(LineBreak())

		with doc.create(LongTabu("|X[l]|X[r]|X[r]|X[r]|X[r]|X[r]|X[r]|",
								 row_height=1.5)) as data_table:
			data_table.add_hline()
			data_table.add_row(["Sector",
								"HV",
								"PS HV",
								"spark/min",
								"PS spark/min",
								"Efficiency",
								"Flag"],
							   mapper=bold,
							   color="lightgray")
			data_table.add_empty_row()
			data_table.add_hline()
			row = ["sector", "hv", "pshv", "spark", "sparkhv", "efficiency", "0 or 1"]
			acceptedlist = []
			not_acc_counter = 0
			pscolor = "blue"
			for i in range(len(hv_notirradiated)):
				acc_color = "black"
				if (i % 2) == 0:
					'''
					if int(hv_notirradiated[i]) > 567.9 and spark_notirradiated[i]<1.0:
						accepted = 1
						acceptedlist.append(accepted)

					else:
						accepted = 0
						acceptedlist.append(accepted)
					'''
					if int(hv_notirradiated[i]) > 567.9:
						hvcolor = "black"

					if 548.0 < int(hv_notirradiated[i]) < 567.9:
						hvcolor = "orange"

					if int(hv_notirradiated[i])< 548.0:
						hvcolor = "red"
						acc_color = "red"
						not_acc_counter = not_acc_counter+1

					if spark_notirradiated[i] > 6.0:
						sparkcolor = "red"
						acc_color = "red"
						not_acc_counter = not_acc_counter+1

					if spark_notirradiated[i] == 6.0:
						sparkcolor = "orange"

					if spark_notirradiated[i] < 6.0:
						sparkcolor = "black"

					if efficiency[i] < 80.0:
						effcolor = "red"
						acc_color = "red"
						not_acc_counter = not_acc_counter+1

					if efficiency[i] > 80.0:
						effcolor = "black"

					if efficiency == 80.0:
						effcolor = "orange"

					if sparkcolor == "black" and hvcolor == "black":
						acceptedcolor = "black"

					if sparkcolor == "red" or hvcolor == "red":
						acceptedcolor = "red"

					if sparkcolor == "orange" and hvcolor == "orange":
						acceptedcolor = "orange"

					if sparkcolor == "orange" and hvcolor == "black":
						acceptedcolor = "orange"

					if sparkcolor == "black" and hvcolor == "orange":
						acceptedcolor = "orange"

					if acceptedcolor == "black":
						accepted = 1
						acceptedlist.append(accepted)

					if acceptedcolor == "red":
						accepted = 0
						acceptedlist.append(accepted)

					if acceptedcolor == "orange":
						accepted = 2
						acceptedlist.append(accepted)

					data_table.add_row([str(sectors_notirradiated[i]), TextColor(hvcolor,str(int(hv_notirradiated[i]))), TextColor(pscolor,str(ps_hv[i])),
					TextColor(sparkcolor, str(round(spark_notirradiated[i],2))),TextColor(pscolor,str(ps_spike[i])), TextColor(effcolor, str(round(efficiency[i],1))),
					TextColor(acc_color, "V")], color="lightgray")
				else:
					'''
					if int(hv_notirradiated[i]) > 567.9 and spark_notirradiated[i]<1.0:
						accepted = 1
						acceptedlist.append(accepted)
					else:
						accepted = 0
						acceptedlist.append(accepted)
					'''
					if int(hv_notirradiated[i]) > 567.9:
						hvcolor = "black"

					if 548.0 < int(hv_notirradiated[i]) < 567.9:
						hvcolor = "orange"

					if int(hv_notirradiated[i])< 548.0:
						hvcolor = "red"
						acc_color = "red"
						not_acc_counter = not_acc_counter+1

					if spark_notirradiated[i] > 6.0:
						sparkcolor = "red"
						acc_color = "red"
						not_acc_counter = not_acc_counter+1

					if spark_notirradiated[i] == 6.0:
						sparkcolor = "orange"

					if spark_notirradiated[i] < 6.0:
						sparkcolor = "black"

					if efficiency[i] < 80.0:
						effcolor = "red"
						acc_color = "red"
						not_acc_counter = not_acc_counter+1

					if efficiency[i] > 80.0:
						effcolor = "black"

					if efficiency == 80.0:
						effcolor = "orange"
					if sparkcolor == "black" and hvcolor == "black" and effcolor == "black":
						acceptedcolor = "black"

					if sparkcolor == "red" or hvcolor == "red" or effcolor == "red":
						acceptedcolor = "red"

					if sparkcolor == "orange" and hvcolor == "orange" and effcolor == "orange":
						acceptedcolor = "orange"

					if sparkcolor == "orange" and hvcolor == "black" and effcolor == "black":
						acceptedcolor = "orange"

					if sparkcolor == "black" and hvcolor == "orange" and effcolor == "black":
						acceptedcolor = "orange"

					if sparkcolor == "orange" and hvcolor == "black" and effcolor == "orange":
						acceptedcolor = "orange"

					if sparkcolor == "black" and hvcolor == "orange" and effcolor == "orange":
						acceptedcolor = "orange"

					if acceptedcolor == "black":
						accepted = 1
						acceptedlist.append(accepted)

					if acceptedcolor == "red":
						accepted = 0
						acceptedlist.append(accepted)

					if acceptedcolor == "orange":
						accepted = 2
						acceptedlist.append(accepted)
					data_table.add_row([str(sectors_notirradiated[i]), TextColor(hvcolor,str(int(hv_notirradiated[i]))), TextColor(pscolor,str(ps_hv[i])),
					TextColor(sparkcolor, str(round(spark_notirradiated[i],2))),TextColor(pscolor,str(ps_spike[i])), TextColor(effcolor, str(round(efficiency[i],1))),
					TextColor(acc_color, "V")])
				#	data_table.add_row([str(sectors_notirradiated[i]), TextColor(hvcolor,str(int(hv_notirradiated[i]))), TextColor(sparkcolor, str(round(spark_notirradiated[i],2))), TextColor(effcolor, str(round(efficiency[i],1))), TextColor(acc_color,"V")])

			data_table.add_empty_row()
			data_table.add_hline()
			data_table.add_row("Out of spec", str(len([x for x in hv_notirradiated if x < 548.0])), " ", str(len([x for x in spark_notirradiated if x > 6.0]))," ", str(len([x for x in efficiency if x < 80.0])), str(not_acc_counter))

			data_table.add_empty_row()
			data_table.add_hline()
			data_table.add_row("Chamber efficiency", "","","","", "", str(round(total_efficiency)))
			data_table.add_hline()

	with doc.create(Section('Summary not irradiated', numbering=False)):

		piecart.create_pie([acceptedlist.count(1), acceptedlist.count(0), acceptedlist.count(2)], "piechart.pdf")


		 # Add cheque images
		with doc.create(LongTabu("X[c]")) as summary1_table:
			pie = glob.iglob("piechart.pdf")
			#png_list = [StandAloneGraphic(x, image_options="width=120px") for x in png_list]
			pienew = [StandAloneGraphic(x, image_options="width=220px") for x in pie]
			summary1_table.add_row([pienew[0]])

		#here I have sectors_notirradiated, hv_notirradiated, spark_notirradiated, acceptedlist
		SM1channels = ["L1","R1","L2","R2","L3","R3","L4","R4","L5","R5"]
		SM2channels = ["L6","R6","L7","R7","L8","R8"]

		badresultsall = []
		badresultseta = []
		badresultsstereo = []

		if chambername[0:3] == "SM1":
		   channels = SM1channels
		if chambername[0:3] == "SM2":
		   channels = SM2channels
		if chambername[0:3] == "LM1":
			channels = SM1channels
		if chambername[0:3] == "LM2":
			channels = SM2channels

		for channel in channels:
		   cntall = sum(1 for x, sector in enumerate(sectors_notirradiated) if sector[2:4] == channel and acceptedlist[x] == 1)
		   cnteta = sum(1 for x, sector in enumerate(sectors_notirradiated) if sector[2:4] == channel and (sector[1:2] == "1" or sector[1:2] == "2") and acceptedlist[x] == 1)
		   cntstereo = sum(1 for x, sector in enumerate(sectors_notirradiated) if sector[2:4] == channel and (sector[1:2] == "3" or sector[1:2] == "4") and acceptedlist[x] == 1)
		   badresultsall.append(4-int(cntall))
		   badresultseta.append(2-int(cnteta))
		   badresultsstereo.append(2-int(cntstereo))

		#doc.append(NewPage())

		with doc.create(LongTabu("X[l] X[r] X[r] X[r]",
								 row_height=1.5)) as data_table2:
			data_table2.add_row(["Sector overimposed (from eta side)",
								"Eta",
								"Stereo",
								"Eta+Stereo"],
								mapper=bold,
								color="lightgray")
			data_table2.add_empty_row()
			data_table2.add_hline()
			row = ["Sector (all layers)", "Out of spec (Eta)", "Out of spec (Stereo)", "Out of spec (E+S)"]

			for i in range(len(channels)):
				if (i % 2) == 0:
					data_table2.add_row([str(channels[i]), str(int(badresultseta[i])), str(badresultsstereo[i]), badresultsall[i]], color="lightgray")
				else:
					data_table2.add_row([str(channels[i]), str(int(badresultseta[i])), str(badresultsstereo[i]), badresultsall[i]])

		with doc.create(LongTabu("X[l] X[r]",
								 row_height=1.5)) as data_table3:
			data_table3.add_row(["Layer",
								"Mean Efficiency"],
								mapper=bold,
								color="lightgray")
			data_table3.add_empty_row()
			data_table3.add_hline()
			row = ["layers", "efficiency"]
			channelsT3 = ["L1", "L2", "L3", "L4"]
			for i in range(len(layers_efficiency)):
				if (i % 2) == 0:
					data_table3.add_row([str(channelsT3[i]), str(round(layers_efficiency[i],1))], color="lightgray")
				else:
					data_table3.add_row([str(channelsT3[i]), str(round(layers_efficiency[i],1))])

	doc.append(NewPage())

	with doc.create(Section('Current with no irradiation', numbering=False)):

	# Add cheque images
		with doc.create(LongTabu("X[c] X[c] X[c] X[c]")) as cheque_table:
			png_list = glob.glob('BB5-i*.pdf')
			png_list.sort(key=os.path.getmtime)
			png_list = [StandAloneGraphic(x, image_options="width=120px") for x in png_list]
			print len(png_list)
			row_image = []
			i = 0
			for image in png_list:
				row_image.append(image)
				i = i +1
				if i==4:
					cheque_table.add_row([row_image[0], row_image[1], row_image[2], row_image[3]])
					row_image = []
					i=0

	png_list = []

	doc.generate_pdf("complex_report", clean_tex=False, compiler='pdflatex')


def generate_unique(sectors_notirradiated, hv_notirradiated, spark_notirradiated):
	geometry_options = {
		"head": "40pt",
		"margin": "0.5in",
		"bottom": "1.0in",
		"includeheadfoot": True
	}
	doc = Document(indent=False,geometry_options=geometry_options)

	# Generating first page style
	first_page = PageStyle("firstpage")

	# Header image
	with first_page.create(Head("L")) as header_left:
		with header_left.create(MiniPage(width=NoEscape(r"0.49\textwidth"),
										 pos='c')) as logo_wrapper:
			logo_file = os.path.join(os.path.dirname(__file__),
									 '../cernlogo.png')
			logo_wrapper.append(StandAloneGraphic(image_options="width=80px",
								filename=logo_file))

	# Add document title
	with first_page.create(Head("R")) as right_header:
		with right_header.create(MiniPage(width=NoEscape(r"0.49\textwidth"),
								 pos='c', align='r')) as title_wrapper:
			title_wrapper.append(LargeText(bold("ATLAS New Small Wheel")))
			title_wrapper.append(LineBreak())
			title_wrapper.append(bold("Integration Tests"))
			title_wrapper.append(LineBreak())
			title_wrapper.append(bold(now.strftime("%d-%m-%Y")))
			title_wrapper.append(LineBreak())
			title_wrapper.append("\n")
			title_wrapper.append(LargeText(bold("Chamber: "+str(chambername))))
			title_wrapper.append(LineBreak())
			title_wrapper.append("ID: "+str(ID))
			title_wrapper.append(LineBreak())

	# Add footer
	with first_page.create(Foot("C")) as footer:

		with footer.create(Tabularx(
				"X X X ",
				width_argument=NoEscape(r"\textwidth"))) as footer_table:

			footer_table.add_empty_row()

			footer_table.add_hline(color="blue")

			branch_address1 = MiniPage(
				width=NoEscape(r"0.25\textwidth"),
				pos='t')
			branch_address1.append("Lorenzo Pezzotti")
			branch_address1.append("\n")
			branch_address1.append("lorenzo.pezzotti@cern.ch")

			branch_address2 = MiniPage(
				width=NoEscape(r"0.25\textwidth"),
				pos='t')
			branch_address2.append("Alan Peyaud")
			branch_address2.append("\n")
			branch_address2.append("alan.peyaud@cern.ch")

			branch_address3 = MiniPage(
				width=NoEscape(r"0.25\textwidth"),
				pos='t')
			branch_address3.append("Ivan Gnesi")
			branch_address3.append("\n")
			branch_address3.append("ivan.gnesi@cern.ch")

			document_details = MiniPage(width=NoEscape(r"0.2\textwidth"),
										pos='t', align='r')
			document_details.append(" ")
			document_details.append(LineBreak())
			document_details.append(simple_page_number())

			footer_table.add_row([branch_address1, branch_address2,
								  branch_address3])

	doc.append(first_page)
	# End first page style
	redcircle = glob.glob("redcircle.png")
	redcircle = StandAloneGraphic(redcircle, image_options="width=220px")

	# Add customer information
	with doc.create(Tabu("X[r]")) as first_page_table:
		'''
		# Add branch information
		branch = MiniPage(width=NoEscape(r"0.49\textwidth"), pos='t!',
						  align='r')
		branch.append("Chamber name: ")
		branch.append(LineBreak())
		branch.append("ID: ")
		branch.append(LineBreak())

		first_page_table.add_row([branch])
		'''
		first_page_table.add_empty_row()

	doc.change_document_style("firstpage")
	doc.add_color(name="lightgray", model="gray", description="0.80")

	#doc.append(NoEscape(r'\vspace{17.634mm}'))
	#doc.append(LargeText(bold("Gas leak (mL/h) "))+str(gas_leak))

	with doc.create(Section('HV not irradiated', numbering=False)):
	   # Add statement table
		doc.append("\n")
		doc.append(timeslot)
		doc.append(LineBreak())
		doc.append(str(deltatime/60)+str("_min"))
		doc.append(LineBreak())
		doc.append("Spike_treshold_0.2_uA")
		doc.append(LineBreak())

		with doc.create(LongTabu("|X[l]|X[r]|X[r]|X[r]|X[r]|",
								 row_height=1.5)) as data_table:
			data_table.add_hline()
			data_table.add_row(["Sector",
								"HV",
								"spark/min",
								"Efficiency",
								"Flag"],
							   mapper=bold,
							   color="lightgray")
			data_table.add_empty_row()
			data_table.add_hline()
			row = ["sector", "hv","spark", "efficiency", "0 or 1"]
			acceptedlist = []
			not_acc_counter = 0
			pscolor = "blue"
			for i in range(len(hv_notirradiated)):
				acc_color = "black"
				if (i % 2) == 0:
					'''
					if int(hv_notirradiated[i]) > 567.9 and spark_notirradiated[i]<1.0:
						accepted = 1
						acceptedlist.append(accepted)

					else:
						accepted = 0
						acceptedlist.append(accepted)
					'''
					if int(hv_notirradiated[i]) > 567.9:
						hvcolor = "black"

					if 548.0 < int(hv_notirradiated[i]) < 567.9:
						hvcolor = "orange"

					if int(hv_notirradiated[i])< 548.0:
						hvcolor = "red"
						acc_color = "red"
						not_acc_counter = not_acc_counter+1

					if spark_notirradiated[i] > 6.0:
						sparkcolor = "red"
						acc_color = "red"
						not_acc_counter = not_acc_counter+1

					if spark_notirradiated[i] == 6.0:
						sparkcolor = "orange"

					if spark_notirradiated[i] < 6.0:
						sparkcolor = "black"

					if efficiency[i] < 80.0:
						effcolor = "red"
						acc_color = "red"
						not_acc_counter = not_acc_counter+1

					if efficiency[i] > 80.0:
						effcolor = "black"

					if efficiency == 80.0:
						effcolor = "orange"

					if sparkcolor == "black" and hvcolor == "black":
						acceptedcolor = "black"

					if sparkcolor == "red" or hvcolor == "red":
						acceptedcolor = "red"

					if sparkcolor == "orange" and hvcolor == "orange":
						acceptedcolor = "orange"

					if sparkcolor == "orange" and hvcolor == "black":
						acceptedcolor = "orange"

					if sparkcolor == "black" and hvcolor == "orange":
						acceptedcolor = "orange"

					if acceptedcolor == "black":
						accepted = 1
						acceptedlist.append(accepted)

					if acceptedcolor == "red":
						accepted = 0
						acceptedlist.append(accepted)

					if acceptedcolor == "orange":
						accepted = 2
						acceptedlist.append(accepted)

					data_table.add_row([str(sectors_notirradiated[i]), TextColor(hvcolor,str(int(hv_notirradiated[i]))),
					TextColor(sparkcolor, str(round(spark_notirradiated[i],2))), TextColor(effcolor, str(round(efficiency[i],1))),
					TextColor(acc_color, "V")], color="lightgray")
				else:
					'''
					if int(hv_notirradiated[i]) > 567.9 and spark_notirradiated[i]<1.0:
						accepted = 1
						acceptedlist.append(accepted)
					else:
						accepted = 0
						acceptedlist.append(accepted)
					'''
					if int(hv_notirradiated[i]) > 567.9:
						hvcolor = "black"

					if 548.0 < int(hv_notirradiated[i]) < 567.9:
						hvcolor = "orange"

					if int(hv_notirradiated[i])< 548.0:
						hvcolor = "red"
						acc_color = "red"
						not_acc_counter = not_acc_counter+1

					if spark_notirradiated[i] > 6.0:
						sparkcolor = "red"
						acc_color = "red"
						not_acc_counter = not_acc_counter+1

					if spark_notirradiated[i] == 6.0:
						sparkcolor = "orange"

					if spark_notirradiated[i] < 6.0:
						sparkcolor = "black"

					if efficiency[i] < 80.0:
						effcolor = "red"
						acc_color = "red"
						not_acc_counter = not_acc_counter+1

					if efficiency[i] > 80.0:
						effcolor = "black"

					if efficiency == 80.0:
						effcolor = "orange"
					if sparkcolor == "black" and hvcolor == "black" and effcolor == "black":
						acceptedcolor = "black"

					if sparkcolor == "red" or hvcolor == "red" or effcolor == "red":
						acceptedcolor = "red"

					if sparkcolor == "orange" and hvcolor == "orange" and effcolor == "orange":
						acceptedcolor = "orange"

					if sparkcolor == "orange" and hvcolor == "black" and effcolor == "black":
						acceptedcolor = "orange"

					if sparkcolor == "black" and hvcolor == "orange" and effcolor == "black":
						acceptedcolor = "orange"

					if sparkcolor == "orange" and hvcolor == "black" and effcolor == "orange":
						acceptedcolor = "orange"

					if sparkcolor == "black" and hvcolor == "orange" and effcolor == "orange":
						acceptedcolor = "orange"

					if acceptedcolor == "black":
						accepted = 1
						acceptedlist.append(accepted)

					if acceptedcolor == "red":
						accepted = 0
						acceptedlist.append(accepted)

					if acceptedcolor == "orange":
						accepted = 2
						acceptedlist.append(accepted)
					data_table.add_row([str(sectors_notirradiated[i]), TextColor(hvcolor,str(int(hv_notirradiated[i]))),
					TextColor(sparkcolor, str(round(spark_notirradiated[i],2))), TextColor(effcolor, str(round(efficiency[i],1))),
					TextColor(acc_color, "V")])
				#	data_table.add_row([str(sectors_notirradiated[i]), TextColor(hvcolor,str(int(hv_notirradiated[i]))), TextColor(sparkcolor, str(round(spark_notirradiated[i],2))), TextColor(effcolor, str(round(efficiency[i],1))), TextColor(acc_color,"V")])

			data_table.add_empty_row()
			data_table.add_hline()
			data_table.add_row("Out of spec", str(len([x for x in hv_notirradiated if x < 548.0])), str(len([x for x in spark_notirradiated if x > 6.0])), str(len([x for x in efficiency if x < 80.0])), str(not_acc_counter))

			data_table.add_empty_row()
			data_table.add_hline()
			data_table.add_row("Chamber efficiency", "","", "", str(round(total_efficiency)))
			data_table.add_hline()

	with doc.create(Section('Summary not irradiated', numbering=False)):

		piecart.create_pie([acceptedlist.count(1), acceptedlist.count(0), acceptedlist.count(2)], "piechart.pdf")


		 # Add cheque images
		with doc.create(LongTabu("X[c]")) as summary1_table:
			pie = glob.iglob("piechart.pdf")
			#png_list = [StandAloneGraphic(x, image_options="width=120px") for x in png_list]
			pienew = [StandAloneGraphic(x, image_options="width=220px") for x in pie]
			summary1_table.add_row([pienew[0]])

		#here I have sectors_notirradiated, hv_notirradiated, spark_notirradiated, acceptedlist
		SM1channels = ["L1","R1","L2","R2","L3","R3","L4","R4","L5","R5"]
		SM2channels = ["L6","R6","L7","R7","L8","R8"]

		badresultsall = []
		badresultseta = []
		badresultsstereo = []

		if chambername[0:3] == "SM1":
		   channels = SM1channels
		if chambername[0:3] == "SM2":
		   channels = SM2channels
		if chambername[0:3] == "LM1":
			channels = SM1channels
		if chambername[0:3] == "LM2":
			channels = SM2channels

		for channel in channels:
		   cntall = sum(1 for x, sector in enumerate(sectors_notirradiated) if sector[2:4] == channel and acceptedlist[x] == 1)
		   cnteta = sum(1 for x, sector in enumerate(sectors_notirradiated) if sector[2:4] == channel and (sector[1:2] == "1" or sector[1:2] == "2") and acceptedlist[x] == 1)
		   cntstereo = sum(1 for x, sector in enumerate(sectors_notirradiated) if sector[2:4] == channel and (sector[1:2] == "3" or sector[1:2] == "4") and acceptedlist[x] == 1)
		   badresultsall.append(4-int(cntall))
		   badresultseta.append(2-int(cnteta))
		   badresultsstereo.append(2-int(cntstereo))

		#doc.append(NewPage())

		with doc.create(LongTabu("X[l] X[r] X[r] X[r]",
								 row_height=1.5)) as data_table2:
			data_table2.add_row(["Sector overimposed (from eta side)",
								"Eta",
								"Stereo",
								"Eta+Stereo"],
								mapper=bold,
								color="lightgray")
			data_table2.add_empty_row()
			data_table2.add_hline()
			row = ["Sector (all layers)", "Out of spec (Eta)", "Out of spec (Stereo)", "Out of spec (E+S)"]

			for i in range(len(channels)):
				if (i % 2) == 0:
					data_table2.add_row([str(channels[i]), str(int(badresultseta[i])), str(badresultsstereo[i]), badresultsall[i]], color="lightgray")
				else:
					data_table2.add_row([str(channels[i]), str(int(badresultseta[i])), str(badresultsstereo[i]), badresultsall[i]])

		with doc.create(LongTabu("X[l] X[r]",
								 row_height=1.5)) as data_table3:
			data_table3.add_row(["Layer",
								"Mean Efficiency"],
								mapper=bold,
								color="lightgray")
			data_table3.add_empty_row()
			data_table3.add_hline()
			row = ["layers", "efficiency"]
			channelsT3 = ["L1", "L2", "L3", "L4"]
			for i in range(len(layers_efficiency)):
				if (i % 2) == 0:
					data_table3.add_row([str(channelsT3[i]), str(round(layers_efficiency[i],1))], color="lightgray")
				else:
					data_table3.add_row([str(channelsT3[i]), str(round(layers_efficiency[i],1))])

	doc.append(NewPage())

	with doc.create(Section('Current with no irradiation', numbering=False)):

	# Add cheque images
		with doc.create(LongTabu("X[c] X[c] X[c] X[c]")) as cheque_table:
			png_list = glob.glob('BB5-i*.pdf')
			png_list.sort(key=os.path.getmtime)
			png_list = [StandAloneGraphic(x, image_options="width=120px") for x in png_list]
			print len(png_list)
			row_image = []
			i = 0
			for image in png_list:
				row_image.append(image)
				i = i +1
				if i==4:
					cheque_table.add_row([row_image[0], row_image[1], row_image[2], row_image[3]])
					row_image = []
					i=0

	png_list = []

	doc.generate_pdf("complex_report", clean_tex=False, compiler='pdflatex')

#---------------------------------------------------------------------------------------------
if ps == "yes":
	ps_filename =  raw_input("Insert production site data filename: ")
	house = raw_input("Data in bb5 or Gif? ")
	folder = raw_input("Insert folder to study: ")
	user = raw_input("Who is it? (type Lorenzo, Natalia or bb5) ")
	if user == "Lorenzo":
		path = "/Users/lorenzo/Data_"+str(house)+"/"+folder+"/HV/"#Changed folder: files in Data_bb5 were in DataBB5 2/5/2019
		ps_path = "Lorenzo's path"
	elif user == "Natalia":
		path = "/home/est/Escritorio/CERN/Data_"+str(house)+"/"+folder+"/HV/"
		ps_path = "/home/est/Escritorio/CERN/PS_Data/"
	elif user == "bb5":
		path = "bb5 path"
		ps_path = "bb5 path"
	else:
	    print "Name not found"
	sectors_notirradiated, hv_notirradiated, spark_notirradiated, ID, timeslot, deltatime, efficiency, layers_efficiency, total_efficiency = MMPlots.createsummaryplots(path,folder)
	ps_hv, ps_spike = production_site.read(ps_path+ps_filename+'.dat')
	generate_unique_ps(sectors_notirradiated,hv_notirradiated,spark_notirradiated, ps_hv, ps_spike)
else:
	sectors_notirradiated, hv_notirradiated, spark_notirradiated, ID, timeslot, deltatime, efficiency, layers_efficiency, total_efficiency = MMPlots.createsummaryplots()
	generate_unique(sectors_notirradiated,hv_notirradiated,spark_notirradiated)

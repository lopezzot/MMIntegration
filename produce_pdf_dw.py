import os
import datetime
import MMPlots
import MMPlots_attenuation
import glob
from termcolor import colored
import bad_sectors

from pylatex import Document, PageStyle, Head, Foot, MiniPage, \
	StandAloneGraphic, MultiColumn, Tabu, LongTabu, LargeText, MediumText, \
	LineBreak, NewPage, Tabularx, TextColor, simple_page_number, Section, Subsection, TextBlock
from pylatex.utils import bold, NoEscape

now = datetime.datetime.now()

DW_name = raw_input("Insert double wedge name: ")
chambername1IP = raw_input("Insert chamber-1 name IP side: ")
chambername2IP = raw_input("Insert chamber-2 name IP side: ")
chambername1HO = raw_input("Insert chamber-1 name HO side: ")
chambername2HO = raw_input("Insert chamber-2 name HO side: ")

house = raw_input("Data in bb5 or Gif? ")
folder1IP = raw_input("Insert folder chamber-1 IP to study: ")
folder2IP = raw_input("Insert folder chamber-2 IP to study: ")
folder1HO = raw_input("Insert folder chamber-1 HO to study: ")
folder2HO = raw_input("Insert folder chamber-2 HO to study: ")

folders = [folder1IP, folder2IP, folder1HO, folder2HO]
hvs = []
paths = []
bad_sec = []
final_hvs = []
sectors = []
user = raw_input("Who is it? (type Lorenzo, Natalia or bb5) ")

for folder in folders:
	if user == "Lorenzo":
		paths.append("/Users/lorenzo/Data_"+str(house)+"/"+folder+"/HV/")
	elif user == "Natalia":
		paths.append("/home/est/Escritorio/CERN/Data_"+str(house)+"/"+folder+"/HV/")
	elif user == "bb5":
		paths.append("bb5 path")
	else:
		print "Name not found"
for i in range(4):
	sectors_notirradiated, hv_notirradiated, spark_notirradiated, ID, timeslot, deltatime, efficiency, layers_efficiency, total_efficiency = MMPlots.createsummaryplots(paths[i], folders[i])
	hvs.append(hv_notirradiated)
	sectors.append(sectors_notirradiated)

final_hvs, hl1, hl2 = bad_sectors.get_sectors_hv(hvs)
#--------------------------------------------------------------------------------
def generate_unique_dw(final_hvs, hl1, hl2, sectors):
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
			title_wrapper.append(LargeText(bold("Double Wedge: "+str(DW_name))))
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
		first_page_table.add_empty_row()

	doc.change_document_style("firstpage")
	doc.add_color(name="lightgray", model="gray", description="0.80")

	# IP
	with doc.create(Section('IP SIDE', numbering=False)):
		# first chamber
		# Verify if its SM1, LM1, SM1 or LM2
		if chambername1IP[0:3] == "SM1" or chambername2HO[0:3] == "LM1":
			limit = 10
		else:
			limit = 6

		with doc.create(Subsection("Chambers: "+chambername1IP+" + "+chambername2IP, numbering=False)):
			with doc.create(Subsection(chambername1IP, numbering=False)):
				with doc.create(LongTabu("|X[l]|X[r]|X[r]|X[r]|X[r]|X[r]|X[r]|",
										 row_height=1.5)) as data_table:
						data_table.add_hline()
						data_table.add_row(["Sector",
											"L1",
											"L2",
											"L3",
											"L4",
											"HL1",
											"HL2"],
										   mapper=bold,
										   color="lightgray")
						data_table.add_hline()
						row = ["blank", "l1", "l2", "l3", "l4", "hl1", "hl2"]
						for i, hv in enumerate(final_hvs[0]):
							hl1_str = ""
							hl2_str = ""
							l1 = ""
							l2 = ""
							l3 = ""
							l4 = ""
							# assign each sector to a line
							if hv == hl1:
								hl1_str = str(hl1)
							elif hv == hl2:
								hl2_str = str(hl2)
							elif i > limit-1+limit*2:
								l4 = "570"
							elif i > limit-1+limit:
								l3 = "570"
							elif i > limit-1:
								l2 = "570"
							else:
								l1 = "570"
							if (i % 2) == 0:
								data_table.add_row([str(sectors[0][i]), l1, l2, l3, l4, hl1_str, hl2_str])
							else:
								data_table.add_row([str(sectors[0][i]), l1, l2, l3, l4, hl1_str, hl2_str],color="lightgray")
						data_table.add_hline()

			# second chamber
			if chambername2IP[0:3] == "SM1" or chambername2HO[0:3] == "LM1":
				limit = 10
			else:
				limit = 6
			with doc.create(Subsection(chambername2IP, numbering=False)):
				with doc.create(LongTabu("|X[l]|X[r]|X[r]|X[r]|X[r]|X[r]|X[r]|",
										 row_height=1.5)) as data_table2:
						data_table2.add_hline()
						data_table2.add_row(["Sector",
											"L1",
											"L2",
											"L3",
											"L4",
											"HL1",
											"HL2"],
										   mapper=bold,
										   color="lightgray")
						data_table2.add_hline()
						row = ["blank", "l1", "l2", "l3", "l4", "hl1", "hl2"]
						for i, hv in enumerate(final_hvs[1]):
							hl1_str = ""
							hl2_str = ""
							l1 = ""
							l2 = ""
							l3 = ""
							l4 = ""
							# assign each sector to a line
							if hv == hl1:
								hl1_str = str(hl1)
							elif hv == hl2:
								hl2_str = str(hl2)
							elif i > limit-1+limit*2:
								l4 = "570"
							elif i > limit-1+limit:
								l3 = "570"
							elif i > limit-1:
								l2 = "570"
							else:
								l1 = "570"

							if (i % 2) == 0:
								data_table2.add_row([str(sectors[1][i]), l1, l2, l3, l4, hl1_str, hl2_str])
							else:
								data_table2.add_row([str(sectors[1][i]), l1, l2, l3, l4, hl1_str, hl2_str],color="lightgray")
						data_table2.add_hline()
	# HO
	# Swap R an L
	final_hvs[2] = swap(final_hvs[2])
	final_hvs[3] = swap(final_hvs[3])
	if chambername1HO[0:3] == "SM1" or chambername2HO[0:3] == "LM1":
		limit = 10
	else:
		limit = 6
	doc.append(NewPage())
	with doc.create(Section('HO SIDE', numbering=False)):
		# first chamber
		with doc.create(Subsection("Chambers: "+chambername1HO+" + "+chambername2HO, numbering=False)):
			with doc.create(Subsection(chambername1HO, numbering=False)):
				with doc.create(LongTabu("|X[l]|X[r]|X[r]|X[r]|X[r]|X[r]|X[r]|",
										 row_height=1.5)) as data_table3:
						data_table3.add_hline()
						data_table3.add_row(["Sector",
											"L1",
											"L2",
											"L3",
											"L4",
											"HL1",
											"HL2"],
										   mapper=bold,
										   color="lightgray")
						data_table3.add_hline()
						row = ["blank", "l1", "l2", "l3", "l4", "hl1", "hl2"]
						for i, hv in enumerate(final_hvs[2]):
							hl1_str = ""
							hl2_str = ""
							l1 = ""
							l2 = ""
							l3 = ""
							l4 = ""
							# assign each sector to a line
							if hv == hl1:
								hl1_str = str(hl1)
							elif hv == hl2:
								hl2_str = str(hl2)
							elif i > limit-1+limit*2:
								l4 = "570"
							elif i > limit-1+limit:
								l3 = "570"
							elif i > limit-1:
								l2 = "570"
							else:
								l1 = "570"
							if (i % 2) == 0:
								data_table3.add_row([str(sectors[2][i]), l1, l2, l3, l4, hl1_str, hl2_str])
							else:
								data_table3.add_row([str(sectors[2][i]), l1, l2, l3, l4, hl1_str, hl2_str],color="lightgray")
						data_table3.add_hline()

			# second chamber
			if chambername2HO[0:3] == "SM1" or chambername2HO[0:3] == "LM1":
				limit = 10
			else:
				limit = 6
			with doc.create(Subsection(chambername2HO, numbering=False)):
				with doc.create(LongTabu("|X[l]|X[r]|X[r]|X[r]|X[r]|X[r]|X[r]|",
										 row_height=1.5)) as data_table4:
						data_table4.add_hline()
						data_table4.add_row(["Sector",
											"L1",
											"L2",
											"L3",
											"L4",
											"HL1",
											"HL2"],
										   mapper=bold,
										   color="lightgray")
						data_table4.add_hline()
						row = ["blank", "l1", "l2", "l3", "l4", "hl1", "hl2"]
						for i, hv in enumerate(final_hvs[3]):
							hl1_str = ""
							hl2_str = ""
							l1 = ""
							l2 = ""
							l3 = ""
							l4 = ""
							# assign each sector to a line
							if hv == hl1:
								hl1_str = str(hl1)
							elif hv == hl2:
								hl2_str = str(hl2)
							elif i > limit-1+limit*2:
								l4 = "570"
							elif i > limit-1+limit:
								l3 = "570"
							elif i > limit-1:
								l2 = "570"
							else:
								l1 = "570"

							if (i % 2) == 0:
								data_table4.add_row([str(sectors[3][i]), l1, l2, l3, l4, hl1_str, hl2_str])
							else:
								data_table4.add_row([str(sectors[3][i]), l1, l2, l3, l4, hl1_str, hl2_str],color="lightgray")
						data_table4.add_hline()
	doc.generate_pdf("complex_report_DW", clean_tex=False, compiler='pdflatex')
#---------------------------------------------------------------------------------------------
# swap R and L
def swap(hvs):
	for i in range(len(hvs)/2):
		hvs[i*2], hvs[i*2+1] = hvs[i*2+1] , hvs[i*2]
	return hvs
#---------------------------------------------------------------------------------------------

generate_unique_dw(final_hvs,hl1, hl2, sectors)

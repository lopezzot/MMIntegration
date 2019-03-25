import os
import datetime
import MMPlots
import MMPlots_attenuation
import glob
import piecart

from pylatex import Document, PageStyle, Head, Foot, MiniPage, \
    StandAloneGraphic, MultiColumn, Tabu, LongTabu, LargeText, MediumText, \
    LineBreak, NewPage, Tabularx, TextColor, simple_page_number, Section, TextBlock
from pylatex.utils import bold, NoEscape

now = datetime.datetime.now()

gas_leak = raw_input("Insert gas leake (mL/h): ")
chambername = raw_input("Insert chamber name (e.g. SM1_M6): ")

sectors_notirradiated, hv_notirradiated, spark_notirradiated, ID, timeslot, deltatime = MMPlots.createsummaryplots()
sectors_irradiated, hv_irradiated, spark_irradiated, ID_irradiated, timeslot_irradiated, deltatime_irradiated = MMPlots_attenuation.createsummaryplot_attenuation()

#--------------------------------------------------------------------------------
def generate_unique(sectors_notirradiated, hv_notirradiated, spark_notirradiated, sectors_irradiated, hv_irradiated, spark_irradiated):
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

    doc.append(NoEscape(r'\vspace{17.634mm}'))
    doc.append(LargeText(bold("Gas leak (mL/h) "))+str(gas_leak))
    
    with doc.create(Section('HV not irradiated', numbering=False)):
       # Add statement table
        doc.append("\n")
        doc.append(timeslot)
        doc.append(LineBreak())
        doc.append(str(deltatime/60)+str("_min"))
        doc.append(LineBreak())
        with doc.create(LongTabu("X[l] X[r] X[r] X[r]",
                                 row_height=1.5)) as data_table:
            data_table.add_row(["Sector",
                                "HV",
                                "spark/min",
                                "Accepted"],
                               mapper=bold,
                               color="lightgray")
            data_table.add_empty_row()
            data_table.add_hline()
            row = ["sector", "hv", "spark", "0 or 1"]
            acceptedlist = []
            for i in range(len(hv_notirradiated)):
                if (i % 2) == 0:
                    if int(hv_notirradiated[i]) > 567.9 and spark_notirradiated[i]<1.0:
                        accepted = 1
                        acceptedlist.append(accepted)
                    else:
                        accepted = 0
                        acceptedlist.append(accepted) 
                    data_table.add_row([str(sectors_notirradiated[i]), str(int(hv_notirradiated[i])), str(round(spark_notirradiated[i],2)), accepted], color="lightgray")
                else:
                    if int(hv_notirradiated[i]) > 567.9 and spark_notirradiated[i]<1.0:
                        accepted = 1
                        acceptedlist.append(accepted)
                    else:
                        accepted = 0
                        acceptedlist.append(accepted)  
                    data_table.add_row([str(sectors_notirradiated[i]), str(int(hv_notirradiated[i])), str(round(spark_notirradiated[i],2)), accepted])

            data_table.add_empty_row()
            data_table.add_hline()
            data_table.add_row("Out of spec", str(len([x for x in hv_notirradiated if x < 567.9])), str(len([x for x in spark_notirradiated if x > 1.0])), str(acceptedlist.count(0)))
    
    with doc.create(Section('Summary not irradiated', numbering=False)):

        piecart.create_pie([len(acceptedlist)-acceptedlist.count(0), acceptedlist.count(0)], "piechart.pdf")

    
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

    doc.append(NewPage())
    
    
    with doc.create(Section('HV irradiated at GIF', numbering=False)):
       # Add statement table
        doc.append("\n")
        doc.append(timeslot_irradiated)
        doc.append(LineBreak())
        doc.append(str(deltatime_irradiated/60)+str("_min"))
        doc.append(LineBreak())
        with doc.create(LongTabu("X[l] X[r] X[r] X[r]",
                                 row_height=1.5)) as data_table_irradiated:
            data_table_irradiated.add_row(["Sector",
                                "HV",
                                "spark/min",
                                "Accepted"],
                               mapper=bold,
                               color="lightgray")
            data_table_irradiated.add_empty_row()
            data_table_irradiated.add_hline()
            row = ["sector", "hv", "spark", "0 or 1"]
            acceptedlist = []
            for i in range(len(hv_irradiated)):
                if (i % 2) == 0:
                    if int(hv_irradiated[i]) > 567.9 and spark_irradiated[i]<1.0:
                        accepted = 1
                        acceptedlist.append(accepted)
                    else:
                        accepted = 0
                        acceptedlist.append(accepted) 
                    data_table_irradiated.add_row([str(sectors_irradiated[i]), str(int(hv_irradiated[i])), str(round(spark_irradiated[i],2)), accepted], color="lightgray")
                else:
                    if int(hv_irradiated[i]) > 567.9 and spark_irradiated[i]<1.0:
                        accepted = 1
                        acceptedlist.append(accepted)
                    else:
                        accepted = 0
                        acceptedlist.append(accepted)  
                    data_table_irradiated.add_row([str(sectors_irradiated[i]), str(int(hv_irradiated[i])), str(round(spark_irradiated[i],2)), accepted])

            data_table_irradiated.add_empty_row()
            data_table_irradiated.add_hline()
            data_table_irradiated.add_row("Out of spec", str(len([x for x in hv_irradiated if x < 567.9])), str(len([x for x in spark_irradiated if x > 1.0])), str(acceptedlist.count(0)))

    with doc.create(Section('Summary irradiated at GIF', numbering=False)):

        piecart.create_pie([len(acceptedlist)-acceptedlist.count(0), acceptedlist.count(0)], "newpie.pdf")

        # Add cheque images
        with doc.create(LongTabu("X[c]")) as summary2_table:
            newpie = glob.iglob("newpie.pdf")
            #png_list = [StandAloneGraphic(x, image_options="width=120px") for x in png_list]
            pie2new = [StandAloneGraphic(x, image_options="width=220px") for x in newpie]
            summary2_table.add_row([pie2new[0]])
    
    #doc.append(NewPage())

        #here I have sectors_irradiated, hv_irradiated, spark_irradiated, acceptedlist
        SM1channels = ["L1","R1","L2","R2","L3","R3","L4","R4","L5","R5"]
        SM2channels = ["L6","R6","L7","R7","L8","R8"]
        badresultsall = []
        badresultseta = []
        badresultsstereo = []

        if chambername[0:3] == "SM1":
    	   channels = SM1channels
        if chambername[0:3] == "SM2":
    	   channels = SM2channels

        for channel in channels:
    	   cntall = sum(1 for x, sector in enumerate(sectors_irradiated) if sector[2:4] == channel and acceptedlist[x] == 1)
    	   cnteta = sum(1 for x, sector in enumerate(sectors_irradiated) if sector[2:4] == channel and (sector[1:2] == "1" or sector[1:2] == "2") and acceptedlist[x] == 1)
    	   cntstereo = sum(1 for x, sector in enumerate(sectors_irradiated) if sector[2:4] == channel and (sector[1:2] == "3" or sector[1:2] == "4") and acceptedlist[x] == 1) 
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
    
    doc.append(NewPage())
    with doc.create(Section('Current with no irradiation', numbering=False)):
    
    # Add cheque images
        with doc.create(LongTabu("X[c] X[c] X[c] X[c]")) as cheque_table:
            png_list = glob.iglob('BB5-i*.pdf')
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
    doc.append(NewPage())	

    with doc.create(Section('Current under irradiation', numbering=False)):
    
    # Add cheque images
        with doc.create(LongTabu("X[c] X[c] X[c] X[c]")) as cheque_table:
            png_list = glob.iglob('GIF-i*.pdf')
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
    doc.append(NewPage())	

    with doc.create(Section('Current vs. flux (GIF)', numbering=False)):
    
    # Add cheque images
        with doc.create(LongTabu("X[c] X[c] X[c] X[c]")) as cheque_table:
            png_list = glob.iglob('i*.pdf')
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
	
    doc.generate_pdf("complex_report", clean_tex=False, compiler='pdflatex')
#---------------------------------------------------------------------------------------------

generate_unique(sectors_notirradiated,hv_notirradiated,spark_notirradiated, sectors_irradiated, hv_irradiated, spark_irradiated)
os.system("rm GIF*.pdf")
os.system("rm i*.pdf")
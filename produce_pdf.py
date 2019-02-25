import os
import datetime

from pylatex import Document, PageStyle, Head, Foot, MiniPage, \
    StandAloneGraphic, MultiColumn, Tabu, LongTabu, LargeText, MediumText, \
    LineBreak, NewPage, Tabularx, TextColor, simple_page_number, Section, TextBlock
from pylatex.utils import bold, NoEscape

now = datetime.datetime.now()

gas_leak = raw_input("Insert gas leake (mL/h): ")


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
                                     'cernlogo')
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
            title_wrapper.append(LargeText(bold("Chamber: to be filled ")))
            title_wrapper.append(LineBreak())
            title_wrapper.append("ID: to be filled")

    # Add footer
    with first_page.create(Foot("C")) as footer:
        
        with footer.create(Tabularx(
                "X X X X",
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
                                  branch_address3, document_details])

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
        with doc.create(LongTabu("X[l] X[r] X[r] X[r]",
                                 row_height=1.5)) as data_table:
            data_table.add_row(["Sector",
                                "HV",
                                "spark/min",
                                "Final"],
                               mapper=bold,
                               color="lightgray")
            data_table.add_empty_row()
            data_table.add_hline()
            row = ["sector", "hv", "spark", "0 or 1"]
            for i in range(len(hv_notirradiated)):
                if (i % 2) == 0:
                    if int(hv_notirradiated[i]) > 565 and spark_notirradiated[i]<1.0:
                        accepted = 1
                    else:
                        accepted = 0 
                    data_table.add_row([str(sectors_notirradiated[i]), str(hv_notirradiated[i]), str(spark_notirradiated[i]), accepted], color="lightgray")
                else:
                    if int(hv_notirradiated[i]) > 565 and spark_notirradiated[i]<1.0:
                        accepted = 1
                    else:
                        accepted = 0  
                    data_table.add_row([str(sectors_notirradiated[i]), str(hv_notirradiated[i]), str(spark_notirradiated[i]), accepted])

    doc.append(NewPage())

    with doc.create(Section('HV irradiated at GIF', numbering=False)):
       # Add statement table
        with doc.create(LongTabu("X[l] X[r] X[r] X[r]",
                                 row_height=1.5)) as data_table:
            data_table.add_row(["Sector",
                                "HV",
                                "spark/min",
                                "Final"],
                               mapper=bold,
                               color="lightgray")
            data_table.add_empty_row()
            data_table.add_hline()
            row = ["sector", "hv", "spark", "0 or 1"]
            for i in range(len(hv_irradiated)):
                if (i % 2) == 0:
                    if int(hv_irradiated[i]) > 565 and spark_irradiated[i]<1.0:
                        accepted = 1
                    else:
                        accepted = 0 
                    data_table.add_row([str(sectors_irradiated[i]), str(hv_irradiated[i]), str(spark_irradiated[i]), accepted], color="lightgray")
                else:
                    if int(hv_irradiated[i]) > 565 and spark_irradiated[i]<1.0:
                        accepted = 1
                    else:
                        accepted = 0  
                    data_table.add_row([str(sectors_irradiated[i]), str(hv_irradiated[i]), str(spark_irradiated[i]), accepted])

    with doc.create(Section('Current vs. flux (GIF)', numbering=False)):
    
    # Add cheque images
        with doc.create(LongTabu("X[c] X[c] X[c] X[c]")) as cheque_table:
            cheque_file = os.path.join(os.path.dirname(__file__),
                                   'example.png')
            cheque = StandAloneGraphic(cheque_file, image_options="width=100px")
            for i in range(0, 10):
                cheque_table.add_row([cheque, cheque, cheque, cheque])
    
    doc.generate_pdf("complex_report", clean_tex=False, compiler='pdflatex')

generate_unique(["L1L1","L1L2","L1L3","L1L4","L2L3","L4L5"],[0,570,567,3,4,5],[0,1.2,0.4,0.2,1.0,0.4],["L1L1","L1L2","L1L3","L1L4","L2L3","L4L5"],[0,570,567,3,4,5],[0,1.2,0.4,0.2,1.0,0.4])

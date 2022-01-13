from datetime import datetime
from fpdf import FPDF
import pandas as pd
import excel2img

date_excel=pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Annual_report_title')
for i in range(0, len(date_excel)):
    date = str(date_excel['date'].loc[i])

fund_name_excel=pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Annual_report_title')
for i in range(0, len(fund_name_excel)):
    fund_name = str(date_excel['fund_name'].loc[i])

for i in range(0, len(fund_name_excel)):
    fund_name_uppercase = str(date_excel['fund_name_uppercase'].loc[i])

def str_repeat(s, count):
	return s * int(count)

class PDF(FPDF):
    def header(self):
        # Line break
        self.ln(5)

    def print_title1(self, name, name1):
        self.df2 = pd.read_excel(name, sheet_name=name1)
        self.set_font('Times', '', 36)
        self.set_text_color(0, 0, 80)
        for i in range(0, len(self.df2)):
            col_a = str(self.df2['col1'].loc[i])
            self.cell(210,65, col_a, align='C')

    def print_title2(self, name, name1):
        self.df3 = pd.read_excel(name, sheet_name=name1)
        self.set_font('Times', '', 36)
        self.set_text_color(0, 0, 80)
        for i in range(0, len(self.df3)):
            col_a = str(self.df3['col2'].loc[i])
            self.cell(211,90, col_a, align='C')

    def print_title3(self, name, name1):
        self.df4 = pd.read_excel(name, sheet_name=name1)
        self.set_font('Times', '', 36)
        self.set_text_color(0, 0, 80)
        for i in range(0, len(self.df4)):
            col_a = str(self.df4['col3'].loc[i])
            self.cell(211,105, col_a, align='C')

    def print_title4(self, name, name1):
        self.df5 = pd.read_excel(name, sheet_name=name1)
        self.set_font('Times', '', 36)
        self.set_text_color(0, 0, 80)
        for i in range(0, len(self.df5)):
            col_a = str(self.df5['col4'].loc[i])
            self.cell(235,120, col_a, align='C')

    def print_date_title(self, name, name1):
        self.df6 = pd.read_excel(name, sheet_name=name1)
        for i in range(0, len(self.df6)):
            col_a = str(self.df5['date'].loc[i])
            self.cell(208, 140, col_a, align='C')

    def print_report_type(self, name, name1):
        self.df8 = pd.read_excel(name, sheet_name=name1)
        for i in range(0, len(self.df8)):
            col_a = str(self.df8['report_type'].loc[i])
            self.cell(210, 140, col_a, align='C')

    def chapter_title(self, label):
        self.set_font('Times', 'B', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, '%s' % (label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def print_chapter_title(self, label):
        self.chapter_title(label)

    def print_text(self, name, name1):
        self.df = pd.read_excel(name, sheet_name=name1)
        self.set_font('Times', '', 12)
        for i in range(0, len(self.df)):
            col_a = str(self.df['col1'].loc[i])
            if col_a.strip().isupper():
                self.set_font('Times', 'B', 12)
            else:
                self.set_font('Times', '', 12)
            col=col_a.strip().replace("$date", date).replace("$fund_name", fund_name).replace("$FUND_NAME_UPPERCASE", fund_name_uppercase)
            self.multi_cell(0, 5, col)
            self.ln()

    def print_text_note(self, name, name1):
        self.df1 = pd.read_excel(name, sheet_name=name1)
        self.set_font('Times', 'I', 10)
        for i in range(0, len(self.df1)):
            col_a = str(self.df1['col1'].loc[i])
            col = col_a.strip().replace("$date", date).replace("$fund_name", fund_name).replace("$FUND_NAME_UPPERCASE", fund_name_uppercase)
            self.multi_cell(0, 3, col)
            self.ln()

class TOC(PDF):
	def __init__(this, orientation='P',unit='mm',format='A4'):
		this._toc=[]
		this._numbering=0
		this._numberingFooter=0
		this._numPageNum=1
		FPDF.__init__(this,orientation,unit,format)

	def AddPage(this,orientation=''):
		FPDF.add_page(this,orientation)
		if(this._numbering):
			this._numPageNum+=1

	def startPageNums(this):
		this._numbering=1
		this._numberingFooter=1

	def stopPageNums(this):
		this._numbering=0

	def numPageNo(this):
		return this.page_no()+1

	def TOC_Entry(this,txt,level=0):
		this._toc+=[{'t':txt,'l':level,'p':this.numPageNo()}]

	def insertTOC(this,location=1,labelSize=20,entrySize=10,tocfont='Times',label='Table of Contents'):
		#make toc at end
		this.stopPageNums()
		this.AddPage()
		tocstart=this.page

		this.set_font(tocfont,'B',labelSize)
		this.cell(0,5,label,0,1,'C')
		this.ln(10)

		for t in this._toc:
			#Offset
			level=t['l']
			if(level>0):
				this.cell(level*8)
			weight=''
			if(level==0):
				weight='B'
			Str=t['t']
			this.set_font(tocfont,weight,entrySize)
			strsize=this.get_string_width(Str)
			this.cell(strsize+2,this.font_size+2,Str)

			#Filling dots
			this.set_font(tocfont,'',entrySize)
			PageCellSize=this.get_string_width(str(t['p']))+2
			w=this.w-this.l_margin-this.r_margin-PageCellSize-(level*8)-(strsize+2)
			nb=w/this.get_string_width('.')
			dots = str_repeat('.', nb)
			this.cell(w, this.font_size + 2, dots, 0, 0, 'R')

			#Page number
			this.cell(PageCellSize,this.font_size+2,str(t['p']),0,1,'R')

		#grab it and move to selected location
		n=this.page
		n_toc = n - tocstart + 1
		last = []

		#store toc pages
		for i in range(tocstart,n+1):
			last+=[this.pages[i]]

		#move pages
		for i in range(tocstart-1,location-1,-1):
		#~ for(i=tocstart - 1;i>=location-1;i--)
			this.pages[i+n_toc]=this.pages[i]

		#Put toc pages at insert point
		for i in range(0,n_toc):
			this.pages[location + i]=last[i]

	def footer(self):
		self.ln(5)

current_date=datetime.today().strftime('%d %B %Y')

# Cover Page
pdf = TOC()
pdf.AddPage()
pdf.set_line_width(2)
pdf.set_draw_color(255, 0, 0)
pdf.line(90, 42, 90, 128)
pdf.print_title1('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Annual_report_title')
pdf.ln(2.5)
pdf.print_title2('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Annual_report_title')
pdf.ln(8.5)
pdf.print_title3('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Annual_report_title')
pdf.ln(9)
pdf.print_title4('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Annual_report_title')
pdf.ln(12)
pdf.set_font('Times', 'B', 14)
pdf.print_report_type('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Annual_report_title')
pdf.ln(8)
pdf.set_font('Times', 'B', 14)
pdf.print_date_title('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Annual_report_title')
pdf.ln(10)
pdf.image("image/logo.PNG", x=100, y=250,w=80)
pdf.AddPage()
pdf.output('Annual Report/Annual Report_UGDEF/Annual Report UGDEF_cover.pdf', 'F')

pdf = TOC()
pdf.AddPage()
pdf.set_text_color(0,0,0)

# Part A
pdf.startPageNums()
pdf.print_chapter_title("(A) MANAGER'S REPORT")
pdf.TOC_Entry("(A) MANAGER'S REPORT", 0)

pdf.print_text('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Key Data of the Fund')
df_MYR = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='MYR hedged Class_table')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 3
th = pdf.font_size
pdf.set_font('Times', '', 12)
for i in range(0, len(df_MYR)):

    col_a = str(df_MYR['col1'].loc[i])
    col_b = str(df_MYR['col2'].loc[i])
    col_c = str(df_MYR['col3'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    if col_a.strip() == 'Total':
        pdf.set_font('Times', 'B', 12)
    pdf.cell(col_width, 1.2*th, '%s' % (col_a), 1, 0, 'L')
    pdf.cell(col_width, 1.2*th, '%s' % (col_b), 1, 0, 'C')
    pdf.cell(col_width, 1.2*th, '%s' % (col_c), 1, 0, 'R')
    pdf.ln(1.2*th)

pdf.ln(10)
pdf.print_text('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'USD Class')
df_USD = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='USD Class_table')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 3
th = pdf.font_size
pdf.set_font('Times', '', 12)
for i in range(0, len(df_USD)):

    col_a = str(df_USD['col1'].loc[i])
    col_b = str(df_USD['col2'].loc[i])
    col_c = str(df_USD['col3'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    if col_a.strip() == 'Total':
        pdf.set_font('Times', 'B', 12)
    pdf.cell(col_width, 1.2*th, '%s' % (col_a), 1, 0, 'L')
    pdf.cell(col_width, 1.2*th, '%s' % (col_b), 1, 0, 'C')
    pdf.cell(col_width, 1.2*th, '%s' % (col_c), 1, 0, 'R')
    pdf.ln(1.2*th)

pdf.ln(10)
pdf.print_text('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'AUD hedged Class')
df_AUD = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='AUD hedged Class_table')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 3
th = pdf.font_size
pdf.set_font('Times', '', 12)
for i in range(0, len(df_AUD)):

    col_a = str(df_AUD['col1'].loc[i])
    col_b = str(df_AUD['col2'].loc[i])
    col_c = str(df_AUD['col3'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    if col_a.strip() == 'Total':
        pdf.set_font('Times', 'B', 12)
    pdf.cell(col_width, 1.2*th, '%s' % (col_a), 1, 0, 'L')
    pdf.cell(col_width, 1.2*th, '%s' % (col_b), 1, 0, 'C')
    pdf.cell(col_width, 1.2*th, '%s' % (col_c), 1, 0, 'R')
    pdf.ln(1.2*th)

pdf.ln(10)
pdf.print_text('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'SGD hedged Class')
df_SGD = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='SGD hedged Class_table')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 3
th = pdf.font_size
pdf.set_font('Times', '', 12)
for i in range(0, len(df_SGD)):

    col_a = str(df_SGD['col1'].loc[i])
    col_b = str(df_SGD['col2'].loc[i])
    col_c = str(df_SGD['col3'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    if col_a.strip() == 'Total':
        pdf.set_font('Times', 'B', 12)
    pdf.cell(col_width, 1.2*th, '%s' % (col_a), 1, 0, 'L')
    pdf.cell(col_width, 1.2*th, '%s' % (col_b), 1, 0, 'C')
    pdf.cell(col_width, 1.2*th, '%s' % (col_c), 1, 0, 'R')
    pdf.ln(1.2*th)

pdf.ln(10)
pdf.print_text('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'GBP hedged Class')
df_GBP = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='GBP hedged Class_table')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 3
th = pdf.font_size
pdf.set_font('Times', '', 12)
for i in range(0, len(df_GBP)):

    col_a = str(df_GBP['col1'].loc[i])
    col_b = str(df_GBP['col2'].loc[i])
    col_c = str(df_GBP['col3'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    if col_a.strip() == 'Total':
        pdf.set_font('Times', 'B', 12)
    pdf.cell(col_width, 1.2*th, '%s' % (col_a), 1, 0, 'L')
    pdf.cell(col_width, 1.2*th, '%s' % (col_b), 1, 0, 'C')
    pdf.cell(col_width, 1.2*th, '%s' % (col_c), 1, 0, 'R')
    pdf.ln(1.2*th)

pdf.ln(10)
pdf.print_text('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Another hedged Class')
df_Ano = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Another hedged Class_table')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 3
th = pdf.font_size
pdf.set_font('Times', '', 12)
for i in range(0, len(df_Ano)):

    col_a = str(df_Ano['col1'].loc[i])
    col_b = str(df_Ano['col2'].loc[i])
    col_c = str(df_Ano['col3'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    if col_a.strip() == 'Total':
        pdf.set_font('Times', 'B', 12)
    pdf.cell(col_width, 1.2*th, '%s' % (col_a), 1, 0, 'L')
    pdf.cell(col_width, 1.2*th, '%s' % (col_b), 1, 0, 'C')
    pdf.cell(col_width, 1.2*th, '%s' % (col_c), 1, 0, 'R')
    pdf.ln(1.2*th)

pdf.ln(10)
pdf.print_text_note('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Breakdown of unit holdings_note')
pdf.ln(12)
pdf.print_text('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Performance Data of the Fund_1')
df_2 = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Portfolio composition')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 3
pdf.set_font('Times', 'B', 12)
pdf.ln(1)

th = pdf.font_size
pdf.ln(4.2)
pdf.set_font('Times', '', 12)
for i in range(0, len(df_2)):

    col_a = str(df_2['col1'].loc[i])
    col_b = str(df_2['col2'].loc[i])
    col_c = str(df_2['col3'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    if col_a.strip() == 'Total':
        pdf.set_font('Times', 'B', 12)
    top = pdf.y
    offset = pdf.x + 90
    pdf.multi_cell(90, 1.2*th, '%s' % (col_a), 1, 'L', False)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(50, 1.2*th, '%s' % (col_b), 1, 'C', False)
    pdf.y = top
    pdf.x = offset+50
    pdf.multi_cell(50, 1.2*th, '%s' % (col_c), 1, 'C', False)

pdf.ln(10)
pdf.ln(2)
pdf.print_text('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Performance Data of the Fund_2')
pdf.AddPage()
df_3 = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Performance details')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 3
pdf.set_font('Times', 'B', 12)
pdf.ln(1)

th = pdf.font_size
pdf.ln(4.2)
pdf.set_font('Times', '', 12)
for i in range(0, len(df_3)):

    col_a = str(df_3['col1'].loc[i])
    col_b = str(df_3['col2'].loc[i])
    col_c = str(df_3['col3'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    top = pdf.y
    offset = pdf.x + 100
    pdf.multi_cell(100, 1.2*th, '%s' % (col_a), 1, 'L', False)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(45, 1.2*th, '%s' % (col_b), 1, 'C', False)
    pdf.y = top
    pdf.x = offset + 45
    pdf.multi_cell(45, 1.2*th, '%s' % (col_c), 1, 'C', False)

pdf.ln(2)
pdf.AddPage()
df_3_1 = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Performance details1')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 3
pdf.set_font('Times', 'B', 12)
pdf.ln(1)

th = pdf.font_size
pdf.ln(4.2)
pdf.set_font('Times', '', 12)
for i in range(0, len(df_3_1)):

    col_a = str(df_3_1['col1'].loc[i])
    col_b = str(df_3_1['col2'].loc[i])
    col_c = str(df_3_1['col3'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    top = pdf.y
    offset = pdf.x + 100
    pdf.multi_cell(100, 1.2*th, '%s' % (col_a), 1, 'L', False)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(45, 1.2*th, '%s' % (col_b), 1, 'C', False)
    pdf.y = top
    pdf.x = offset + 45
    pdf.multi_cell(45, 1.2*th, '%s' % (col_c), 1, 'C', False)

pdf.ln(2)
pdf.print_text_note('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Performance Data of the Fund_3')
pdf.ln(5)
pdf.AddPage()
pdf.print_text('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Average total return')
df_4 = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Average total return_table')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 2
pdf.set_font('Times', 'B', 12)
th = pdf.font_size
pdf.set_font('Times', '', 12)
for i in range(0, len(df_4)):

    col_a = str(df_4['col1'].loc[i])
    col_b = str(df_4['col2'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    top = pdf.y
    offset = pdf.x + 95
    pdf.multi_cell(95, 1.2*th, '%s' % (col_a), 1, 0, 'L')
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(95, 1.2*th, '%s' % (col_b), 1, 0, 'C')

pdf.ln(10)
pdf.AddPage()
pdf.print_text('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Annual total return')
df_5 = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Annual total return_table')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 2
pdf.set_font('Times', 'B', 12)
th = pdf.font_size
pdf.set_font('Times', '', 12)
for i in range(0, len(df_5)):

    col_a = str(df_5['col1'].loc[i])
    col_b = str(df_5['col2'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    top = pdf.y
    offset = pdf.x + 95
    pdf.multi_cell(95, 1.2*th, '%s' % (col_a), 1, 0, 'L')
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(95, 1.2*th, '%s' % (col_b), 1, 0, 'C')

pdf.ln(10)
pdf.print_text_note('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Annual total return_Note')
pdf.ln(2)
pdf.print_text('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Annual total return_Note1')
# print graph
excel2img.export_img("Annual Report/graph/Graph_UGDEF_MYR.xlsx","Annual Report/graph/image_graph_UGDEF_MYR.png")
pdf.image("Annual Report/graph/image_graph_UGDEF_MYR.png", w=190)
pdf.ln(2)
pdf.print_text_note('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Graph source')
pdf.ln(5)
df_MYR1 = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Performance review_table_MYR')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 6
pdf.set_font('Times', 'B', 12)
pdf.ln(1)

th = pdf.font_size

pdf.ln(2)
pdf.set_font('Times', '', 12)
for i in range(0, len(df_MYR1)):

    col_a = str(df_MYR1['col1'].loc[i])
    col_b = str(df_MYR1['col2'].loc[i])
    col_c = str(df_MYR1['col3'].loc[i])
    col_d = str(df_MYR1['col4'].loc[i])
    col_e = str(df_MYR1['col5'].loc[i])
    col_f = str(df_MYR1['col6'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    top = pdf.y
    offset = pdf.x + 28
    pdf.multi_cell(28, 1.2*th, '%s' % (col_a), 1, 'L', False)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(28, 1.2*th, '%s' % (col_b), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+28
    pdf.multi_cell(28, 1.2*th, '%s' % (col_c), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+56
    pdf.multi_cell(28, 1.2*th, '%s' % (col_d), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+84
    pdf.multi_cell(28, 1.2*th, '%s' % (col_e), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+112
    pdf.multi_cell(50, 1.2*th, '%s' % (col_f), 1, 'R', False)

pdf.ln(2)
pdf.print_text_note('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Performance review_table_source')
pdf.ln(5)
pdf.print_text('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Performance review_USD')
excel2img.export_img("Annual Report/graph/Graph_UGDEF_USD.xlsx","Annual Report/graph/image_graph_UGDEF_USD.png")
pdf.image("Annual Report/graph/image_graph_UGDEF_USD.png", w=190)
pdf.ln(2)
pdf.print_text_note('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Graph source')
df_USD = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Performance review_table_USD')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 6
pdf.set_font('Times', 'B', 12)
pdf.ln(1)

th = pdf.font_size

pdf.ln(2)
pdf.set_font('Times', '', 12)
for i in range(0, len(df_USD)):

    col_a = str(df_USD['col1'].loc[i])
    col_b = str(df_USD['col2'].loc[i])
    col_c = str(df_USD['col3'].loc[i])
    col_d = str(df_USD['col4'].loc[i])
    col_e = str(df_USD['col5'].loc[i])
    col_f = str(df_USD['col6'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    top = pdf.y
    offset = pdf.x + 28
    pdf.multi_cell(28, 1.2*th, '%s' % (col_a), 1, 'L', False)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(28, 1.2*th, '%s' % (col_b), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+28
    pdf.multi_cell(28, 1.2*th, '%s' % (col_c), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+56
    pdf.multi_cell(28, 1.2*th, '%s' % (col_d), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+84
    pdf.multi_cell(28, 1.2*th, '%s' % (col_e), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+112
    pdf.multi_cell(50, 1.2*th, '%s' % (col_f), 1, 'R', False)

pdf.ln(2)
pdf.print_text_note('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Performance review_table_source')
pdf.ln(5)
pdf.print_text('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Performance review_AUD')
excel2img.export_img("Annual Report/graph/Graph_UGDEF_AUD.xlsx","Annual Report/graph/image_graph_UGDEF_AUD.png")
pdf.image("Annual Report/graph/image_graph_UGDEF_AUD.png", w=190)
pdf.ln(2)
pdf.print_text_note('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Graph source')
df_AUD = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Performance review_table_AUD')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 6
pdf.set_font('Times', 'B', 12)
pdf.ln(1)

th = pdf.font_size

pdf.ln(2)
pdf.set_font('Times', '', 12)
for i in range(0, len(df_AUD)):

    col_a = str(df_AUD['col1'].loc[i])
    col_b = str(df_AUD['col2'].loc[i])
    col_c = str(df_AUD['col3'].loc[i])
    col_d = str(df_AUD['col4'].loc[i])
    col_e = str(df_AUD['col5'].loc[i])
    col_f = str(df_AUD['col6'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    top = pdf.y
    offset = pdf.x + 28
    pdf.multi_cell(28, 1.2*th, '%s' % (col_a), 1, 'L', False)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(28, 1.2*th, '%s' % (col_b), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+28
    pdf.multi_cell(28, 1.2*th, '%s' % (col_c), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+56
    pdf.multi_cell(28, 1.2*th, '%s' % (col_d), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+84
    pdf.multi_cell(28, 1.2*th, '%s' % (col_e), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+112
    pdf.multi_cell(50, 1.2*th, '%s' % (col_f), 1, 'R', False)

pdf.ln(2)
pdf.print_text_note('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Performance review_table_source')
pdf.ln(5)
pdf.print_text('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Performance review_SGD')
excel2img.export_img("Annual Report/graph/Graph_UGDEF_SGD.xlsx","Annual Report/graph/image_graph_UGDEF_SGD.png")
pdf.image("Annual Report/graph/image_graph_UGDEF_SGD.png", w=190)
pdf.ln(2)
pdf.print_text_note('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Graph source')
df_SGD = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Performance review_table_SGD')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 6
pdf.set_font('Times', 'B', 12)
pdf.ln(1)

th = pdf.font_size

pdf.ln(2)
pdf.set_font('Times', '', 12)
for i in range(0, len(df_SGD)):

    col_a = str(df_SGD['col1'].loc[i])
    col_b = str(df_SGD['col2'].loc[i])
    col_c = str(df_SGD['col3'].loc[i])
    col_d = str(df_SGD['col4'].loc[i])
    col_e = str(df_SGD['col5'].loc[i])
    col_f = str(df_SGD['col6'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    top = pdf.y
    offset = pdf.x + 28
    pdf.multi_cell(28, 1.2*th, '%s' % (col_a), 1, 'L', False)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(28, 1.2*th, '%s' % (col_b), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+28
    pdf.multi_cell(28, 1.2*th, '%s' % (col_c), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+56
    pdf.multi_cell(28, 1.2*th, '%s' % (col_d), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+84
    pdf.multi_cell(28, 1.2*th, '%s' % (col_e), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+112
    pdf.multi_cell(50, 1.2*th, '%s' % (col_f), 1, 'R', False)

pdf.ln(2)
pdf.print_text_note('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Performance review_table_source')
pdf.ln(5)
pdf.print_text('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Performance review_GBP')
excel2img.export_img("Annual Report/graph/Graph_UGDEF_GBP.xlsx","Annual Report/graph/image_graph_UGDEF_GBP.png")
pdf.image("Annual Report/graph/image_graph_UGDEF_GBP.png", w=190)
pdf.ln(2)
pdf.print_text_note('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Graph source')
df_GBP = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Performance review_table_GBP')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 6
pdf.set_font('Times', 'B', 12)
pdf.ln(1)

th = pdf.font_size

pdf.ln(2)
pdf.set_font('Times', '', 12)
for i in range(0, len(df_GBP)):

    col_a = str(df_GBP['col1'].loc[i])
    col_b = str(df_SGD['col2'].loc[i])
    col_c = str(df_GBP['col3'].loc[i])
    col_d = str(df_GBP['col4'].loc[i])
    col_e = str(df_GBP['col5'].loc[i])
    col_f = str(df_GBP['col6'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    top = pdf.y
    offset = pdf.x + 28
    pdf.multi_cell(28, 1.2*th, '%s' % (col_a), 1, 'L', False)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(28, 1.2*th, '%s' % (col_b), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+28
    pdf.multi_cell(28, 1.2*th, '%s' % (col_c), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+56
    pdf.multi_cell(28, 1.2*th, '%s' % (col_d), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+84
    pdf.multi_cell(28, 1.2*th, '%s' % (col_e), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+112
    pdf.multi_cell(50, 1.2*th, '%s' % (col_f), 1, 'R', False)

pdf.ln(2)
pdf.print_text_note('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Performance review_table_source')
pdf.ln(5)
pdf.print_text('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Performance review_GBP_1')
excel2img.export_img("Annual Report/graph/Graph_UGDEF_GBP_1.xlsx","Annual Report/graph/image_graph_UGDEF_GBP_1.png")
pdf.image("Annual Report/graph/image_graph_UGDEF_GBP_1.png", w=190)
pdf.ln(2)
pdf.print_text_note('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Graph source')
df_GBP_Ano = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Performance review_table_GBP_1')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 6
pdf.set_font('Times', 'B', 12)
pdf.ln(1)

th = pdf.font_size

pdf.ln(2)
pdf.set_font('Times', '', 12)
for i in range(0, len(df_GBP_Ano)):

    col_a = str(df_GBP_Ano['col1'].loc[i])
    col_b = str(df_GBP_Ano['col2'].loc[i])
    col_c = str(df_GBP_Ano['col3'].loc[i])
    col_d = str(df_GBP_Ano['col4'].loc[i])
    col_e = str(df_GBP_Ano['col5'].loc[i])
    col_f = str(df_GBP_Ano['col6'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    top = pdf.y
    offset = pdf.x + 28
    pdf.multi_cell(28, 1.2*th, '%s' % (col_a), 1, 'L', False)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(28, 1.2*th, '%s' % (col_b), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+28
    pdf.multi_cell(28, 1.2*th, '%s' % (col_c), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+56
    pdf.multi_cell(28, 1.2*th, '%s' % (col_d), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+84
    pdf.multi_cell(28, 1.2*th, '%s' % (col_e), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+112
    pdf.multi_cell(50, 1.2*th, '%s' % (col_f), 1, 'R', False)

pdf.ln(2)
pdf.print_text_note('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Performance review_table_source')
pdf.ln(5)
pdf.print_text("Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx", 'Target fund performance')
pdf.AddPage()
df_6 = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Target fund performance_table')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 6
pdf.set_font('Times', 'B', 12)
pdf.ln(1)

th = pdf.font_size

pdf.ln(2)
pdf.set_font('Times', '', 12)
for i in range(0, len(df_6)):

    col_a = str(df_6['col1'].loc[i])
    col_b = str(df_6['col2'].loc[i])
    col_c = str(df_6['col3'].loc[i])
    col_d = str(df_6['col4'].loc[i])
    col_e = str(df_6['col5'].loc[i])
    col_f = str(df_6['col6'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    top = pdf.y
    offset = pdf.x + 28
    pdf.multi_cell(28, 1.2*th, '%s' % (col_a), 1, 'L', False)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(28, 1.2*th, '%s' % (col_b), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+28
    pdf.multi_cell(28, 1.2*th, '%s' % (col_c), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+56
    pdf.multi_cell(28, 1.2*th, '%s' % (col_d), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+84
    pdf.multi_cell(28, 1.2*th, '%s' % (col_e), 1, 'R', False)
    pdf.y = top
    pdf.x = offset+112
    pdf.multi_cell(50, 1.2*th, '%s' % (col_f), 1, 'R', False)

pdf.ln(2)
pdf.print_text_note("Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx", 'Target fund performance_source')
pdf.ln(5)
pdf.print_text("Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx", 'Strategies')
pdf.ln(2)
df_7 = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Asset allocation_table')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 4
pdf.set_font('Times', 'B', 12)
pdf.ln(1)

th = pdf.font_size

pdf.ln(2)
pdf.set_font('Times', '', 12)
for i in range(0, len(df_7)):

    col_a = str(df_7['col1'].loc[i])
    col_b = str(df_7['col2'].loc[i])
    col_c = str(df_7['col3'].loc[i])
    col_d = str(df_7['col4'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    top = pdf.y
    offset = pdf.x + 50
    pdf.multi_cell(50, 1.2 * th, '%s' % (col_a), 1, 'L', False)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(50, 1.2 * th, '%s' % (col_b), 1, 'C', False)
    pdf.y = top
    pdf.x = offset + 50
    pdf.multi_cell(50, 1.2 * th, '%s' % (col_c), 1, 'C', False)
    pdf.y = top
    pdf.x = offset + 100
    pdf.multi_cell(40, 1.2 * th, '%s' % (col_d), 1, 'C', False)

pdf.ln(5)
pdf.print_text("Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx", 'Asset allocation')
pdf.ln(2)
df_MYR2 = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Income distribution MYR_table')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 4
pdf.set_font('Times', 'B', 12)
th = pdf.font_size
pdf.set_font('Times', '', 12)
for i in range(0, len(df_MYR2)):

    col_a = str(df_MYR2['col1'].loc[i])
    col_b = str(df_MYR2['col2'].loc[i])
    col_c = str(df_MYR2['col3'].loc[i])
    col_d = str(df_MYR2['col4'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    if col_a.strip()=="Total":
        pdf.set_font('Times', 'B', 12)
    top = pdf.y
    offset = pdf.x + 49
    pdf.multi_cell(49, 1.2 * th, '%s' % (col_a), 1, 'L', False)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(47, 1.2 * th, '%s' % (col_b), 1, 'C', False)
    pdf.y = top
    pdf.x = offset + 47
    pdf.multi_cell(47, 1.2 * th, '%s' % (col_c), 1, 'C', False)
    pdf.y = top
    pdf.x = offset + 94
    pdf.multi_cell(47, 1.2 * th, '%s' % (col_d), 1, 'C', False)

pdf.ln(5)
pdf.print_text("Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx", 'Income distribution USD')
pdf.ln(2)
df_USD2 = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Income distribution USD_table')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 4
pdf.set_font('Times', 'B', 12)
th = pdf.font_size
pdf.set_font('Times', '', 12)
for i in range(0, len(df_USD2)):

    col_a = str(df_USD2['col1'].loc[i])
    col_b = str(df_USD2['col2'].loc[i])
    col_c = str(df_USD2['col3'].loc[i])
    col_d = str(df_USD2['col4'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    if col_a.strip()=="Total":
        pdf.set_font('Times', 'B', 12)
    top = pdf.y
    offset = pdf.x + 49
    pdf.multi_cell(49, 1.2 * th, '%s' % (col_a), 1, 'L', False)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(47, 1.2 * th, '%s' % (col_b), 1, 'C', False)
    pdf.y = top
    pdf.x = offset + 47
    pdf.multi_cell(47, 1.2 * th, '%s' % (col_c), 1, 'C', False)
    pdf.y = top
    pdf.x = offset + 94
    pdf.multi_cell(47, 1.2 * th, '%s' % (col_d), 1, 'C', False)

pdf.ln(5)
pdf.print_text("Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx", 'Income distribution AUD')
pdf.ln(2)
df_AUD2 = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Income distribution AUD_table')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 4
pdf.set_font('Times', 'B', 12)
th = pdf.font_size
pdf.set_font('Times', '', 12)
for i in range(0, len(df_AUD2)):

    col_a = str(df_AUD2['col1'].loc[i])
    col_b = str(df_AUD2['col2'].loc[i])
    col_c = str(df_AUD2['col3'].loc[i])
    col_d = str(df_AUD2['col4'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    if col_a.strip()=="Total":
        pdf.set_font('Times', 'B', 12)
    top = pdf.y
    offset = pdf.x + 49
    pdf.multi_cell(49, 1.2 * th, '%s' % (col_a), 1, 'L', False)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(47, 1.2 * th, '%s' % (col_b), 1, 'C', False)
    pdf.y = top
    pdf.x = offset + 47
    pdf.multi_cell(47, 1.2 * th, '%s' % (col_c), 1, 'C', False)
    pdf.y = top
    pdf.x = offset + 94
    pdf.multi_cell(47, 1.2 * th, '%s' % (col_d), 1, 'C', False)

pdf.ln(5)
pdf.print_text("Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx", 'Income distribution AUD_1')
pdf.ln(2)
df_AUD2_Ano = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Income distribution AUD_table_1')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 4
pdf.set_font('Times', 'B', 12)
th = pdf.font_size
pdf.set_font('Times', '', 12)
for i in range(0, len(df_AUD2_Ano)):

    col_a = str(df_AUD2_Ano['col1'].loc[i])
    col_b = str(df_AUD2_Ano['col2'].loc[i])
    col_c = str(df_AUD2_Ano['col3'].loc[i])
    col_d = str(df_AUD2_Ano['col4'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    if col_a.strip()=="Total":
        pdf.set_font('Times', 'B', 12)
    top = pdf.y
    offset = pdf.x + 49
    pdf.multi_cell(49, 1.2 * th, '%s' % (col_a), 1, 'L', False)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(47, 1.2 * th, '%s' % (col_b), 1, 'C', False)
    pdf.y = top
    pdf.x = offset + 47
    pdf.multi_cell(47, 1.2 * th, '%s' % (col_c), 1, 'C', False)
    pdf.y = top
    pdf.x = offset + 94
    pdf.multi_cell(47, 1.2 * th, '%s' % (col_d), 1, 'C', False)

pdf.ln(5)
pdf.AddPage()
pdf.print_text("Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx", 'Income distribution AUD_2')
pdf.ln(2)
df_AUD2_Ano1 = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Income distribution AUD_table_2')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 4
pdf.set_font('Times', 'B', 12)
th = pdf.font_size
pdf.set_font('Times', '', 12)
for i in range(0, len(df_AUD2_Ano1)):

    col_a = str(df_AUD2_Ano1['col1'].loc[i])
    col_b = str(df_AUD2_Ano1['col2'].loc[i])
    col_c = str(df_AUD2_Ano1['col3'].loc[i])
    col_d = str(df_AUD2_Ano1['col4'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    if col_a.strip()=="Total":
        pdf.set_font('Times', 'B', 12)
    top = pdf.y
    offset = pdf.x + 49
    pdf.multi_cell(49, 1.2 * th, '%s' % (col_a), 1, 'L', False)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(47, 1.2 * th, '%s' % (col_b), 1, 'C', False)
    pdf.y = top
    pdf.x = offset + 47
    pdf.multi_cell(47, 1.2 * th, '%s' % (col_c), 1, 'C', False)
    pdf.y = top
    pdf.x = offset + 94
    pdf.multi_cell(47, 1.2 * th, '%s' % (col_d), 1, 'C', False)

pdf.ln(5)
pdf.print_text("Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx", 'Income distribution AUD_3')
pdf.ln(2)
df_AUD2_Ano2 = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Income distribution AUD_table_3')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

pdf.set_font('Times', '', 12)
col_width = page_width / 4
pdf.set_font('Times', 'B', 12)
th = pdf.font_size
pdf.set_font('Times', '', 12)
for i in range(0, len(df_AUD2_Ano2)):

    col_a = str(df_AUD2_Ano2['col1'].loc[i])
    col_b = str(df_AUD2_Ano2['col2'].loc[i])
    col_c = str(df_AUD2_Ano2['col3'].loc[i])
    col_d = str(df_AUD2_Ano2['col4'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    if col_a.strip()=="Total":
        pdf.set_font('Times', 'B', 12)
    top = pdf.y
    offset = pdf.x + 49
    pdf.multi_cell(49, 1.2 * th, '%s' % (col_a), 1, 'L', False)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(47, 1.2 * th, '%s' % (col_b), 1, 'C', False)
    pdf.y = top
    pdf.x = offset + 47
    pdf.multi_cell(47, 1.2 * th, '%s' % (col_c), 1, 'C', False)
    pdf.y = top
    pdf.x = offset + 94
    pdf.multi_cell(47, 1.2 * th, '%s' % (col_d), 1, 'C', False)

pdf.ln(5)
pdf.print_text("Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx", 'State of affairs')
pdf.set_font('Times', '', 12)
pdf.cell(0,0,current_date,align='L')
pdf.ln(2)

# Part B
pdf.AddPage()
pdf.print_chapter_title("(B) TRUSTEE'S REPORT")
pdf.TOC_Entry("(B) TRUSTEE'S REPORT", 0)
pdf.ln(5)
pdf.print_text('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Trustee Report')
pdf.ln(10)
df_9 = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Trustee Report_table')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

col_width = page_width / 2
pdf.ln(1)

th = pdf.font_size

pdf.ln(4.2)
pdf.set_font('Times', '', 12)
for i in range(0, len(df_9)):

    col_a = str(df_9['col1'].loc[i])
    col_b = str(df_9['col2'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    pdf.cell(col_width, 1.5*th, '%s' % (col_a), 0, 0, 'L')
    pdf.cell(col_width, 1.5*th, '%s' % (col_b), 0, 0, 'L')

    pdf.ln(1.5*th)
pdf.ln(5)
pdf.cell(0,0,current_date,align='L')
pdf.ln(5)

# Part C
pdf.AddPage()
pdf.print_chapter_title("(C) STATEMENT BY MANAGER")
pdf.TOC_Entry("(C) STATEMENT BY MANAGER", 0)
pdf.ln(5)
pdf.print_text('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Statement by Manager')
pdf.ln(20)
pdf.print_text('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', 'Statement by Manager_1')
pdf.ln(10)
df_10 = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Statement by Manager_table')

pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

col_width = page_width / 2
pdf.ln(1)

th = pdf.font_size

pdf.ln(4.2)
pdf.set_font('Times', '', 12)
for i in range(0, len(df_10)):

    col_a = str(df_10['col1'].loc[i])
    col_b = str(df_10['col2'].loc[i])
    if col_a.strip().isupper():
        pdf.set_font('Times', 'B', 12)
    else:
        pdf.set_font('Times', '', 12)
    pdf.cell(col_width, 1.5*th, '%s' % (col_a), 0, 0, 'L')
    pdf.cell(col_width, 1.5*th, '%s' % (col_b), 0, 0, 'L')

    pdf.ln(1.5*th)
pdf.ln(5)
pdf.cell(0,0,current_date,align='L')
pdf.ln(5)
pdf.output('Annual Report/Annual Report_UGDEF/Annual Report UGDEF_partd.pdf', 'F')

# Part F
pdf = TOC()
pdf.AddPage()
pdf.print_chapter_title("(F) CORPORATE INFORMATION")
pdf.TOC_Entry("(F) CORPORATE INFORMATION", 0)
df_36 = pd.read_excel('Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx', sheet_name='Corporate Information')
pdf.set_line_width(0.1)
pdf.set_draw_color(0, 0, 0)
page_width = pdf.w - 2 * pdf.l_margin

col_width = page_width / 2
pdf.ln(1)

th = pdf.font_size

pdf.set_font('Times', '', 12)
for i in range(0, len(df_36)):

    col_a = str(df_36['col1'].loc[i])
    col_b = str(df_36['col2'].loc[i])
    top = pdf.y
    offset = pdf.x + 70
    pdf.multi_cell(70, 1.5 * th, '%s' % (col_a), 1, 'L', False)
    pdf.y = top
    pdf.x = offset
    pdf.multi_cell(120, 1.5 * th, '%s' % (col_b), 1, 'L', False)

pdf.ln(5)
pdf.output('Annual Report/Annual Report_UGDEF/Annual Report UGDEF_partf.pdf', 'F')

# Combine Table of Content, Part A, B, C and F
from PyPDF2 import PdfFileMerger, PdfFileReader

# Call the PdfFileMerger
mergedObject = PdfFileMerger()
df_url1=pd.read_excel("Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx", sheet_name="Table of content")
for idx in df_url1.index:
   url1=df_url1['URL'][idx]
mergedObject.append(PdfFileReader(open(url1, 'rb')))

mergedObject.append(PdfFileReader(open("Annual Report/Annual Report_UGDEF/Annual Report UGDEF_partd.pdf", 'rb')))

df_url2=pd.read_excel("Annual Report/Annual Report_UGDEF/Annual Report_UGDEF.xlsx", sheet_name="PartD&E")
for idx in df_url2.index:
   url2=df_url2['URL'][idx]
mergedObject.append(PdfFileReader(open(url2, 'rb')))

mergedObject.append(PdfFileReader(open("Annual Report/Annual Report_UGDEF/Annual Report UGDEF_partf.pdf", 'rb')))

# Write all the files into a file which is named as shown below
mergedObject.write("Annual Report/Annual Report_UGDEF/mergedfilesoutput_UGDEF.pdf")

# Print Page Number
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import os
from PyPDF4.pdf import PdfFileReader, PdfFileWriter


def createPagePdf(num, tmp):
    c = canvas.Canvas(tmp)
    for i in range(1, num + 1):
        c.setFont('Times-Roman', 12)
        c.drawString((210 // 2) * mm, (8) * mm, str(i))
        c.showPage()
    c.save()


def add_page_number(pdf_path):
    """
    Add page numbers to a pdf, save the result as a new pdf
    @param pdf_path: path to pdf
    """
    tmp = "__tmp.pdf"

    output = PdfFileWriter()
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f, strict=False)
        n = pdf.getNumPages()

        # create new PDF with page numbers
        createPagePdf(n, tmp)

        with open(tmp, 'rb') as ftmp:
            numberPdf = PdfFileReader(ftmp)
            # iterarte pages
            for p in range(n):
                page = pdf.getPage(p)
                numberLayer = numberPdf.getPage(p)
                # merge number page with actual page
                page.mergePage(numberLayer)
                output.addPage(page)

            # write result
            if output.getNumPages():
                newpath = pdf_path[:-4] + "_numbered.pdf"
                with open(newpath, 'wb') as f:
                    output.write(f)
        os.remove(tmp)

add_page_number("Annual Report/Annual Report_UGDEF/mergedfilesoutput_UGDEF.pdf")

# Combine the merged PDF with cover page to generate final output
import PyPDF2

# Open the files that have to be merged one by one
pdf1File = open('Annual Report/Annual Report_UGDEF/Annual Report UGDEF_cover.pdf', 'rb')
pdf2File = open('Annual Report/Annual Report_UGDEF/mergedfilesoutput_UGDEF_numbered.pdf', 'rb')

# Read the files that you have opened
pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
pdf2Reader = PyPDF2.PdfFileReader(pdf2File)

# Create a new PdfFileWriter object which represents a blank PDF document
pdfWriter = PyPDF2.PdfFileWriter()

# Loop through all the page numbers for the first document
for pageNum in range(pdf1Reader.numPages):
    pageObj = pdf1Reader.getPage(pageNum)
    pdfWriter.addPage(pageObj)

# Loop through all the page numbers for the second document
for pageNum in range(pdf2Reader.numPages):
    pageObj = pdf2Reader.getPage(pageNum)
    pdfWriter.addPage(pageObj)

# After read all the pages in both the documents, write them into the a new PDF document
pdfOutputFile = open('Annual Report/Annual Report_UGDEF/UGDEF_Final_output_latest.pdf', 'wb')
pdfWriter.write(pdfOutputFile)

# Close all the files - Created as well as opened
pdfOutputFile.close()
pdf1File.close()
pdf2File.close()
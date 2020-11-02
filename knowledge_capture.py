
# %%
# from IPython import get_ipython


# %%
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
# get_ipython().run_line_magic('matplotlib', 'inline')
import datetime as dt
# from IPython.display import Image
# from IPython.core.display import HTML
import sqlite3
from networkx.algorithms import community
# from ipywidgets import interact
# import ipywidgets as widgets
from IPython.display import clear_output
from graphviz import Digraph
import graphviz
# import pydot
import csv
import os
import sys
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

try:
    import tkinter.ttk
    from tkinter import *
#     from tkinter.ttk import *
except:
    from tkinter import *
    
from tabulate import tabulate    


# %%
global sqlite_server
sqlite_server='knowledge.db'

class Graph_Data():
   """Instance Source--Target--Attribute data to be graphed"""
   
   headers=['SOURCE','TARGET','DESCR','CLASSIFICATION']
   e_class='TBD'
   type_file='TBD'
   df=pd.DataFrame()
   
   def __init__(self,type_file,e_class):
       
       self.type_file=type_file
       self.e_class=e_class
       Graph_Data.e_class=e_class
       Graph_Data.type_file=type_file
       
       if (self.type_file=='sql'):
           get_data(self.type_file)
           return None
       elif (self.type_file=='csv'):
           filename=input('Enter name of csv file: ')
           self.filename=f'{filename}.csv'
           try:
               self.num_attributes=int(input('num_attributes:'))
           except ValueError:
               self.num_attributes=0
       
           self.headers=['SOURCE', 'TARGET']
           
       
   def set_attributes(self):
       """Request attribute titles (names) and creates the attibute title list"""
       
       attribute_list=[]
       for i in range(self.num_attributes):
           attribute=input(f'Attribute{i}:')
           attribute_list.append(attribute)
       print(attribute_list)
       self.headers.extend(attribute_list)
   
   def create_file(self):
       """Initially create the file and place file headers"""
       
       if (self.num_attributes>0):
           self.set_attributes()
       
       with open(self.filename, mode='w+',newline='') as test_file:
           test_writer = csv.writer(test_file,dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
           test_writer.writerow(self.headers)
       
       self.num_attributes=0    
       
   def manual_data_entry(self,data_type='csv'):
       """Line by line entry of Source--Target--Attribute data in a csv file """
       
       # Read the first (header)row to get the column count from len(headers)
       with open(self.filename, newline='') as f:
           reader = csv.reader(f)
           self.headers=list(reader)[0]
        
           print(f'before extend: {self.headers}')
           
       if (self.num_attributes>0):
           self.set_attributes()
           print(f'after extend: {self.headers}')
           
           with open(self.filename, 'r+') as csvfile:
               fieldnames = self.headers
               writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
               writer.writeheader()
               csvfile.close()
   
           self.num_attributes=0  
       
       row_list=[]
       for i in range(len(self.headers)):
           k=input(f'{self.headers[i]}:')  # 9-21-2019:temporary (optional) interface. Replace with GUI interface.
           row_list.append(k)
       with open(self.filename, mode='a',newline='') as test_file:
           test_writer = csv.writer(test_file,dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
           test_writer.writerow(row_list)
   
       self.data_display()
  
   @classmethod
   def sql_manual_data_entry(cls,row_list,data_type='sql'):
       """Line by line entry of Source--Target--Attribute data in a SQL database table"""
       
       print(Graph_Data.e_class)
#         row_list.append(Graph_Data.e_class)
       
       columns=tuple(Graph_Data.headers)
       values=tuple(row_list)
       the_sql_command=f'INSERT INTO knowledge_1 {columns} VALUES {values}'
       
#         sqlite_server='J:/CTDC_Systems/HCTC_EMR_CSP_database/emr_database.db'
       
       try:
           conn=sqlite3.connect(sqlite_server)
           cur=conn.cursor()
       except:
           print('UNABLE TO ACCESS DATABASE. TRY AGAIN.')
        
       print(the_sql_command)
       cur.execute(the_sql_command)
       conn.commit()
       
       get_data(Graph_Data.type_file)
       
       
   def revise_data_entry(self):
       """Used to revise, update or correct previous entries"""
       pass
   
   def data_display(self,data_type):
       """Display the data following each entry"""
       path=self.filename
       df1=pd.read_csv(path)
       print(tabulate(df1, headers='keys', tablefmt='psql')) # 9-21-2019:temporary (optional) display. Replace with GUI display
       display(HTML(df1.to_html())) # 9-21-2019:temporary (optional) display. Replace with GUI display
   
   @staticmethod
   def get_graph_data_plot():
       """Call functions to get the Graphviz display of the data"""
       q=Graph_Data.df.query(f'CLASSIFICATION=="{The_Frame.class_var}"',inplace=False)
       print(f'the class is:{The_Frame.class_var}')
#         q=Graph_Data.df
       print(f'type:{type(q)}')
    #    display(HTML(q.to_html()))
       create_edge_list(q)
#         create_edge_list(Graph_Data.df)
   
   
   def external_data_entry(self):
       """Provide data from external file i.e, csv, dataframe, excel,etc."""
       pass
       
       
       


# %%
class Make_Graph():
    """create an instance of a networkx graph for display and analysis"""
    pass

# %%
class My_Window(Tk):
    
    now=dt.date.today().strftime('%B %d, %Y')
    time_of_day=dt.datetime.today().strftime('%I:%M:%S %p')

    def __init__(self,parent,*args,**kargs):
        Tk.__init__(self,parent,*args,**kargs)
        self.parent=parent
        self.initialize()
        
        self.banner=Label(self,text=f'KNOWLEDGE CAPTURE',fg='white',bg='blue',font='Ariel 30 bold')
        self.banner.grid(row=0,column=0)
        self.date_banner=Label(self,text=f'{My_Window.now}',fg='white',bg='blue',font='Ariel 20 bold')
        self.date_banner.grid(row=1,column=0)
        
        self.menubar=Menu(self)
        self.menubar.add_command(label="Exit",font='ariel',command=self.bye_bye)
        self.config(menu=self.menubar)
        
    def bye_bye(self):
        """Close the UI Window on menu Exit"""
        self.destroy()
        
    def initialize(self):
        self.title('KNOWLEDGE CAPTURE')
        self['borderwidth']=4
        self['bg']='blue'


# %%
class The_Frame(Frame):
    
    drop_down_list=None
    class_var='TBD'
    classification_list=[]
    
    the_sql_command='SELECT * FROM knowledge_1;'
    
    
    def __init__ (self,the_window,*args,**kwargs):
        """Instance of the frame"""
        Frame.__init__(self,the_window,*args,**kwargs)
    
        self.frame=Frame(self)
        self.the_window=the_window
        self['background']='purple'
        self['relief']='raised'
        self['borderwidth']=5
        self.grid(row=1,column=0)
        banner_text='Nodes and Attributes'
        self.frame_banner=Label(self,text=banner_text,fg='yellow',bg='red',font='Ariel 15 bold')
        self.frame_banner.grid(row=0,column=0,columnspan=5,pady=15)
        
        self.combo_drop_downs()
        self.submit_button()
        self.display_graph_button()
        self.display_table()
    
    @staticmethod
    def get_drop_down_lists():
        """Obtain the distinct drop down list for SOURCE, TARGET,DESCR and CLASSIFICATION from the database."""
        
        conn=sqlite3.connect(sqlite_server)
        cur=conn.cursor()
        
        headers=['SOURCE','TARGET','DESCR','CLASSIFICATION']
        d1=d2=d3=d4=None
        The_Frame.drop_down_list=[d1,d2,d3,d4]
        for i,k in enumerate (headers):
            if (The_Frame.class_var=='TBD'):
                the_sql_command=f'select DISTINCT {k} from knowledge_1 ORDER by {k} ASC;'
            else:
                the_sql_command=f'select DISTINCT {k} from knowledge_1 WHERE CLASSIFICATION="{The_Frame.class_var}"  ORDER by {k} ASC;'
            print(the_sql_command)
            df=pd.read_sql_query(sql=the_sql_command,con=conn, index_col=None)
            The_Frame.drop_down_list[i]=list(df[k])
            if (k=='CLASSIFICATION' and bool(The_Frame.classification_list)==False):
                The_Frame.classification_list=list(df[k])
        return The_Frame.drop_down_list

    def combo_drop_downs(self):
        """Create combo boxes"""
        The_Frame.drop_down_list=The_Frame.get_drop_down_lists()
        
        self.combo_win=Frame(master=self)
        self.source_label=Label(self.combo_win,text=f'SOURCE',fg='white',bg='red',font='Ariel 10 bold')
        self.source_label.pack()
        
        self.source_var=StringVar()
        self.source_combo=ttk.Combobox(self.combo_win,font='Ariel 12 bold',width=30,
                                    background='red',textvariable=self.source_var,
                                       values=The_Frame.drop_down_list[0]+The_Frame.drop_down_list[1],
                                       postcommand=self.updateComboDropDowns)
        self.source_combo.pack()
        
        self.target_label=Label(self.combo_win,text=f'TARGET',fg='white',bg='red',font='Ariel 10 bold')
        self.target_label.pack()
        self.target_var=StringVar()
        self.target_combo=ttk.Combobox(self.combo_win,font='Ariel 12 bold',width=30,
                                    background='blue',textvariable=self.target_var,values=The_Frame.drop_down_list[1],
                                       postcommand=self.updateComboDropDowns)
        self.target_combo.pack()
        
        self.descr_label=Label(self.combo_win,text=f'DESCR',fg='white',bg='red',font='Ariel 10 bold')
        self.descr_label.pack()
        self.descr_var=StringVar()
        self.descr_combo=ttk.Combobox(self.combo_win,font='Ariel 12 bold',width=30,
                                    background='red',textvariable=self.descr_var,values=The_Frame.drop_down_list[2])
        self.descr_combo.pack()
        
        
        self.class_label=Label(self.combo_win,text=f'CLASS',fg='white',bg='red',font='Ariel 10 bold')
        self.class_label.pack()
        self.class_var=StringVar()
        self.class_combo=ttk.Combobox(self.combo_win,font='Ariel 12 bold',width=30,
                                    background='red',textvariable=self.class_var,values=The_Frame.drop_down_list[3])
        
        self.class_combo.pack()
        self.class_combo.bind("<<ComboboxSelected>>", self.refresh_per_class)
        
        self.combo_win.grid(row=1,column=0)
        
    def updateComboDropDowns(self):
        The_Frame.drop_down_list=The_Frame.get_drop_down_lists()
        self.source_combo['values']=self.bfs_node_combo['values']=list(set(The_Frame.drop_down_list[0]+The_Frame.drop_down_list[1]))
        self.target_combo['values']=list(set(The_Frame.drop_down_list[0]+The_Frame.drop_down_list[1]))
        self.descr_combo['values']=The_Frame.drop_down_list[2]
        self.class_combo['values']=The_Frame.classification_list
        self.bfs_node_var.set('')
        
    def refresh_per_class(self,event):
        The_Frame.the_sql_command=f'SELECT * FROM knowledge_1 WHERE CLASSIFICATION="{self.class_var.get()}";'
        print(The_Frame.the_sql_command)
        self.class_node_var.set(self.class_var.get())
        get_data()
        
        The_Frame.class_var=self.class_var.get()
        self.refresh_display()
        self.updateComboDropDowns()
        
        
    
    def refresh_display(self):
        """Clear and refresh comboboxes and treeview following an update"""
        self.my_tree.destroy()
        self.display_table()
        
    
    def sta_values(self):
        """get the source-target-attribute values from the comboboxes"""
        sta_list=['s','t','a','b']
        sta_list[0]=self.source_var.get()
        sta_list[1]=self.target_var.get()
        sta_list[2]=self.descr_var.get()
        sta_list[3]=self.class_var.get()
        print(f'stat values:{sta_list}')
        
        Graph_Data.sql_manual_data_entry(sta_list)
        
#         Graph_Data.get_drop_down_lists()
        The_Frame.class_var=self.class_var.get()
        self.updateComboDropDowns()
        self.refresh_display()
     
    def submit_button(self):
        """Press button to commit upload to knowledge_1 table"""
        self.the_button=Button(master=self,text='Commit',bg='black',fg='white',relief='raised',command=self.sta_values)
        self.the_button.grid(row=2,column=0,sticky=W)
    
    
    def display_graph_button(self):
        """Press button for Graphviz display of the data"""
        
        drop_down_list=The_Frame.get_drop_down_lists()
        self.graph_button_win=Frame(master=self)
        self.bfs_node_label=Label(self.graph_button_win,text=f'BFS Start Node',fg='yellow',bg='red',font='Ariel 10 bold')
        self.bfs_node_label.pack()
        
        self.bfs_node_var=StringVar()
        self.bfs_node_combo=ttk.Combobox(self.graph_button_win,font='Ariel 12 bold',width=20,
                                    background='red',textvariable=self.bfs_node_var,
                                         values=The_Frame.drop_down_list[0])
        
        self.bfs_node_combo.pack()
        
        self.class_node_label=Label(self.graph_button_win,text=f'Class Start Node',fg='yellow',bg='red',font='Ariel 10 bold')
        self.class_node_label.pack()
        
        self.class_node_var=StringVar()
        self.class_node_combo=ttk.Combobox(self.graph_button_win,font='Ariel 12 bold',width=20,
                                    background='red',textvariable=self.class_node_var,
                                         values=The_Frame.drop_down_list[3])
        
        
        self.class_node_combo.pack()
        
        
#         self.the_button=Button(master=self.graph_button_win,text='Graph',bg='black',fg='white',relief='raised',command=Graph_Data.get_graph_data_plot)
        self.the_button=Button(master=self.graph_button_win,text='Graph',bg='black',fg='white',relief='raised',
                               command=self.get_the_class_var)
        self.the_button.pack()
        
        self.graph_button_win.grid(row=1,column=1,padx=20,sticky=None)
    
    
    def get_the_class_var(self):
#         The_Frame.class_var=self.class_node_var.get()
#         print(f'the var is !!:{self.class_node_var.get()}')
        Graph_Data.get_graph_data_plot()
    
    def display_table(self):
        """Display knowledge_1 table data"""
        table_display_frame=Frame(master=self)
        
        head_cols=tuple(Graph_Data.df.columns.tolist())
        the_index=Graph_Data.df.index.tolist()
        
        self.my_tree=ttk.Treeview(table_display_frame, height=10,columns=head_cols)
        for col_num,i in enumerate(head_cols,0):
            self.my_tree.heading(str(col_num), text=i,anchor='center')
        
        for j,k in enumerate (the_index,0):
            self.my_tree.insert('',str(j),'index'+str(j),text=str(the_index[j]))

            for m,n in enumerate(head_cols,0):
                self.my_tree.set(item='index'+str(j),column=n,value=Graph_Data.df[n].iloc[j])

        self.my_tree.grid(row=0,column=0,sticky=W)
        yscrollbar = ttk.Scrollbar(table_display_frame, orient='vertical', command=self.my_tree.yview)
        yscrollbar.grid(row=0,column=1,sticky='ns')
        
        self.my_tree.configure(yscrollcommand = yscrollbar.set, selectmode="browse")
        
        
#         self.table_text_box=Text(master=table_display_frame,borderwidth=2,height=20,width=160,font='Ariel 6 bold')
#         the_table=tabulate(Graph_Data.df, headers='keys', tablefmt='github')
#         self.table_text_box.insert(INSERT,the_table)
#         self.table_text_box.pack()
        
        table_display_frame.grid(row=4,column=0,pady=20,sticky=None)
        
    

# # Functions

# %%
def get_data(type_file='sql',filename=None):
    """read the data (csv file) or (sql table) following an update or upon request"""
    
    if (type_file=='csv'):
        df=pd.read_csv(filename)
        display(HTML(df.to_html()))

        answer=input('View the graph?')
        if (answer=='y'):
            create_edge_list(df)
    elif (type_file=='sql'):
        sqlite_server='knowledge.db'
        try:
            conn=sqlite3.connect(sqlite_server)
            cur=conn.cursor()
        except:
            print('UNABLE TO ACCESS DATABASE. TRY AGAIN.')
        
#         the_sql_command='SELECT * FROM knowledge_1;'
        the_sql_command=The_Frame.the_sql_command
        df=pd.read_sql_query(sql=the_sql_command,con=conn,index_col=None)
        print(tabulate(df, headers='keys', tablefmt='psql'))
        
        # display(HTML(df.to_html()))
    
    Graph_Data.df=df

  
# %%
def create_edge_list(df):
    """Create the list of edges from the dataset"""
    e = zip(df['SOURCE'],df['TARGET'])
    e=list(e)
    
    print(f'this is e\n:{e}')
    
    header_list=df.columns.tolist()
    print(header_list)
    
    create_graph(e,header_list,df)


# %%
def create_graph(e,header_list,df):
    """Create an instance of a networkx graph and map the edges to the attributes"""
    global G
    G = nx.DiGraph()
    G.add_edges_from(e) # creating graph from the edge list
    
    # map edges to attributes
    for k in header_list[2:]: 
        for i,m in enumerate(e):
            G[e[i][0]][e[i][1]][k]=df[k].iloc[i]
            
    BFS()


# %%
def BFS():
    """Conduct Breath First Search (BFS) for the selected node with selected attributes as edge labels"""

#     source_node=input('Enter source node: ')
    source_node=the_gui.bfs_node_var.get()
    if (source_node==""):
        source_node=list(G.edges)[0][0]
    
    k='DESCR'
    
    reverse=False  # False
    
    bfs_path=list(nx.bfs_tree(G, source=source_node, reverse=reverse, depth_limit=None))
    print(f'The BFS Path: {bfs_path}')

    H=G.subgraph(bfs_path)
    #     list(H)
    edge_label = nx.get_edge_attributes(H, k)
    
    print(f'Edge Label Values: {edge_label.values()}')

    x=edge_label.keys()
    print(f'Edge Label Keys: {x}')
    
    print(f'bfs path[0]: {bfs_path[0]}')
#     return edge_label,bfs_path[0]

    
        
    make_graph(edge_label,source_node)
    


# %%
def make_graph(edge_labels,selected_node,*args):
    """Create a Grapviz plot of the data"""
    
    print(edge_labels)

    graph_set={'rankdir':'TB',
              'landscape':'False',
              'size':'20,16',
              'splines':'polyline'}

    node_set={'color':'blue',
             'shape':'ellipse',
             'style':'filled',
              'fillcolor':'None'}

    edge_set={'headlabel':None,
             'taillabel':None,
             'arrowsize':'1',
             'label':None,
             'labelfontsize':'6',
             'labeldistance':'2.0',
             'labelangle':'45',
             'headport':'c',
             'fontsize':'8',
             'fontcolor':'red'}
    
    
    the_format='pdf' #'png'
    
    g = Digraph(name='learn_1', comment='What goes here', filename=None, directory=None, format=the_format,
                engine=None, encoding='utf-8', graph_attr=graph_set, 
                node_attr=node_set, edge_attr=edge_set, body=None, strict=False)
    
    
    # Extracting the edge values for labeling the graph edges
    z=list(edge_labels)
    for i in range(len(z)):
        g.edge(z[i][0],z[i][1],label=str(edge_labels.get((z[i][0],z[i][1]))))
    

    g.node(z[0][0], shape='box') #for a BFS, z[0][0] is the first (start) node of the flow
#     g.node(z[i][1], shape='Msquare')  #for a BFS, z[len of the edge list][1] is the last (stop) node of the flow
    
    now=dt.datetime.now()
    tag=now.strftime('%Y%m%d%H%M%S')
    
    the_path=classification_folder(The_Frame.class_var)
    
    tree_name=f'{selected_node}-{tag}'
#     the_path="knowledge_data/"
    print(the_path+tree_name)
#     g.view(the_path+tree_name)
    g.render(the_path+tree_name,view=True)


# %%
def classification_folder(classification_var):
    
    subFolder=classification_var

    dir_chk=os.path.isdir(f'knowledge_data/{subFolder}')
    print(dir_chk)


    print(f'knowledge_data/{subFolder}')


    if (dir_chk==False):
        os.mkdir(f'knowledge_data/{subFolder}/')
#         path=f'knowledge_data/{subFolder}/'
        return path
    else:
        print(f'{subFolder} already exist')
    
    path=f'knowledge_data/{subFolder}/'
    
    return path
        

# # Main

# %%
root=My_Window(None)


# %%
file_type='sql'
e_class='Personnel'


# %%
j=Graph_Data(file_type,e_class)


# %%
the_gui=The_Frame(root)


# %%
mainloop()


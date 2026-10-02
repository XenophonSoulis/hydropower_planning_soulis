#PROBLEM AT 233

import numpy as np
import math
import time
import json
import openpyxl
import os
import dijkstar
import heapq

#TIME MEASUREMENT

start=time.time()

#END TIME MEASUREMENT
address=r'C:\Works\paper_hydropower_XKS\1temp-hydropower'
def logprint(*mess,sep=' ',end='\n'):
    print(*mess)
    try:
        with open(f'{address}\\logging.txt','a') as file:
            file.write(sep.join(map(str,mess)))
            file.write(end)
    except Exception:
        pass
with open(f'{address}\\logging.txt','w') as file:
    pass

#INPUTS

def reset_input_file():
    '''Resets the input 'config.txt' file to default values.
Useful if the file is missing or corrupted.'''
    with open(f'{address}\\config.txt','w') as config:
        config.write('density_gravity:9.8\n')
        config.write('cell_length:5\n')
        config.write('open_price:1\n')
        config.write('closed_price:2\n')
        config.write('wanted_cases:10000\n')
        config.write('check_factor:2\n')
        config.write('minimum_power:10\n')
        config.write('maximum_upstream_downstream_distance:-1\n') #in metres, -1 to turn off
        config.write('losses:0\n') #0-100, percentage loss per metre of open
        config.write('use_open_price_raster:1\n')
        config.write('use_closed_price_raster:0\n')
        config.write('use_no_pass_raster:1\n')
        config.write('reach_raster:stream_reach4\n')
        config.write('flow_direction_raster:Flow_Direction\n')
        config.write('dem_raster:Fill_DEM\n')
        config.write('flow_accumulation_raster:Flow_accumulation\n')
        config.write('print_results_raster:steam_reach4_results\n')
        config.write('flowrate_raster:flowrate\n')
        config.write('open_price_raster:cost_fin\n')
        config.write('closed_price_raster:closed_cost\n')
        config.write('ban_raster:no_pass\n')
        config.write('END\n\n')
        config.write('"""\n')
        config.write('    If use_open_price_raster is set to 0, the open_price_raster setting is irrelevant\n')
        config.write('    If use_open_price_raster is set to 1, the open_price setting is irrelevant\n')
        config.write('    If use_closed_price_raster is set to 0, the closed_price_raster setting is irrelevant\n')
        config.write('    If use_closed_price_raster is set to 1, the closed_price setting is still used in Step 6 (estimation of penstock price)\n')
        config.write('    Set closed_price equal to -1 in order to use the average of closed_price_raster as closed_price\n')
        config.write('    If use_no_pass_raster is set to 0, the ban_raster setting is irrelevant\n')
        config.write('    If maximum_upstream_downstream_distance is set to -1, ignore this setting\n')
        config.write('    Losses is the slope of the headrace.\n')
        config.write('"""\n')
def write_input_file(*inputs):
    '''Edits the input 'config.txt file to the provided values,
while keeping the existing values for the rest.
For a friendlier interface, check change_settings.
Accepts up to 15 inputs.'''
    inputs=list(inputs)
    if len(inputs)>17:
        raise IndexError('too many config initializers')
    if len(inputs)<17:
        inputs.extend([None]*(17-len(inputs)))
    if None in inputs:
        old_config=read_input()
        for i in range(17):
            if inputs[i]==None:
                inputs[i]=old_config[i]
    with open(f'{address}\\config.txt','w') as config:
        config.write(f'density_gravity:{inputs[0]}\n')
        config.write(f'cell_length:{inputs[1]}\n')
        config.write(f'open_price:{inputs[2]}\n')
        config.write(f'closed_price:{inputs[3]}\n')
        config.write(f'wanted_cases:{inputs[4]}\n')
        config.write(f'check_factor:{inputs[5]}\n')
        config.write(f'minimum_power:{inputs[6]}\n')
        config.write(f'maximum_upstream_downstream_distance:{int(inputs[7])}\n')
        config.write(f'losses:{inputs[8]}\n')
        config.write(f'use_open_price_raster:{int(inputs[9])}\n')
        config.write(f'use_closed_price_raster:{int(inputs[10])}\n')
        config.write(f'use_no_pass_raster:{int(inputs[11])}\n')
        config.write(f'reach_raster:{inputs[12]}\n')
        config.write(f'flow_direction_raster:{inputs[13]}\n')
        config.write(f'dem_raster:{inputs[14]}\n')
        config.write(f'flow_accumulation_raster:{inputs[15]}\n')
        config.write(f'print_results_raster:{inputs[16]}\n')
        config.write(f'flowrate_raster:{inputs[17]}\n')
        config.write(f'open_price_raster:{inputs[18]}\n')
        config.write(f'closed_price_raster:{inputs[19]}\n')
        config.write(f'ban_raster:{inputs[20]}\n')
        config.write('END\n\n')
        config.write('"""\n')
        config.write('    If use_open_price_raster is set to 0, the open_price_raster setting is irrelevant\n')
        config.write('    If use_open_price_raster is set to 1, the open_price setting is irrelevant\n')
        config.write('    If use_closed_price_raster is set to 0, the closed_price_raster setting is irrelevant\n')
        config.write('    If use_closed_price_raster is set to 1, the closed_price setting is still used in Step 6 (estimation of penstock price)\n')
        config.write('    Set closed_price equal to -1 in order to use the average of closed_price_raster as closed_price\n')
        config.write('    If use_no_pass_raster is set to 0, the ban_raster setting is irrelevant\n')
        config.write('    If maximum_upstream_downstream_distance is set to -1, ignore this setting\n')
        config.write('    Losses is the slope of the headrace.\n')
        config.write('"""\n')

#Uncomment the line below to reset the input file in case it is missing or corrupted:
#reset_input_file()

def read_input():
    '''Reads the input 'config.txt' file'''
    with open(f'{address}\\config.txt') as config:
        logprint(f'The input data are in {address}\\config.txt')
        logprint('~~~~~~~~~~\nINPUT DATA CONTENT\n')
        logprint(config.read())
    with open(f'{address}\\config.txt') as config:
        int_read_config=lambda:int(config.readline()[:-1].split(sep=':')[1])
        float_read_config=lambda:float(config.readline()[:-1].split(sep=':')[1])
        bool_read_config=lambda:bool(int(config.readline()[:-1].split(sep=':')[1]))
        str_read_config=lambda:config.readline()[:-1].split(sep=':')[1]
        return float_read_config(),float_read_config(),float_read_config(),float_read_config(),int_read_config(),int_read_config(),float_read_config(),int_read_config(),float_read_config(),bool_read_config(),bool_read_config(),bool_read_config(),str_read_config(),str_read_config(),str_read_config(),str_read_config(),str_read_config(),str_read_config(),str_read_config(),str_read_config(),str_read_config()

#Only used for reference. These are the values in each element of price_list.
price_list_key=['cost per height','total cost','cost of open duct','cost of closed pipe','upstream point index in stream_pixels_list','downstream point index in stream_pixels_list','contour point in the relevant contour','left/right identifier','x coordinate of upstream point','y coordinate of upstream point','x coordinate of downstream point','y coordinate of downstream point','x coordinate of contour point','y coordinate of contour point','final_price']

class raster_data:
    '''Object designed to hold all raster data for a specific set of rasters.
A raster_data object called iodata is created by default
with values imported from 'config.txt'.
The arguments are the entries of 'config.txt'
in the same order that they are there.'''
    def __init__(self,density_gravity,cell_length,open_price,closed_price,wanted_cases,check_factor,minimum_power,maximum_distance,losses,use_open_price_raster,use_closed_price_raster,use_no_pass_raster,reach_raster,fldir_raster,dem_raster,flacc_raster,results_raster,flowrate_raster,open_price_raster,closed_price_raster,ban_raster):
        self.density_gravity=density_gravity
        self.cell_length=cell_length
        self.open_price=open_price
        self.closed_price=closed_price
        self.wanted_cases=wanted_cases
        self.check_factor=check_factor
        self.minimum_power=minimum_power
        self.maximum_distance=maximum_distance
        self.losses=losses
        self.use_open_price_raster=use_open_price_raster
        self.use_closed_price_raster=use_closed_price_raster
        self.use_no_pass_raster=use_no_pass_raster
        self.run_parts=[False]*7
        self.reach_layer = QgsProject.instance().mapLayersByName(reach_raster)[0]
        self.flowdir_layer = QgsProject.instance().mapLayersByName(fldir_raster)[0]
        self.FlDEM_layer = QgsProject.instance().mapLayersByName(dem_raster)[0]
        self.FlowAcc_layer = QgsProject.instance().mapLayersByName(flacc_raster)[0]
        self.results_layer = QgsProject.instance().mapLayersByName(results_raster)[0]
        self.flowrate_layer = QgsProject.instance().mapLayersByName(flowrate_raster)[0]
        if self.use_open_price_raster:
            self.open_price_layer = QgsProject.instance().mapLayersByName(open_price_raster)[0]
        if self.use_closed_price_raster:
            self.closed_price_layer = QgsProject.instance().mapLayersByName(closed_price_raster)[0]
        if self.use_no_pass_raster:
            self.ban_layer = QgsProject.instance().mapLayersByName(ban_raster)[0]
        self.provider_reach = self.reach_layer.dataProvider()
        self.provider_flowdir = self.flowdir_layer.dataProvider()
        self.provider_FlDEM = self.FlDEM_layer.dataProvider()
        self.provider_FlowAcc = self.FlowAcc_layer.dataProvider()
        self.provider_results = self.results_layer.dataProvider()
        self.provider_flowrate = self.flowrate_layer.dataProvider()
        if self.use_open_price_raster:
            self.provider_open_price = self.open_price_layer.dataProvider()
        if self.use_closed_price_raster:
            self.provider_closed_price = self.closed_price_layer.dataProvider()
        if self.use_no_pass_raster:
            self.provider_ban = self.ban_layer.dataProvider()
        self.extent = self.provider_reach.extent()
        self.raster_edges()
        self.rows = self.reach_layer.height()
        self.cols = self.reach_layer.width()
        self.reach_block = self.provider_reach.block(1, self.extent, self.cols, self.rows)
        self.flowdir_block = self.provider_flowdir.block(1, self.extent, self.cols, self.rows)
        self.FlDEM_block = self.provider_FlDEM.block(1, self.extent, self.cols, self.rows)
        self.FlowAcc_block = self.provider_FlowAcc.block(1, self.extent, self.cols, self.rows)
        self.results_block = self.provider_results.block(1, self.extent, self.cols, self.rows)
        self.flowrate_block = self.provider_flowrate.block(1, self.extent, self.cols, self.rows)
        if self.use_open_price_raster:
            self.open_price_block = self.provider_open_price.block(1, self.extent, self.cols, self.rows)
        if self.use_closed_price_raster:
            self.closed_price_block = self.provider_closed_price.block(1, self.extent, self.cols, self.rows)
        if self.use_no_pass_raster:
            self.ban_block = self.provider_ban.block(1, self.extent, self.cols, self.rows)
        self.reach_array,self.flowdir_array,self.FlDEM_array,self.FlowAcc_array,self.flowrate_array,self.open_price_array,self.closed_price_array,self.ban_array,self.log_flow_direction,self.ban_set,self.min_iso,self.to_check=self.block_array_maker()
        if self.closed_price==-1:
            self.closed_price=np.mean(self.closed_price_array[self.closed_price_array>-999999])
        self.make_graph()
        self.stream_pixels_list,self.stream_list=self.make_stream_pixels_list()
        self.non_basin=set()
        self.problems=self.problematic_points()
        self.last_pixel=self.stream_pixels_list[-1]
        self.stream_length=len(self.stream_pixels_list)
        self.list_iso=self.make_list_iso()
        self.stream_set=set(self.stream_list)
        self.leftisos={}
        self.rightisos={}
        self.left_total_len_list={}
        self.left_total_cost_list={}
        self.right_total_len_list={}
        self.right_total_cost_list={}
        self.left_all_costs_open_list={}
        self.right_all_costs_open_list={}
        self.left_max=0
        self.right_max=0
        self.distances=np.array(0,dtype=np.float16)
        self.price_list=[]
    def block_array_maker(self):
        '''Creates arrays for all the data blocks from the raster,
as well as some other helper arrays.'''
        reach_array=np.zeros((self.rows,self.cols))
        flowdir_array=np.zeros((self.rows,self.cols))
        FlDEM_array=np.zeros((self.rows,self.cols))
        FlowAcc_array=np.zeros((self.rows,self.cols))
        flowrate_array=np.zeros((self.rows,self.cols))
        open_price_array=np.zeros((self.rows,self.cols))
        closed_price_array=np.zeros((self.rows,self.cols))
        ban_array=np.zeros((self.rows,self.cols))
        log_flow_direction=-np.ones((self.rows,self.cols))
        ban_set=set()
        min_iso=-np.ones((self.rows,self.cols))
        to_check=np.zeros((self.rows,self.cols))
        for i in range(self.rows):
            for j in range(self.cols):
                f=self.flowdir_block.value(i,j)
                g=self.FlDEM_block.value(i,j)
                if self.use_no_pass_raster:
                    h=self.ban_block.value(i,j)
                if self.use_closed_price_raster:
                    k=self.closed_price_block.value(i,j)
                reach_array[i,j]=self.reach_block.value(i,j)
                flowdir_array[i,j]=f
                FlDEM_array[i,j]=g
                FlowAcc_array[i,j]=self.FlowAcc_block.value(i,j)
                flowrate_array[i,j]=self.flowrate_block.value(i,j)
                if self.use_open_price_raster:
                    open_price_array[i,j]=self.open_price_block.value(i,j)
                else:
                    open_price_array[i,j]=self.open_price
                if self.use_closed_price_raster:
                    closed_price_array[i,j]=k
                else:
                    closed_price_array[i,j]=self.closed_price
                if self.use_no_pass_raster:
                    ban_array[i,j]=h
                    if not h:
                        ban_set.add((i,j))
                else:
                    ban_array[i,j]=1
                h=(g>=-999999)
                if h:
                    log_flow_direction[i,j]=custom_log2[f]
                min_iso[i,j]=-2+h
                to_check[i,j]=h
        return reach_array,flowdir_array,FlDEM_array,FlowAcc_array,flowrate_array,open_price_array,closed_price_array,ban_array,log_flow_direction,ban_set,min_iso,to_check
    def make_stream_pixels_list(self):
        '''Makes stream_pixels_list, a list containing the
flowacc, x-coord, y-coord, flowdir and dem of each point of the stream,
sorted based on order of the stream.'''
        stream_pixels_list = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.reach_array[i,j] == 1:
                    stream_pixel_data = (self.FlowAcc_array[i,j], i, j, self.flowdir_array[i,j], self.FlDEM_array[i,j])
                    stream_pixels_list.append(stream_pixel_data)
        stream_pixels_list.sort()
        stream_list=list(map(lambda x:x[1:3],stream_pixels_list))
        return stream_pixels_list,stream_list
    def make_list_iso(self):
        '''Initializes list_iso, a list eventually containing
all points at the same height as each point of the stream.'''
        list_iso=[]
        for i in range(self.stream_length+1):
            list_iso.append(set())
        return list_iso
    def save_left_max(self,lm):
        self.left_max=lm
    def save_right_max(self,rm):
        self.right_max=rm
    def mark_part_as_run(self,part):
        '''Marks a specific step as already completed for that raster_data object.'''
        self.run_parts[part]=True
    def make_distances(self):
        '''Makes the distances list, a 3d tuple that saves the result of the
Pythagorean theorem for any triple of dx, dy and dz.
This allows for much faster access to that information
on step 6, when speed matters the most.'''
        min_row=99999
        min_col=99999
        min_hei=round(self.stream_pixels_list[-1][-1])
        max_row=-99999
        max_col=-99999
        max_hei=round(self.stream_pixels_list[0][-1])
        for i in range(self.rows):
            for j in range(self.cols):
                if self.min_iso[i,j]>-1:
                    if i<min_row:
                        min_row=i
                    if i>max_row:
                        max_row=i
                    if j<min_col:
                        min_col=j
                    if j>max_col:
                        max_col=j
        distances=np.ndarray((max_row-min_row+1,max_col-min_col+1,max_hei-min_hei+1),np.float16)
        clm2=self.cell_length**(-2)
        for i in range(max_row-min_row+1):
            for j in range(max_col-min_col+1):
                for k in range(max_hei-min_hei+1):
                    distances[i,j,k]=math.sqrt(i**2+j**2+clm2*k**2)
        self.distances=distances
    def sort_price_list(self):
        '''Sorts the price_list based on a straight closed pipe.'''
        self.price_list.sort()
    def short_price_list(self):
        '''Shortens the price_list to avoid eating up too much RAM.'''
        self.price_list=self.price_list[:self.check_factor*self.wanted_cases]
    def partition_price_list(self):
        self.price_list=heapq.nsmallest(self.check_factor*self.wanted_cases, self.price_list)
    def sort_accurate_price_list(self):
        '''Sorts the first self.check_factor*self.wanted_cases elements of the price_list
into a new accurate_price_list based on the traced closed pipe.'''
        no=min(len(self.price_list),self.check_factor*self.wanted_cases)
        self.accurate_price_list=[]
        if len(self.price_list)>0 and self.price_list[0][-1]>0:
            self.accurate_price_list.append(self.price_list[0])
        i=0
        while len(self.accurate_price_list)<self.check_factor*self.wanted_cases and i<len(self.price_list)-1:
            i+=1
            if self.price_list[i][-1]>0 and self.price_list[i][:7]!=self.price_list[i-1][:7]:
                self.accurate_price_list.append(self.price_list[i])
            else:
                continue
        self.accurate_price_list.sort(key=lambda x:x[-1])
        if len(self.accurate_price_list)>=self.wanted_cases:
            if self.accurate_price_list[self.wanted_cases-1][-1]>self.price_list[-1][0]:
                for i in range(self.wanted_cases):
                    if self.accurate_price_list[i][-1]>self.price_list[-1][0]:
                        break
                logprint(f'There may be ideal solutions beyond the {i} solution.Consider running the algorithm with a higher check_factor (currently {self.check_factor})')
        else:
            logprint(f'There are only {len(self.accurate_price_list)} accepted solutions with wanted_cases = {self.wanted_cases} and check_factor = {self.check_factor}')
    def list_iso_to_list(self):
        '''Unused'''
        ret=[]
        for i in self.list_iso:
            ret.append(list(i))
        return ret
    def update_price_list(self,quality_number,path_list,new_cost,new_val):
        '''Adds details of the traced closed pipe to a price_list entry.'''
        self.price_list[quality_number]=(*self.price_list[quality_number][:-3],tuple(path_list),new_cost,new_val)
    def raster_edges(self):
        '''Saves the edges of the rasters in an easier form.
M for Maximum, m for minimum.'''
        self.xm=self.extent.xMinimum()
        self.xM=self.extent.xMaximum()
        self.ym=self.extent.yMinimum()
        self.yM=self.extent.yMaximum()
    def coords_from_pixel(self,i,j):
        '''Returns the coordinates of a pixel (x, y, z)'''
        return (self.xm+i*self.cell_length,self.yM+j*self.cell_length,self.FlDEM_array[i,j])
    def problematic_points(self):
        stretch=False
        val=0
        start=0
        problems={0}
        for i in range(len(self.stream_pixels_list[:-1])):
            if self.stream_pixels_list[i][-1]<=self.stream_pixels_list[i+1][-1]:
                if stretch==False:
                    stretch=True
                    start=i
                    val=self.stream_pixels_list[i][-1]
                else:
                    problems.add(i)
            else:
                if stretch==True:
                    stretch=False
                    problems.add(i)
        return problems
    def reduce_list_iso(self):
        del self.list_iso[-1]
    def make_graph(self):
        start=time.time()
        self.graph=dijkstar.Graph()
        for i in range(self.rows):
            for j in range(self.cols):
                c=(i,j)
                if self.FlDEM_array[c]>-999999 and c not in self.ban_set:
                    self.graph.add_node(c)
                    for k in adj_cells(i,j,self.rows,self.cols):
                        if self.FlDEM_array[k]>-999999 and c not in self.ban_set:
                            d=eucl_dist(self.cell_length*abs(c[0]-k[0]),self.cell_length*abs(c[1]-k[1]),abs(self.FlDEM_array[c]-self.FlDEM_array[k]))/2
                            self.graph.add_edge(c,k,d*(self.closed_price_array[c]+self.closed_price_array[k]))
        end=time.time()
        logprint('Time to complete transformation of raster to graph: ',end-start)
    def make_basin(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.min_iso[i,j]==-2:
                    self.non_basin.add((i,j))

sqrt2=math.sqrt(2)
custom_log2={1:0,2:1,4:2,8:3,16:4,32:5,64:6,128:7}
def right(x,step=1):
    '''Finds the direction 'step' steps to the right of direction x
For more on directions, type help_direction().'''
    return (x+step)%8
def left(x,step=1):
    '''Finds the direction 'step' steps to the left of direction x
For more on directions, type help_direction().'''
    return (x-step)%8
def isright(x,y):
    '''returns True if x is to the right of y
For more on directions, type help_direction().'''
    return (x-y)%8 in {1,2,3}
def isleft(x,y):
    '''returns True if x is to the left of y
For more on directions, type help_direction().'''
    return (y-x)%8 in {1,2,3}

def adj_cells(cell_row,cell_col,arr_row,arr_col):
    '''Returns the adjacent cells (incl. diagonals) of a given cell.
cell_row and cell_col are the coordinates of the cell in question.
arr_row and arr_col as given by raster_data.rows and raster_data.cols'''
    z=[]
    for i in range(-1,2):
        if cell_row+i>=0 and cell_row+i<arr_row:
            for j in range(-1,2):
                if cell_col+j>=0 and cell_col+j<arr_col and ((i,j) != (0,0)):
                    z.append((cell_row+i,cell_col+j))
    return z
def orth_cells(cell_row,cell_col,arr_row,arr_col):
    '''Returns the adjacent cells (excl. diagonals) of a given cell.
cell_row and cell_col are the coordinates of the cell in question.
arr_row and arr_col as given by raster_data.rows and raster_data.cols'''
    z=[]
    for i in ((cell_row-1,cell_col),(cell_row+1,cell_col),(cell_row,cell_col-1),(cell_row,cell_col+1)):
        if i[0]>=0 and i[0]<arr_row and i[1]>=0 and i[1]<arr_col:
            z.append(i)
    return z

def eucl_dist(dx,dy,dz):
    return math.sqrt(dx**2+dy**2+dz**2)
def neighbor_dist(p,q):
    dx=abs(p[0]-q[0])
    dy=abs(p[1]-q[1])
    if dx>1 or dy>1:
        raise ValueError(f'non neighboring points {p} and {q} in neighbor_dist')
    if dx+dy==2:
        return sqrt2
    else:
        return 1

def make_straight_line(x1,y1,x2,y2):
    '''Helper function to calculate the distance between two points.
    (x1,y1) and (x2,y2) are the points.'''
    xm=min(x1,x2)
    xM=max(x1,x2)
    ym=min(y1,y2)
    yM=max(y1,y2)
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0:
        return {(x1,y) for y in range(ym,yM+1)}
    elif dy == 0:
        return {(x,y1) for x in range(xm,xM+1)}
    m = dy/dx
    ret=set()
    if abs(m)<1:
        for x in range(xm,xM):
            y = int(m * (x - x1) + y1)
            ret.add((x,y))
    else:
        m=1/m
        for y in range(ym,yM):
            x = int(m * (y - y1) + x1)
            ret.add((x,y))
    return ret

def help_direction():
    '''Prints an explanation of the direction system used in the algorithm'''
    to_print='''Directions in this algorithm are taken as the
base-2 logarithm of flow direction. They work in modulo-8 arithmetic.
Add 1 to move one spot ccw, subtract one to move one spot cw.
The values of the directions are 0 (to the east) to 7 (to the NW).
As a shape where C is the central point itself:
    5 6 7
    4 C 0
    3 2 1'''
    print(to_print)

#These three tuples save:
# the necessary row change to go to the direction of the index
# the necessary column change to go to the direction of the index
# the direction defined by a (dx, dy) pair.
# For more on directions, check help_direction().

modif_rows=(0,1,1,1,0,-1,-1,-1)
modif_cols=(1,1,0,-1,-1,-1,0,1)
modif_array=np.array([[5,6,7],[4,8,0],[3,2,1]])
def apply_movement(x,fldir):
    '''Returns the cell that is in fldir direction of cell x.
For more on directions, type help_direction().'''
    return (x[0]+modif_rows[fldir],x[1]+modif_cols[fldir])
def invert_apply_movement(x,y):
    '''Returns the direction one needs  to move to go from cell x to cell y.
For more on directions, type help_direction().'''
    z=(y[0]-x[0]+1,y[1]-x[1]+1)
    return modif_array[z]

def remake_iodata():
    '''Remakes the iodata raster_data based on the current form of
the input 'cnofig.txt' file.'''
    global iodata
    iodata=raster_data(*read_input())

#Arguments of the __init__ of raster_data as well as contents of config.txt
config_arguments=('density_gravity','cell_length','closed_price','open_price','wanted_cases','minimum_power','maximum_upstream_downstream_distance','losses','use_open_price_raster','use_no_pass_raster','reach_raster','flow_direction_raster','dem_raster','flow_accumulation_raster','print_results_raster','flowrate_raster','open_price_raster','ban_raster')

def change_settings(**kwargs):
    '''Changes specific settings of the input 'config.txt' file.
Designed for manual use (as opposed towrite_input_file).'''
    remake_inp=[None]*20
    for i in kwargs:
        if i not in arguments:
            raise KeyError(f'nonexistent argument {i}')
        remake_inp[config_arguments.index(i)]=kwargs[i]
    write_input_file(*remake_inp)
    remake_iodata()

#A default raster_data object created using the parameters of config.txt
iodata=raster_data(*read_input())

def minimum_neighbor_height(j,bottom_height,data=iodata):
    adj_alts=list(map(lambda x:data.FlDEM_array[x], adj_cells(*j,data.rows,data.cols)))
    adj_alts=[i for i in adj_alts if i >= bottom_height]
    return min(adj_alts)

def valid_coords(coords,data=iodata):
    return coords[0]>=0 and coords[1]>=0 and coords[0]<data.rows and coords[1]<data.cols

#TIME MEASUREMENT

end = time.time()
logprint('Time to complete data aquisition (step 0):',end-start)
start = time.time()

#END TIME MEASUREMENT

def categorize_points(data=iodata):
    '''For every pixel on the basin, the data.stream_pixels_list index of the
lowest point of the stream that's higher than the point in question is placed
on data.miniso. The results of this process are seen in make_map_4().
The process starts from the lowest point of the stream. Afterwards, it moves
to neighboring points iteratively. Whenever a point that's higher than the
highest point of the stream is processed, the algorithm stops and ignores
subsequent neighboring points.'''
    if data.run_parts[0]:
        raise RuntimeError('The points have already been categorized for these data.')
    data.mark_part_as_run(0)
    start=time.time()
    temp_check = ((data.last_pixel[1],data.last_pixel[2]),)
    data.min_iso[data.last_pixel[1],data.last_pixel[2]]=len(data.stream_pixels_list)
    data.to_check[data.last_pixel[1],data.last_pixel[2]]=False
    bottom_height=data.stream_pixels_list[-1][4]
    top_height=data.stream_pixels_list[0][4]
    while temp_check:
        new_temp_check=[] #pixels to check in the next iteration
        for i in temp_check:
            for j in adj_cells(i[0],i[1],data.rows,data.cols):
                if data.to_check[j[0],j[1]]:
                    k=0 #################################################What if k=-1?
                    if data.FlDEM_array[j[0],j[1]]<=bottom_height:
                        k=len(data.stream_pixels_list)
                    else:
                        while data.FlDEM_array[j[0],j[1]]<=data.stream_pixels_list[k+1][4]:
                            k+=1
                    if k==0 and minimum_neighbor_height(j,bottom_height,data)>top_height:
                        k=-1
                    data.min_iso[j[0],j[1]]=k
                    if k>-1:
                        new_temp_check.append(j)
                    data.to_check[j[0],j[1]]=False
        temp_check=tuple(new_temp_check)
    end=time.time()
    logprint('Time to categorize the points (step 1):',end-start)

def find_border(data=iodata):
    if data.run_parts[1]:
        raise RuntimeError('The border has already been found for these data.')
    data.mark_part_as_run(1)
    start=time.time()
    for i in range(data.rows):
        for j in range(data.cols):
            if data.min_iso[i,j]>-1:
                y=[]
                for k in orth_cells(i,j,data.rows,data.cols):
                    r=int(data.min_iso[k])
                    if r>-2:
                        y.append(r)
                if y:
                    for p in range(int(data.min_iso[i,j])+1,max(y)+1):
                        data.list_iso[p].add((i,j))
    data.reduce_list_iso()
    for i in range(len(data.list_iso)):
        data.list_iso[i].add(data.stream_pixels_list[i][1:3])
    end=time.time()
    logprint('Time to find the borders (step 2):',end-start)

def draw_contours(data=iodata):
    if data.run_parts[2]:
        raise RuntimeError('The contours have already been drawn for these data.')
    data.mark_part_as_run(2)
    start=time.time()
    data.make_basin()
    for i in range(len(data.list_iso)):
        if i in data.problems:
            continue
        iso_start=tuple(data.stream_pixels_list[i][1:3])
        temp_isos={left:[iso_start],right:[iso_start]}
        cur_pt=iso_start
        cur_fldir=int(data.log_flow_direction[cur_pt])
        previous_points={}
        next_points={}
        temp_list_iso=set(data.list_iso[i])
        if len(temp_list_iso)<=1:
            continue
        for turn,save in zip((left,right),(data.leftisos,data.rightisos)):
            previous_points={k:set() for k in temp_list_iso}
            next_points={k:set() for k in temp_list_iso}
            previous_points[None]=set()
            next_points[None]=set()
            prev_pt=None
            cur_pt=iso_start
            next_pt=None
            dir_to_prev_pt=None
            dir_to_next_pt=None
            for j in range(1,9):
                looked_dir=turn(cur_fldir,j)
                looked_pt=apply_movement(cur_pt,looked_dir)
                if valid_coords(looked_pt,data) and looked_pt in temp_list_iso:
                    #temp_isos[turn].append(looked_pt)
                    next_pt=looked_pt
                    dir_to_next_pt=looked_dir
                    break
            previous_points[cur_pt].add(prev_pt)
            next_points[cur_pt].add(next_pt)
            while next_pt:
                previous_points[cur_pt].add(prev_pt)
                next_points[cur_pt].add(next_pt)
                prev_pt,cur_pt,next_pt=cur_pt,next_pt,None
                dir_to_prev_pt,dir_to_next_pt=(dir_to_next_pt+4)%8,None
                neighboring_stream=data.stream_set&set(adj_cells(cur_pt[0],cur_pt[1],data.rows,data.cols))
                if set(adj_cells(cur_pt[0],cur_pt[1],data.rows,data.cols))&data.non_basin:
                    continue
                if neighboring_stream:
                    lowest_stream_pt=max(neighboring_stream,key=lambda x:data.FlowAcc_array[x])
                    lowest_stream_dir=invert_apply_movement(cur_pt,lowest_stream_pt)
                    for j in range(1,8):
                        looked_dir=turn(lowest_stream_dir,j)
                        looked_pt=apply_movement(cur_pt,looked_dir)
                        if valid_coords(looked_pt,data):
                            if looked_pt in temp_list_iso and looked_pt!=prev_pt:
                                #temp_isos[turn].append(looked_pt)
                                next_pt=looked_pt
                                dir_to_next_pt=looked_dir
                                break
                            if looked_pt in data.stream_set:
                                break
                else:
                    for j in range(1,8):
                        looked_dir=turn(dir_to_prev_pt,j)
                        looked_pt=apply_movement(cur_pt,looked_dir)
                        if valid_coords(looked_pt,data) and looked_pt in temp_list_iso and looked_pt!=prev_pt:
                            #temp_isos[turn].append(looked_pt)
                            next_pt=looked_pt
                            dir_to_next_pt=looked_dir
                            break
                if cur_pt in previous_points[next_pt]:
                    next_pt=None
                    dir_to_next_pt=None
                else:
                    temp_isos[turn].append(cur_pt)
            save[i]=temp_isos[turn]
            if len(temp_isos[turn])<=1:
                data.problems.add(i)
    end=time.time()
    logprint('Time to draw the contours (step 3):',end-start)

def calculate_open_distance(data=iodata):
    if data.run_parts[3]:
        raise RuntimeError('The open distances have already been calculated for these data.')
    data.mark_part_as_run(3)
    start=time.time()
    for i in range(len(data.list_iso)):
        if len(data.list_iso[i])<=1:
            continue
        if i in data.problems:
            continue
        #if not i%10:
        #logprint(f'Starting iteration {i} of the calculate_open_distance step.\nIt took {time.time()-start} seconds.')
        contours={left:data.leftisos[i],right:data.rightisos[i]}
        len_list={left:data.left_total_len_list,right:data.right_total_len_list}
        cost_list={left:data.left_total_cost_list,right:data.right_total_cost_list}
        for side in (left,right):
            ones_len=0
            rt2s_len=0
            ones_cost=0
            rt2s_cost=0
            main_path=[]
            contour=contours[side]
            contour_set=set(contour)
            total_len=[0]*len(contour)
            total_cost=[0]*len(contour)
            contour_dict={x:[] for x in contour}
            done=set()
            for j,pixel in enumerate(contour):
                contour_dict[pixel].append(j)
            j=0
            while j<len(contour):
                old_j=j
                checking=contour[j]
                next_pt=max(set(adj_cells(checking[0],checking[1],data.rows,data.cols))&contour_set,key=lambda x:contour_dict[x][-1])
                j=contour_dict[next_pt][0]
                main_path.append(j)
                if contour[j][0]==checking[0] or contour[j][1]==checking[1]:
                    ones_len+=1
                    ones_cost+=data.open_price_array[contour[j]]
                else:
                    rt2s_len+=1
                    rt2s_cost+=data.open_price_array[contour[j]]
                total_len[j]=data.cell_length*(ones_len+sqrt2*rt2s_len)
                total_cost[j]=data.cell_length*(ones_cost+sqrt2*rt2s_cost)
                done.add(old_j)
                if j<=old_j:
                    break
            breaking=10000
            while len(total_len)>1 and min(total_len[1:])==0 and breaking:
                breaking-=1
                for s in range(len(contour)):
                    if total_len[s]==0:
                        temp_ones_len=0
                        temp_rt2s_len=0
                        temp_ones_cost=0
                        temp_rt2s_cost=0
                        temp_path=[]
                        j=s
                        while total_len[j]==0:
                            old_j=j
                            checking=contour[j]
                            next_pt=max(set(adj_cells(checking[0],checking[1],data.rows,data.cols))&contour_set,key=lambda x:contour_dict[x][-1])
                            j=contour_dict[next_pt][-1]
                            temp_path.append(j)
                            if contour[j][0]==checking[0] or contour[j][1]==checking[1]:
                                temp_ones_len+=1
                                temp_ones_cost+=data.open_price_array[contour[j]]
                            else:
                                temp_rt2s_len+=1
                                temp_rt2s_cost+=data.open_price_array[contour[j]]
                            if j<=old_j:
                                break
                        dist_inc=total_len[j]+data.cell_length*(temp_ones_len+sqrt2*temp_rt2s_len)
                        cost_inc=total_cost[j]+data.cell_length*(temp_ones_cost+sqrt2*temp_rt2s_cost)
                        temp_ones_len=0
                        temp_rt2s_len=0
                        temp_ones_cost=0
                        temp_rt2s_cost=0
                        temp_path=[]
                        j=s
                        while total_len[j]==0 and j>0:
                            old_j=j
                            checking=contour[j]
                            st=set(adj_cells(checking[0],checking[1],data.rows,data.cols))&contour_set
                            next_pt=min(st,key=lambda x:contour_dict[x][0])
                            j=contour_dict[next_pt][0]
                            temp_path.append(j)
                            if contour[j][0]==checking[0] or contour[j][1]==checking[1]:
                                temp_ones_len+=1
                                temp_ones_cost+=data.open_price_array[contour[j]]
                            else:
                                temp_rt2s_len+=1
                                temp_rt2s_cost+=data.open_price_array[contour[j]]
                            if j>=old_j:
                                break
                        dist_dec=total_len[j]+data.cell_length*(temp_ones_len+sqrt2*temp_rt2s_len)
                        cost_dec=total_cost[j]+data.cell_length*(temp_ones_cost+sqrt2*temp_rt2s_cost)
                        total_len[s]=min(dist_inc,dist_dec)
                        total_cost[s]=min(cost_inc,cost_dec)
            len_list[side][i]=total_len
            cost_list[side][i]=total_cost
        #break
    end=time.time()
    logprint('Time to calculate the open distance (step 4):',end-start)

def calculate_open_prices(data=iodata):
    if data.run_parts[4]:
        raise RuntimeError('The open prices have already been calculated for these data.')
    data.mark_part_as_run(4)
    start=time.time()
    left_max=0
    for i in range(len(data.stream_list)):
        if i in data.problems:
            continue
        if len(data.leftisos[i])>left_max:
            left_max=len(data.leftisos[i])
        costs_open=[]
        for j in data.left_total_cost_list[i]:
            costs_open.append(j)
        data.left_all_costs_open_list[i]=tuple(costs_open)
    right_max=0
    for i in range(len(data.stream_list)):
        if i in data.problems:
            continue
        if len(data.rightisos[i])>right_max:
            right_max=len(data.rightisos[i])
        costs_open=[]
        for j in data.right_total_cost_list[i]:
            costs_open.append(j)
        data.right_all_costs_open_list[i]=tuple(costs_open)
    data.save_left_max(left_max)
    data.save_right_max(right_max)
    end=time.time()
    logprint('Time to calculate the open prices (step 5):',end-start)
    start=time.time()
    data.make_distances()
    end=time.time()
    logprint('Time to calculate the distances (step intermediary):',end-start)

def estimate_best_prices(data=iodata):
    cl=data.cell_length
    losses=data.losses
    if data.run_parts[5]:
        raise RuntimeError('The prices have already been estimated for these data.')
    data.mark_part_as_run(5)
    start=time.time()
    distances=data.distances
    open_price=data.open_price
    closed_price=data.closed_price
    ban_set=data.ban_set
    for i in range(len(data.stream_list)):
        if not i%10:
            logprint(f'Finished iteration {i} of the estimate_best_prices step.\nIt took {time.time()-start} seconds.')
            data.partition_price_list()
        on_stream_len=0
        if i in data.problems:
            continue
        high_row=data.stream_list[i][0]
        high_col=data.stream_list[i][1]
        if (high_row,high_col) in ban_set:
            continue
        temp_leftisos=data.leftisos[i]
        temp_rightisos=data.rightisos[i]
        temp_left_all_costs_open_list=data.left_all_costs_open_list[i]
        temp_right_all_costs_open_list=data.right_all_costs_open_list[i]
        temp_left_total_len_list=data.left_total_len_list[i]
        temp_right_total_len_list=data.right_total_len_list[i]
        up_height=round(data.stream_pixels_list[i][-1])
        flowrate=data.flowrate_array[high_row,high_col]
        for j in range(i+1,len(data.stream_list)):
            on_stream_len+=data.cell_length*neighbor_dist(data.stream_list[j-1],data.stream_list[j])
            stream_row=data.stream_list[j][0]
            stream_col=data.stream_list[j][1]
            height_dif=up_height-round(data.stream_pixels_list[j][-1])
            stream_dist=cl*distances[abs(stream_row-high_row),abs(stream_col-high_col),height_dif]
            if on_stream_len>data.maximum_distance and data.maximum_distance>0:
                break
            if (stream_row,stream_col) in ban_set:
                continue
            power=height_dif*flowrate
            if power<data.minimum_power or data.minimum_power==-1:
                continue
            closed_i_j_cost=closed_price*stream_dist
            left_price_list=[]
            for k in range(len(temp_leftisos)):
                point_row=temp_leftisos[k][0]
                point_col=temp_leftisos[k][1]
                if (point_row,point_col) in ban_set:
                    break
                open_cost=temp_left_all_costs_open_list[k]
                closed_len=cl*distances[abs(stream_row-point_row),abs(stream_col-point_col),height_dif]
                cost_temp=open_cost+closed_price*closed_len
                adj_height=max(0,height_dif-losses*temp_left_total_len_list[k]*cl)
                if adj_height==0:
                    continue
                adj_power=adj_height*flowrate
                left_price_list.append((cost_temp/adj_power,cost_temp,float(open_cost),closed_price*closed_len,i,j,k,0,high_row,high_col,stream_row,stream_col,point_row,point_col,(),0,0))
                if open_cost>closed_i_j_cost:
                    break
            data.price_list.extend(left_price_list)
            right_price_list=[]
            for k in range(len(temp_rightisos)):
                point_row=temp_rightisos[k][0]
                point_col=temp_rightisos[k][1]
                if (point_row,point_col) in ban_set:
                    break
                open_cost=temp_right_all_costs_open_list[k]
                closed_len=cl*distances[abs(stream_row-point_row),abs(stream_col-point_col),height_dif]
                cost_temp=open_cost+closed_price*closed_len
                adj_height=max(0,height_dif-losses*temp_right_total_len_list[k]*cl)
                if adj_height==0:
                    continue
                adj_power=adj_height*flowrate
                right_price_list.append((cost_temp/adj_power,cost_temp,float(open_cost),closed_price*closed_len,i,j,k,1,high_row,high_col,stream_row,stream_col,point_row,point_col,(),0,0))
                if open_cost>closed_i_j_cost:
                    break
            data.price_list.extend(right_price_list)
    data.partition_price_list()
    data.sort_price_list()
    end=time.time()
    logprint('Time to estimate the prices (step 6):',end-start)

def calculate_good_values(data=iodata):
    '''Finds the best (upstream, downstream, contour) triple in terms of cost divided by height difference.
    The calculation stops at data.wanted_cases iterations.
    Returns the price per height of the found solution and the index of the solution in price_list.'''
    start=time.time()
    for quality_number,solution in enumerate(data.price_list):
        downstream=solution[10],solution[11]
        contour=solution[12],solution[13]
        try:
            path=dijkstar.find_path(data.graph,contour,downstream)
            ret=path.nodes,path.total_cost,(path.total_cost+solution[2])*solution[0]/solution[1]
            data.update_price_list(quality_number,*ret)
        except dijkstar.algorithm.NoPathError:
            data.update_price_list(quality_number,(),-1,-1)
    data.sort_accurate_price_list()
    end=time.time()
    logprint('Time to calculate the exact closed prices for the wanted cases (step 7):',end-start)

def comma_str(content):
    if isinstance(content,float):
        s=str(content).split(sep='.')
        return s[0]+','+s[1]
    else:
        return str(content)

def save_to_csv(data=iodata,sep='.'):
    if sep not in {'.',','}:
        raise ValueError("sep must be either '.' or ','")
    start=time.time()
    if sep=='.':
        with open(f'{address}\\Results.csv','w') as f:
            for title in ['ID number','Up x','Up y','Up z','Down x','Down y','Down z','Cont x','Cont y','Up flow acc','Up flow rate','Open length','Closed length','Open cost','Closed cost','Total cost']:
                f.write(f'{title};')
            f.write('Price index\n')
            for row,datum in enumerate(data.accurate_price_list[:data.wanted_cases]):
                to_save=[row+1,*data.coords_from_pixel(datum[8],datum[9]),*data.coords_from_pixel(datum[10],datum[11]),*data.coords_from_pixel(datum[12],datum[13])[:2],float(data.FlowAcc_array[datum[8],datum[9]]),float(data.flowrate_array[datum[8],datum[9]]),datum[2]/data.open_price,datum[-2]/data.closed_price,datum[2],datum[-2],datum[2]+datum[-2],datum[-1]]
                for content in to_save[:-1]:
                    f.write(f'{content},')
                f.write(f'{content}\n')
    else:
        with open(f'{address}\\Results.csv','w') as f:
            for title in ['ID number','Up x','Up y','Up z','Down x','Down y','Down z','Cont x','Cont y','Up flow acc','Up flow rate','Open length','Closed length','Open cost','Closed cost','Total cost']:
                f.write(f'{title};')
            f.write('Price index\n')
            for row,datum in enumerate(data.accurate_price_list[:data.wanted_cases]):
                to_save=[row+1,*data.coords_from_pixel(datum[8],datum[9]),*data.coords_from_pixel(datum[10],datum[11]),*data.coords_from_pixel(datum[12],datum[13])[:2],float(data.FlowAcc_array[datum[8],datum[9]]),float(data.flowrate_array[datum[8],datum[9]]),datum[2]/data.open_price,datum[-2]/data.closed_price,datum[2],datum[-2],datum[2]+datum[-2],datum[-1]]
                for content in to_save[:-1]:
                    f.write(f'{comma_str(content)};')
                f.write(f'{comma_str(content)}\n')
    end=time.time()
    logprint('Time to save the result to csv:',end-start)

def save_to_xlsx(data=iodata):
    start=time.time()
    wb=openpyxl.Workbook()
    ws=wb.active
    for col,title in zip('ABCDEFGHIJKLMNOPQ',['ID number','Up x','Up y','Up z','Down x','Down y','Down z','Cont x','Cont y','Up flow acc','Up flow rate','Open length','Closed length','Open cost','Closed cost','Total cost','Price index']):
        ws[f'{col}1']=title
    for row,datum in enumerate(data.accurate_price_list[:data.wanted_cases]):
        to_save=[row+1,*data.coords_from_pixel(datum[8],datum[9]),*data.coords_from_pixel(datum[10],datum[11]),*data.coords_from_pixel(datum[12],datum[13])[:2],float(data.FlowAcc_array[datum[8],datum[9]]),float(data.flowrate_array[datum[8],datum[9]]),datum[2]/data.open_price,datum[-2]/data.closed_price,datum[2],datum[-2],datum[2]+datum[-2],datum[-1]]
        for col,content in zip('ABCDEFGHIJKLMNOPQ',to_save):
            ws[f'{col}{row+2}']=content
    wb.save(f'{address}\\Results.xlsx')
    end=time.time()
    logprint('Time to save the result to xlsx (step 8):',end-start)

def main(data=iodata):
    start=time.time()
    categorize_points(data)
    #raise KeyboardInterrupt
    find_border(data)
    #raise KeyboardInterrupt
    draw_contours(data)
    #raise KeyboardInterrupt
    calculate_open_distance(data)
    calculate_open_prices(data)
    estimate_best_prices(data)
    calculate_good_values(data)
    save_to_xlsx(data)
    end=time.time()
    logprint('Total time:',end-start)


#TIME MEASUREMENT

end = time.time()
logprint('Time to complete function definition (step 0):',end-start)

#END TIME MEASUREMENT

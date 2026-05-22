def make_map_1(b,v1=100,v2=150,v3=200,data=iodata,coords=None):
    '''Create map that shows all points with the same height as the starting point.
    b is the index of the starting point in data.stream_pixels_list.
    v1 and v2 are the values used for the intensity of the map:
    v1 for the same-height points.
    v2 for the stream points.
    v3 for the upstream point.
    If coords!=None, the map also includes a crosshair centered at the specified point.
    coords is a tuple that includes the coordinates of the specified point and optionally the intensity of the crosshair.'''
    start = time.time()
    y=set()
    if coords:
        if len(coords)<2 or len(coords)>3:
            raise ValueError('incorrect coordinate tuple')
        if coords[0]<0 or coords[0]>=data.rows or coords[1]<0 or coords[1]>=data.cols:
            raise IndexError('coordinates out of bounds')
        if len(coords)==2:
            coords=(*coords,150)
        z1,z2,vcross=coords
        for i in data.stream_pixels_list:
            y.add((i[1],i[2]))
        for i in range(data.rows):
            for j in range(data.cols):
                data.results_block.setValue(i, j, 0.5*(v1*int((i,j) in data.list_iso[b])+v2*int((i,j) in y)+v3*int(bval==b))+vcross*(i==z1)+vcross*(j==z2))
    else:
        for bval,i in enumerate(data.stream_pixels_list):
            y.add((i[1],i[2]))
            if bval==b:
                bco=(i[1],i[2])
        for i in range(data.rows):
            for j in range(data.cols):
                data.results_block.setValue(i, j, v1*int((i,j) in data.list_iso[b])+v2*int((i,j) in y)+v3*int(bco==(i,j)))
    data.provider_results.setEditable(True)
    data.provider_results.writeBlock(data.results_block, 1, 0, 0)
    data.provider_results.setEditable(False)
    end = time.time()
    logprint('Time to complete map:',end - start)

def make_map_2(b,v1=100,v2=200,v3=50,v4=70,data=iodata,coords=None):
    '''Create map that shows all points with the same height as the starting point
     and highlights the contours.
    b is the index of the starting point in data.stream_pixels_list.
    v1, v2, v3 and v4 are the values used for the intensity of the map:
    v1 for the same-height points.
    v2 for the stream points.
    v3 for the left contour.
    v4 for the right contour.
    If coords!=None, the map also includes a crosshair centered at the specified point.
    coords is a tuple that includes the coordinates of the specified point and optionally the intensity of the crosshair.'''
    start = time.time()
    y=set()
    l=set(data.leftisos[b])
    r=set(data.rightisos[b])
    if coords:
        if len(coords)<2 or len(coords)>3:
            raise ValueError('incorrect coordinate tuple')
        if coords[0]<0 or coords[0]>=data.rows or coords[1]<0 or coords[1]>=data.cols:
            raise IndexError('coordinates out of bounds')
        if len(coords)==2:
            coords=(*coords,150)
        z1,z2,vcross=coords
        for i in data.stream_pixels_list:
            y.add((i[1],i[2]))
        for i in range(data.rows):
            for j in range(data.cols):
                data.results_block.setValue(i, j, 0.5*(v1*int((i,j) in data.list_iso[b])+v2*int((i,j) in y)+v3*((i,j) in l)+v4*((i,j) in r))+vcross*(i==z1)+vcross*(j==z2))
    else:
        for i in data.stream_pixels_list:
            y.add((i[1],i[2]))
        for i in range(data.rows):
            for j in range(data.cols):
                data.results_block.setValue(i, j, v1*int((i,j) in data.list_iso[b])+v2*int((i,j) in y)+v3*((i,j) in l)+v4*((i,j) in r))#+50*(i==x)+50*(j==z))
    data.provider_results.setEditable(True)
    data.provider_results.writeBlock(data.results_block, 1, 0, 0)
    data.provider_results.setEditable(False)
    end = time.time()
    logprint('Time to complete map:',end - start)

def make_map_3(b,v1=150,v2=20,v3=0.085,data=iodata,coords=None):
    '''Create map that shows all contour points according to their distance from the starting point.
    b is the index of the starting point in data.stream_pixels_list.
    v1, v2 and v3 are the values used for the intensity of the map:
    v1 for the stream points.
    v2 for the contours.
    v3 parameter for the length.
    If coords!=None, the map also includes a crosshair centered at the specified point.
    coords is a tuple that includes the coordinates of the specified point and optionally the intensity of the crosshair.'''
    start = time.time()
    y=set()
    l=set(data.leftisos[b])
    r=set(data.rightisos[b])
    iso_set=l|r
    for i in data.stream_pixels_list:
        y.add((i[1],i[2]))
    if coords:
        if len(coords)<2 or len(coords)>3:
            raise ValueError('incorrect coordinate tuple')
        if coords[0]<0 or coords[0]>=data.rows or coords[1]<0 or coords[1]>=data.cols:
            raise IndexError('coordinates out of bounds')
        if len(coords)==2:
            coords=(*coords,150)
        z1,z2,vcross=coords
        for i in range(data.rows):
            for j in range(data.cols):
                if (i,j) in l:
                    x=data.leftisos[b].index((i,j))
                    data.results_block.setValue(i, j,0.5*(v1*int((i,j) in y)+v2*((i,j) in iso_set)+v3*data.left_total_len_list[b][x])+vcross*(i==z1)+vcross*(j==z2))
                elif (i,j) in r:
                    x=data.rightisos[b].index((i,j))
                    data.results_block.setValue(i, j,0.5*(v1*int((i,j) in y)+v2*((i,j) in iso_set)+v3*data.right_total_len_list[b][x])+vcross*(i==z1)+vcross*(j==z2))
                else:
                    data.results_block.setValue(i, j,0.5*v1*int((i,j) in y)+vcross*(i==z1)+vcross*(j==z2))
    else:
        for i in range(data.rows):
            for j in range(data.cols):
                if (i,j) in l:
                    x=data.leftisos[b].index((i,j))
                    data.results_block.setValue(i, j,v1*int((i,j) in y)+v2*((i,j) in iso_set)+v3*data.left_total_len_list[b][x])
                elif (i,j) in r:
                    x=data.rightisos[b].index((i,j))
                    data.results_block.setValue(i, j,v1*int((i,j) in y)+v2*((i,j) in iso_set)+v3*data.right_total_len_list[b][x])
                else:
                    data.results_block.setValue(i, j,v1*int((i,j) in y))
    data.provider_results.setEditable(True)
    data.provider_results.writeBlock(data.results_block, 1, 0, 0)
    data.provider_results.setEditable(False)
    end = time.time()
    logprint('Time to complete map:',end - start)

def make_map_4(n = 1, data=iodata,coords=None):
    '''Create map that shows the lowest point of the stream that's higher than each pixel.
    n is the number of consecutive stream cells that correspond to the same color.
    If coords!=None, the map also includes a crosshair centered at the specified point.
    coords is a tuple that includes the coordinates of the specified point and optionally the intensity of the crosshair.'''
    start = time.time()
    if coords:
        if len(coords)<2 or len(coords)>3:
            raise ValueError('incorrect coordinate tuple')
        if coords[0]<0 or coords[0]>=data.rows or coords[1]<0 or coords[1]>=data.cols:
            raise IndexError('coordinates out of bounds')
        if len(coords)==2:
            coords=(*coords,150)
        z1,z2,vcross=coords
        for i in range(data.rows):
            for j in range(data.cols):
                if data.min_iso[i,j] == -2:
                    data.results_block.setValue(i, j, -1+vcross*(i==z1)+vcross*(j==z2))
                elif data.min_iso[i,j] == -1:
                    data.results_block.setValue(i, j, -0.5+vcross*(i==z1)+vcross*(j==z2))
                else:
                    data.results_block.setValue(i, j, 0.5*data.min_iso[i,j]//n*n+vcross*(i==z1)+vcross*(j==z2))
    else:
        for i in range(data.rows):
            for j in range(data.cols):
                if data.min_iso[i,j] == -2:
                    data.results_block.setValue(i, j, -2)
                elif data.min_iso[i,j] == -1:
                    data.results_block.setValue(i, j, -1)
                else:
                    data.results_block.setValue(i, j, data.min_iso[i,j]//n*n)
    data.provider_results.setEditable(True)
    data.provider_results.writeBlock(data.results_block, 1, 0, 0)
    data.provider_results.setEditable(False)
    end = time.time()
    logprint('Time to complete map:',end - start)

def make_map_5(quality_number=0,v1=100,v2=50,v3=80,v4=80,data=iodata,coords=None):
    '''Create map that:
    Shows an upstream point, a downstream point and a contour point.
    Highlights the contour path between the upstream and downstream points.
    Connects the downstream and contour points with a straight line.
    quality_number is the index of the solution being checked in price_list.
    v1, v2, v3 and v4 are the values used for the intensity of the map:
    v1 for the stream points.
    v2 for the contours.
    v3 for the path on the contour.
    v4 for the straight line.
    If coords!=None, the map also includes a crosshair centered at the specified point.
    coords is a tuple that includes the coordinates of the specified point and optionally the intensity of the crosshair.'''
    start = time.time()
    point=data.price_list[quality_number]
    i,j,k,side=point[4:8]
    iso_path=(data.leftisos,data.rightisos)[side][i][:k]
    iso_set=set(data.leftisos[i])|set(data.rightisos[i])
    try:
        closed=make_straight_line(point[10],point[11],point[12],point[13])
    except ZeroDivisionError:
        closed=set()
    if coords:
        if len(coords)<2 or len(coords)>3:
            raise ValueError('incorrect coordinate tuple')
        if coords[0]<0 or coords[0]>=data.rows or coords[1]<0 or coords[1]>=data.cols:
            raise IndexError('coordinates out of bounds')
        if len(coords)==2:
            coords=(*coords,150)
        z1,z2,vcross=coords
        for x in range(data.rows):
            for y in range(data.cols):
                data.results_block.setValue(x, y, 0.5*(v1*((x,y) in data.stream_set)+v2*((x,y) in iso_set)+v3*((x,y) in iso_path)+v4*((x,y) in closed))+vcross*(x==z1)+vcross*(y==z2))
    else:
        for x in range(data.rows):
            for y in range(data.cols):
                data.results_block.setValue(x, y, v1*((x,y) in data.stream_set)+v2*((x,y) in iso_set)+v3*((x,y) in iso_path)+v4*((x,y) in closed))
    data.results_block.setValue(point[8], point[9], 343)
    data.results_block.setValue(point[10], point[11], 343)
    data.results_block.setValue(point[12], point[13], 343)
    data.provider_results.setEditable(True)
    data.provider_results.writeBlock(data.results_block, 1, 0, 0)
    data.provider_results.setEditable(False)
    end = time.time()
    logprint('Time to complete map:',end - start)

def make_map_6(quality_number=0,acc=1,v1=100,v2=50,v3=80,v4=80,data=iodata,coords=None):
    '''Create map that:
    Shows an upstream point, a downstream point and a contour point.
    Highlights the contour path between the upstream and downstream points.
    Highlights the shortest path between the downstream and contour points.
    quality_number is the index of the solution being checked in price_list.
    v1, v2, v3 and v4 are the values used for the intensity of the map:
    v1 for the stream points.
    v2 for the contours.
    v3 for the path on the contour.
    v4 for the closed pipe path.
    If coords!=None, the map also includes a crosshair centered at the specified point.
    coords is a tuple that includes the coordinates of the specified point and optionally the intensity of the crosshair.'''
    start = time.time()
    point=data.accurate_price_list[quality_number]
    i,j,k,side=point[4:8]
    iso_path=(data.leftisos,data.rightisos)[side][i][:k]
    iso_set=set(data.leftisos[i])|set(data.rightisos[i])
    if (closed:=tuple(data.accurate_price_list[quality_number][-3]))==():
        closed=path_from_price_list(quality_number,1,data)
    if acc>1:
        closed2=set()
        for u,cl in enumerate(closed[:-1]):
            closed2.update(make_straight_line(cl[0],cl[1],closed[u+1][0],closed[u+1][1]))
        closed=closed2
    closed=set(closed)
    if coords:
        if len(coords)<2 or len(coords)>3:
            raise ValueError('incorrect coordinate tuple')
        if coords[0]<0 or coords[0]>=data.rows or coords[1]<0 or coords[1]>=data.cols:
            raise IndexError('coordinates out of bounds')
        if len(coords)==2:
            coords=(*coords,150)
        z1,z2,vcross=coords
        for x in range(data.rows):
            for y in range(data.cols):
                data.results_block.setValue(x, y, 0.5*(v1*((x,y) in data.stream_set)+v2*((x,y) in iso_set)+v3*((x,y) in iso_path)+v4*((x,y) in closed))+vcross*(x==z1)+vcross*(y==z2))
    else:
        for x in range(data.rows):
            for y in range(data.cols):
                data.results_block.setValue(x, y, v1*((x,y) in data.stream_set)+v2*((x,y) in iso_set)+v3*((x,y) in iso_path)+v4*((x,y) in closed))
    data.results_block.setValue(point[8], point[9], 343)
    data.results_block.setValue(point[10], point[11], 343)
    data.results_block.setValue(point[12], point[13], 343)
    data.provider_results.setEditable(True)
    data.provider_results.writeBlock(data.results_block, 1, 0, 0)
    data.provider_results.setEditable(False)
    end = time.time()
    logprint('Time to complete map:',end - start)

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

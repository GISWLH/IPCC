def oneDimFunction(valueArray, weightArray):
    import numpy
    #
    assert len(valueArray.shape) == 1
    assert len(weightArray.shape) == 1
    assert len(valueArray) == len(weightArray)
    #
    sort_indexes = numpy.argsort(valueArray)
    sort_values = numpy.sort(valueArray)
    #
    cumArray = numpy.zeros(valueArray.shape)
    cumArray[0] = weightArray[sort_indexes[0]]
    for i in range(1, len(valueArray)):
        cumArray[i] = cumArray[i-1] + weightArray[sort_indexes[i]]
    # end of for i in range(1, len(valueArray)+1):
    #
    index_05 = numpy.searchsorted(cumArray, 0.05)
    p05 = sort_values[index_05-1] + ((sort_values[index_05]- sort_values[index_05-1])/(cumArray[index_05] - cumArray[index_05-1])) * (0.05- cumArray[index_05-1])
    #
    index_95 = numpy.searchsorted(cumArray, 0.95, side='right')
    p95 = sort_values[index_95]
    p95 = sort_values[index_95-1] + ((sort_values[index_95]- sort_values[index_95-1])/(cumArray[index_95] - cumArray[index_95-1])) * (0.95- cumArray[index_95-1])
    #
    return p05, p95

def percentileFunction(valueArray,weightArray):
    #
    # Takes a 2-dimensional valueArray (m,t) and 1-dimensional weightArray
    # and returns one dimensional arrays with shape (t) of 5th and 95th percentile
    #
    import numpy
    assert valueArray.shape[0] == weightArray.shape[0]
    #
    p05_array = numpy.zeros(valueArray.shape[1])
    p95_array = numpy.zeros(valueArray.shape[1])
    #
    for i in range(valueArray.shape[1]):
        p05, p95 = oneDimFunction(valueArray[...,i], weightArray)
        p05_array[i] = p05
        p95_array[i] = p95
    # end of for i in range(valueArray.shape[0]):
    #
    return p05_array, p95_array
        
def mmm_list(_2d_list):
    import numpy
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            ele_avg = numpy.average(numpy.array(element))
            flat_list.append(ele_avg)
        else:
            flat_list.append(element)
        # end of if type(element) is list:
    # end of for element in _2d_list:
    mmm = numpy.average(flat_list)
    return mmm
        
def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list

def raw_to_perc_rgb(RGB):
    assert type(RGB) == type([])
    assert len(RGB) == 3
    [r, g, b] = RGB
    r_p = r/255.
    g_p = g/255.
    b_p = b/255.
    return [r_p, g_p, b_p]

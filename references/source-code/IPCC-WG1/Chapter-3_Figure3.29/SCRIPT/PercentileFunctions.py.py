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
    #
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
        

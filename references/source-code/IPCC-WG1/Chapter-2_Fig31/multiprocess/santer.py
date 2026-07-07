from collections import namedtuple

import numpy as np
from scipy import stats
from scipy.stats import distributions

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning) 


LinregressResult = namedtuple('LinregressResult', ('slope', 'intercept',
                                                   'rvalue', 'pvalue',
                                                   'stderr'))


def santer_compensation(xvec, yvec, slope, intercept):
    """Compensate for autocorrelation in linear regression pvals

    Helpfunction extending scipy's `linregress` function. The santer 
    method adjusts standard errors for temporal persistence in the 
    residuals from a linear regression analysis by using a lag-1 
    autoregressive statistical model. This adjustment is mandatory 
    for OLS trend analyses presented in the IPCC report as of AR6.

    Parameters
    ----------
    xvec, yvec : array_like
        Two sets of measurements.  Both arrays should have the same length.
    slope: float
        The calculated slope from a linear regression of xvec and yvec
        (use scipy.stats.linregress)
    intercept: float
        The calculated intercept from a linear regression of xvec and yvec   
        (use scipy.stats.linregress)

    Returns
    -------
    pvalue : float
        Two-sided p-value for a hypothesis test whose null hypothesis is
        that the slope is zero, using Wald Test with t-distribution of
        the test statistic. Adjusted for autocorrelation in the 
        residuals.

    References
    ----------
    Santer et al 2000, doi:10.1029/1999JD901105
    Santer et al 2008, doi:10.1002/joc.1756

    Autocorrelation:
    https://www.itl.nist.gov/div898/handbook/eda/section3/eda35c.htm
    """
    ymod = xvec * slope + intercept
    evec = yvec - ymod
    emean = np.mean(evec)
    n_t = len(xvec)

    r1 = np.abs(np.sum((evec[:-1]-emean) * (evec[1:]-emean)) /
                np.sum((evec-emean)**2))
    n_e = n_t * (1-r1) / (1+r1)
    se_e = np.sqrt(1/(n_e-2) * np.sum(evec**2))
    se_b = np.sqrt(se_e**2/sum((xvec-np.mean(xvec))**2))
    t_b = slope/se_b
    prob = 2 * distributions.t.sf(np.abs(t_b), n_t-2)
    return prob,se_b

def linregress(x, y=None, santer=False):
    """
    Calculate a linear least-squares regression for two sets of measurements.

    Parameters
    ----------
    x, y : array_like
        Two sets of measurements.  Both arrays should have the same length.  If
        only `x` is given (and ``y=None``), then it must be a two-dimensional
        array where one dimension has length 2.  The two sets of measurements
        are then found by splitting the array along the length-2 dimension.  In
        the case where ``y=None`` and `x` is a 2x2 array, ``linregress(x)`` is
        equivalent to ``linregress(x[0], x[1])``.

    Returns
    -------
    slope : float
        Slope of the regression line.
    intercept : float
        Intercept of the regression line.
    rvalue : float
        Correlation coefficient.
    pvalue : float
        Two-sided p-value for a hypothesis test whose null hypothesis is
        that the slope is zero, using Wald Test with t-distribution of
        the test statistic.
    stderr : float
        Standard error of the estimated gradient.

    See also
    --------
    :func:`scipy.optimize.curve_fit` : Use non-linear
     least squares to fit a function to data.
    :func:`scipy.optimize.leastsq` : Minimize the sum of
     squares of a set of equations.

    Notes
    -----
    Missing values are considered pair-wise: if a value is missing in `x`,
    the corresponding value in `y` is masked.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from scipy import stats

    Generate some data:

    >>> np.random.seed(12345678)
    >>> x = np.random.random(10)
    >>> y = 1.6*x + np.random.random(10)

    Perform the linear regression:

    >>> slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    >>> print("slope: %f    intercept: %f" % (slope, intercept))
    slope: 1.944864    intercept: 0.268578

    To get coefficient of determination (R-squared):

    >>> print("R-squared: %f" % r_value**2)
    R-squared: 0.735498
    Plot the data along with the fitted line:

    >>> plt.plot(x, y, 'o', label='original data')
    >>> plt.plot(x, intercept + slope*x, 'r', label='fitted line')
    >>> plt.legend()
    >>> plt.show()

    Example for the case where only x is provided as a 2x2 array:

    >>> x = np.array([[0, 1], [0, 2]])
    >>> r = stats.linregress(x)
    >>> r.slope, r.intercept
    (2.0, 0.0)

    """
    TINY = 1.0e-20
    if y is None:  # x is a (2, N) or (N, 2) shaped array_like
        x = np.asarray(x)
        if x.shape[0] == 2:
            x, y = x
        elif x.shape[1] == 2:
            x, y = x.T
        else:
            msg = ("If only `x` is given as input, it has to be of shape "
                   "(2, N) or (N, 2), provided shape was %s" % str(x.shape))
            raise ValueError(msg)
    else:
        x = np.asarray(x)
        y = np.asarray(y)

    if x.size == 0 or y.size == 0:
        raise ValueError("Inputs must not be empty.")

    n = len(x)
    xmean = np.mean(x, None)
    ymean = np.mean(y, None)

    # average sum of squares:
    ssxm, ssxym, _, ssym = np.cov(x, y, bias=1).flat
    r_num = ssxym
    r_den = np.sqrt(ssxm * ssym)
    if r_den == 0.0:
        r = 0.0
    else:
        r = r_num / r_den
        # test for numerical error propagation
        if r > 1.0:
            r = 1.0
        elif r < -1.0:
            r = -1.0

    df = n - 2
    slope = r_num / ssxm
    intercept = ymean - slope*xmean
    if n == 2:
        # handle case when only two points are passed in
        if y[0] == y[1]:
            prob = 1.0
        else:
            prob = 0.0
        sterrest = 0.0
    elif santer:
        prob,sterrest = santer_compensation(x, y, slope, intercept)
    else:
        t = r * np.sqrt(df / ((1.0 - r + TINY)*(1.0 + r + TINY)))
        prob = 2 * distributions.t.sf(np.abs(t), df)
        sterrest = np.sqrt((1 - r**2) * ssym / ssxm / df)
    return LinregressResult(slope, intercept, r, prob, sterrest)

def test_santer():

    xvec = np.array([ 0,  1,  2,  3,
                      4,  5,  6,  7,
                      8,  9, 10, 11, 
                     12, 13, 14, 15,
                     16, 17, 18, 19])

    yvec = np.array([ 0.    ,  0.4978,  0.7206,  1.9535,
                      0.5788,  0.7561,  1.7292,  0.2122,
                      5.1823,  0.1341,  0.5614,  0.612 ,  
                      1.4844,  8.5561,  5.4761,  2.6145,  
                      6.5494,  2.5787, 11.2566,  2.2232])

    #Without Santer adjustment
    #santer.linregress(xvec,yvec, santer=False)
    slope=0.3146593984962407
    intercept=-0.3054142857142863
    rvalue=0.5958362275110908
    pvalue=0.005566608061650651
    #stderr=0.09996555961807213)

    #With Santer adjustment
    #santer.linregress(xvec,yvec, santer=True)                              
    slope=0.3146593984962407
    intercept=-0.3054142857142863
    rvalue=0.5958362275110908
    pvalue=0.06006116662952272


    xvec = np.array([ 0,  1,  2,  3,  
                      4,  5,  6,  7,
                      8,  9, 10, 11, 
                     12, 13, 14, 15, 
                     16, 17, 18, 19, 
                     20, 21, 22, 23, 
                     24, 25, 26])

    yvec = np.array([ 2.2360, -1.0770,  2.0051,  1.4514,
                     -1.0014, -0.1399, -0.0250,  0.8910,
                     -4.0382,  0.4722,  3.4042,  3.3871,
                      1.5494, -1.7826, -2.0474, -0.3433,
                      2.7284, -0.3357,  1.6052,  0.3491,
                      3.0301,  3.5874,  4.2895,  2.4965,
                      3.6025,  5.4142, -0.645 ])

    #Without Santer adjustment
    #santer.linregress(xvec, yvec, santer=False)
    slope=0.10740842490842487
    intercept=-0.24579841269841207
    rvalue=0.38499755862762375
    pvalue=0.047363175702464524
    #stderr=0.05149597578084682)

    #With Santer adjustment
    #santer.linregress(xvec,yvec, santer=True) 
    slope=0.10740842490842487
    intercept=-0.24579841269841207
    rvalue=0.38499755862762375
    pvalue=0.07680052314363177
    #stderr=0.05149597578084682
"""
ds = xr.open_dataset("ncfiles/arctic_days_stat.nc") 
last_day_pvalue   = chlorophyll.linregress(ds.all_last_days.data, stat="pvalue")
first_day_pvalue  = chlorophyll.linregress(ds.all_first_days.data, stat="pvalue")
number_day_pvalue = chlorophyll.linregress(ds.all_number_days.data, stat="pvalue")
maxval_day_pvalue = chlorophyll.linregress(ds.all_maxval_days.data, stat="pvalue")
ds.first_day_pvalue.values = first_day_pvalue
ds.last_day_pvalue.values = last_day_pvalue
ds.number_day_pvalue.values = number_day_pvalue
ds.maxval_day_pvalue.values = maxval_day_pvalue
ds.to_netcdf("ncfiles/arctic_days_stat_santer.nc")
"""
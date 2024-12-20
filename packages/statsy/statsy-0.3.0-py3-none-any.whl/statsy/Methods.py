from .main import *
from .Logarithms import *

def Sturges_rule(number_of_points:Number)->Number:
    """
    Sturges' rule for determining the approx. number of intervals for histograms.
    """
    return round(1 + log(2,number_of_points))

def Rice_rule(number_of_points:Number)->Number:
    """
    Rice rule for determining the approx. number of intervals for histograms.
    """
    return round(2 * (root(3,number_of_points)))

def arithmetic_mean(data:list)->Number:
    """
    Returns the arithmetic mean of a list of data points.
    """
    return (summation(None,None,None,[data])) / len(data)

def median(data:list)->Number:
    """
    Returns the simple mean of an ordered quantitative list.
    """
    total_length = len(data)
    if total_length & 1:
        return  data[int((total_length+1)/2)-1]
    else:
        return (data[ int((total_length/2)-1)] + data[int((total_length/2))])/2

def mode(data:list)->any:
    """
    A shortcut for statistics.mode(data)
    """
    return statistics.mode(data)

def trimean(data:list)->Number:
    """
    Returns the trimean of a set of data.
    Be sure to order list in an increasing order.
    """
    p25 = get_value_from_percentile(25,data)
    p50 = get_value_from_percentile(50,data)
    p75 = get_value_from_percentile(75,data)
    
    return ( (p25 + (2 * p50) + p75 ) / 4 )

def geometric_mean(data:list)->Number:
    """
    Returns the geometric mean of a list of data.
    """
    return (product_notation(None,None,None,[data]) ** (1/len(data)))

def trimmed_mean(trim:Number,data:list)->Number:
    """
    #Returns the trimmed mean of some data.
    """
    partial_trim = (trim/100)/2
    # Find how many elements to remove from each side of the
    number_to_slice_off = round((len(data) * partial_trim))
    trimmed_data = data[int(number_to_slice_off):len(data)-number_to_slice_off]
    return arithmetic_mean(trimmed_data)

def vrange(data:list)->Number:
    """
    #Returns the range variability of a set of data.
    """
    return abs(data[0] - data[int(len(data)-1)])

def interquartile_range(data:list)->Number:
    """
    #Also known as the H-spread. \n
    #Returns the interquartile range of a set of data.
    """
    total_length = len(data)
    if total_length & 1:
        # If the data is of odd length
        # Remove the median value and pass the data to the rest of the function.
        temporary_IQR_function_data = data[:]
        del temporary_IQR_function_data[int((total_length+1)/2)-1]
    total_length = total_length - 1
    return abs( median(temporary_IQR_function_data[:int(total_length//2)]) - median(temporary_IQR_function_data[int(total_length//2):]))

def variance(data:list,type:str,rooted:Optional[bool]=None)->Number:
    """
    type = 'sample' returns the variance of a sample \n
    type = 'population' returns the variance of a population \n
    Returns the variance of a normally distributed set of data points. \n
    """  
    n = len(data)
    if type == 'sample':
        n = len(data) - 1
    m = arithmetic_mean(data)
    varian = (((  summation(None,None,lambda x: ((x - m)**2) ,[data]) / n ))) 
    if rooted is True:
        varian = root(2,varian)
    return varian

def standard_deviation(data:list,type:str):
    """
    type = 'sample' returns the variance of a sample \n
    type = 'population' returns the variance of a population \n
    Returns the standard deviation of a normally distributed set of data points. \n
    """
    return variance(data,type,True)

def skewness(data:list,type:str)->Number:
    """
    type = 'sample' or 'population" \n
    Return the skew of a set of data. \n
    """
    mew = arithmetic_mean(data)
    n = len(data)
    sd = standard_deviation(data,'sample')
    fron =(n / ((n-1) * (n-2))) 
    if type == "population":
        sd = standard_deviation(data,'population')
        fron = (1/n)
    skew = fron  *   summation(None,None,lambda x: (((x - mew)/ sd) ** 3) ,[data])
    return skew

def Pearson_skewness(data:list,skew_type:Optional[str]=None,data_type:Optional[str]=None)-> Number:
    """
    skew_type = 'median' or 'mode' (median is default) \n
    data_type = 'sample' or 'population' (sample by default) \n
    Return's Pearson's coefficent of skewness. \n
    """
    x = arithmetic_mean(data)
    top = 3 * ( x - median(data) )
    if skew_type == 'mode':
        top = ( x - mode(data))
    bot = standard_deviation(data,'sample')
    if data_type == 'population':
        bot = standard_deviation(data,'population')
    return top / bot

def kurtosis(data:list,type:str)->Number:
    """
    type = 'sample' or 'population" \n
    Return the kurtosis of a set of data. \n
    """
    mew = arithmetic_mean(data)
    n = len(data)
    sd = standard_deviation(data,'sample')
    fron =  (  (n * (n + 1)) / ((n-1) * (n-2) * (n-3))) 
    end = 3     *   (  ((n-1)**2) / ((n-2)*(n-3))   )
    sm = summation(None,None,lambda x: (((x - mew)/ sd) ** 4) ,[data])
    if type == "population":
        sd = standard_deviation(data,'population')
        fron = (1/n)
        end = 3
        sm = summation(None,None,lambda x: (((x - mew)/ sd) ** 4) ,[data])
    kurt = (fron * sm) - end
    return kurt

def Pearson_correlation_coefficient_r(data:List[list])->Number:
    """
    Returns Pearson's correlation coefficient of r.
    """
    n = len(data[0])
    t1 = summation(None,None,lambda x, y: x*y,data)
    t2 = ( summation(None,None,None,[data[0]]) * summation(None,None,None,[data[1]]) ) / n
    b1 =  root(2,(summation(None,None,lambda x: x**2,[data[0]]) - ((summation(None,None,None,[data[0]])**2) / n)))
    b2 = root(2,(summation(None,None,lambda x: x**2,[data[1]]) - ((summation(None,None,None,[data[1]])**2) / n)))
    r = (t1-t2) / (b1 * b2)
    return r

def variance_sum_of_correlated_variables(data:List[list],type:str)->Number:
    """
    Returns the sum of correlated variance of two variables. \n
    """
    t1 = variance(data[0],type)
    t2 = variance(data[1],type)
    t3 = 2 * Pearson_correlation_coefficient_r(data) * standard_deviation(data[0],type) * standard_deviation(data[1],type)
    return t1 + t2 + t3
from .main import *
from .Constants import *

def simple_probability(desired_outcomes:str,total_outcomes:str)->Number:
    """
    Returns the probability of a set of outcomes A out of the number of all equally likely outcomes B. \n
    """
    return desired_outcomes / total_outcomes

def joint_probability(a:Number,b:Number)->Number:
    """
    Returns the joint probability of A and B where A and B are independent outcomes. \n
    Formula: P (A and B) = P (A) X P (B) \n
    Also known as conjunctive probability. \n
    """
    return a * b

def bare_joint_probability(a_desired:Number,a_possible:Number,b_desired:Number,b_possible:Number)->Number:
    """
    Returns the joint probability of A and B where A and B are independent outcomes and P(A) and P(B) must be calculated. \n
    Formula: P (A and B) = P (A) X P (B) \n
    Where P(A) and P(B) are not known. \n
    """
    return simple_probability(a_desired,a_possible) * simple_probability(b_desired,b_possible)

def disjunctive_probability(P_of_a:Number,P_of_b:Number,P_of_a_and_b:Optional[Number]=None):
    """
    Returns the disjunctive probability of A where A and B are independent outcomes. \n
    Formula: P (A or B) = P (A) + P (B) - P (A and B) \n
    Where P(A) , P(B), and P(A and B) is known.
    """
    jp = joint_probability(P_of_a,P_of_b)
    if P_of_a_and_b is not None:
        jp = P_of_a_and_b
    return P_of_a + P_of_b - jp

def bare_disjunctive_probability(a_desired:Number,a_possible:Number,b_desired:Number,b_possible:Number)->Number:
    """
    Returns the disjunctive probability of A where A and B are independent outcomes. \n
    Formula: P (A or B) = P (A) + P (B) - P (A and B) \n
    Where P(A) and P(B) are not known. \n
    """
    P_of_a = simple_probability(a_desired,a_possible)
    P_of_b = simple_probability(b_desired,b_possible)
    jp = joint_probability(P_of_a,P_of_b)
    return P_of_a + P_of_b - jp

def permutation(number_of_items:Optional[str],r:Number,data:Optional[list]=None)->Number:
    """
    Returns the permutation of formula nPr .\n
    Either the number of items in the set must be given or the data itself. \n
    """
    if data is not None:
        number_of_items = len(data)
    return (math.factorial(number_of_items)) / (math.factorial(number_of_items-r))

def combination(number_of_items:Optional[str],r:Number,data:Optional[list]=None)->Number:
    """
    Returns the permutation of formula nPr .\n
    Either the number of items in the set must be given or the data itself. \n
    """
    if data is not None:
        number_of_items = len(data)
    return (math.factorial(number_of_items)) / (math.factorial(number_of_items-r) * math.factorial(r))

def binomial_probability(number_of_items:Optional[str],p:Number,k:Number,data:Optional[list]=None)->Number:
    """
    Returns the binomial probability where: \n
    number_of_items = number of events, trials, etc. \n
    p = probability of desired outcome \n
    k = number of sucesses \n
    """
    if data is not None:
        number_of_items=len(data)
    return combination(number_of_items,k) * (p**k) * ( (1-p)** (number_of_items-k))

def binomial_distribution_mean(number_of_items:int,p:Number,data:Optional[list]=None)->Number:
    """
    Returns the mean of binomial distribution where N = number of items and \n
    p = probability of desired outcome. \n 
    """
    if data is not None:
        number_of_items=len(data)
    return number_of_items * p

def variance_of_binomial_distribution(number_of_items:int,p:Number,data:Optional[list]=None)->Number:
    """
    Returns the variance of binomial distribution. \n
    """
    if data is not None:
        number_of_items=len(data)
    return number_of_items * (1-p)

def standard_deviation_of_binomial_distribution(number_of_items:int,p:Number,data:Optional[list]=None)->Number:
    """
    Returns the standard deviation of binomial distribution. \n
    """
    if data is not None:
        number_of_items=len(data)
    return root(2,(number_of_items * (1-p)))

def Poisson_distribution(m:Number,x:Number,data:Optional[list]=None)->Number:
    """
    Returns the Poisson distribution where: \n
    m = average number of desired outcomes \n
    x = number of sucesses \n
    """
    return ((e**(-m))*(m **x)) / math.factorial(x)

def multinomial_distribution(n:Number,p_of_n:list,p_of_o:list)->Number:
    """
    Returns the multinomial distribution of events such that: \n
    n is the number of events or trials \n
    p_of_n is an ordered list of the probability that n1, n2, n3 ... occurs. \n
    p_of_o is an ordered list of the probability of outcome p1, p2, p3 ... \n
    Formula = \n
    p = ( n! / (n1!)(n2!)...(nk!)) * ( (p ** n1) (p ** n2) ... (p ** nk) )
    """
    top = math.factorial(n)
    bot = product_notation(None,None,lambda x: math.factorial(x),[p_of_n])
    end = product_notation(None,None,lambda p, x: p**x,[p_of_o,p_of_n])
    return (top/bot) * end

def hypergeometric_distribution(Number_in_population:Number,number_in_sample:Number,k_sucess:Number,n_sucess:Number)->Number:
    """
    Returns the hypergeometric distribution \n
    Where: \n
    Number_in_population = size of population \n
    number_in_sample = size of the sample \n
    k_sucess = number of sucesses in the population \n
    n_sucess = number of sucesses in the sample \n
    
    """
    t = combination(k_sucess,n_sucess) * combination((Number_in_population-k_sucess),(number_in_sample-n_sucess))
    b = combination(Number_in_population,number_in_sample)
    return t/b

def mean_of_hypergeometric_distribution(Number_in_population:Number,number_in_sample:Number,k:Number)->Number:
    """
    Returns the mean of hypergeometric distribution where: \n
    N = size of population \n
    k = sucesses in population \n
    n = size of sample \n
    """
    return (number_in_sample * k) / Number_in_population

def standard_deviation_of_hypergeometric_distribution(Number_in_population:Number,number_in_sample:Number,k:Number)->Number:
    """
    Returns the standard deviation of hypergeometric distribution where: \n
    N = size of population \n
    k = sucesses in population \n
    n = size of sample \n
    """
    t = number_in_sample * k * (Number_in_population - k) * (Number_in_population - number_in_sample)
    b = (Number_in_population ** 2) * (Number_in_population - 1)
    return root(2, (t/b))

import sympy as sp

# our SR methods give us a table with equations in a column 'sympy_format'
# we convert to latex format for use in a paper
# the variables may contain underscores, let's replace with empty string

# Claude.ai generated some of this
def process_equations_latex(df):
    df = df.copy()
    eqns = []
    vars = []
    consts = []
    for eq in df['sympy_format']:
        if type(eq) == str: eq = sp.sympify(eq)
        
        #print(eq)
        #print(eq.atoms())
        eq = printM(eq, 2)

        
        # Apply \mathrm{} to variable names
        for symbol in eq.free_symbols:
            new_name = f"\\mathrm{{{str(symbol).replace('_', '')}}}"
            new_symbol = sp.Symbol(new_name)
            eq = eq.subs(symbol, new_symbol)
        
        simplified = sp.simplify(eq)

        # Variables/parameters 
        n_vars = len(simplified.free_symbols)
        vars.append(n_vars)

        # Constants (atomic numbers)
        n_constants = count_true_constants(eq) 
        #for atom in simplified.atoms():
        #    print(f'{atom} {atom.is_number}')
        consts.append(n_constants)

        
        latex_eq = sp.latex(simplified, mul_symbol='ldot', mode='inline')
        
        eqns.append(latex_eq)
        #print(simplified.atoms())
        #print(f'{simplified} {n_vars} {n_constants}')
        #print('-----')
        
    df['equation'] = eqns
    df['vars'] = vars
    df['consts'] = consts
    
    return df

def printM(expr, num_digits):
    return expr.xreplace({n.evalf() : round(n, num_digits) for n in expr.atoms(sp.Number)})

def is_power_of_two_fraction(num):
    if not isinstance(num, sp.Rational):
        return False
    return (num.p == 1 and 
           (num.q & (num.q - 1) == 0))  # Check if q is power of 2

def count_true_constants(eq):
    sqrt_powers = set()
    for arg in eq.args:
        if isinstance(arg, sp.Pow) and is_power_of_two_fraction(arg.args[1]):
            sqrt_powers.add(arg.args[1])
            
    constants = {atom for atom in eq.atoms() if atom.is_number} - sqrt_powers
    return len(constants)


#df = process_equations_latex(m.equations_)
#df
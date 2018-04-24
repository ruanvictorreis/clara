'''
Generating correct feedback from repair for Python programs
'''

from feedback_python import *

class CodeRepairFeedback(object):

    def __init__(self, impl, spec, result, cleanstrings=None):
        self.impl = impl
        self.spec = spec
        self.result = result
        self.feedback = []
        self.expr_orig = None
        self.code_repaired = impl.code.splitlines()

    def add(self, msg, *args):
        if args:
            msg %= args
        if self.expr_orig:
            msg = '%s [%s]' % (msg, self.expr_orig)
        self.feedback.append(msg)
    
    def apply_repair(self):
		print(self.code_repaired)
				
    def genfeedback(self):
        gen = PythonStatementGenerator()
        # Iterate all functions
        # fname - function name
        # mapping - one-to-one mapping of variables
        # repairs - list of repairs
        # sm - structural matching betweeb locations of programs
        for fname, (mapping, repairs, sm) in self.result.items():

            # Copy mapping with converting '*' into a 'new_' variable
            nmapping = {k: '$new_%s' % (k,)
                        if v == '*' else v for (k, v) in mapping.items()}

            # Go through all repairs
            # loc1 - location from the spec.
            # var1 - variable from the spec.
            # var2 - variable from the impl.
            # cost - cost of the repair
            for rep in repairs:

                loc1 = rep.loc1
                var1 = rep.var1
                var2 = rep.var2
                cost = rep.cost
                expr1 = rep.expr1
                self.expr_orig = rep.expr1_orig

                # Get functions and loc2
                fnc1 = self.spec.getfnc(fname)
                fnc2 = self.impl.getfnc(fname)
                loc2 = sm[loc1]

                # Get exprs (spec. and impl.)
                #expr1 = fnc1.getexpr(loc1, var1)
                expr2 = fnc2.getexpr(loc2, var2)

                # Location of the expression
                if expr2.line:
                    # Either line
                    locdesc = 'at line %s' % (expr2.line,)
                else:
                    # Or location description
                    locdesc = fnc2.getlocdesc(loc2)

                # Delete feedback
                if var1 == '-':
                    self.add("Delete '%s' at line %s (cost=%s)",
                             str(gen.assignmentStatement(var2, expr2)), expr2.line, cost)
                    continue

                # Rewrite expr1 (from spec.) with variables of impl.
                expr1 = expr1.replace_vars(nmapping)

                # '*' means adding a new variable (and also statement)
                if var2 == '*':
                    self.add("Add assignment '%s' %s (cost=%s)",
                             str(gen.assignmentStatement('$new_%s' % (var1,), expr1)), locdesc, cost)
                    continue

                # Output original and new (rewriten) expression for var2
                
                if var2.startswith('iter#'):
                    pyexpr1 = gen.pythonExpression(expr1, True)[0]
                    pyexpr2 = gen.pythonExpression(expr2, True)[0]
                    self.add("Change iterated expression of for loop '%s' to '%s' %s (cost=%s)", str(pyexpr2), str(pyexpr1), locdesc, cost)
                elif str(var2) == str(expr2):
                    self.add("Add a statement '%s' %s (cost=%s)", str(gen.assignmentStatement(var2, expr1)), locdesc, cost)
                else:
                    self.add(
                        "Change '%s' to '%s' %s (cost=%s)",
                        str(gen.assignmentStatement(var2, expr2)), str(gen.assignmentStatement(var2, expr1)), locdesc, cost)

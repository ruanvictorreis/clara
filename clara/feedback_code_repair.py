'''
Generating correct feedback from repair for Python programs
'''

from feedback_python import *
from difflib import SequenceMatcher

class CodeRepairFeedback(object):

    def __init__(self, impl, spec, result, cleanstrings=None):
        self.impl = impl
        self.spec = spec
        self.result = result
        self.feedback = []
        self.expr_orig = None
        self.code_repaired = impl.code

    def apply_change_repair(self, expr1, expr2):
        impl_code = self.code_repaired
        
        if expr1 in impl_code:
            new_code = impl_code.replace(expr1, expr2)
            self.code_repaired = new_code
        else:
			loc = self.find_expression_line(expr1)
			self.apply_assignment_change_repair(expr1, expr2, loc)
	
    def apply_assignment_change_repair(self, expr1, expr2, loc):
        code_lines = self.code_repaired.splitlines()
        line_target = code_lines[loc - 1]
        
        expr1_striped = expr1.strip()
        line_target_striped = line_target.strip()
             
        seq_matcher = SequenceMatcher(
            None, line_target_striped, expr1_striped)
        
        first_match = seq_matcher.get_matching_blocks()[0]
        
        common_expression = line_target_striped[
            first_match.a: first_match.a + first_match.size][:-1]
        
        if common_expression not in expr2:
            seq_matcher = SequenceMatcher(
                None, common_expression, expr2)
            
            first_match = seq_matcher.get_matching_blocks()[0]
            
            common_expression = common_expression[
                first_match.a: first_match.a + first_match.size]   		
        
        line_target_splited = line_target.split(common_expression, 1)
        expression_splited = expr2.split(common_expression, 1)
        
        line_target_splited[-1] = expression_splited[-1]
        line_target = common_expression.join(line_target_splited)
        code_lines[loc - 1] = line_target
        self.code_repaired = '\n'.join(code_lines)
    
    def apply_delete_repair(self, expr):
        code_lines = self.code_repaired.splitlines()
        loc = self.find_expression_line(expr)
        del code_lines[loc - 1]
        self.code_repaired = '\n'.join(code_lines)
    
    def apply_add_statement_repair(self, var, expr, loc):        
        ret_statement = False 
        
        if var == '$ret':
            loc = loc - 1
            ret_statement = True	
        
        code_lines = self.code_repaired.splitlines()
        target_line = code_lines[loc]    
        indentation_level = len(target_line) - len(target_line.strip())     
        target_line = target_line[:indentation_level] + expr      
        
        if(ret_statement):
		    code_lines.append(target_line)
        else:
            code_lines.insert(loc, target_line)

        self.code_repaired = '\n'.join(code_lines)
        		
    def find_expression_line(self, expr):
        ratio_line = -1
        target_line = 0
        impl_code = self.code_repaired
        code_lines = impl_code.splitlines()
        
        for i in range(len(code_lines)):
            line = code_lines[i]
            ratio = SequenceMatcher(None, line, expr).ratio()
            
            if(ratio > ratio_line):
                ratio_line = ratio
                target_line = i + 1    
        
        return target_line    				
    
    def genfeedback(self):
        loc_added = 0
        gen = PythonStatementGenerator()
        # Iterate all functions
        # fname - function name
        # mapping - one-to-one mapping of variables
        # repairs - list of repairs
        # sm - structural matching betweeb locations of programs
        for fname, (mapping, repairs, sm) in self.result.items():

            # Copy mapping with converting '*' into a 'new_' variable
            nmapping = {k: 'new_%s' % (k,)
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

                # delete feedback
                if var1 == '-':
                    self.apply_delete_repair(str(gen.assignmentStatement(var2, expr2)))    					
                    continue

                # rewrite expr1 (from spec.) with variables of impl.
                expr1 = expr1.replace_vars(nmapping)

                # '*' means adding a new variable (and also statement)
                if var2 == '*':
                    self.apply_add_statement_repair(var1,
                        str(gen.assignmentStatement('new_%s' % 
                        (var1,), expr1)), loc1 - loc_added)                   
                    loc_added += 1
                    continue

                # output original and new (rewriten) expression for var2              
                if var2.startswith('iter#'):
                    pyexpr1 = str(gen.pythonExpression(expr1, True)[0]) + ":"
                    pyexpr2 = str(gen.pythonExpression(expr2, True)[0]) + ":"
                    self.apply_change_repair(pyexpr2, pyexpr1)

                elif str(var2) == str(expr2):
                    self.apply_add_statement_repair(var2,
                        str(gen.assignmentStatement(var2, expr1)), loc1)    					
                    loc_added += 1
					
                else:
                    self.apply_change_repair(
                        str(gen.assignmentStatement(var2, expr2)), 
                        str(gen.assignmentStatement(var2, expr1)))     
        
        #adding repaired code to feedback list
        self.feedback.append(self.code_repaired)

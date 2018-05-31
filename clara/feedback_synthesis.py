'''
Generating correct feedback from repair for Python programs
'''

from feedback_python import *
from difflib import SequenceMatcher

class SynthesisFeedback(object):

    def __init__(self, impl, spec, result, cleanstrings=None):
        self.impl = impl
        self.spec = spec
        self.result = result
        self.feedback = []
        self.expr_orig = None
        self.error = False
        
        self.added_lines = []
        self.removed_lines = []
        self.code_repaired = impl.code
	
    def apply_change_repair(self, expr1, expr2):
        code_lines = self.code_repaired.splitlines()
        loc = self.find_expression_line(expr1)
        line_target = code_lines[loc - 1]
        colon = False
		
        if (line_target.strip().endswith(':')):
            colon = True
		
        if (expr1 in line_target):
            line_target = line_target.replace(expr1, expr2)
        
        matched_expr = self.find_matched_expression(
            line_target.strip(), expr1.strip(), -1)

        if (matched_expr not in expr2):
            matched_expr = self.find_matched_expression(
                matched_expr, expr2, len(matched_expr)) 		
        
        line_target_splited = line_target.split(matched_expr, 1)
        expression_splited = expr2.split(matched_expr, 1)
        line_target_splited[-1] = expression_splited[-1]
        
        matched_expr = expression_splited[0] + matched_expr
        line_target = matched_expr.join(line_target_splited)
        
        if (colon) : 
            line_target += ':'
        
        code_lines[loc - 1] = line_target
        self.code_repaired = '\n'.join(code_lines)
    
    def apply_delete_repair(self, expr):			
        code_lines = self.code_repaired.splitlines()
        loc = self.find_expression_line(expr) - 1
        del code_lines[loc]
        
        self.removed_lines.append(loc)
        self.code_repaired = '\n'.join(code_lines)
    
    def apply_add_statement_repair(self, var, expr, loc):    
        ret_statement = False
        
        if (loc == 0):
            loc += 1
        
        if var == '$ret':
            loc = loc - 1
            ret_statement = True
        
        loc_off = loc + self.line_offset(loc)
        code_lines = self.code_repaired.splitlines()
        target_line = self.find_indentation_level(loc) + expr     
        
        if(ret_statement):
		    code_lines.append(target_line)
		    self.added_lines.append(len(code_lines) - 1)
        else:
            code_lines.insert(loc_off, target_line)
            self.added_lines.append(loc_off)

        self.code_repaired = '\n'.join(code_lines)
        
    def apply_new_statement_repair(self, var, expr, loc):
        if (loc == 0):
            loc += 1
        
        lineExists = loc < len(self.impl.code.splitlines())
        if (not lineExists):
            loc -= 1
        
        loc_off = loc + self.line_offset(loc)
        code_lines = self.code_repaired.splitlines()
        target_line = self.find_indentation_level(loc) + expr     
        
        code_lines.insert(loc_off, target_line)
        self.added_lines.append(loc_off)       
        self.code_repaired = '\n'.join(code_lines)
        		
    def find_indentation_level(self, loc):
        impl_code = self.impl.code
        code_lines = impl_code.splitlines()
        target_line = code_lines[loc]
        level = len(target_line) - len(target_line.strip())
        return target_line[:level]	
		
    def find_expression_line(self, expr):
        ratio_line = -1
        target_line = 0
        impl_code = self.code_repaired
        code_lines = impl_code.splitlines()
        pattern = expr.replace('(', '').replace(')', '').strip()
        
        for i in range(len(code_lines)):
            line = code_lines[i].strip()
            ratio = SequenceMatcher(None, line, expr.strip()).ratio()
            
            if pattern in line:
				ratio += 0.1
            
            if(ratio > ratio_line):
                ratio_line = ratio
                target_line = i + 1    
        
        return target_line    				
    
    def line_offset(self, new_line):
        offset = 0
		
        for line in self.removed_lines:
            if new_line > line:
                offset -= 1

        for line in self.added_lines:
            if new_line >= line:
                offset += 1		
        
        return offset	 
    
    def find_matched_expression(self, target, expr, offset):        
        seq_matcher = SequenceMatcher(
            None, target, expr)
        
        first_match = seq_matcher.get_matching_blocks()[0]
        
        return target[first_match.a: 
            first_match.a + first_match.size][:offset]
    
    def genfeedback(self):
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
                    try:                    
                        self.apply_delete_repair(
                            str(gen.assignmentStatement(var2, expr2)))    					
                        continue
                    except:
                        self.error = True   

                # rewrite expr1 (from spec.) with variables of impl.
                expr1 = expr1.replace_vars(nmapping)

                # '*' means adding a new variable (and also statement)
                if var2 == '*':
                    try: 
                        self.apply_new_statement_repair(var1,
                            str(gen.assignmentStatement('new_%s' % 
                            (var1,), expr1)), loc1 - 1)                   
                        continue
                    except:
                        self.error = True 

                # output original and new (rewriten) expression for var2              
                if var2.startswith('iter#'):
                    try:
                        pyexpr1 = str(gen.pythonExpression(expr1, True)[0])
                        pyexpr2 = str(gen.pythonExpression(expr2, True)[0])
                        self.apply_change_repair(pyexpr2, pyexpr1)
                    except:
                        self.error = True   

                elif str(var2) == str(expr2):
                    try:
                        self.apply_add_statement_repair(var2,
                            str(gen.assignmentStatement(var2, expr1)), loc1 - 1)
                    except:
                        self.error = True  					
                
                elif str(var2) == str(expr1):
                     try:				
                        self.apply_delete_repair(
                            str(gen.assignmentStatement(var2, expr2)))
                     except:
                        self.error = True
                    
                else:
                    try:
                        self.apply_change_repair(
                            str(gen.assignmentStatement(var2, expr2)), 
                            str(gen.assignmentStatement(var2, expr1)))     
                    except:
                        self.error = True
        
        # adding repaired code to feedback list
        if (not self.error):
            self.feedback.append(self.code_repaired)

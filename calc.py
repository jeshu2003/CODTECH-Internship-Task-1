import tkinter as tk
from tkinter import messagebox, Toplevel, scrolledtext
import sympy as sp
import re

def clear_display():
    entry_expression.delete(0, tk.END)
    show_text.configure(state='normal')
    show_text.delete('1.0', tk.END)
    show_text.configure(state='disabled')

def format_number(expr):
    if isinstance(expr, sp.Basic):
        if expr.is_real:
            try:
                value = float(expr.evalf())
                if value.is_integer():
                    return str(int(value))
                else:
                    return f"{value:.4f}"
            except:
                return str(expr.evalf())
        else:
            return str(expr.evalf())
    else:
        try:
            value = float(expr)
            if value.is_integer():
                return str(int(value))
            else:
                return f"{value:.4f}"
        except:
            return str(expr)

def evaluate_expression(event=None):
    expression = entry_expression.get().strip()

    if not expression:
        messagebox.showerror("Error", "Please enter an expression to evaluate.")
        return

    try:
        if re.search(r'(<=|>=|==|!=|<|>)', expression):
            handle_relational_expression(expression, re.search(r'(<=|>=|==|!=|<|>)', expression))
        elif ',' in expression:
            solve_system_of_equations(expression)
        else:
            evaluate_arithmetic_expression(expression)
    except Exception as e:
        messagebox.showerror("Error", f"Invalid Expression: {e}")

def handle_relational_expression(expression, match):
    operator = match.group(1)
    parts = expression.split(operator)
    if len(parts) != 2:
        messagebox.showerror("Error", "Invalid relational expression format.")
        return

    left_expr = parts[0].strip()
    right_expr = parts[1].strip()

    try:
        left = sp.sympify(left_expr).evalf()
        right = sp.sympify(right_expr).evalf()

        if operator == '<':
            result = left < right
        elif operator == '>':
            result = left > right
        elif operator == '<=':
            result = left <= right
        elif operator == '>=':
            result = left >= right
        elif operator == '==':
            result = left == right
        elif operator == '!=':
            result = left != right
        else:
            messagebox.showerror("Error", "Unknown relational operator.")
            return

        show_text.configure(state='normal')
        show_text.insert(tk.END, f"> {expression}\nResult: {result}\n\n")
        show_text.configure(state='disabled')
    except Exception as e:
        messagebox.showerror("Error", f"Error evaluating relational expression: {e}")

def solve_system_of_equations(expression):
    try:
        equations = expression.split(',')
        equations = [eq.strip().replace('=', '==') for eq in equations]

        variables = set()
        for eq in equations:
            symbols_in_eq = sp.sympify(eq).free_symbols
            variables.update(symbols_in_eq)
        symbols = tuple(sorted(variables, key=lambda x: x.name))

        sympy_eqs = [sp.sympify(eq) for eq in equations]
        solution = sp.solve(sympy_eqs, symbols)

        if not solution:
            result_str = "No solution found.\n\n"
        elif isinstance(solution, dict):
            result = ', '.join([f"{key} = {format_number(value)}" for key, value in solution.items()])
            result_str = f"Solution: {result}\n\n"
        else:
            formatted_solution = []
            for sol in solution:
                if isinstance(sol, tuple):
                    sol_formatted = ', '.join([f"{var} = {format_number(val)}" for var, val in zip(symbols, sol)])
                    formatted_solution.append(sol_formatted)
                else:
                    formatted_solution.append(format_number(sol))
            result = '; '.join(formatted_solution)
            result_str = f"Solution: {result}\n\n"

        show_text.configure(state='normal')
        show_text.insert(tk.END, f"> Solve: {expression}\n{result_str}")
        show_text.configure(state='disabled')

    except Exception as e:
        messagebox.showerror("Error", f"Invalid Expression for solving: {e}")

def evaluate_arithmetic_expression(expression):
    try:
        expr = sp.sympify(expression, evaluate=True)
        result = expr.evalf(5)

        formatted_result = format_number(result)

        show_text.configure(state='normal')
        show_text.insert(tk.END, f"> {expression}\nResult: {formatted_result}\n\n")
        show_text.configure(state='disabled')
    except Exception as e:
        messagebox.showerror("Error", f"Invalid Arithmetic Expression: {e}")

def show_calculus_formulas():
    formulas_window = Toplevel(root)
    formulas_window.title("Calculus Formulas")
    formulas_window.geometry("800x600")
    formulas_window.configure(bg='#34495e')
    formulas_window.resizable(True, True)

    formulas_text = scrolledtext.ScrolledText(formulas_window, width=95, height=35, font=('Arial', 14), bg='#34495e', fg='white', wrap='word')
    formulas_text.pack(padx=10, pady=10, fill='both', expand=True)

    formulas_content = '''
Differential and Integral Calculus Formulas

Differential Calculus:
1. Derivative of f(x): f'(x) = lim(h -> 0) [(f(x+h) - f(x))/h]
2. Product Rule: (fg)' = f'g + fg'
3. Quotient Rule: (f/g)' = (f'g - fg')/g²
4. Chain Rule: (f(g(x)))' = f'(g(x)) * g'(x)
5. Second Derivative: f''(x) = d²f/dx²

Integral Calculus:
1. Definite Integral: ∫[a,b] f(x)dx = F(b) - F(a), where F'(x) = f(x)
2. Fundamental Theorem of Calculus: If F'(x) = f(x), then ∫f(x)dx = F(x) + C
3. Integration by Parts: ∫u dv = uv - ∫v du
4. Substitution Method: ∫f(g(x))g'(x)dx = ∫f(u)du, where u = g(x)
5. Area under the curve: A = ∫[a,b] f(x)dx
'''
    formulas_text.insert(tk.END, formulas_content)
    formulas_text.configure(state='disabled')

def calculate_derivative():
    expression = entry_expression.get().strip()
    if not expression:
        messagebox.showerror("Error", "Please enter a function to differentiate.")
        return

    try:
        x = sp.symbols('x')
        func = sp.sympify(expression)
        derivative = sp.diff(func, x)
        formatted_derivative = format_number(derivative)

        show_text.configure(state='normal')
        show_text.insert(tk.END, f"> d/dx ({expression})\nDerivative: {formatted_derivative}\n\n")
        show_text.configure(state='disabled')
    except Exception as e:
        messagebox.showerror("Error", f"Invalid Function: {e}")

def calculate_integral():
    expression = entry_expression.get().strip()
    if not expression:
        messagebox.showerror("Error", "Please enter a function to integrate.")
        return

    try:
        x = sp.symbols('x')
        func = sp.sympify(expression)
        integral = sp.integrate(func, x)
        formatted_integral = format_number(integral)

        show_text.configure(state='normal')
        show_text.insert(tk.END, f"> ∫({expression})dx\nIntegral: {formatted_integral} + C\n\n")
        show_text.configure(state='disabled')
    except Exception as e:
        messagebox.showerror("Error", f"Invalid Function: {e}")

def matrix_operations_window():
    matrix_window = Toplevel(root)
    matrix_window.title("Matrix Operations")
    matrix_window.geometry("800x600")
    matrix_window.configure(bg='#34495e')
    matrix_window.resizable(True, True)

    title_label = tk.Label(matrix_window, text='Matrix Operations', font=('Arial', 18, 'bold'), bg='#34495e', fg='white')
    title_label.pack(pady=10)

    instructions = tk.Label(
        matrix_window,
        text='Enter matrices separated by commas. Use ";" to separate rows and spaces to separate elements.\n\nFor example:\nMatrix A:\n1 2 3;4 5 6;7 8 9\nMatrix B:\n9 8 7;6 5 4;3 2 1',
        font=('Arial', 12),
        bg='#34495e',
        fg='white',
        justify='left',
        wraplength=760
    )
    instructions.pack(pady=10, padx=20)

    matrix_entry = scrolledtext.ScrolledText(matrix_window, width=80, height=10, font=('Arial', 12))
    matrix_entry.pack(pady=10)

    def perform_matrix_operations():
        entry = matrix_entry.get("1.0", tk.END).strip()
        if not entry:
            messagebox.showerror("Error", "Please enter matrices to operate on.")
            return

        try:
            matrices = entry.split('\n')
            A = sp.Matrix([list(map(sp.sympify, row.split())) for row in matrices[0].split(';')])
            B = sp.Matrix([list(map(sp.sympify, row.split())) for row in matrices[1].split(';')])
            sum_matrix = A + B
            product_matrix = A * B

            show_text.configure(state='normal')
            show_text.insert(tk.END, f"> A = {A}\nB = {B}\n\nA + B = {sum_matrix}\n\nA * B = {product_matrix}\n\n")
            show_text.configure(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", f"Invalid Matrix Input: {e}")

    calculate_button = tk.Button(matrix_window, text='Calculate', command=perform_matrix_operations, font=('Arial', 14), bg='#bf1011', fg='white')
    calculate_button.pack(pady=10)

root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("800x600")
root.configure(bg='#2c3e50')
root.resizable(True, True)

entry_expression = tk.Entry(root, font=('Arial', 16), bg='white', fg='black', bd=2, relief=tk.SUNKEN)
entry_expression.pack(pady=20, padx=20, fill='x')

calculate_button = tk.Button(root, text='Calculate', command=evaluate_expression, font=('Arial', 14), bg='#27ae60', fg='white')
calculate_button.pack(pady=10)

clear_button = tk.Button(root, text='Clear', command=clear_display, font=('Arial', 14), bg='#e74c3c', fg='white')
clear_button.pack(pady=10)

show_text = scrolledtext.ScrolledText(root, width=95, height=25, font=('Arial', 12), bg='#34495e', fg='white')
show_text.pack(pady=10, padx=10)
show_text.configure(state='disabled')

# Additional buttons for derivative, integral, and matrix operations
derivative_button = tk.Button(root, text='Derivative', command=calculate_derivative, font=('Arial', 14), bg='#072A6C', fg='white')
derivative_button.pack(pady=5)

integral_button = tk.Button(root, text='Integral', command=calculate_integral, font=('Arial', 14), bg='purple', fg='white')
integral_button.pack(pady=5)

matrix_button = tk.Button(root, text='Matrix Operations', command=matrix_operations_window, font=('Arial', 14), bg='cyan', fg='white')
matrix_button.pack(pady=5)

formulas_button = tk.Button(root, text='Show Calculus Formulas', command=show_calculus_formulas, font=('Arial', 14), bg='black', fg='white')
formulas_button.pack(pady=5)

root.bind('<Return>', evaluate_expression)

root.mainloop()

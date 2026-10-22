import re

class PythonToJSTranslator:
    def __init__(self):
        self.operators = {
            ' and ': ' && ',
            ' or ': ' || ',
            ' not ': ' ! ',
            ' is ': ' === ',
            ' is not ': ' !== ',
            ' None ': ' null ',
            ' True ': ' true ',
            ' False ': ' false ',
            'print': 'console.log'
        }
        self.declared_variables = set()  # Множество для отслеживания объявленных переменных
    
    def translate(self, python_code):
        """Основной метод трансляции Python в JavaScript"""
        lines = python_code.split('\n')
        js_lines = []
        indent_stack = [0]  # Стек для отслеживания уровней отступов
        self.declared_variables.clear()  # Очищаем при новом переводе
        
        for i, line in enumerate(lines):
            line = line.rstrip()
            
            # Пропускаем пустые строки и комментарии
            if not line or line.startswith('#'):
                continue
            
            # Определяем текущий отступ
            current_indent = len(line) - len(line.lstrip())
            stripped_line = line.lstrip()
            
            # Закрываем блоки, если отступ уменьшился
            while current_indent < indent_stack[-1]:
                indent_stack.pop()
                js_lines.append(' ' * indent_stack[-1] + '}')
            
            # Если отступ увеличился, начинаем новый блок
            if current_indent > indent_stack[-1]:
                indent_stack.append(current_indent)
                # Добавляем { к предыдущей строке, если она того требует
                if js_lines and not js_lines[-1].rstrip().endswith('{'):
                    last_line = js_lines[-1]
                    # Проверяем, является ли предыдущая строка началом блока
                    if any(last_line.strip().startswith(keyword) for keyword in 
                          ['if', 'for', 'while', 'function', 'else']):
                        js_lines[-1] = last_line.rstrip() + ' {'
            
            # Трансляция строки
            js_line = self.translate_line(stripped_line, current_indent)
            
            # Определяем, требует ли строка открывающей скобки
            requires_brace = (stripped_line.endswith(':') and 
                             not stripped_line.startswith('#') and
                             not any(keyword in stripped_line for keyword in ['lambda', 'print']))
            
            if js_line:
                if requires_brace:
                    # Убираем двоеточие и добавляем {
                    js_line = js_line.rstrip(':').rstrip()
                    js_lines.append(' ' * current_indent + js_line + ' {')
                else:
                    js_lines.append(' ' * current_indent + js_line)
        
        # Закрываем все оставшиеся открытые блоки в конце
        while len(indent_stack) > 1:
            indent_stack.pop()
            js_lines.append(' ' * indent_stack[-1] + '}')
        
        return '\n'.join(js_lines)
    
    def translate_line(self, line, current_indent=0):
        """Трансляция одной строки"""
        # Удаление комментариев
        line = re.sub(r'#.*$', '', line)
        line = line.strip()
        if not line:
            return ''
        
        # Трансляция различных конструкций
        if line.startswith('def '):
            return self.translate_function(line)
        elif line.startswith('if '):
            return self.translate_if(line)
        elif line.startswith('elif '):
            return self.translate_elif(line)
        elif line.startswith('else:'):
            return self.translate_else(line)
        elif line.startswith('for '):
            return self.translate_for(line)
        elif line.startswith('while '):
            return self.translate_while(line)
        elif ' = ' in line:
            return self.translate_assignment(line)
        elif line.startswith('return '):
            return self.translate_return(line)
        elif line.startswith('print('):
            return self.translate_print(line)
        else:
            return self.translate_expression(line)
    
    def translate_function(self, line):
        """Трансляция объявления функции"""
        line = line.replace('def ', 'function ')
        line = line.replace('):', ')')
        return self.replace_operators(line)

    def translate_if(self, line):
        """Трансляция условного оператора if"""
        line = line.replace('if ', 'if (')
        line = line.replace(':', ')')
        return self.replace_operators(line)

    def translate_for(self, line):
        """Трансляция цикла for"""
        # for i in range(10): -> for (i = 0; i < 10; i++)
        match = re.match(r'for\s+(\w+)\s+in\s+range\(([^)]+)\):', line)
        if match:
            var_name = match.group(1)
            range_args = match.group(2)
            
            # Добавляем переменную в множество объявленных
            self.declared_variables.add(var_name)
            
            # Разбираем аргументы range
            args = [arg.strip() for arg in range_args.split(',')]
            
            if len(args) == 1:
                # range(end)
                end = args[0]
                # Используем существующую переменную без let
                return f'for ({var_name} = 0; {var_name} < {end}; {var_name}++)'
            elif len(args) == 2:
                # range(start, end)
                start, end = args
                return f'for ({var_name} = {start}; {var_name} < {end}; {var_name}++)'
            elif len(args) == 3:
                # range(start, end, step)
                start, end, step = args
                return f'for ({var_name} = {start}; {var_name} < {end}; {var_name} += {step})'
        
        # for item in array: -> for (item of array)
        match = re.match(r'for\s+(\w+)\s+in\s+([^:]+):', line)
        if match:
            var_name = match.group(1)
            array_name = match.group(2)
            # Добавляем переменную в множество объявленных
            self.declared_variables.add(var_name)
            # Используем существующую переменную без let
            return f'for ({var_name} of {array_name})'
        
        return line.replace('for ', 'for (').replace(':', ')')

    def translate_while(self, line):
        """Трансляция цикла while"""
        line = line.replace('while ', 'while (')
        line = line.replace(':', ')')
        return self.replace_operators(line)

    def translate_elif(self, line):
        """Трансляция elif"""
        line = line.replace('elif ', '} else if (')
        line = line.replace(':', ')')
        return self.replace_operators(line)
    
    def translate_else(self, line):
        """Трансляция else"""
        return 'else'
    
    def translate_assignment(self, line):
        """Трансляция присваивания"""
        if ' = ' in line:
            parts = line.split(' = ')
            var_name = parts[0].strip()
            
            # Извлекаем чистое имя переменной (без индексов и атрибутов)
            clean_var_name = re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*', var_name)
            if clean_var_name:
                clean_var_name = clean_var_name.group(0)
                
                # Проверяем, не является ли это уже объявленной переменной
                if (clean_var_name not in self.declared_variables and 
                    not any(word in var_name for word in ['let', 'const', 'var'])):
                    line = f'let {line}'
                    self.declared_variables.add(clean_var_name)
        
        return self.replace_operators(line)
    
    def translate_return(self, line):
        """Трансляция return"""
        return self.replace_operators(line)
    
    def translate_print(self, line):
        """Трансляция print"""
        line = line.replace('print(', 'console.log(')
        return self.replace_operators(line)
    
    def translate_expression(self, line):
        """Трансляция выражений"""
        return self.replace_operators(line)
    
    def replace_operators(self, line):
        """Замена операторов Python на JavaScript"""
        # Сначала обрабатываем специальные случаи
        
        # Целочисленное деление //
        line = re.sub(r'(\w+)\s*//\s*(\w+)', r'Math.floor(\1 / \2)', line)
        
        # Возведение в степень **
        line = re.sub(r'(\w+)\s*\*\*\s*(\w+)', r'Math.pow(\1, \2)', line)
        
        # Затем заменяем операторы с пробелами
        for py_op, js_op in self.operators.items():
            line = line.replace(py_op, js_op)
        
        # Дополнительная замена для True/False/None без пробелов
        line = re.sub(r'\bTrue\b', 'true', line)
        line = re.sub(r'\bFalse\b', 'false', line)
        line = re.sub(r'\bNone\b', 'null', line)
        
        return line


def get_python_input():
    """Получение ввода Python кода от пользователя"""
    print("Код питона ниже")
    print("Введите ваш Python код (для завершения ввода введите пустую строку):")
    print("Или введите 'EXAMPLE' для использования тестового примера")
    
    lines = []
    while True:
        try:
            line = input()
            if line == "":
                break
            if line.upper() == "EXAMPLE":
                return get_example_code()
            lines.append(line)
        except (EOFError, KeyboardInterrupt):
            print("\nВвод прерван")
            break
    
    return '\n'.join(lines)

def get_example_code():
    """Возвращает тестовый пример"""
    return '''i = 0
for i in range(20):
    i += 1
    while i < 10:
        print(i * i)
        i += 1
    if i > 10:
        print(i // i)
if i or 1 == True:
    print("Yes")'''

def save_to_file(content, filename="translation_result.txt"):
    """Сохранение результата в файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Ошибка при сохранении в файл: {e}")
        return False


def main():
    """Основная функция программы"""
    translator = PythonToJSTranslator()
    
    # Получаем ввод от пользователя
    python_code = get_python_input()
    
    if not python_code.strip():
        print(" Не введен Python код!")
        return
    
    # ТРАНСЛИРУЕМ код в JavaScript
    js_code = translator.translate(python_code)
    
    # Показываем результат в консоли
    print("\nджээскод")
    print("```javascript")
    print(js_code)
    print("```")
    
    # Сохраняем в файл
    output_content = "// Транслировано из Python в JavaScript\n\n"
    output_content += "питон:\n```python\n"
    output_content += python_code + "\n```\n\n"
    output_content += "джээс:\n```javascript\n"
    output_content += js_code + "\n```"
    
    if save_to_file(output_content):
        print("Результат сохранен в файл: 'translation_result.txt'")
    else:
        print("Нет.")


if __name__ == "__main__":
    print("Транслятор из питона в джээс")
    
    # Запускаем основной режим с вводом от пользователя
    main()
    
    print("\n Всё гуд")
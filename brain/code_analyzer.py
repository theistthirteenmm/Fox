"""
🔍 تحلیلگر کد روباه
تحلیل، بررسی و اصلاح کدهای برنامه‌نویسی
"""

import ast
import re
import json
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import subprocess
import tempfile
import os

class CodeAnalyzer:
    def __init__(self):
        self.supported_languages = {
            'python': ['.py'],
            'javascript': ['.js', '.jsx', '.ts', '.tsx'],
            'java': ['.java'],
            'cpp': ['.cpp', '.cc', '.cxx'],
            'c': ['.c'],
            'html': ['.html', '.htm'],
            'css': ['.css'],
            'sql': ['.sql'],
            'json': ['.json'],
            'xml': ['.xml']
        }
        
        self.common_issues = {
            'python': [
                'IndentationError',
                'SyntaxError', 
                'NameError',
                'TypeError',
                'ValueError'
            ],
            'javascript': [
                'SyntaxError',
                'ReferenceError',
                'TypeError',
                'undefined variables'
            ]
        }
    
    def detect_language(self, code: str, filename: str = None) -> str:
        """تشخیص زبان برنامه‌نویسی"""
        if filename:
            ext = os.path.splitext(filename)[1].lower()
            for lang, extensions in self.supported_languages.items():
                if ext in extensions:
                    return lang
        
        # تشخیص بر اساس محتوا
        if 'def ' in code and 'import ' in code:
            return 'python'
        elif 'function' in code and ('var ' in code or 'let ' in code):
            return 'javascript'
        elif 'public class' in code and 'public static void main' in code:
            return 'java'
        elif '#include' in code and 'int main' in code:
            return 'cpp'
        elif '<html' in code.lower() and '</html>' in code.lower():
            return 'html'
        elif 'SELECT' in code.upper() and 'FROM' in code.upper():
            return 'sql'
        
        return 'unknown'
    def analyze_python_code(self, code: str) -> Dict[str, Any]:
        """تحلیل کد پایتون"""
        issues = []
        suggestions = []
        
        try:
            # بررسی syntax
            ast.parse(code)
            syntax_valid = True
        except SyntaxError as e:
            syntax_valid = False
            issues.append({
                'type': 'SyntaxError',
                'line': e.lineno,
                'message': str(e),
                'severity': 'high'
            })
        
        # بررسی مشکلات رایج
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            # بررسی import های غیرضروری
            if line_stripped.startswith('import ') or line_stripped.startswith('from '):
                if line_stripped not in code[code.find(line_stripped) + len(line_stripped):]:
                    suggestions.append({
                        'type': 'unused_import',
                        'line': i,
                        'message': 'Import احتمالاً استفاده نشده',
                        'severity': 'low'
                    })
            
            # بررسی متغیرهای تعریف نشده
            if '=' in line_stripped and not line_stripped.startswith('#'):
                var_match = re.match(r'(\w+)\s*=', line_stripped)
                if var_match:
                    var_name = var_match.group(1)
                    if var_name not in code[:code.find(line)]:
                        suggestions.append({
                            'type': 'new_variable',
                            'line': i,
                            'message': f'متغیر جدید: {var_name}',
                            'severity': 'info'
                        })
        
        return {
            'language': 'python',
            'syntax_valid': syntax_valid,
            'issues': issues,
            'suggestions': suggestions,
            'complexity': self._calculate_complexity(code),
            'lines_count': len(lines)
        }
    
    def analyze_javascript_code(self, code: str) -> Dict[str, Any]:
        """تحلیل کد جاوااسکریپت"""
        issues = []
        suggestions = []
        
        # بررسی مشکلات رایج JS
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            # بررسی استفاده از var به جای let/const
            if line_stripped.startswith('var '):
                suggestions.append({
                    'type': 'use_let_const',
                    'line': i,
                    'message': 'بهتر است از let یا const استفاده کنید',
                    'severity': 'medium'
                })
            
            # بررسی == به جای ===
            if '==' in line_stripped and '===' not in line_stripped:
                suggestions.append({
                    'type': 'strict_equality',
                    'line': i,
                    'message': 'از === به جای == استفاده کنید',
                    'severity': 'medium'
                })
        
        return {
            'language': 'javascript',
            'syntax_valid': True,  # نیاز به parser پیچیده‌تر
            'issues': issues,
            'suggestions': suggestions,
            'complexity': self._calculate_complexity(code),
            'lines_count': len(lines)
        }
    def _calculate_complexity(self, code: str) -> str:
        """محاسبه پیچیدگی کد"""
        lines = len(code.split('\n'))
        
        if lines < 10:
            return 'ساده'
        elif lines < 50:
            return 'متوسط'
        elif lines < 200:
            return 'پیچیده'
        else:
            return 'خیلی پیچیده'
    
    def suggest_improvements(self, code: str, language: str) -> List[str]:
        """پیشنهاد بهبودها"""
        suggestions = []
        
        if language == 'python':
            # بررسی PEP 8
            if '\t' in code:
                suggestions.append('از 4 space به جای tab استفاده کنید')
            
            if len([l for l in code.split('\n') if len(l) > 79]) > 0:
                suggestions.append('خطوط بلندتر از 79 کاراکتر را کوتاه کنید')
        
        elif language == 'javascript':
            if 'var ' in code:
                suggestions.append('از let/const به جای var استفاده کنید')
            
            if code.count(';') < code.count('\n') * 0.5:
                suggestions.append('semicolon ها را فراموش نکنید')
        
        return suggestions
    
    def fix_common_issues(self, code: str, language: str) -> str:
        """اصلاح مشکلات رایج"""
        fixed_code = code
        
        if language == 'python':
            # اصلاح indentation
            lines = fixed_code.split('\n')
            fixed_lines = []
            
            for line in lines:
                # تبدیل tab به space
                fixed_line = line.replace('\t', '    ')
                fixed_lines.append(fixed_line)
            
            fixed_code = '\n'.join(fixed_lines)
        
        elif language == 'javascript':
            # اصلاح var به let
            fixed_code = re.sub(r'\bvar\b', 'let', fixed_code)
            
            # اصلاح == به ===
            fixed_code = re.sub(r'(?<!=)==(?!=)', '===', fixed_code)
        
        return fixed_code
    
    def analyze_code(self, code: str, filename: str = None) -> Dict[str, Any]:
        """تحلیل کامل کد"""
        language = self.detect_language(code, filename)
        
        if language == 'python':
            analysis = self.analyze_python_code(code)
        elif language == 'javascript':
            analysis = self.analyze_javascript_code(code)
        else:
            analysis = {
                'language': language,
                'syntax_valid': None,
                'issues': [],
                'suggestions': [],
                'complexity': self._calculate_complexity(code),
                'lines_count': len(code.split('\n'))
            }
        
        # اضافه کردن پیشنهادات عمومی
        general_suggestions = self.suggest_improvements(code, language)
        analysis['general_suggestions'] = general_suggestions
        
        # اضافه کردن کد اصلاح شده
        analysis['fixed_code'] = self.fix_common_issues(code, language)
        
        return analysis

# نمونه سراسری
code_analyzer = CodeAnalyzer()
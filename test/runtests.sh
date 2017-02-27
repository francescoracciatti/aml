#!/bin/bash

coverage run -m unittest discover -v -p '*_test.py'

coverage report --omit=/usr/local/lib/python3.5/dist-packages/ply/lex.py,/usr/local/lib/python3.5/dist-packages/ply/yacc.py,keywords_test.py,lexer_test.py,parser_test.py,statements_test.py,types_test.py,/home/francesco/Desktop/aml/aml/parsetab.py,/home/francesco/Desktop/aml/aml/lexer/__init__.py,/home/francesco/Desktop/aml/aml/model/__init__.py,/home/francesco/Desktop/aml/aml/parser/__init__.py,/usr/local/lib/python3.5/dist-packages/ply/__init__.py


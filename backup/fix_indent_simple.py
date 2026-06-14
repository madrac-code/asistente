#!/usr/bin/env python3
# Simple script to fix indentation error

import sys

# Read the file
with open('D:\madrac-asistente\ui\commands\__init__.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the indentation error
content = content.replace('\t\t\t\tthread.start()', '\t\tthread.start()')

# Write the file back
with open('D:\madrac-asistente\ui\commands\__init__.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed indentation error in ui/commands/__init__.py")

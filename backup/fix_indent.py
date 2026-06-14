#!/usr/bin/env python3
# Simple script to fix indentation error

# Read the file
with open('D:\madrac-asistente\ui\commands\__init__.py', 'r') as f:
    lines = f.readlines()

# Fix the indentation error
for i, line in enumerate(lines):
    if '\\t\\t\\t\\tthread.start()' in line:
        lines[i] = line.replace('\\t\\t\\t\\tthread.start()', '\\t\\tthread.start()')

# Write the file back
with open('D:\madrac-asistente\ui\commands\__init__.py', 'w') as f:
    f.writelines(lines)

print("Fixed indentation error in ui/commands/__init__.py")

import os

files = ['agent.py', 'main.py', 'telegram_bot.py', 'tools.py']

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    for line in lines:
        s = line.rstrip()
        if not s:
            # It's a blank line now.
            # If it had no spaces to begin with (len <= 2 for '\n' or '\r\n') keep it.
            # Otherwise, it might be a line that formerly contained a comment and spaces.
            # Actually, standard python code shouldn't have trailing spaces on blank lines anyway.
            # Let's just keep lines that were originally completely empty, and drop lines 
            # that became empty because we removed a comment. 
            # When tokenize removes a comment, the line still has space/tab from indentation.
            if len(line) <= 2: 
                cleaned_lines.append('\n')
        else:
            cleaned_lines.append(s + '\n')
            
    with open(file, 'w', encoding='utf-8', newline='') as f:
        f.writelines(cleaned_lines)

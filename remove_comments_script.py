import tokenize
import sys
import os

def remove_comments(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()

    # We can also do a simple regex but tokenize is safer for Python
    # However, untokenize might format code differently.
    # To keep exact formatting, we manually reconstruct:
    # (Adapted from standard comment stripping recipes)
    
    with open(file_path, 'rb') as f:
        try:
            tokens = tokenize.tokenize(f.readline)
            out_tokens = []
            for tok in tokens:
                if tok.type != tokenize.COMMENT:
                    out_tokens.append(tok)
            # untokenize returns bytes
            out_code = tokenize.untokenize(out_tokens).decode('utf-8')
        except tokenize.TokenError:
            return  # parse error, skip
            
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        f.write(out_code)

for file in ['agent.py', 'main.py', 'telegram_bot.py', 'tools.py']:
    print(f"Removing comments from {file}")
    remove_comments(file)


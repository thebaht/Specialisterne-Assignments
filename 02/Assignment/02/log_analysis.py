


# Explicit closing____________________________________________________

log = open('app_log.txt', 'r')
output = open('filtered_log.txt', 'w')
try:
    for entry in log:
        if any(keyword in entry for keyword in ('ERROR', 'WARNING')):
                output.write(entry + '\n')
finally:
    log.close()
    output.close()
    

# implicit closing____________________________________________________
with open('app_log.txt', 'r') as log:
    with open('filtered_log.txt', 'w') as output:
        for entry in log:
            if any(keyword in entry for keyword in ('ERROR', 'WARNING')):
                output.write(entry + '\n')


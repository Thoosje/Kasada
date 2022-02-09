counter = 0
test = [ 'counter' ]
locals()[test[0]] = locals()[test[0]] + 1
print(counter)
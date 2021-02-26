from tasks import add

result = add.delay(4,4)
print('Is result ready: %s' % result.ready())

print('task result is: %s' % result.get(propagate=False))
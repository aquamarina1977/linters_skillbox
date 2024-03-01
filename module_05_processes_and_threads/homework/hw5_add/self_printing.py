"""
Напишите код, который выводит сам себя.
Обратите внимание, что скрипт может быть расположен в любом месте.
"""

result = 0
for n in range(1, 11):
    result += n ** 2

# Secret magic code
with open(__file__, 'r') as f:
    code = f.read()

print(code)

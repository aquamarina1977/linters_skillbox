"""
С помощью команды ps можно посмотреть список запущенных процессов.
С флагами aux эта команда выведет информацию обо всех процессах, запущенных в системе.

Запустите эту команду и сохраните выданный результат в файл:

$ ps aux > output_file.txt

Столбец RSS показывает информацию о потребляемой памяти в байтах.

Напишите функцию get_summary_rss, которая на вход принимает путь до файла с результатом выполнения команды ps aux,
а возвращает суммарный объём потребляемой памяти в человекочитаемом формате.
Это означает, что ответ надо перевести в байты, килобайты, мегабайты и так далее.
"""


def get_summary_rss(ps_output_file_path: str) -> str:
    with open(ps_output_file_path, 'r', encoding='utf8') as output_file:
        lines = output_file.readlines()[1:]
        count = 0
        for line in lines:
            columns = line.split()
            count += int(columns[5])
        if len(str(count)) <= 3:
            return f'{count}Б'
        elif len(str(count)) > 3:
            return f'{round(count/1000)}Кб'
        elif len(str(count)) > 6:
            return f'{round(count/1000000)}Мб'
        elif len(str(count)) > 9:
            return f'{round(count/1000000000)}Гб'

if __name__ == '__main__':
    path: str = '/home/marina/output_file.txt'
    summary_rss: str = get_summary_rss(path)
    print(summary_rss)

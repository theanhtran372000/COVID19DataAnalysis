import re


def get_table_name(script):
    text = script.text

    keyword = 'Highcharts.chart\('
    start_indexs = [m.start() for m in re.finditer(keyword, text)]

    names = []
    for start_index in start_indexs:
        end_index = text.find(',', start_index + len(keyword))

        names.append(text[start_index + len(keyword): end_index - 1])

    return names


def get_date_data(script):
    text = script.text

    keyword = 'xAxis'
    start_indexs = [m.start() for m in re.finditer(keyword, text)]

    dates = []
    for start_index in start_indexs:
        index_1 = text.find('[', start_index + len(keyword))
        index_2 = text.find(']', start_index + len(keyword))

        data = text[index_1 + 1: index_2]
        data = [d for d in data.split('"') if d != ',' and d != ""]
        dates.append(data)

    return dates


def get_count_data(script):
    text = script.text

    keyword = 'data'
    start_indexs = [m.start() for m in re.finditer(keyword, text)]

    counts = []
    for start_index in start_indexs:
        index_1 = text.find('[', start_index + len(keyword))
        index_2 = text.find(']', start_index + len(keyword))

        data = text[index_1 + 1: index_2]

        nums = [float(d) if d.isnumeric()
                else 0 for d in data.split(',')]
        counts.append(nums)

    return counts

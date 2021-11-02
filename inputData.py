import pandas as pd

df = pd.read_excel('\отчеты\input1.xlsx', 0)

# print(df)

listINN = df['INN'].tolist()
# print(listINN)

count = 0
list2 = df['К-ть правильних ІПН'].tolist()
for i in list2:
    if i == 1:
        count += 1
# print(count)

segment = df.loc[(df['К-ть правильних ІПН'] == 1) & (df['Сегмент боргу'] == '0 - 30 000')]
print(segment.shape[0])


# workbook = openpyxl.load_workbook('\отчеты\input1.xlsx')
#
# sheet = workbook['Аркуш1']
#
# print(workbook.sheetnames)
#
# cell = sheet['A1'].value
# print(cell)
def segmentINP(segment):
    count_ipn = df.loc[(df['Сегмент боргу'] == segment)]
    countInp = count_ipn.shape[0]

    return countInp


print(segmentINP('250 000 - 500 000'))


def segmentRightINP(segment, inp=1):
    count_ipn = df.loc[(df['К-ть правильних ІПН'] == inp) & (df['Сегмент боргу'] == segment)]
    countInp = count_ipn.shape[0]

    return countInp


def segmentINPfree(segment, inp=1):
    count_ipn = df.loc[(df['К-ть перевірених ІПН по безкоштовній перевірці'] == inp)
                       & (df['Сегмент боргу'] == segment)]
    countInp = count_ipn.shape[0]

    return countInp


print(segmentINPfree('250 000 - 500 000'))


def segmentINPfree(segment, inp=1):
    count_ipn = df.loc[(df['К-ть ІПН з майном по безкоштовній перевірці'] == inp)
                       & (df['Сегмент боргу'] == segment)]
    countInp = count_ipn.shape[0]

    return countInp


print(segmentINPfree('250 000 - 500 000'))

segmenlist = ['500 000+', '250 000 - 500 000',
              '100 000 - 250 000', '50 000 - 100 000', '30 000 - 50 000', '0 - 30 000']
while True:
    print("1. выбор сегмента 500 000+")
    print("2. выбор  250 000 - 500 000")
    print("3. выбор 100 000 - 250 000")
    print("4. выбор сегмента 50 000 - 100 000")
    print("5. выбор  30 000 - 50 000")
    print("6. выбор 0 - 30 000")
    print("0. выйти из программы")
    cmd = int(input("Выберите пункт: "))

    if cmd == 1:
        elem = segmenlist[0]
        e = segmentRightINP(elem)
        print(e)
    elif cmd == 2:
        elem = segmenlist[1]
        e = segmentRightINP(elem)
        print(e)
    elif cmd == 3:
        elem = segmenlist[2]
        e = segmentRightINP(elem)
        print(e)
    elif cmd == 4:
        elem = segmenlist[3]
        e = segmentRightINP(elem)
        print(e)
    elif cmd == 5:
        elem = segmenlist[4]
        e = segmentRightINP(elem)
        print(e)
    elif cmd == 6:
        elem = segmenlist[5]
        e = segmentRightINP(elem)
        print(e)
    elif cmd == 0:
        break
    else:
        print("Вы ввели не правильное значение")

# options = ['Do Something 1', 'Do Something 2', 'Do Something 3']
# choice = enquiries.choose('Choose one of these options: ', options)
# print(choice)

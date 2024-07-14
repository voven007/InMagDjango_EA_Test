min = 1
max = 100


def algoritm(number):
    number1 = number + 1
    sequence = ''
    for x in range(1, number1):
        x1 = x + 1
        for y in range(1, x1):
            sequence += str(x)
    return (sequence)


def test(number_checked):
    if number_checked.isdigit() == True:
        number_checked = int(number_checked)
        if number_checked < min or number_checked > max:
            return ('Введенное значение вне указанного диапазона')
        else:
            return algoritm(number_checked)
    else:
        return ('Введенне значение не является числом')


def main():
    number = input(f'Введите число от {min} до {max}: ')
    the_list = test(number)
    print(the_list)


if __name__ == '__main__':
    main()

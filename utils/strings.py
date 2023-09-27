def is_positive_number(value):
    try:
        number_string = float(value)
    except Exception as e:
        print(e)
        # para ver a classe do erro
        # print(e.__class__.__name__)
        return False

    return number_string > 0

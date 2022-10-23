from django import template


class MatFilterException(Exception):
    pass

register = template.Library()


@register.filter()
def filter_mata(text):

    try:
        if type(text) is not str:
            raise MatFilterException("Фильтр применяется к переменной нестрокового типа")

        mat = ["редиска",
               "прописка",
               "давление",
               "кризис",
               "гастроли"
               ]

        text_f = text
        for i in mat:
            text_f = text_f.replace(i, i[0] + '*' * (len(i) - 1))
            text_f = text_f.replace(i.title(), i.title()[0] + '*' * (len(i) - 1))

        return (text_f)


    except MatFilterException as e:
            print('MatFilterException: ', e)
            return (text)

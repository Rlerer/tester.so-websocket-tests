# tester.so-websocket-tests
Отчет о тестах allure serve ./allure-results




allure generate --clean
allure serve
Ошибка в ТЗ:
# id: string, идентификатор запроса
# method: update
# name: string, Имя юзера
# surname: string, Фамилия юзера
# phone: string, unique, primary key, Телефон юзера
# age: integer, Возраст юзера

# Ответ: - status: success | failure
# method: delete     -----                        должен быть UPDATE
# id: id запроса


    вопрос к документации нахуя поиск только по имени
    на голый селект крашится 
    сделать енам для методов запросов
    "reason": "[json.exception.out_of_range.403] key 'age' not found",
    "reason": "[json.exception.out_of_range.403] key 'name' not found"
    ...
    "reason": "[json.exception.type_error.302] type must be number, but is string",
    "reason": "[json.exception.parse_error.101] parse error at line 6, column 5: syntax error while parsing object key - unexpected '}'; expected string literal",
    "reason": "[json.exception.parse_error.101] parse error at line 5, column 15: syntax error while parsing value - unexpected ','; expected '[', '{', or a literal"
    "reason": "[json.exception.type_error.302] type must be string, but is null"
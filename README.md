# mipt-python-encryption
Проект для курса по питону в МФТИ, 2021

Это проект по реализации криптографического алгоритма RSA на чистом питоне. Для того, чтобы проект запустился,
не надо ставить никаких внешних библиотек.

## Структура проекта

Для провкрки корректности работы, используется библиотека unittest. Запуск тестов осуществляется
через
````
python3 test.py
````

В rsa/primes.py лежит реализация алгоритма Миллера — Рабина для генерации простых чисел, а в
rsa/rsa.py — реализация самого алгоритма RSA. Слишком затратно было бы писать документацию к
учебному проекту, поэтому вместо неё можно использовать файл test.py в качестве источника примеров
использования методов.
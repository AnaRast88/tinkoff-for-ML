import argparse
import re
import random as rnd
import pickle

class Model(object):
    def __init__(self):
        # задаем в конструкторе значение N и пустой словарь для префиксов
        self.dictPrefix = dict()
        self.N = 1

    def fit(self, text_path, N):
        '''Ф-я для обучения модели. На вход примаются путь к файлу и N'''

        self.N = N
        if text_path != None:    # если передали путь к файлу с текстом, считываем текст
            with open(text_path, 'r', encoding='utf-8') as file:
                text = file.read()
        else:
            text = input("Введите текст для обучения модели: ")    # иначе просим ввести текст вручную

        text = text.lower()    # приводим к нижнему регистру
        text_prep = re.sub(r'[*—,()]', '', text)    # удалим внутри предлож-й неалфав-е символы
        text_prep = re.sub(r'[?!]', '.', text_prep)    # заменим знаки "?!" на точку,
                                                       # для удобного разделения на предложения
        listSentence = text_prep.split('.')    # делим текст на предложения, чтобы
                                               # слова из разных предложений не сопоставлялись

        for sentence in listSentence:    # проходим по списку предложений
            listWord = sentence.split()    # делим предложение на слова
            n = len(listWord)
            for i in range(n - N + 1):
                prefix = tuple(listWord[i:i + N - 1])    # берем префикс в виде кортежа слов.
                if prefix not in self.dictPrefix:        # если такого префикса ещё не было,
                    self.dictPrefix[prefix] = dict()     # добавляем его в словарь и присваем ему пустой словарь.
                dcp = self.dictPrefix[prefix]    # обращаемся к словарю для слов, следующих после префикса.
                t = listWord[i + N - 1]          # берем слово идущее после префикса,
                if t in dcp.keys():              # если оно есть в словаре, то +1
                    dcp[t] += 1
                if t not in dcp.keys():          # если нет, то 1
                    dcp[t] = 1

        for key in self.dictPrefix.keys():
            # заменяем количество слов на их вероятность
            # путем деления кол-ва повторений (val) слова (k) после префикса
            # на общее кол-во повторений префикса в тексте (count)
            count = sum(self.dictPrefix[key].values())
            self.dictPrefix[key] = {k: val / count for k, val in self.dictPrefix[key].items()}

    def generate(self, length, prefix = None):
        '''Ф-я генерации последовательности слов.
        На вход принимаются длина послед-ти и префикс'''

        if prefix == None:      # если префикс не передали, то рандомно берем из словаря
            prefix_tup = rnd.choices(list(self.dictPrefix.keys()), k=1)[0]
        else:
            prefix = prefix.lower()     # если передали, то приводим к нижнему регистру,
            prefix_tup = tuple(prefix.split())    # разбиваем префикс на слова и формируем кортеж

        new_sentence = ' '.join(prefix_tup)    # присваиваем префикс генерируемому предложению
        for i in range(length):
            if prefix_tup in self.dictPrefix:               # если префикс есть в словаре,
                dictWord = self.dictPrefix[prefix_tup]      # берем словарь слов, следующих за ним,
                max_p = max(dictWord.values())              # берем макс-ю вероятность,
                dict_max = {k: v for k, v in dictWord.items() if v == max_p}     # выбираем слова с макс.вероят-ю,
                next = rnd.choices(list(dict_max.keys()), k=1)[0]            # рандомно выбираем из них одно,
                new_sentence += (" " + next)                               # конкатенируем с предложением,
                prefix_tup = prefix_tup[1:self.N - 1] + (next,)          # меняем префикс.
            else:
                break    # если префикс не встречался в тексте, то завершаем генерацию
        return new_sentence

    def save(self, path):
        '''Ф-я сохранения модели. На вход принимается путь к файлу для сохранения'''

        with open(path, 'wb') as f:
            pickle.dump(self, f)    # сохраняем объект класса в файл
            print("Модель сохранена успешно.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Model for generating sentences')
    parser.add_argument('--input_dir', type=str, help='Input dir for data')
    parser.add_argument('model', type=str, help='The path to the file to save the model')
    namespace = parser.parse_args()

    N = 3
    model = Model()    # создаем объект класса
    model.fit(namespace.input_dir, N)    # вызываем метод обучения
    model.save(namespace.model)        # вызываем метод сохранения
import argparse
import pickle
from train import Model
import random as rnd

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Model for generating sentences')
    parser.add_argument('model', type=str, help='The path to the saved model')
    parser.add_argument('--prefix', type=str, help='Initial word (default: random word from the text)')
    parser.add_argument('length', type=int, help='Sequence length')
    namespace = parser.parse_args()

    with open(namespace.model, 'rb') as f:
        model = pickle.load(f)     # загружаем предварительно обученный объект класса Model
    sentence = model.generate(namespace.length, namespace.prefix)     # генерируем предложение
    print(sentence)
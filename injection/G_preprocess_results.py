import os, pickle

from eda_tools.preprocess_stopwords import apply_stopwords, preprocess_non_printable_characters
from utils.config import FEATURES_PATH



# leer el objeto results_....pkl



# crear una lista para cada pdf, que contenga el contenido -> tupla[-1]

# considerar un bucle para simple, uno para grouped


# aplicar el metodo apply_stopwords a cada lista


# *crear los bucles para generar los langchaing.Document

# guardar la feature content serializada en la carpeta '.serialized_features' con el nombre 'feature_contents.pkl'

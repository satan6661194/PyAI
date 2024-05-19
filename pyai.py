import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import seaborn as sns

class PyAI:
    def __init__(self):
        self.dados = None

    def load_data(self, filepath):
        self.dados = pd.read_csv(filepath)
        return self

    def limpar_nulos(self):
        self.dados.dropna(inplace=True)
        return self

    def normalizar(self):
        scaler = StandardScaler()
        self.dados = pd.DataFrame(scaler.fit_transform(self.dados), columns=self.dados.columns)
        return self

    def codificar_categoricos(self):
        le = LabelEncoder()
        for coluna in self.dados.select_dtypes(include=['object']).columns:
            self.dados[coluna] = le.fit_transform(self.dados[coluna])
        return self

    def criar_caracteristica(self, novo_nome, operacao):
        self.dados[novo_nome] = operacao(self.dados)
        return self

    def selecionar_caracteristicas(self, colunas):
        self.dados = self.dados[colunas]
        return self

    def bin(coluna, bins):
        def func(dados):
            return pd.cut(dados[coluna], bins=bins, labels=False)
        return func

    def balancear(self, metodo="SMOTE"):
        X = self.dados.iloc[:, :-1].values
        y = self.dados.iloc[:, -1].values

        if metodo == "SMOTE":
            sm = SMOTE()
            X_res, y_res = sm.fit_resample(X, y)
            self.dados = pd.DataFrame(X_res, columns=self.dados.columns[:-1])
            self.dados['target'] = y_res

        return self

    def model(tipo, **kwargs):
        def decorator(func):
            def wrapper(*args, **kwargs_inner):
                dados = args[0].dados
                X = dados.iloc[:, :-1].values
                y = dados.iloc[:, -1].values
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                if tipo == "rede_neural":
                    modelo = tf.keras.models.Sequential()
                    for camada in kwargs.get('camadas', []):
                        modelo.add(tf.keras.layers.Dense(camada, activation='relu'))
                    modelo.add(tf.keras.layers.Dense(1, activation='sigmoid'))
                    modelo.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
                    modelo.fit(X_train, y_train, epochs=kwargs_inner.get('epocas', 10), batch_size=kwargs_inner.get('batch_size', 32))
                    
                    resultado = modelo.evaluate(X_test, y_test)
                    return {"modelo": modelo, "resultado": resultado}
                elif tipo == "arvore_decisao":
                    modelo = DecisionTreeClassifier(max_depth=kwargs.get('profundidade_maxima', None))
                    modelo.fit(X_train, y_train)
                    precisao = modelo.score(X_test, y_test)
                    return {"modelo": modelo, "resultado": precisao}
                elif tipo == "svm":
                    modelo = SVC(kernel=kwargs.get('kernel', 'linear'), C=kwargs.get('C', 1.0))
                    modelo.fit(X_train, y_train)
                    precisao = modelo.score(X_test, y_test)
                    return {"modelo": modelo, "resultado": precisao}
            return wrapper
        return decorator

    def avaliar(self, metrica):
        if metrica == "precisao":
            return self["resultado"][1] * 100  # accuracy

    def validacao_cruzada(self, folds, metrica):
        X = self.dados.iloc[:, :-1].values
        y = self.dados.iloc[:, -1].values
        scores = cross_val_score(self["modelo"], X, y, cv=folds, scoring=metrica)
        return np.mean(scores) * 100

    def plotar(self, tipo):
        if tipo == "curva_de_aprendizado":
            plt.plot(self['resultado'].history['accuracy'])
            plt.plot(self['resultado'].history['val_accuracy'])
            plt.title('Curva de Aprendizado')
            plt.ylabel('Precisão')
            plt.xlabel('Época')
            plt.legend(['Treino', 'Validação'], loc='upper left')
            plt.show()
        elif tipo == "matriz_de_confusao":
            sns.heatmap(self['matriz_de_confusao'], annot=True, fmt="d", cmap="Blues")
            plt.title('Matriz de Confusão')
            plt.ylabel('True label')
            plt.xlabel('Predicted label')
            plt.show()

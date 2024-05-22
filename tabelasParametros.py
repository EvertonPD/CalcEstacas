import pandas as pd


def paramAokiTab():

    coefKeAlfa = [
                  [1, 'Areia', 1000.0, 0.014],
                  [12, 'Areia Siltosa', 800.0, 0.02],
                  [123, 'Areia Siltoargilosa', 700.0, 0.024],
                  [13, 'Areia Argilosa', 600.0, 0.03],
                  [132, 'Areia Argilossiltosa', 500.0, 0.028],
                  [2, 'Silte', 400.0, 0.03],
                  [21, 'Silte Arenoso', 550.0, 0.022],
                  [213, 'Silte Arenoargiloso', 450.0, 0.028],
                  [23, 'Silte Argiloso', 230.0, 0.034],
                  [231, 'Silte Argiloarenoso', 250.0, 0.03],
                  [3, 'Argila', 200.0, 0.06],
                  [31, 'Argila Arenosa', 350.0, 0.024],
                  [312, 'Argila Arenossiltosa', 300.0, 0.028],
                  [32, 'Argila Siltosa', 220.0, 0.04],
                  [321, 'Argila Siltoarenosa', 330.0, 0.03]
                  ]


    dfParamAoki = pd.DataFrame(coefKeAlfa, columns=['Código', 'Solo', 'K (kPa)', 'Alfa'])


    return dfParamAoki


def fatorCorrAoki():

    corrAoki = [
        ['Escavada', 3 , 6],
        ['Raiz', 2, 4],
        ['HCM', 2, 4]
    ]

    dfCorrecaoAoki = pd.DataFrame(corrAoki, columns=['Tipo de Estaca', 'F1', 'F2'])


    return dfCorrecaoAoki



def paramDecQuarTab():

    coefSoloC = [
        [1, 'Areia', 400.0],
        [12, 'Areia Siltosa', 400.0],
        [123, 'Areia Siltoargilosa', 400.0],
        [13, 'Areia Argilosa', 400.0],
        [132, 'Areia Argilossiltosa', 400.0],
        [2, 'Silte', 200.0],
        [21, 'Silte Arenoso', 250.0],
        [213, 'Silte Arenoargiloso', 250.0],
        [23, 'Silte Argiloso', 200.0],
        [231, 'Silte Argiloarenoso', 200.0],
        [3, 'Argila', 120.0],
        [31, 'Argila Arenosa', 120.0],
        [312, 'Argila Arenossiltosa', 120.0],
        [32, 'Argila Siltosa', 120.0],
        [321, 'Argila Siltoarenosa', 120.0]
    ]

    dfCoefSoloC = pd.DataFrame(coefSoloC, columns=['Código', 'Tipo de Solo', 'C (kPa)'])

    return dfCoefSoloC


def fatorAlfaDecQuar():

    coefAlfa = [
        [1, 'Areia', 0.5, 0.5, 0.3],
        [12, 'Areia Siltosa', 0.5, 0.5, 0.3],
        [123, 'Areia Siltoargilosa', 0.5, 0.5, 0.3],
        [13, 'Areia Argilosa', 0.5, 0.5, 0.3],
        [132, 'Areia Argilossiltosa', 0.5, 0.5, 0.3],
        [2, 'Silte', 0.6, 0.6, 0.3],
        [21, 'Silte Arenoso', 0.6, 0.6, 0.3],
        [213, 'Silte Arenoargiloso', 0.6, 0.6, 0.3],
        [23, 'Silte Argiloso', 0.6, 0.6, 0.3],
        [231, 'Silte Argiloarenoso', 0.6, 0.6, 0.3],
        [3, 'Argila', 0.85, 0.85, 0.3],
        [31, 'Argila Arenosa', 0.85, 0.85, 0.3],
        [312, 'Argila Arenossiltosa', 0.85, 0.85, 0.3],
        [32, 'Argila Siltosa', 0.85, 0.85, 0.3],
        [321, 'Argila Siltoarenosa', 0.85, 0.85, 0.3]
    ]

    dfCoefAlfa = pd.DataFrame(coefAlfa, columns=['Código', 'Tipo de Solo', 'Escavada', 'Raiz', 'HCM'])

    return dfCoefAlfa


def fatorBetaDecQuar():

    coefBeta = [
        [1, 'Areia', 0.5, 1.5, 1.0],
        [12, 'Areia Siltosa', 0.5, 1.5, 1.0],
        [123, 'Areia Siltoargilosa', 0.5, 1.5, 1.0],
        [13, 'Areia Argilosa', 0.5, 1.5, 1.0],
        [132, 'Areia Argilossiltosa', 0.5, 1.5, 1.0],
        [2, 'Silte', 0.65, 1.5, 1.0],
        [21, 'Silte Arenoso', 0.65, 1.5, 1.0],
        [213, 'Silte Arenoargiloso', 0.65, 1.5, 1.0],
        [23, 'Silte Argiloso', 0.65, 1.5, 1.0],
        [231, 'Silte Argiloarenoso', 0.65, 1.5, 1.0],
        [3, 'Argila', 0.8, 1.5, 1.0],
        [31, 'Argila Arenosa', 0.8, 1.5, 1.0],
        [312, 'Argila Arenossiltosa', 0.8, 1.5, 1.0],
        [32, 'Argila Siltosa', 0.8, 1.5, 1.0],
        [321, 'Argila Siltoarenosa', 0.8, 1.5, 1.0]
    ]

    dfCoefBeta = pd.DataFrame(coefBeta, columns=['Código', 'Tipo de Solo', 'Escavada', 'Raiz', 'HCM'])

    return dfCoefBeta


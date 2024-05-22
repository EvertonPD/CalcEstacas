from funcDecQuar import paFinalDecQuar
from funcCapCargAoki import paFinalAoki
import pandas as pd
from matplotlib import pyplot as plt


def resultAoki(listaTipoSolo, tipoEstaca, listaNspt, diametroEst):

    aokiResul = paFinalAoki(listaTipoSolo, tipoEstaca, listaNspt, diametroEst)

    return aokiResul

def resulDecQuar(listaTipoSolo, tipoEstaca, listaNspt, diametroEst):

    DecQuarResul = paFinalDecQuar(listaTipoSolo, tipoEstaca, listaNspt, diametroEst)

    return DecQuarResul


def minAokiDec(listaTipoSolo, tipoEstaca, listaNspt, diametroEst):

    aokiRes = paFinalAoki(listaTipoSolo, tipoEstaca, listaNspt, diametroEst)
    decRes = paFinalDecQuar(listaTipoSolo, tipoEstaca, listaNspt, diametroEst)

    aokiDecFinal = []

    for i in range(len(aokiRes)):
        aokiDecFinal.append(min([aokiRes[i], decRes[i]]))

    return aokiDecFinal


def cotasPonta(listaTipoSolo):

    cotasProf = []

    for i in range(len(listaTipoSolo)):

        cotasProf.append((i + 1) * (-1))
                         
    return cotasProf


def resulNotaveis(listaTipoSolo, tipoEstaca, listaNspt, diametroEst):

    resultCompletoNot = {
        'Cotas de Apoio (m)': cotasPonta(listaTipoSolo),
        'Valor Pa Aoki (kN)': resultAoki(listaTipoSolo, tipoEstaca, listaNspt, diametroEst),
        'Valor Pa DecQua (kN)': resulDecQuar(listaTipoSolo, tipoEstaca, listaNspt, diametroEst),
        'Menor valor Aoki-DecQua (kN)': minAokiDec(listaTipoSolo, tipoEstaca, listaNspt, diametroEst)            
    }

    dfResult = round(pd.DataFrame(resultCompletoNot), 1)

    return dfResult



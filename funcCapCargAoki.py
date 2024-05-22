from tabelasParametros import paramAokiTab, fatorCorrAoki
import math
import pandas as pd


def searchParamAoki(tipoSolo):

    df = paramAokiTab()
    df2 = df.loc[df['Código'] == tipoSolo]
    listaComK = df2['K (kPa)'].tolist()
    listaComAlfa = df2['Alfa'].tolist()

    listaParamAoki = [listaComK[0], listaComAlfa[0]]


    return listaParamAoki


def searchCorrAoki(tipoEstaca):

    df = fatorCorrAoki()
    df2 = df.loc[df['Tipo de Estaca'] == tipoEstaca]
    listaComF1 = df2['F1'].tolist()
    listaComF2 = df2['F2'].tolist()

    listaFatorCorr = [listaComF1[0], listaComF2[0]]


    return listaFatorCorr



def calc_rpAoki(tipoSolo, tipoEstaca, nspt):

    valorK = searchParamAoki(tipoSolo)[0]
    valorF1 = searchCorrAoki(tipoEstaca)[0]


    rp = valorK * nspt / valorF1            #rp em kPa


    return rp




def calc_rlAoki(tipoSolo, tipoEstaca, nspt):

    valorK = searchParamAoki(tipoSolo)[0]
    valorAlfa = searchParamAoki(tipoSolo)[1]
    valorF2 = searchCorrAoki(tipoEstaca)[1]

    rl = valorK * nspt * valorAlfa / valorF2


    return rl


def propGeomEst(diametro):

    perimetroEst = diametro * math.pi
    areaEst = pow(diametro, 2) * math.pi / 4

    resulPropGeom = [diametro, perimetroEst, areaEst]

    return resulPropGeom


def valoresK(listaTipoSolo):

    listaComValoresK = []

    for ts in range(len(listaTipoSolo)):
        listaComValoresK.append(searchParamAoki(listaTipoSolo[ts])[0])

    return listaComValoresK


def valoresrp(listaTipoSolo, tipoEstaca, listaNspt):

    listaNspt.append(listaNspt[-1])

    listaComValoresrp = []

    for i in range(len(listaTipoSolo)):

        listaComValoresrp.append(calc_rpAoki(listaTipoSolo[i], tipoEstaca, listaNspt[i + 1]))

    listaNspt.pop()             #exclui o último elemento adicionado na lista


    return listaComValoresrp



def valoresRp(listaTipoSolo, tipoEstaca, listaNspt, diametroEst):

    areaEst = propGeomEst(diametroEst)[2]
    rp = valoresrp(listaTipoSolo, tipoEstaca, listaNspt)

    listaComValoresRp = []

    for i in range(len(listaTipoSolo)):
        listaComValoresRp.append(rp[i] * areaEst)

    return listaComValoresRp


def valoresrl(listaTipoSolo, tipoEstaca, listaNspt):

    listaComValoresrl = []

    for i in range(len(listaTipoSolo)):
        listaComValoresrl.append(calc_rlAoki(listaTipoSolo[i], tipoEstaca, listaNspt[i]))

    return listaComValoresrl


def valoresRl(listaTipoSolo, tipoEstaca, listaNspt, diametroEst):

    perimetroEst = propGeomEst(diametroEst)[1]
    rl = valoresrl(listaTipoSolo,  tipoEstaca, listaNspt)

    listaComValoresRl = []

    for i in range(len(listaTipoSolo)):
        listaComValoresRl.append(rl[i] * perimetroEst)

    return listaComValoresRl


def valoresAcumRl(listaTipoSolo, tipoEstaca, listaNspt, diametroEst):

    listaComValoresRl = valoresRl(listaTipoSolo, tipoEstaca, listaNspt, diametroEst)

    series = pd.Series(listaComValoresRl)
    listaAcumuladaRl = series.cumsum()

    return listaAcumuladaRl


def resistenciaTotal(listaTipoSolo, tipoEstaca, listaNspt, diametroEst):
    lateralAcumulado = valoresAcumRl(listaTipoSolo, tipoEstaca, listaNspt, diametroEst)
    resistenciaPonta = valoresRp(listaTipoSolo, tipoEstaca, listaNspt, diametroEst)

    resistenciaTotalRpRl = []

    for i in range(len(lateralAcumulado)):

        resistenciaTotalRpRl.append(lateralAcumulado[i] + resistenciaPonta[i])

    return resistenciaTotalRpRl


def paNbr6122(listaTipoSolo, tipoEstaca, listaNspt, diametroEst):

    resistTotal = resistenciaTotal(listaTipoSolo, tipoEstaca, listaNspt, diametroEst)

    pa6122 = []

    for i in range(len(resistTotal)):
        pa6122.append(resistTotal[i] / 2)

    return pa6122


def paEscavadas(listaTipoSolo, tipoEstaca, listaNspt, diametroEst):

    valoresRlacum = valoresAcumRl(listaTipoSolo, tipoEstaca, listaNspt, diametroEst)
    paEsc = []

    for i in range(len(valoresRlacum)):
        paEsc.append(valoresRlacum[i] * 1.25)

    return paEsc


def paFinalAoki(listaTipoSolo, tipoEstaca, listaNspt, diametroEst):

    pa6122 = paNbr6122(listaTipoSolo, tipoEstaca, listaNspt, diametroEst)
    paEsc = paEscavadas(listaTipoSolo, tipoEstaca, listaNspt, diametroEst)
    paFinal = []

    for i in range(len(pa6122)):
        paFinal.append(min([pa6122[i], paEsc[i]]))

    return paFinal


def cotasPonta(listaTipoSolo):

    cotasProf = []

    for i in range(len(listaTipoSolo)):

        cotasProf.append((i + 1) * (-1))
                         
    return cotasProf



def resultAoki(listaTipoSolo, tipoEstaca, listaNspt, diametroEst):

    resultCompletoAoki = {
        'Cotas de Apoio (m)': cotasPonta(listaTipoSolo),
        'k (kPa)': valoresK(listaTipoSolo),
        'rp (kPa)': valoresrp(listaTipoSolo, tipoEstaca, listaNspt),
        'Rp (kN)': valoresRp(listaTipoSolo, tipoEstaca, listaNspt, diametroEst),
        'rl (kPa)': valoresrl(listaTipoSolo, tipoEstaca, listaNspt),
        'Rl (kN)': valoresRl(listaTipoSolo, tipoEstaca, listaNspt, diametroEst),
        'Rl (kN) acum.': valoresAcumRl(listaTipoSolo, tipoEstaca, listaNspt, diametroEst),
        'Rt (kN)': resistenciaTotal(listaTipoSolo, tipoEstaca, listaNspt, diametroEst),
        'Pa (kN) NBR 6122': paNbr6122(listaTipoSolo, tipoEstaca, listaNspt, diametroEst),
        'Pa (kN) Escavadas': paEscavadas(listaTipoSolo, tipoEstaca, listaNspt, diametroEst),
        'Pa (kN) Final': paFinalAoki(listaTipoSolo, tipoEstaca, listaNspt, diametroEst)
    }

    dfResult = round(pd.DataFrame(resultCompletoAoki), 1)

    return dfResult


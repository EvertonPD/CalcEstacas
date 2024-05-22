from tabelasParametros import paramDecQuarTab, fatorAlfaDecQuar, fatorBetaDecQuar
import math
import pandas as pd


def searchParamDecQuar(tipoSolo):

    df = paramDecQuarTab()
    df2 = df.loc[df['Código'] == tipoSolo]
    listaComC = df2['C (kPa)'].tolist()

    listaParamC = listaComC[0]

    return listaParamC


def searchFatorAlfa(tipoSolo, tipoEstaca):

    df = fatorAlfaDecQuar()
    df2 = df.loc[df['Código'] == tipoSolo]
    
    listaAlfa = df2[tipoEstaca].tolist()

    listaParamAlfa = listaAlfa[0]

    return listaParamAlfa


def searchFatorBeta(tipoSolo, tipoEstaca):

    df = fatorBetaDecQuar()
    df2 = df.loc[df['Código'] == tipoSolo]
    
    listaBeta = df2[tipoEstaca].tolist()

    listaParamBeta = listaBeta[0]

    return listaParamBeta


def calc_Np(nsptAnterior, nsptPonta, nsptPosterior):

    valorNp = (nsptPonta + nsptAnterior + nsptPosterior) / 3

    return valorNp


def calc_media_nspt(listaNspt):

    listaNspt.append(listaNspt[-1])
    listaNspt.append(listaNspt[-1])

    media_nspt = []

    for i in range(len(listaNspt) - 2):

        media_nspt.append(calc_Np(listaNspt[i + 1], listaNspt[i], listaNspt[i + 2]))

    listaNspt.pop()
    listaNspt.pop()

    return media_nspt


def propGeomEst(diametro):

    perimetroEst = diametro * math.pi
    areaEst = pow(diametro, 2) * math.pi / 4

    resulPropGeom = [diametro, perimetroEst, areaEst]

    return resulPropGeom

    
def calc_nl(nspt):

    nl = (nspt / 3) + 1
            
    return nl


def valores_C(listaTipoSolo):

    listaComValoresC = []

    for ts in range(len(listaTipoSolo)):
        listaComValoresC.append(searchParamDecQuar(listaTipoSolo[ts]))

    return listaComValoresC

def valores_Alfa(listaTipoSolo, tipoEstaca):

    listaValoresAlfa = []

    for i in range(len(listaTipoSolo)):
        listaValoresAlfa.append(searchFatorAlfa(listaTipoSolo[i], tipoEstaca))
        
    return listaValoresAlfa

def valores_Beta(listaTipoSolo, tipoEstaca):

    listaValoresBeta = []

    for i in range(len(listaTipoSolo)):
        listaValoresBeta.append(searchFatorBeta(listaTipoSolo[i], tipoEstaca))
        
    return listaValoresBeta


def valoresRp(listaTipoSolo, tipoEstaca, listaNspt, diametroEst):

    areaEst = propGeomEst(diametroEst)[2]   
    alfa = valores_Alfa(listaTipoSolo, tipoEstaca)
    valor_C = valores_C(listaTipoSolo)
    media_nspt = calc_media_nspt(listaNspt)

    listaComValoresRp = []

    for i in range(len(listaTipoSolo)):
        listaComValoresRp.append(valor_C[i] * areaEst * alfa[i] * media_nspt[i])

    return listaComValoresRp

def valores_nl(listaNspt):

    valorNl = []

    for i in range(len(listaNspt)):

        valorNl.append(calc_nl(listaNspt[i]))

    return valorNl


def valoresRl(listaTipoSolo, tipoEstaca, listaNspt, diametroEst):

    beta = valores_Beta(listaTipoSolo, tipoEstaca)
    u = propGeomEst(diametroEst)[1]
    lEstaca = 1
    nl = valores_nl(listaNspt)
    

    valores_Rl = []

    for i in range(len(listaTipoSolo)):

        valores_Rl.append(beta[i] * 10 * nl[i] * u * lEstaca)
        
    return valores_Rl

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

def valores_PaDQ(listaTipoSolo, tipoEstaca, listaNspt, diametroEst):

    Rp = valoresRp(listaTipoSolo, tipoEstaca, listaNspt, diametroEst) 
    RlAcum = valoresAcumRl(listaTipoSolo, tipoEstaca, listaNspt, diametroEst) 

    
    paDcQua = []

    for i in range(len(listaNspt)):

        paDcQua.append(Rp[i] / 4 + RlAcum[i] / 1.3)

    return paDcQua

def paFinalDecQuar(listaTipoSolo, tipoEstaca, listaNspt, diametroEst):

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


def resulDecQuar(listaTipoSolo, tipoEstaca, listaNspt, diametroEst):

    resultCompletoDecQuar = {
        'Cotas de Apoio (m)': cotasPonta(listaTipoSolo),
        'C (kPa)': valores_C(listaTipoSolo),
        'α': valores_Alfa(listaTipoSolo, tipoEstaca),
        'β': valores_Beta(listaTipoSolo, tipoEstaca),
        'Rp (kN)': valoresRp(listaTipoSolo, tipoEstaca, listaNspt, diametroEst),
        'Rl (Kn)': valoresRl(listaTipoSolo, tipoEstaca, listaNspt, diametroEst),
        'Rl acum. (kN)': valoresAcumRl(listaTipoSolo, tipoEstaca, listaNspt, diametroEst),
        'R total (kN)': resistenciaTotal(listaTipoSolo, tipoEstaca, listaNspt, diametroEst),
        'Pa 6122 (kN)': paNbr6122(listaTipoSolo, tipoEstaca, listaNspt, diametroEst),
        'Pa Escavadas (kN)': paEscavadas(listaTipoSolo, tipoEstaca, listaNspt, diametroEst),
        'Pa Met. DecQua (kN)': valores_PaDQ(listaTipoSolo, tipoEstaca, listaNspt, diametroEst),
        'Pa Final DecQuar (kN)': paFinalDecQuar(listaTipoSolo, tipoEstaca, listaNspt, diametroEst)                   
    }

    dfResult = round(pd.DataFrame(resultCompletoDecQuar), 1)

    return dfResult

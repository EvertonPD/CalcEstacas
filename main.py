import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import tkinter.font as tkFont
import sys
from PyQt5.QtWidgets import QApplication
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication
import sys
from PyQt5.QtWidgets import QApplication

from docWord import word_Doc, geracaoGraficos, excel_Doc, ImageWindow


# Lista de nomes dos solos para exibição no Combobox
nomes_solos = [
    'Areia',
    'Areia Siltosa',
    'Areia Siltoargilosa',
    'Areia Argilosa',
    'Areia Argilossiltosa',
    'Silte',
    'Silte Arenoso',
    'Silte Arenoargiloso',
    'Silte Argiloso',
    'Silte Argiloarenoso',
    'Argila',
    'Argila Arenosa',
    'Argila Arenossiltosa',
    'Argila Siltosa',
    'Argila Siltoarenosa'
]

# Mapeamento de nome de solo para código de solo
nome_para_codigo = {
    'Areia': 1,
    'Areia Siltosa': 12,
    'Areia Siltoargilosa': 123,
    'Areia Argilosa': 13,
    'Areia Argilossiltosa': 132,
    'Silte': 2,
    'Silte Arenoso': 21,
    'Silte Arenoargiloso': 213,
    'Silte Argiloso': 23,
    'Silte Argiloarenoso': 231,
    'Argila': 3,
    'Argila Arenosa': 31,
    'Argila Arenossiltosa': 312,
    'Argila Siltosa': 32,
    'Argila Siltoarenosa': 321
}



def adicionar_camada():
    nspt = int(entryNspt.get())
    nome_solo = comboSolo.get()
    tipo_solo_codigo = nome_para_codigo[nome_solo]
    if camadas:
        ultima_profundidade = camadas[-1][0]
        nova_profundidade = ultima_profundidade + 1.0
    else:
        nova_profundidade = 1.0
    camadas.append((nova_profundidade, nspt, nome_solo, tipo_solo_codigo))
    atualizar_lista_camadas()

def remover_camada():
    indice = listaCamadas.curselection()
    if indice:
        camadas.pop(indice[0])
        atualizar_lista_camadas()

def atualizar_lista_camadas():
    listaCamadas.delete(0, tk.END)
    for camada in camadas:
        profundidade, nspt, nome_solo, tipo_solo_codigo = camada
        listaCamadas.insert(tk.END, f"Profundidade: {profundidade} m | Nspt: {nspt} | Tipo de Solo: {nome_solo}")

def limpar_camadas():
    camadas.clear()
    atualizar_lista_camadas()

def calcular_memorial_word():
    if not camadas:
        messagebox.showwarning("Erro", "Adicione pelo menos uma camada de solo.")
        return

    tipoEstaca = tipoEstacaVar.get()
    diametroEst = float(entryDiaEst.get()) / 100
    alturaBloco = float(entryAltBloc.get()) / 100
    cargaAdmEsperada = float(entryCargaAdm.get())

    global listaNspt, listaTipoSolo
    listaNspt = [camada[1] for camada in camadas]
    listaTipoSolo = [camada[3] for camada in camadas]

    filename = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Document", "*.docx")], initialfile="Memorial_Word")
    if not filename:
        # O usuário cancelou a janela de diálogo
        return

    resultado = word_Doc(listaTipoSolo, tipoEstaca, listaNspt, diametroEst, alturaBloco, cargaAdmEsperada, filename)

    messagebox.showinfo("Sucesso", resultado)

def calcular_memorial_excel():
    if not camadas:
        messagebox.showwarning("Erro", "Adicione pelo menos uma camada de solo.")
        return

    tipoEstaca = tipoEstacaVar.get()
    diametroEst = float(entryDiaEst.get()) / 100
    alturaBloco = float(entryAltBloc.get()) / 100
    cargaAdmEsperada = float(entryCargaAdm.get())

    global listaNspt, listaTipoSolo
    listaNspt = [camada[1] for camada in camadas]
    listaTipoSolo = [camada[3] for camada in camadas]

    filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Workbook", "*.xlsx")], initialfile="Memorial_Excel")
    if not filename:
        # O usuário cancelou a janela de diálogo
        return

    resultado = excel_Doc(listaTipoSolo, tipoEstaca, listaNspt, diametroEst, alturaBloco, cargaAdmEsperada, filename)

    messagebox.showinfo("Sucesso", resultado)

def visualizar_dados():
    tipoEstaca = tipoEstacaVar.get()
    diametroEst = float(entryDiaEst.get()) / 100
    alturaBloco = float(entryAltBloc.get()) / 100
    cargaAdmEsperada = float(entryCargaAdm.get())

    if not camadas:
        messagebox.showwarning("Erro", "Adicione pelo menos uma camada de solo.")
        return

    global listaNspt, listaTipoSolo
    listaNspt = [camada[1] for camada in camadas]
    listaTipoSolo = [camada[3] for camada in camadas]

    caminhos_graficos = geracaoGraficos(listaTipoSolo, tipoEstaca, listaNspt, diametroEst, alturaBloco, cargaAdmEsperada)

    image_names = [
        'Tabela Aoki', 'Gráfico Aoki', 'Tabela Décourt-Quaresma', 'Gráfico Décourt-Quaresma',
        'Tabela Notáveis', 'Gráfico Menor entre Aoki-DecQuar', 'Gráfico Aoki e DecQuar'
    ]

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    image_viewer = ImageWindow(caminhos_graficos, image_names)
    image_viewer.show()

    # Adiciona o loop do evento da aplicação do PyQt5 sem bloquear o Tkinter
    app.exec_()

    # Após fechar a janela PyQt5, limpa as figuras para evitar o erro de memória
    plt.close('all')


def on_closing():
    if messagebox.askokcancel("Sair", "Você quer sair?"):
        janela.destroy()
        if QApplication.instance() is not None:
            QApplication.instance().quit()

 
janela = tk.Tk()
janela.title("Calculadora de Estacas")

tipoEstacaVar = tk.StringVar(value=" ")
entryDiaEst = tk.StringVar()
entryAltBloc = tk.StringVar()
entryCargaAdm = tk.StringVar()

bold_font = tkFont.Font(family="Courier New", size=12, weight="bold")
bold = tkFont.Font(family="Courier New", size=12)

tk.Label(janela, text="Tipo de estaca: ", font=bold_font).grid(row=0, column=0, pady=5)
tipos_estaca = ['HCM', 'Escavada', 'Raiz']
for i, tipo in enumerate(tipos_estaca):
    tk.Radiobutton(janela, text=tipo, font=bold, variable=tipoEstacaVar, value=tipo).grid(row=0, column=i+1, padx=10)


tk.Label(janela, text="Diâmetro da Estaca (cm): ", font=bold_font).grid(row=1, column=0, pady=5)
diaEst = tk.Entry(janela, font=bold, textvariable=entryDiaEst, highlightbackground="black", highlightcolor="red", highlightthickness=2)
diaEst.grid(row=1, column=1, columnspan=2, pady=10)

tk.Label(janela, text="Altura do Bloco (cm): ", font=bold_font).grid(row=2, column=0, pady=5)
altBloc = tk.Entry(janela, font=bold, textvariable=entryAltBloc, highlightbackground="black", highlightcolor="red", highlightthickness=2)
altBloc.grid(row=2, column=1, columnspan=2, pady=10)

tk.Label(janela, text="Carga Admissível Esperada (kN): ", font=bold_font).grid(row=3, column=0, pady=5)
entryCargaAdm = tk.Entry(janela, font=bold, textvariable=entryCargaAdm, highlightbackground="black", highlightcolor="red", highlightthickness=2)
entryCargaAdm.grid(row=3, column=1, columnspan=2, pady=10)

tk.Label(janela, text="Camadas de Solo:", font=bold_font).grid(row=6, column=1, columnspan=2, pady=10)

tk.Label(janela, text="Nspt:", font=bold_font).grid(row=7, column=0, pady=5)
entryNspt = tk.Entry(janela, font=bold, highlightbackground="black", highlightcolor="red", highlightthickness=2)
entryNspt.grid(row=7, column=1, columnspan=2, pady=10)

tk.Label(janela, text="Tipo de Solo:", font=bold_font).grid(row=8, column=0, pady=5)
comboSolo = ttk.Combobox(janela, values=nomes_solos, state='readonly')
comboSolo.grid(row=8, column=1, columnspan=2, pady=10)
comboSolo.option_add('*TCombobox*Listbox.font', bold)
comboSolo['width'] = 40


botaoAdicionar = tk.Button(janela, text="Adicionar Camada", font=bold_font, bg='#ADD8E6', command=adicionar_camada)
botaoAdicionar.grid(row=9, column=1, columnspan=2, pady=10)

botaoRemover = tk.Button(janela, text="Remover Camada Selecionada", font=bold_font, bg='#FFA07A', command=remover_camada)
botaoRemover.grid(row=10, column=1, columnspan=2, pady=10)

botaoLimpar = tk.Button(janela, text="Limpar Camadas", font=bold_font, bg='#FFFFFF', command=limpar_camadas)
botaoLimpar.grid(row=11, column=1, columnspan=2, pady=10)

listaCamadas = tk.Listbox(janela, font=bold_font, width=70, height=10, highlightbackground="black", highlightcolor="red", highlightthickness=2)
listaCamadas.grid(row=12, column=1, columnspan=2, pady=10)

botao_visualizar = tk.Button(janela, text="Visualizar Dados", font=bold_font, bg='#CCCCCC', command=visualizar_dados)
botao_visualizar.grid(row=13, column=1, columnspan=2, pady=10)

botaoGerarMem = tk.Button(janela, text="Gerar Memorial Word", font=bold_font, bg='#2E75B6', command=calcular_memorial_word)
botaoGerarMem.grid(row=15, column=1, columnspan=2, pady=10)

botaoExcel = tk.Button(janela, text="Gerar Memorial Excel", font=bold_font, bg='#00B050', command=calcular_memorial_excel)
botaoExcel.grid(row=17, column=1, columnspan=2, pady=10)

camadas = []

janela.protocol("WM_DELETE_WINDOW", on_closing)

janela.mainloop()



'''
tipoEstaca = 'HCM'      #HCM, Escavada, Raiz
diametroEst = 0.3     #m
alturaBloco = 0.45      #m
cargaAdmEsperada = 170  #kN
listaNspt =     [0,  1,  1,  3,  6,  10, 11, 16, 30, 50, 50, 50, 50 ,50, 50]
listaTipoSolo = [23, 23, 23, 23, 32, 32, 32, 32, 32, 12, 12, 12, 12, 12, 12]
fileName = 'Memorial de Cálculo'

#print(excel_Doc(listaTipoSolo, tipoEstaca, listaNspt, diametroEst, alturaBloco, cargaAdmEsperada, fileName))
#print(word_Doc(listaTipoSolo, tipoEstaca, listaNspt, diametroEst, alturaBloco, cargaAdmEsperada, fileName))
print(plotGrafic(frame, listaTipoSolo, tipoEstaca, listaNspt, diametroEst, alturaBloco, cargaAdmEsperada, alturaBloco, cargaAdmEsperada))
'''

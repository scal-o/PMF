# code by scalo

# LIBRERIA DI FUNZIONI PER IL POSTPROCESSING
# DA MODIFICARE SOLO IN CASO CI SIA QUALCHE PROBLEMA

import re, math
import numpy
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# svolge l'analisi statistica dei dati, calcolando media, 
# dev. standard ed intervallo di confidenza
def statistical_analysis(cx): 
    # Svolge l'analisi statistica dei dati. calcola media,
    # dev. standard ed intervallo di confidenza al 99%.
    cx_mean = numpy.mean(cx)
    cx_dev_std = numpy.std(cx, ddof = 1) # ddof = 1 per dividere per N-1
    cx_conf_lev99 = 2.58*(cx_dev_std)/(math.sqrt(len(cx)))
    return cx_mean, cx_conf_lev99



# analisi delle forze e dei momenti sulle varie parti della carena
def forces(path, part, f, m, ticks_x, ticks_y):

    if not(f or m):
        print("\n\nERRORE: non si stanno calcolando nè forze nè momenti.\n\n")
        return

    with open(path, 'r') as pipefile, open("results/Risultati analisi.txt", 'a') as res:  
        lines = pipefile.readlines()

        scalarStr = r"\-?[0-9]+\.?[eE\-+0-9]*"  # regex utilizzata per filtrare i dati dal file .dat

        t, fpx, fpy, fpz, fvx, fvy, fvz, fpox, fpoy, fpoz, mpx, mpy, mpz, mvx, mvy, mvz, mpox, mpoy, mpoz =[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
        components = [t, fpx, fpy, fpz, fvx, fvy, fvz, fpox, fpoy, fpoz, mpx, mpy, mpz, mvx, mvy, mvz, mpox, mpoy, mpoz]

        for line in lines:
            file_data = re.findall(scalarStr, line)  # per ogni riga del file restituisce tutte le istanze della regex definita prima
            
            if file_data != [] and len(file_data) == 19:  # controlla che la riga non sia vuota e/o che la lettura sia stata effettuata correttamente                    
                for i, column in enumerate(components):
                    column.append(float(file_data[i])) # aggiunge ad ogni lista la componente calcolata alla nuova iterazione

        moto_poro = re.search("Moto con porosità", part)
        if not moto_poro: res.write("\n\nForze e momenti "+ part + '\n')

        if f:
            # effettua la somma delle componenti sullo stesso asse
            if moto_poro:
                fx = [x+y+z for x,y,z in zip(fpx,fvx,fpox)]
                fy = [x+y+z for x,y,z in zip(fpy,fvy,fpoy)]
                fz = [x+y+z for x,y,z in zip(fpz,fvz,fpoz)]
            else:
                fx = [x+y for x,y in zip(fpx,fvx)]
                fy = [x+y for x,y in zip(fpy,fvy)]
                fz = [x+y for x,y in zip(fpz,fvz)]

            # effettua l'analisi statistica
            fx_mean, fx_conf_lev99 = statistical_analysis(fx[-250:])
            fy_mean, fy_conf_lev99 = statistical_analysis(fy[-250:])
            fz_mean, fz_conf_lev99 = statistical_analysis(fz[-250:])

            # scrive i risultati dell'analisi statistica su un file di output
            if not moto_poro:
                res.write("Fx = "+ str(fx_mean)+ " +/- "+ str(fx_conf_lev99) + '\n')
                res.write("Fy = "+ str(fy_mean)+ " +/- "+ str(fy_conf_lev99) + '\n')
                res.write("Fz = "+ str(fz_mean)+ " +/- "+ str(fz_conf_lev99) + '\n')

            # traccia i grafici
            forces = [fx,fy,fz]
            F_mean = [fx_mean, fy_mean, fz_mean]
            fm_plot(t, forces, F_mean, "forces", ticks_x, ticks_y, part)

        if m:
            # effettua la somma delle componenti sullo stesso asse
            if moto_poro:
                mx = [x+y+z for x,y,z in zip(mpx,mvx,mpox)]
                my = [x+y+z for x,y,z in zip(mpy,mvy,mpoy)]
                mz = [x+y+z for x,y,z in zip(mpz,mvz,mpoz)]
            else:
                mx = [x+y for x,y in zip(mpx,mvx)]
                my = [x+y for x,y in zip(mpy,mvy)]
                mz = [x+y for x,y in zip(mpz,mvz)]

            # effettua l'analisi statistica  
            mx_mean, mx_conf_lev99 = statistical_analysis(mx[-250:])
            my_mean, my_conf_lev99 = statistical_analysis(my[-250:])
            mz_mean, mz_conf_lev99 = statistical_analysis(mz[-250:])


            # scrive i risultati dell'analisi statistica su un file di output
            if not moto_poro:
                res.write("Mx = "+ str(mx_mean)+ " +/- "+ str(mx_conf_lev99) + '\n')
                res.write("My = "+ str(my_mean)+ " +/- "+ str(my_conf_lev99) + '\n')
                res.write("Mz = "+ str(mz_mean)+ " +/- "+ str(mz_conf_lev99) + '\n')

            # traccia i grafici
            moments = [mx,my,mz]
            M_mean = [mx_mean, my_mean, mz_mean]
            fm_plot(t, moments, M_mean, "moments", ticks_x, ticks_y, part)     


    
# tracciamento dei grafici di forze e momenti
def fm_plot(t, fm, mean_fm, mode, n_ticks_x, n_ticks_y, part):
    # prende come argomenti numero di iterazioni, lista delle forze o momenti sui tre assi, 
    # modalità (ovvero se si sta lavorando con forze o momenti, per cambiare le intestazioni 
    # dei grafici). n_ticks_x e n_ticks_y sono argomenti opzionali utilizzati per variare 
    # la spaziatura degli assi (default = 10)

    # imposta label e titoli
    if mode == "forces":
        xlabel = '$F_x$'
        ylabel = '$F_y$'
        zlabel = '$F_z$'
        tit = "Forze "
        m_lab = '$F_'
    elif mode == "moments":
        xlabel = '$M_x$'
        ylabel = '$M_y$'
        zlabel = '$M_z$'
        tit = "Momenti "
        m_lab = '$M_'

    part_titles = [part, part + " finali"]
    t = [t, t[-250:]]
    fm0 = [fm[0], fm[0][-250:]]
    fm1 = [fm[1], fm[1][-250:]]
    fm2 = [fm[2], fm[2][-250:]]

    for t_, fmx, fmy, fmz, part in zip(t, fm0, fm1, fm2, part_titles):

        # crea figure e Axes
        fig, axs = plt.subplots(ncols=len(fm), sharex=True, figsize=(24, 5))

        axs[0].plot(t_,fmx, label =xlabel)

        axs[1].plot(t_,fmy, label =ylabel)
        axs[1].set_title(tit + part + " [N]", fontweight = "bold")

        axs[2].plot(t_,fmz, label =zlabel)

        if part == part_titles[1]:
            axs[0].axhline([mean_fm[0]], linestyle='-.', linewidth = 0.8, label = m_lab +'{x, mean}$', color="orange")
            axs[1].axhline([mean_fm[1]], linestyle='-.', linewidth = 0.8, label = m_lab +'{y, mean}$', color="orange")
            axs[2].axhline([mean_fm[2]], linestyle='-.', linewidth = 0.8, label = m_lab +'{z, mean}$', color="orange")


        #applica spaziatura assi ed attiva griglia e legenda
        for graph in axs:
            graph.xaxis.set_major_locator(ticker.MaxNLocator(n_ticks_x))
            graph.yaxis.set_major_locator(ticker.MaxNLocator(n_ticks_y))

            graph.grid(True)
            graph.legend()

        #salva i grafici
        fig.savefig('results/'+tit+part+'.png', format = 'png', dpi = 250) # l'argomento dpi indica la risoluzione dell'immagine finale
        plt.close(fig)



def coefficients(path, tick_spacing_x = 50, tick_spacing_y = 0.05):

    t, cd, cl = [], [], [] # inizializza vettori in cui inserire le mie variabili d'interesse
    dati = numpy.genfromtxt(path, skip_header=9, skip_footer=1) # importa dati saltando header

    # copia in ogni lista la rispettiva colonna di valori
    for column in dati: 
        t.append(column[0]) 
        cd.append(column[2])
        cl.append(column[3])

    # effettua l'analisi statistica
    cd_mean, cd_conf_lev99 = statistical_analysis(cd[-250:])
    cl_mean, cl_conf_lev99 = statistical_analysis(cl[-250:])

    t = [t, t[-250:]]
    cd = [cd, cd[-250:]]
    cl = [cl, cl[-250:]]
    coeff_titles = ["Coefficienti aerodinamici totali", "Coefficienti aerodinamici finali"]

    # traccia i grafici di cd e cl
    for t_, cd_, cl_, title in zip(t, cd, cl, coeff_titles):
        fig, ax = plt.subplots() # crea figura e Axes
        plt.title(f"{title}", fontweight = "bold")
        ax.plot(t_, cd_, label ='$C_D$') # plotta cd e cl con il numero di iterazioni
        ax.plot(t_, cl_, label ='$C_L$')

        if title == coeff_titles[1]:
            ax.axhline(cd_mean, linestyle='--', linewidth = 0.8, label = '$C_{D, mean}$', color = 'red')    
            ax.axhline(cl_mean, linestyle='--', linewidth = 0.8, label = '$C_{L, mean}$', color = 'green')

        ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing_x)) # spazia asse x di quantità definita prima
        ax.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing_y)) # spazia asse y di quantità definita prima

        plt.legend() # attiva legenda
        plt.grid()   # attiva griglia
        ax.set_xlabel('Iterazioni') # nome asse x

        # salva i grafici
        plt.savefig(f"results/{title}.png", dpi = 250)  # l'argomento dpi indica la risoluzione dell'immagine finale
        plt.close(fig)

    with open("results/Risultati analisi.txt", 'a') as res:
        res.write("\nCd = " + str(cd_mean) + " +/- " + str(cd_conf_lev99))
        res.write("\nCl = " + str(cl_mean) + " +/- " + str(cl_conf_lev99))




def residuals(path):

    t, p, Ux, Uy, Uz, k, omega = [],[],[],[],[],[],[] # inizializza vettori in cui inserire le mie variabili d'interesse
    dati = numpy.genfromtxt(path, skip_header=3, skip_footer=1) # importa dati saltando header
    data_list = [t, p, Ux, Uy, Uz, k, omega] # lista di liste, necessaria per poter iterare

    # l'ordine con cui vengono importati i dati è lo stesso che si vede nel file .dat
    # "dati" sono memorizzati in riga. metti ogni elemento della riga nella rispettiva colonna
    for row in dati:
        for i, col in enumerate(data_list, 0):
            col.append(row[i])
        

    # tracciamento grafici
    fig, ax = plt.subplots() # crea figure e Axes
   
    ax.plot(t,p, label = 'p')
    ax.plot(t,Ux,label='$U_x$')
    ax.plot(t,Uy,label='$U_y$')
    ax.plot(t,Uz,label='$U_z$')
    ax.plot(t,omega,label='$\omega$')
    ax.plot(t,k,label='k')
    ax.set_yscale('log')

    plt.legend()
    plt.grid()

    # aggiunge titolo e label
    ax.set_title("Residui", fontweight = "bold")
    ax.set_xlabel("Iterazioni")

    # salva i grafici
    plt.savefig("results/Residui.png", dpi = 250) # l'argomento dpi indica la risoluzione dell'immagine finale
    plt.close(fig)
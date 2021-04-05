from time import clock
from pylab import *
from numpy import *
from math import *
# *****************************************************************************
#*****************************************************************************#
#*****************************************************************************#
#
#  Discussion:
#
#  Bioreactor Modelling for Bio-ethanol (P) production
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    Tus Mar 29 19:07:00 2016
#
#  Author:
#
#    MEHDI AYOUZ LGPM CENTRALESUPELEC
#    mehdi.ayouz@centralesupelec.fr
#    Bat DUMAS B324. 0141131603
#
#  Coauthors:
#    Filipa Lopez, Francois Puel, Julien Lemaire and Thomas Chastang
#
#  Parameters:
#    n, t_max, D, mu_max, Ks, Y_XS and Y_PX
#
#*****************************************************************************#
#*****************************************************************************#
#*****************************************************************************#

if __name__ == "__main__":

    print('')
    print('')
    print('....')

    wtime1 = clock()

#*****************************************************************************#
#*****************************************************************************#
#*************************   VARIBALES DECLARATION  **************************#
#*****************************************************************************#
#*****************************************************************************#

    n = 15000  # Le nombre d itération en temps
    t_max = 60.  # Le temps de calcul en heure
    D = 0.25  # Donnee sur le taux de dilution
    mu_max = 0.3  # Donnee sur le taux de conversion maximum
    Ks = 0.2  # Donnee sur la quantité Ks
    Y_XS = 0.06  # Donnee sur rendement biomasse/substrat
    Y_PX = 7.7  # Donnee sur rendement production/biomasse

#*****************************************************************************#
#*****************************************************************************#
#*************************   VARIBALES DECLARATION  **************************#
#*****************************************************************************#
#*****************************************************************************#
    t = np.zeros(n, float)  # Déclaration du tableau temps à n éléments
    X = np.zeros(n, float)  # Déclaration du tableau Bimasse à n éléments
    S = np.zeros(n, float)  # Déclaration du tableau Substrat à n éléments
    P = np.zeros(n, float)  # Déclaration du tableau Produit à n éléments
    mu = np.zeros(n, float)  # Déclaration du tableau mu à n éléments

    dt = t_max/(n-1)       # Définition du pas de temps de calcul
    # à l'aide tu temps de calcul et du
    # nombre d'itération
#*****************************************************************************#
#*****************************************************************************#
#***************************    INITIALIZATION    ****************************#
#*****************************************************************************#
#*****************************************************************************#
    X[0] = 0.2           # Initialisation X(t=0)
    S[0] = 10.3          # Initialisation S(t=0)
    P[0] = 0.8           # Initialisation P(t=0)
    Sin = 12             # Initialisation Sin
    Xin = 0              # Initialisation Xin
    Pin = 0              # Initialisation Pin
    t[0] = 0             # Initialisation t[0]=0

#*****************************************************************************#
#*****************************************************************************#
#***************************        CALCUL        ****************************#
#*****************************************************************************#
#*****************************************************************************#
    for it in range(n-1):
        t[it+1] = t[it]+dt          # Définition de la grille de calcul
        # allant de 0 à t_max
        # t[0]=0 h et t[n]=t_max h

#   Loop over integration steps:
#   Finite difference method (Euler) for solving coupled differential equations

    for it in range(n-1):         # Boucle d'itération allant de 0 à n-1 car
        # on calcule X(t+dt), P(t+dt) et S(t+dt)

        print('it= %d' % it)
        mu[it] = mu_max*S[it]/(Ks+S[it])  # calcul µ(t)
        X[it+1] = D*(Xin-X[it]) # calcul X(t+dt)
        S[it+1] =  # calcul S(t+dt)
        P[it+1] =  # calcul P(t+dt)

        mu[n-1] =      # calcul µ(t_max)

        Px = D*X[n-1]     # calcul de la productivité en biomasse à X(t_max)
        Pp = D*P[n-1]     # calcul de la productivité en produit à P(t_max)

    print("La productivité en biomasse =%g" % Px)
    print("La productivité en produit =%g" % Pp)

    figure(1)
    plot(t, S, 'r', label="S")
    title(" S vs time")
    legend()
    xlabel("t(h)")
    ylabel("S(g/L)")
    draw()  # force le dessin de la figure
    show()

    figure(2)
    plot(t, X, 'b', label="X")
    title("X  vs time")
    legend()
    xlabel("t(h)")
    ylabel(" X(g/L)")
    draw()  # force le dessin de la figure
    show()

    figure(3)
    plot(t, P, 'b', label="P")
    title("P  vs time")
    legend()
    xlabel("t(h)")
    ylabel(" P(g/L)")
    draw()  # force le dessin de la figure
    show()

    figure(4)
    plot(t, mu, 'b', label="mu")
    title("mu  vs time")
    legend()
    xlabel("t(h)")
    ylabel(" mu(1/h)")
    draw()  # force le dessin de la figure
    show()
    wtime2 = clock()

    print('')
    print('    Elapsed wall clock time = %g seconds.' % (wtime2 - wtime1))
    print('')
    print('Modelisation_Bioprocedes')
    print('  Normal end of execution.')
    print('')

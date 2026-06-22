import marimo

__generated_with = "0.23.9"
app = marimo.App(
    width="medium",
    layout_file="layouts/robots_articules.slides.json",
)


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import base64
    with open("figs/arm.jpg", "rb") as f:
        data = base64.b64encode(f.read()).decode()
    img = f'data:image/jpeg;base64,{data}'
    return (img,)


@app.cell(hide_code=True)
def _(img, mo):
    mo.md(rf"""
    ## Robots articulés

    ![description]({img})
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Quelques exemples
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Quelques exemples
    - Bras manipulateurs
    - Robots sur chaîne d'assemblage
    - Machines outils
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### En quelques mots

    - **Chaîne cinématique** composée de liaisons :
      - *Rotoïdes* (laisons "tournantes")
      - *Prismatiques* (translation)
    - À chaque liaison est associée un repère $\mathcal{F}_i$
    - But : contrôler le mouvement d'un effecteur qui se trouve dans le repère $\mathcal{F}_n$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Robots séries
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Robots série

    - Une liaison attachée à un bâti (fixe en général)
    - Enchaînement de liaisons les unes à la suite des autres
    - Jusqu'à un effecteur terminal
    - Formellement : enchaînement de changements de repères !
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Rappel : Matrices homogènes
    - Coordonnées de $X\in \mathbb{R}^3$ dans $\mathcal{F}_i$ : $^iX$
    - Si on a $^j\!X = \mathbf{R}\ {}^i\!X + t$ alors on peut noter
    $$
      \begin{bmatrix}
        {}^j\!X \\ 1
      \end{bmatrix}
      \begin{bmatrix}
        R & t \\ 0 & 1
      \end{bmatrix}\cdot
      \begin{bmatrix}
        {}^i\!X \\ 1
      \end{bmatrix}
    $$
    soit
    $$
      {}^j\!\bar{X} = {}^jT_i\cdot {}^i\!\bar{X}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Chaîne cinématique

    Si $\mathcal{F}_W$ est le repère du monde et $\mathcal{F}_n$ le repère associé à l'organe terminal, la matrice de passage de $\mathcal{F}_n$ à $\mathcal{F}_W$ est donnée par :
    $$
      ^W T_n = ^W T_0 \cdot\ ^0 T_1 \cdot\ ^1 T_2 \cdots\  ^{n-1} T_n
    $$
    ➡️ Permet de convertir les coordonnées d'un point exprimée dans le repère terminal (effecteur) dans le repère du monde.

    Ici, $n$ représente le nombre d'articulations ou **degrés de liberté** du robot
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Robots parallèles
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Robots parallèles
    - Contiennent au moins une boucle
    - Très souvent : plusieurs liaisons liées au bâti
    - Difficultés en terme de contrôle : **contraintes** dans l'espace des articulation
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exemples de robots parallèles
    - [Robot "delta"](https://www.youtube.com/watch?v=1euatWManHs) (ex. imprimante 3D)
    - [Simulateur](https://www.youtube.com/watch?v=xiECumcaEx0)
    - [Robot à câbles](https://www.youtube.com/watch?v=AppA-SYxDbk) (ex. stades)
    - [Avantages](https://www.youtube.com/watch?v=xHuDvVa7mkw) : résistance, précision, rapidité
    - Inconvénients : amplitude de mouvement limitée, contrôle peu évident
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Retour sur le robot série
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Coordonnées articulaires
    $$
      ^W T_n = {}^W T_0 \cdot\ ^0 T_1 \cdot\ ^1 T_2 \cdots\  ^{n-1} T_n
    $$
    avec
    $$
      ^{i} T_{i+1}(q_i) =
      \begin{bmatrix}
        R(q_i) & t(q_i) \\ 0 & 1
      \end{bmatrix}\mbox{   et   }
        ^{i+1} T_{i}(q_i) = \left(^{i} T_{i+1}(q_i)\right)^{-1} =
      \begin{bmatrix}
        R^T(q_i) & -R^T(q_i)t(q_i) \\ 0 & 1
      \end{bmatrix}
    $$
    - Liaison prismatique :  $q_i$ paramètre la translation $t(q_i)$ ; $R(q_i)$ est donc constant (matrice identité en général)
    - Liaison rotoïde : $q_i$ paramètre la rotation $R(q_i)$ ; $-R^T(q_i)t(q_i)$ est constant (longueur du bras)
    - Liaison prismatique et rotoïde : peut être modélisée comme une rotoïde avec bras de longueur nulle puis prismatique
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Espace articulaire / cartésien

    - $q = [q_0,q_1,\dots,q_{n-1}]$ : coordonnées articulaires
      - C'est ce qu'on peut contrôler directement ! (actionneurs)
      - Peuvent être limités (butées, vitesse,...)
    - $^W T_n$ : définit la position et l'orientation de l'effecteur dans le repère du monde
      - On parle aussi d'espace cartésien
      - C'est ce qu'on veut contrôler !
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Modèle géométrique direct

    - Retrouver $^WT_n$ à l'aide de $q$
    - Connaissant les coordonnées articulaires, l'obtension de la pose de l'effecteur s'obtient en suivant la chaîne cinématique
    """)
    return


@app.cell(hide_code=True)
def _(check_direct, mo):
    mo.md(rf"""
    ### Exemple fil rouge : robot "RR" en 2D

    - On considère un robot série avec deux liaisons de type rotoïde
    - Longueur des bras : $l_0$ et $l_1$
    - Vecteur de coordonnées articulaires : $q = [\theta_0,\theta_1]$
    - Exercice :
      - Trouver les équations du modèle direct ($x$,$y$ et l'orientation $\theta$ de l'effecteur)
      - Implémenter le résultat dans la fonction `direct_model_RR` en se limitant à la position uniquement (`x` et `y`)
      - Statut de l'exercice : {"🎯 Modèle direct correct !" if check_direct() else "🔧  Pas encore, au boulot !"}
    """)
    return


@app.cell
def _():
    import numpy as np
    from numpy import cos,sin,pi
    l0 = 2
    l1 = 1
    def direct_model_RR(theta0,theta1):
        def Ti(theta,l):
            c , s = cos(theta),sin(theta)
            return np.array([[c,-s,l*c],[s,c,l*s],[0,0,1]])
        T = Ti(theta0,l0)@Ti(theta1,l1)

        # Solution alternative
        x = l0*cos(theta0) + l1*cos(theta0+theta1)
        y = l0*sin(theta0) + l1*sin(theta0+theta1)
        #print(np.array([x,y]))
        #return T[0:2,2]
        return (x,y)


    return cos, direct_model_RR, l0, l1, np, pi, sin


@app.cell
def _(direct_model_RR, l0, l1, np, pi):
    def check_direct(tol=1e-10):
        (a,b) = direct_model_RR(0,0)
        if not np.allclose((a,b),(l0+l1,0),atol=tol):
            return False
        (a,b) = direct_model_RR(0,pi/2)
        if not np.allclose((a,b),(l0,l1),atol=tol):
            return False
        (a,b) = direct_model_RR(pi/2,0)
        if not np.allclose((a,b),(0,l0+l1),atol=tol):
            return False
        (a,b) = direct_model_RR(pi,0)
        if not np.allclose((a,b),(-l0-l1,0),atol=tol):
            return False
        (a,b) = direct_model_RR(pi,pi/2)
        if not np.allclose((a,b),(-l0,-l1),atol=tol):
            return False
        return True


    return (check_direct,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Modèle géométrique inverse

    - Objectif : retrouver $q$ sur la base de $^WT_n$
    - Problème beaucoup plus compliqué !
    - Existance de solution non garantie ($^WT_n$ doit appartenir aux configuration accessibles)
    - Possible **non unicité** de la solution !
    - Pas toujours de solution analytiques !
    """)
    return


@app.cell
def _(cos, l0, l1, sin):
    from numpy import acos,atan2

    def inverse_model_RR(x,y):
        if (x*x + y*y > (l0+l1)**2 or x*x + y*y < (l0-l1)**2):
            print("Out of accessible space")
            return None

        c1 = (x**2+y**2-l0**2-l1**2)/2/l0/l1
        if acos(c1)==0:
            Theta1 = [acos(c1)]
        else:
            Theta1 = [acos(c1),-acos(c1)]
        Theta0=[]
        for theta1 in Theta1:
            c0 = (l0+l1*cos(theta1))*x + l1*sin(theta1)*y
            s0 =-l1*sin(theta1)*x + (l0+l1*cos(theta1))*y
            Theta0.append(atan2(s0,c0)) # by convention: atan2(0,0)=0 --> fine for the (0,0) case

        sol = []
        # Recompile solution
        for i in range(len(Theta0)):
            sol.append((float(Theta0[i]),float(Theta1[i])))

        return sol

    return (inverse_model_RR,)


@app.cell
def _(direct_model_RR, inverse_model_RR, np, pi):
    def check_inverse(tol=1e-10):
        Q0 = np.linspace(-pi,pi,100)
        Q1 = np.linspace(-pi+1e-6,pi-1e-6,100) # For theta1=pi, the x,y returned is slightly outside the domain because of approx errors
        for q0 in Q0:
            for q1 in Q1:
                (x,y) = direct_model_RR(q0,q1)
                Q_test = inverse_model_RR(x,y)
                if Q_test is None:
                    print("None",q0,q1,x,y,x**2+y**2)
                    return False
                for (q0_test,q1_test) in Q_test:
                    #print(f"Testing {q0,q1,q0_test,q1_test,x,y}")
                    if (abs((q0_test - q0+pi)%(2*pi)-pi)<tol and abs((q1_test - q1+pi)%(2*pi)-pi) < tol):
                        current_test = True
                        break
                else:
                    return False
        return True




    return (check_inverse,)


@app.cell(hide_code=True)
def _(check_inverse, mo):
    mo.md(rf"""
    ### Modèle inverse du RR 2D

    - Calculer la ou les solutions du modèle inverse du robot 2D avec deux liaisons rotoïdes
      - On ne s'intéressera qu'à donner $x$ et $y$ : l'orientation de l'effecteur sera contrainte
      - Trouver également l'espace accessible par le robot
    - Implémenter le résultat dans la fonction `inverse_model_RR` du notebook
    - Statut de l'exercice : {"🎯 Modèle inverse correct !" if check_inverse() else "🔧  Pas encore, au boulot !"}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Contrôle cinématique

    - On voudrait que le robot suive une trajectoire définie par $^W{T}_n(t)$. Quelle trajectoire donner pour $q(t)$ ?
    - Passer par le modèle géométrique inverse semble illusoire...
    - En notant $X(t)$ un vecteur qui paramétrise $^W{T}_n(t)$ (ex :$(x,y,z)$ + 3 angles ou quaternions), on peut noter :
    $$
         X = f(X)
    $$
    - où $f$ désigne la fonction associée au modèle géométrique direct
    - Que se passe-t-il si on se donne une trajectoire paramétrée par $\dot{X}$ ?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    En partant de $X(t) = f(q(t))$, le théorème de dérivation des fonctions composées nous donne :
    $$
      \dot X(t)= \frac{\partial f}{\partial q} \dot q(t)
    $$

    - $\frac{\partial f}{\partial q}$ est la matrice jacobienne de $f$ contenant les dérivées de $f$ par rapport à $q$, de dimensions :
      - $n$ lignes associées au nombre de **degrés de liberté** du robot
      - $m$ colonnes associées au nombre de paramètres qu'on souhaite contrôler (en général : 6 pour le cas 3D, 3 pour le cas 2D)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On voudrait écrire
    $$
    \dot q(t) = \left(\frac{\partial f}{\partial q}\right)^{-1} \dot X(t)
    $$
    mais en a-t-on le droit ?
    - $n = m$ : oui quand la matrice est inversible. Quand elle ne l'est pas, on parle de **singularité**
    - $n < m$ : non : on est **sous actionné**
    - $m > n$ : oui quand le rang est au moins égal à $n$. Dans ce cas, plusieurs solutions existent, par exemple :
      - pseudo-inverse de **Moore-Penrose** (minimise la norme de $q$)
      - extraire une sous-matrice de bon rang...
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Retour sur le fil rouge

    - Calculer la matrice jacobienne associée au cas 2D dont on s'intéresse au contrôle de la position uniquement
    - Trouver dans quelle condition la matrice est inversible
    - Interpréter ce qu'il se passe lorsqu'elle ne l'est pas. Pistes :
        - Calculer le vecteur propre à droite
        - Calculer le vecteur propre à gauche
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - Faire en sorte de dessiner un carré dans le simulateur
      - Calculer un profil de vitesse cartésien qui va bien
      - En déduire le profil sur $\dot q$
      - Calculer $q(0)$ à l'aide du modèle inverse
      - Intégrer $\dot q(t)$ à l'aide de `solve_ivp`
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

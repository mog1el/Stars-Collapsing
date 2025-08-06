## Collapsing Stars

A fun little project created by me to learn the basics of pygame for simulations and improve my understanding of the phenomenom of collapsing stars. I've used real-world equations (not constants tho...) in order to show the behaviour of such stars. I've modified the constants c and G as them being their original value made the simulation unusable. A giant c made gthe loss of energy in the system so small, that python did not modify the radius. A small G meant low velocity values, which prolonged the simulation. (you can always change them if you want to)

---

Equations used:

Luminosity formula: $L_{GW} = \frac{32}{5}\frac{G^4}{c^5}\frac{M^3 \mu^2}{a^5}$

Gravitational force: $F_G = G\frac{Mm}{r^2}$

Total orbital energy: $E = - \frac{1}{2}\frac{G\mu M}{a}$

and some other more fundamental ones that do not need to be written here.

---

Areas for improvement:

1. Using C++ and OpenGL for better efficiency (maybe?)
2. Adding the possibility to use stars of different masses (A MAJOR PROBLEM)

---

In the simulation there is a constant dt that determines the amount of small fragments that time will be cut into. To get better (more acurate) results, you can lower the number. It, however, increases the number of calculations made by the computer, prolonging the time of completion.

For the code to work, some dependencies are necessary. To install them, run  `pip install numpy pygame matplotlib` . After doing this and downloading the python files, you are ready to go.

---

A plot created at the end of the simulation with constants seen in the program on github:

<img width="956" height="982" alt="GW_collapse" src="https://github.com/user-attachments/assets/28221614-c068-417c-b0af-94d92a123da8" />

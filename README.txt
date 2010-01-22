Izlučivanje značajki lica Gaborovim filtrom
===========================================


1) Sadržaj CD-a
===============
- data/ - direktorij sa uzorcima
- doc/ - direktorij s dokumentacijom
- src/ - direktorij s izvornim/izvršnim kodom
- lica.model - naučeni model SVM klasifikatora
- README.txt - ova datoteka


2) Upute za pokretanje
======================
Projekt je napisan u skriptnom jeziku pythonu tako da je izvorni kod ujedno
i izvršni.

2.1) Ovisnosti
==============
Za pokretanje potrebno je instalirati:
- Python (verziju 2.5 ili noviju) - http://python.org/
- Python modul scipy - http://www.scipy.org/
- Python modul numpy - http://numpy.scipy.org/
- Python modul PIL - http://www.pythonware.com/products/pil/
- LibSVM - http://www.csie.ntu.edu.tw/~cjlin/libsvm/

2.2) Pokretanje učenja
======================
Treniranje klasifikatora se vrši train.py skriptom.
- Primjer korištenja:
bash-4.0$ python train.py -m ../lica.model ../data/*
Skipping non-nrm file ../data/readme.txt
Ukupno zadano 295 razreda uzoraka.
Ukupno zadano 2360 uzoraka.

Training libsvmclassifier classifier.
Done!
Model for libsvmclassifier classifier saved to: ../lica.model

2.3) Pokretanje klasifikacije
=============================
Klasifikacija se izvodi preko classify.py skripte.
- Primjer korištenja:
Klasifikacija:
bash-4.0$ python classify.py -m ../lica.model ../data/006_4_2.nrm ../data/007_4_2.nrm ../data/008_4_2.nrm
Ukupno zadano 3 uzoraka.

Classifying by libsvmclassifier classifier.
../data/006_4_2.nrm is classified as 006
../data/007_4_2.nrm is classified as 007
../data/008_4_2.nrm is classified as 008

Putanje odgovaraju putanjama na CD-u.
Ako se python nalazi uz izvršnoj putanji (PATH), postupak je jednak za operacijske sustave Windows i Linux.

2.4) Pokretanje evaluacije klasifikatora
========================================
Evaluacija se vrši skriptom test.py.
- Primjer poziva:
bash-4.0$ python test.py ../data/*


3) AUTORI
======
Tomislav Reicher (voditelj)
Krešimir Antolic
Igor Belša
Marko Ivankovic
Ivan Krišto
Maja Legac
Tomislav Novak


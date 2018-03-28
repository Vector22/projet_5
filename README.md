# projet_5
First release of the Open Food Facts (project_5)

#obtention des fichiers du programme git clone https://github.com/Vector22/projet_4_test

#installation Placez vous dans votre environement virtuel et installez les paquets requis

pip install -r requirements.txt

#configuration de la base de donnees Ouvrez le fichier dbconfig.py modifier les valeus des champs du dictionnaire cfg pour les adapter a votre config personnelle.

Cependant, assurez vous d'avoir cree une base de donnees mysql et d'y etre connecte au moins une fois

#initialisation de la base de donnees Notez que cette partie depend quelque peu de vos attentes sur la bd: voulez vous des dizaines, centaines ou milliers de categories ? A vous de voir ! L'initialisation de la base etant faites entierement des donnees recuperees en ligne, alors cela peut etre tres long pour un grand volume de donnees; et depend biensure du debit de votre connexion internet.

Donc pour avoir un nombre de categorie d'aliments different que celui par defaut du programme, ouvrez les fichier [filldb.py] et [functions.py] et chamger la valeur de MAX_FOODS_CAT. Aussi les aliments etant groupes par categories alors vous pouvez eventuelement modifier la valeur de MAX_FOODS_PAGES pour permetre un grand nombre d'aliments par categories. Nb: une page compte environ 20 aliments, don si vous mettez 5, vous aurez environ 100 aliments par categories.

La premiere fois que vous lancez le programe, faites: python initdb.py cela permettra de recuperer les donnes

ensuite:
python run.py
le programme lui meme...

Pour les autres fois, si vous ne voulez pas reinitialiser la bd, alors faites: python run.py

Et voila c'est encore incomplet et assez instable alors si vous rencontrez des bugs n'hesitez pas a me contacter au rekinvector@gmail.com

Amusez vous bien...

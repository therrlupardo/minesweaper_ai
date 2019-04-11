# MINESWEEPER AI
Repozytorium projektu z przedmiotu Sztuczna Inteligencja.
Rozwiązywanie sapera za pomocą sieci neuronowych.

# Najważniejsze informacje
* Będziemy się uczyć na [saper](http://minesweeperonline.com)
* Pobieranie danych + wykonywanie akcji: [Selenium](https://selenium-python.readthedocs.io)


# Instalacja
* Zalecana jest anaconda, ale do uruchomienia samego rozwiązywania algorytmem wystarczy instalajca kilku bibliotek
* Potrzebne są ```python 3.6.*```,```selenium 3.141.0```,```numpy 1.16.2```(konieczne do algorytmu), ```tensorflow 1.13.1```, ```tensorflow-gpu 1.12``` (konieczne do uczenia sieci neuronowej)
* Selenium wymaga sterownika oraz przeglądarki, dokładna instrukcja [tutaj](https://selenium-python.readthedocs.io)
* Anaconda dostępna jest [tutaj](https://www.anaconda.com/distribution/)
* Aby wszystko ładnie działało, należy w Anacondzie utworzyć nowe środowisko ```conda create --name nazwa_srodowiska```, następnie uruchomić je za pomocą ```conda activate nazwa_srodowiska```
* Teraz należy zainstalować powyższe biblioteki za pomocą ```conda install python==3.6.8 numpy==1.16.2 ...```
* Pozostaje wybranie utworzonego środowiska w pycharmie, ```settings -> Project -> Project Interpreter```. W opcji ```add python interpreter``` należy dodać ścieżkę do utworzonego środowiska. Znajduje się ono domyślnie w folderze ```envs``` w folderze instalacyjnym anacondy.
# Dodatkowe źródła wiedzy
* [JAVA + logic](https://luckytoilet.wordpress.com/2012/12/23/2125/) - blog post o pisaniu AI rozwiązującym sapera.
* [repo java](https://github.com/luckytoilet/MSolver/blob/master/MSolver.java) - repozytorium do powyższego
* [sieć neuronowa python](https://github.com/ryanbaldini/MineSweeperNeuralNet) - repozytorium z gotową, wytrenowaną siecią neuronową rozwiązującą sapera. Chyba ten sam autor co powyższe.
* [macierze](https://massaioli.wordpress.com/2013/01/12/solving-minesweeper-with-matricies/) - rozwiązywanie sapera za pomocą macierzy. Raczej nie o to chodzi, ale może się przydać. 
* [repo macierze](https://bitbucket.org/robertmassaioli/minesweeper-and-matricies/overview) - repozytorium do powyższego

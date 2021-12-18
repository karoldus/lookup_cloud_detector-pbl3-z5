# Monitorowanie pokrywy chmur
Projekt detektora chmur oparty o sieć czujników IoT w ramach przedmiotu PBL-3.

Zespół: Michał Ciesielski, Karol Duszczyk, Kamil Kmieć\
Opiekun: mgr inż. Marcin Kołakowski

## O projekcie
Celem projektu jest stworzenie rozproszonego systemu IoT umożliwiającego ocenę stopnia zachmurzenia nieba na danym obszarze. Obecnie taka ocena pokrywy chmur jest dokonywana poprzez analizę zdjęć satelitarnych lub wykorzystanie zaawansowanych czujników laserowych. Zdjęcia satelitarne wydają się wystarczającym źródłem informacji dla działań związanych z prognozowaniem pogody, jednak są niewystarczająco szczegółowe, aby spełnić wymagania osób zajmujących się zawodowo lub hobbystycznie obserwacjami astronomicznymi. Duża dokładność pomiarów dokonanych na obszarze prowadzenia takich obserwacji jest kwestią istotną, ponieważ nawet niewielkie zachmurzenie może skutecznie uniemożliwić prawidłowe ich wykonanie. Problem ten mogłoby rozwiązać opracowanie sieci czujników zbierających dane o aktualnie panujących warunkach pogodowych na danym obszarze połączonej z aplikacją prezentującą użytkownikowi interesujące go informacje w przystępnej formie.

W projekcie wykorzystywane są technologie: LoRaWAN, MQTT

Szczegółowe informacje można znaleźć w dokumentacji projektu.

## Oprogramowanie
W projekcie wykorzystywane jest oprogramowanie dla węzła pomiarowego (sensor_node) i serwera (server).

### sensor_node
- main.py - główny plik
- lora.py - funkcje odpowiedzialne za obsługę komunikacji LoRaWAN
- sensors.py - funkcje odpowiedzialne za obsługę czujników (przykładowe zastosowanie znajduje się w sensors_example.py)
- json_configuration.py - funkcje pomocnicze do obsługi plików json
- configuration.json - plik z danymi konfiguracyjnymi
- requirements.txt - wymagane zależności

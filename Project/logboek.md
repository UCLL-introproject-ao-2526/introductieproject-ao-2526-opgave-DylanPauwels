## 15 november 1908 
Start van het project na voldoende challenges gedaan te hebben. Start met het maken van de files en deze al een keer te pushen naar de repository om te zorgen dat dit vlot verloopt.
Opnieuw lezen hoe het hele Git push gebeuren werkt

## 15 november 2120 
Tot de conclusie gekomen tijdens het volgen van tutorial dat pygame niet correct werkt ten gevolge van foutief geïnstalleerde Python 3.14. Complete reinstall naar versie 3.13.9 uitgevoerd. Test toonde pygame venster en eerste knop.
Nadien verder de tutorial gevolgd tot basis af is. Veel moeten pauzeren om over te nemen, hoe had ik dit efficiënter kunnen doen? 

## 16 november 1730 
Kleine aanpassingen maken om vertrouwd te raken met de code en kleine details te testen. Ideeën om uit te voeren: 'New hand' & scores meer centraliseren (op zicht), spelen met verschillende kleuren, uitzoeken hoe waardes kaart in alle hoeken te krijgen.
-> lijn 30 een dubbele 'outcome = 0' gevonden, stond ook reeds in lijn 27. Wissen en testen (VSC geeft rode melding???)

## 16 november 1824 
kleuren aangepast naar eigen voorkeur, geland op grijstonen, verschillende percentages mogelijk. Ook getest met groen maar werkt niet, mogelijkheid andere gradaties kleuren?
waardes kaarten in alle hoeken, enkele lijnen kopieren en aanpassen. ('10' komt net uit de kaart maar meer verplaatsen naar links verpest andere hun zicht te erg. Is hier een oplossing voor? -> Googlen wanneer tijd, geen prio.)
(rode) meldingen VSC gutter = aanpassingen sinds push? Verdwenen na push anyway

Welke aanpassingen kunnen nog gemaakt worden met deze basis? Window resizable maken? tekens toevoegen centraal per kaart? (Eventueel ander spel? Poker? Balatro? Hoe + mogelijk in 20 ish uur?)
Starten met (uitzoeken) resizable maken, grootte van de window stoort me wanneer ik wissel van scherm.

## 16 november 2100
Na opzoekwerk volgende gevonden en geimplenteerd;
pygame.RESIZABLE, logical size en surface toegevoegd aan init variables,
functie screen to logical, alles qua screen vervangen door logical surface.
Scherm is aanpasbaar tot full screen, verhouding = fix -> zwarte banden wanneer scherm niet perfect aansluit. Is dit het resultaat dat ik wou?
Misschien lay-out nog aanpassen naar landschap ipv portret? Volstaat init verhouding aanpassen + opnieuw centreren van alle knoppen/kaarten?

## 16 november 2330
Gespeeld met verschillende verhoudingen, waarvoor hebben we andere verhouding nodig? Welke content komt nog bij het spel? Bets plaatsen?
Bekijken voor het implementeren van bets volgende werkmoment project ;
Hoe beginnen? Copy paste van andere knoppen? -> Lay out/locatie aanpassen
Wanneer moeten de knoppen beschikbaar zijn? Voor hand gedeeld/zichtbaar is of bij zien eerste kaart? 

 
## 22 november 1345
Idee van vorige week proberen implementeren, starten met bet x, all-in en clear voor evt foutief inzetten
Hoeveelheden? 10, 50, 100, 500 -> Voldoende? Te veel? Kan nog aangepast worden

## 22 november 1550
Bij eerste ronde na opstarten kan er nu ingezet worden, spel start na place bet.
Na elke hand moet er nochtans ook ingezet kunnen worden en een verandering van kapitaal zijn anders is betting nog steeds nutteloos.
Volgens blakcjack regels bij normale winst return 1 op 1 of blackjack 3 op 2.
-> Na place bet = geld van kapitaal afgetrokken dus return bij winst zou huidige inzet + 2 of 2.5 moeten zijn.
 Mogelijke uitkomsten volgens google bij blackjack: Win, lose, push, blackjack
 Deze opties hernemen in helper functies.

 ## 23 november 1630
Verder met UI betting in verdere rondes na onderbreking gisteren
Ergens in de fout gegaan, game crashes bij all-in. Na gespeelde hand geen mogelijkheid tot nieuwe bet, ondanks dat de functies bij helprs en main geplaatst zijn -> uitzoeken waar de fout zit

## 23 november 2020
Extra variabele toegevoegd "stake_reserved" om duidelijkere info te geven buiten current_bet om
Outcome possibilities ergens de nummers gewisseld, inconsistentie creeerde crash? Outcomes aangepast
Momenteel mogelijk om na een hand opnieuw in te zetten, terugkeer naar bet screen oke.
Bij inzetten tot '0' of all in geen mogelijkheid meer tot deal hand:
Uitzoeken waar deze blokkeert? Pygame crashed niet maar UI reageert ook niet meer. 

## 23 november 2035
in main game loop "if bankroll <= 0 disable game start' -> deze aanpassen met toevoeging stake reserved?
-> Deal hand terug mogelijk na krijgen melding 'out of money', na hand geen nieuwe bet meer mogelijk omdat game end getriggerd is(?)
Hoe aan te pakken? Game end mag pas komen als $0 door bet en verlies hand

## 23 november 2100
Enkele aanpassingen zorgden voor onverwacht sluiten bij "$0" -> import traceback om eventuele errors te lezen
-> enkele nieuwe lijnen verkeerde shift + aanpassing font naar smallerfont door tab smallerfontfont ontdekt
Spel sluit niet meer automatisch maar stopt nog steeds na de hand waar all in gegaan is ongeacht resultaat -> neemt ergens nog steeds bankroll <= 0 als absoluut?

## 23 november 2200
Na opzoeken verschillende kanalen debug lines ingevoerd om per frame te bekijken of de statussen kloppen
-> FPS tijdelijk verlaagd om overzicht te bewaren (later verhogen voor soepelheid)
Niet alle debug lines komen zichtbaar in de terminal? -> is er een functie die niet effectief gecalled wordt?
-> resolve en payout lines missen
resolve(result) -> result in grijs, verwijderd en nu komt er enkel debug lines wanneer initial blackjack
resolve ook laten gelden wanneer andere handen gespeeld worden

## 23 november 2310
problemen kwamen onder andere uit verwarring bij uitkomsten, deze als constanten bij globals gezet met benamingen
-> na all in + winst kan er verder gespeeld worden
Game crashte bij initial blackjack: terminal geeft fout in lijn 318 -> result[result] vervangen door labels
Volgende stap te ondernemen = indien bankroll $0 en verliezende hand -> "Game Over" + optie om terug opnieuw te beginnen
Hoe hieraan te beginnen? Mogelijkheid main game loop opnieuw te laten starten na een "Try again" knop? 
Heb ik hier nog de tijd voor? Time's precious, hoeveel tijd heb ik al gespendeerd? Ongeveer de aangeraden timing van ca. 20hr? Andere prio's eerst afwerken?

## Reflectie Feedback
Over het algemeen valt er niet te discussiëren over of de feedback correct is, het legt overal simpele pijnpunten of details bloot die beter kunnen. De makkelijke voorstellen voor aanpassen die erbij worden gegeven zijn ook mooi meegenomen. Het toepassen op dit project zal jammer genoeg niet lukken denk ik, maar de lessen neem ik mee naar de rest van de vakken.
Er wordt bijvoorbeeld enkele malen aangehaald dat sommige zaken gerust korter kunnen, door oftewel lijnen samen te voegen of extra variabelen te gebruiken waar veel herhaling is, zoals bijvoorbeeld de x-coördinaten. Hier had ik zelf niet eerder over nagedacht, maar dit vind ik wel een goede tip om in de toekomst te kunnen toepassen. Simpel maar efficiënt.
De opmerking aangaande het debug gebeuren is eentje waar ik zelf ook mee in de knoop lag. Dit gedeelte liet me het hardste twijfelen of het geheel nog wel leesbaar was, de bevestiging die hier bij komt kijken was dan ook wel verwacht. Een debug functie proberen implementeren zou veel overzichtelijker zijn en vermoedelijk ook makkelijker om nadien terug eruit te halen indien "klaar" of "niet meer nodig". 

Enkel met de opmerking bovenaan over de "game variables" was ik om te beginnen niet akkoord. Ik had hier eerst niet echt aandacht voor, dit was namelijk letterlijk overgenomen uit de tutorial, niet mijn fout dus, toch? Bij de volgende keren de feedback lezen om rustig te kunnen reflecteren, weg van het scherm en niet gewoon te reageren bleef dat zinnetje echter wel een beetje een door in het oog. Het voelde "oneerlijk", maar dat ben je gewoon na 9 jaar defensie, waarom trek ik me dit aan?
Uiteindelijk bleek dit dan ook mijn favoriet gedeelte uit de feedback, doordat het me aanzet tot nadenken: Waarom neem je dit persoonlijk, je hebt het toch maar gewoon overgenomen?
Dit deed me beseffen dat ik liever een fout maak dan zoeken naar excuses om achter te schuilen, ik had ook een tweede maal kunnen nadenken en tot de conclusie komen dat het "game variables" noemen wanneer je bezig bent met de variables van een game, dit inderdaad gewoon overbodig is. 
Niemand heeft mij gedwongen tot het letterlijk overnemen, waarom ben je dan niet iets kritischer? Blijf zelf nadenken en werk verder met aangeboden middelen maar durf deze ook te verbeteren.
Iets waarvan ik dacht dat het me van nature lukt, bleek toch iets waar ik bewuster bij stil moet staan. 
In m'n huidige job, zeker in groepsverbanden, nemen we ook altijd kritiek op als een collectief werkpunt onder het motto "de ketting is maar zo sterk als de zwakste schakel". Bij een individueel project als dit, waar je zaken overneemt van iemand anders is het uiteindelijk net zo goed iets waar die collectieve team-player mindset nodig is. 
Hoe kan ik toekomstig externe bronnen (Google, YouTube, AI?,...) het beste gebruiken om een zo goed mogelijk resultaat te bekomen.
Deze denkoefeningen, het besef, de reminder "voetjes op de grond" en durf je eigen grootste criticus te zijn.
Een mentale les die ik goud waard vindt, ontstaan uit een klein detail dat ik initieel wou negeren.
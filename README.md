# RecipeList
Kolegij: Poslovni informacijski sustavi

-------------------

## Opis i svrha web aplikacije

Web aplikacija RecipeList namjenjena je gotovo svakom tko želi nešto kuhati ili podijeliti s drugima što kuhati. Osim osnovnih ima i nekoliko dodatnih funkcija koje mogu značajno poboljšati korisničko iskustvo korištenja aplikacije. 

 ## Funkcionalnosti

 ### Osnovne funkcionalnosti - CRUD:
  - Dohvaćanje i prikaz recepata iz baze podataka
  - Dodavanje novih recepata u bazu podataka
  - Uređivanje podataka već postojećih recepata
  - Brisanje recepata

### Dodatne funkcionalnosti:
  - Mogućnost više korisnika
  - Korisnici mogu brisati i mijenjati samo svoje recepte
  - Svaki korisnik ima poseban "tab" za pregled svih svojih recepata
  - Svaki korisnik može spremiti bilo koji recept i lakše ga vidjeti na posebnom "tabu"
  - Recepti se mogu dodatno pretraživati prema njihovim nazivima
  - Recepti se mogu sortirati prema nazivu i kategoriji, uzlazno i silazno
  - Na "tabu" statistika mogu se vidjeti 3 grafa koji prikazuju različite podatke iz baze podataka


*Napomena: U aplikaciji se trenutno ne mogu registrirati niti prijaviti različiti korisnici već su hardcodirani u obliku "usera1" i "usera2", no njihovo dodavanje dodano je u funkcije baze podataka te se lako u budućnosti može implementirati register/login prozor.*

## Struktura web aplikacije
Web aplikaciju pokreće samo jedan malo kompleksniji web servis. Serivs obavlja sve routing, osnovne, te dodatne funkcije. 

## Pokretanje web aplikacije
 1. Preuzeti sve datoteke ili klonirati repozitorij
 2. Pomoću CLI sučelja navigirati u mapu aplikacije (`/cond-env`)
 3. izraditi docker image pomoću naredbe: `sudo docker build --tag recipe-list:1.0 .`  *<--- napomena: ne zaboraviti točku na kraju*
 4. Pokrenuti docker kontejner pomoću izrađene docker slike: `sudo docker run -d -p 8080:8080 recipe-list:1.0`
 5. pokrenutom kontejneru tj aplikaciji pristupa se na lokalnom web pregledniku na lokaciji `localhost:8080`

*Napomena: ja sam radio preko wsl subsitema tako da sam u app.py na dnu morao definirati `host=0.0.0.0`, što nije radilo kada sam pokretao sa dockera na windowsu u kojem slučaju se samo `host=0.0.0.0` mora obrisati kako je zakomenitrano i u samom app.py dokumentu (možda se samo meni desio bug pa će raditi svakako)*

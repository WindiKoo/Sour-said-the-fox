import pygame
import random
from threading import Timer

#################################

# Näyttö
pygame.init()
nayton_leveys = 640
nayton_korkeus = 480
naytto = pygame.display.set_mode((nayton_leveys, nayton_korkeus))
pygame.display.set_caption("Sour said fox")

# Värit ja fontit
punainen = (155, 0, 10)
musta = (0, 0, 0)
harmaa = (100,100,100)
ruskea = (90, 60, 40)
tumma_harmaa = (50, 50, 50)
valkoinen = (255,255,255)
fontti_40 = pygame.font.SysFont("Arial", 40)
fontti_26 = pygame.font.SysFont("Serif", 26)
fontti_20 = pygame.font.SysFont("Serif", 20)

# Aloitusnapin muuttujat
napin_leveys = 130
napin_korkeus = 22
nappi_x = nayton_leveys/2 - napin_leveys/2
nappi_y = 340

# Kuvien lataus
robo = pygame.image.load("lilfox.png")
kolikko = pygame.image.load("rowan_berries.png")
hirvio = pygame.image.load("shrooms.png")
tausta = pygame.image.load("woods.png")
# Jos pelin kuvin lataaminen ei toimi muodossa "kuva.png",
# voi kokeilla muotoa "src/kuva.png".
# Voit joutua muuttamaan muotoa, jos tämä toimii koneellasi eri tavalla.


# Robotin muuttujat
x_robo = 0
y_robo = 475-robo.get_height()
robon_leveys = robo.get_width()
robon_korkeus = robo.get_height()
oikealle = False
vasemmalle = False

# Putoavien asioiden muuttujat
kolikon_leveys = kolikko.get_width()
kolikon_korkeus = kolikko.get_height()

hirvion_leveys = hirvio.get_width()
hirvion_korkeus = hirvio.get_height()

putoavat = []
y = -10
nopeus_y = 0.8
nopeus_x = 0
id = 1

# Pisteet
pisteet = 0
pisteputki = 1
parhaat_pisteet = 0

# Kello
kello = pygame.time.Clock()

# Nopeutustoiminnot
nopeus = 10
nopeutus = None
intervalli = 20000 # noin 20s välein peli nopeutuu

#####################################
  
# Tällä käsitellään putoavia olioita
class Putoavat:
  def __init__(self, id: int, x: int, y: int, nopeus_x: int, nopeus_y: int, tyyppi: int):
    self.id = id
    self.x = x
    self.y = y
    self.nopeus_x = nopeus_x
    self.nopeus_y = nopeus_y

    if tyyppi == 1:
      self.tyyppi = "hirvio"
      self.hirvio_rect = hirvio.get_rect()    
      self.hirvio_rect.inflate_ip(-20, -20)   # määritellään hirviön ala ja pienennetään sitä hieman
    else:
      self.tyyppi = "kolikko"

  def liikuta_putoavia(self):
    if self.tyyppi == "kolikko":
      if self.nopeus_y >= 0 and self.y+kolikon_korkeus >= 475:
        self.nopeus_y = 0
        return 1 # kolikko osuu maahan
      elif (self.x+25 > x_robo and self.x+10 < x_robo + robon_leveys) and (self.y + 35 > y_robo and self.y+35 < y_robo + robon_korkeus):
        return -1 # saadaan kolikko kiinni
      elif self.nopeus_y >= 0 and self.y+kolikon_korkeus < 475:
        self.y += self.nopeus_y 
        naytto.blit(kolikko, (self.x, self.y))
        return 0 # kolikko jatkaa matkaa

    if self.tyyppi == "hirvio":
      if self.nopeus_y >= 0 and self.y >= nayton_korkeus + 50:
        self.nopeus_y = 0
        return 2 # hirviö osuu maahan
      elif self.hirvio_rect.colliderect(robo_rect): 
        return 3 # hirviö osuu Roboon
      elif self.nopeus_y > 0 and self.y < nayton_korkeus + 50:
        self.y += self.nopeus_y 
        self.hirvio_rect.topleft = [self.x+10,self.y+10]
        naytto.blit(hirvio, (self.x, self.y))
        return 0 # hirviö jatkaa matkaa

######################################

# Tätä kutsutaan heti pelin pyörityksen alussa
def aloitusruutu():
  while True:
    for tapahtuma in pygame.event.get():

      if tapahtuma.type == pygame.MOUSEBUTTONDOWN:
        if nappi_x <= mouse[0] <= nappi_x+napin_leveys and nappi_y <= mouse[1] <= nappi_y+napin_korkeus:
          return None

      if tapahtuma.type == pygame.KEYDOWN:
        if tapahtuma.key == pygame.K_n:
          return None
        if tapahtuma.key == pygame.K_ESCAPE:
          pygame.quit()
          quit()

      if tapahtuma.type == pygame.QUIT:
        pygame.quit()
        quit()

    naytto.fill(tumma_harmaa)
    naytto.blit(tausta, (0,0))

    # Ohjeruutu
    pygame.draw.rect(naytto,musta,[130,85,380,335])
    pygame.draw.rect(naytto,valkoinen,[135,90,370,325])
    ohjeet1 = fontti_26.render(f"SOUR SAID FOX", True, musta)
    ohjeet2 = fontti_20.render(f"Ota kiinni pihlajanmarjoja, mutta", True, musta)
    ohjeet3 = fontti_20.render(f"varo osumasta kärpässieniin!", True, musta)
    ohjeet4 = fontti_20.render(f"Mitä useamman pihlajanmarjan saat kiinni", True, musta)
    ohjeet5 = fontti_20.render(f"ilman että yksikään osuu maahan,", True, musta)
    ohjeet6 = fontti_20.render(f"sitä suuremmaksi pistekerroin kasvaa.", True, musta)
    naytto.blit(ohjeet1, (nayton_leveys/2 - ohjeet1.get_width()/2, 120))
    naytto.blit(ohjeet2, (nayton_leveys/2 - ohjeet2.get_width()/2, 180))
    naytto.blit(ohjeet3, (nayton_leveys/2 - ohjeet3.get_width()/2, 200))
    naytto.blit(ohjeet4, (nayton_leveys/2 - ohjeet4.get_width()/2, 240))
    naytto.blit(ohjeet5, (nayton_leveys/2 - ohjeet5.get_width()/2, 260))
    naytto.blit(ohjeet6, (nayton_leveys/2 - ohjeet6.get_width()/2, 280))

    # Aloitusnappi
    mouse = pygame.mouse.get_pos()
    teksti_nappi = fontti_20.render(f"Aloita uusi peli", True, musta)
    teksi_x = (napin_leveys - teksti_nappi.get_width())/2
    pygame.draw.rect(naytto,musta,[nappi_x+3,nappi_y+3,napin_leveys,napin_korkeus])
    pygame.draw.rect(naytto,harmaa,[nappi_x,nappi_y,napin_leveys,napin_korkeus])
    naytto.blit(teksti_nappi, (nappi_x + teksi_x, nappi_y+2))

    # Ohjeteksti
    teksti_ohje = fontti_20.render(f"(Uusi peli: N    Poistu: esc)", True, punainen)
    paikka_ohje = teksti_ohje.get_width()
    naytto.blit(teksti_ohje, (nayton_leveys/2 - paikka_ohje/2, 370))

    pygame.display.update()
    kello.tick(10)  

#####################################

# Tänne päädytään kun peli päättyy. Pelin voi aloittaa uudestaan tai sulkea.
def game_over():
  while True:
    for tapahtuma in pygame.event.get():

      if tapahtuma.type == pygame.MOUSEBUTTONDOWN:
        if nappi_x <= mouse[0] <= nappi_x+napin_leveys and nappi_y <= mouse[1] <= nappi_y+napin_korkeus:
          return None

      if tapahtuma.type == pygame.KEYDOWN:
        if tapahtuma.key == pygame.K_n:
          return None
        if tapahtuma.key == pygame.K_ESCAPE:
          pygame.quit()
          quit()

      if tapahtuma.type == pygame.QUIT:
        pygame.quit()
        quit()

    # Game_over -teksti
    teksti = fontti_40.render(f"GAME OVER", True, punainen)
    paikka = teksti.get_width()
    naytto.blit(teksti, (nayton_leveys/2 - paikka/2, 150))
    
    # Pisteet -teksti
    teksti2 = fontti_26.render(f"Sait {pisteet} pistettä", True, punainen)
    paikka2 = teksti2.get_width()
    naytto.blit(teksti2, (nayton_leveys/2 - paikka2/2, 200))

    # Ennätyspisteet -teksti
    teksti3 = fontti_20.render(f"Ennätyksesi pelikierroksilla on {parhaat_pisteet} pistettä", True, punainen)
    paikka3 = teksti3.get_width()
    naytto.blit(teksti3, (nayton_leveys/2 - paikka3/2, 235))

    # Ohjeteksti
    teksti_ohje = fontti_20.render(f"(Uusi peli: N    Poistu: esc)", True, punainen)
    paikka_ohje = teksti_ohje.get_width()
    naytto.blit(teksti_ohje, (nayton_leveys/2 - paikka_ohje/2, 370))

    # Aloitusnappi
    mouse = pygame.mouse.get_pos()
    teksti_nappi = fontti_20.render(f"Aloita uusi peli", True, musta)
    teksi_x = (napin_leveys - teksti_nappi.get_width())/2
    pygame.draw.rect(naytto,musta,[nappi_x+3,nappi_y+3,napin_leveys,napin_korkeus])
    pygame.draw.rect(naytto,harmaa,[nappi_x,nappi_y,napin_leveys,napin_korkeus])
    naytto.blit(teksti_nappi, (nappi_x + teksi_x, nappi_y+2))
    
    pygame.display.update()
    kello.tick(10)

######################################
    
# Peli alkaa tästä, aloitusruudun jälkeen edetään pelilooppiin
alkaa = aloitusruutu()
if alkaa == None:
  edellinen = pygame.time.get_ticks()

while True:
  for tapahtuma in pygame.event.get():
    if tapahtuma.type == pygame.KEYDOWN:
      if tapahtuma.key == pygame.K_LEFT:
        vasemmalle = True
      if tapahtuma.key == pygame.K_RIGHT:
        oikealle = True

      if tapahtuma.key == pygame.K_ESCAPE:
          pygame.quit()
          quit()

    if tapahtuma.type == pygame.KEYUP:
      if tapahtuma.key == pygame.K_LEFT:
        vasemmalle = False
      if tapahtuma.key == pygame.K_RIGHT:
        oikealle = False
  
    if tapahtuma.type == pygame.QUIT:
      exit()

  # Näytön tausta
  naytto.fill(tumma_harmaa)
  naytto.blit(tausta, (0,0))
  pygame.draw.line(naytto, ruskea, (0,nayton_korkeus - 5), (nayton_leveys, nayton_korkeus - 5), 6)
  
  # Pisteet ja kerroin
  teksti = fontti_26.render(f"Pisteet: {pisteet}", True, punainen)
  naytto.blit(teksti, (5, 10))
  teksti = fontti_26.render(f"Kerroin: {pisteputki}", True, punainen)
  naytto.blit(teksti, (nayton_leveys - 140, 10))

  # Robo liikkuu näin
  naytto.blit(robo, (x_robo, y_robo))
  if oikealle:
    if nopeus > 4: 
      x_robo += 5
    else:           # Robon nopeus kasvaa kun peli on nopeutunut tarpeeksi
      x_robo += 7
  if vasemmalle:
    if nopeus > 4:
      x_robo -= 5
    else:
      x_robo -= 7

  x_robo = max(x_robo,0)
  x_robo = min(x_robo,640-robo.get_width())

  robo_rect = robo.get_rect()
  robo_rect.topleft = [x_robo,y_robo]

  # Putoavat asiat luodaan ja niitä liikutetaan
  nyt = pygame.time.get_ticks()
  if nyt - edellinen >= intervalli and nopeus > 1: # tietyllä aikajänteellä peli nopeutuu
      edellinen = nyt
      nopeus -= 1
      print(nopeus)
      
      
  if nopeus <= 10 and nopeus > 8:  # myös ilmaantuvuus kasvaa nopeuden kasvaessa 
    ilmestyy = random.randint(0,95)
  elif nopeus <= 8 and nopeus > 6:
    ilmestyy = random.randint(0,80)
  elif nopeus <= 6 and nopeus > 4:
    ilmestyy = random.randint(0,65)
  elif nopeus <= 4 and nopeus > 2:
    ilmestyy = random.randint(0,50)
  elif nopeus <= 2 and nopeus > 1:
    ilmestyy = random.randint(0,30)
  else:
    ilmestyy = random.randint(0,20)
  
  if ilmestyy == 0: # vain arvan osuessa nollaan tuotetaan putoava olio
    x = random.randint(0, 640-kolikon_leveys)
    putoavat.append(Putoavat(id, x, y, nopeus_x, ((random.randint(5,15))/nopeus), (random.randint(1,2))))
    id += 1

  for r in putoavat:
    liikkuu = r.liikuta_putoavia()
    if liikkuu == 0:        # putoava asia matkalla
      pass
    elif liikkuu == 1:      # kolikko osuu maahan ja katoaa
      putoavat.remove(r)
      pisteputki = 1        # pisteputki nollaantuu kun kolikko osuu maahan
    elif liikkuu == -1:     # kolikko saatiin kiinni
      putoavat.remove(r)
      pisteet += pisteputki  # pisteputki lisää kolikon arvoa
      pisteputki += 1
    elif liikkuu == 2:      # hirviö poistuu ruudusta ja katoaa
      putoavat.remove(r)
    elif liikkuu == 3:      # hirviö sai Robon kiinni ja peli päättyy
      putoavat.remove(r)
      oikealle = False
      vasemmalle = False
      if pisteet > parhaat_pisteet:
        parhaat_pisteet = pisteet
      ohi = game_over()
      if ohi == None:       # uuden pelin aloitus, muuttuneet arvot asetetaan alkuarvoihin
        pisteet = 0
        pisteputki = 1
        putoavat.clear()
        id = 1
        nopeus = 10
        edellinen = pygame.time.get_ticks()
        break
  
  pygame.display.flip()  

  kello.tick(60)
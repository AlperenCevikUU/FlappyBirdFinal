import pygame
from pygame.locals import *
import random
import os
# pygame'e ait genel ve ses icin baslatma fonksiyonlari(Alperen cevik)
pygame.init()
pygame.mixer.init()
# Oyunun kare hizinin ayarlanmasi(Alperen Cevik)
clock = pygame.time.Clock()
fps = 60
# pencere boyutunun piksel olarak belirlenmesi (yagmur umutlu)
screen_width = 864
screen_height = 936
# girilen piksellerin pencereye tanimlanmasi ve pencerenin isminin atanmasi (yagmur umutlu)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird by Alperen,Yagmur, Emre')

# Yazi tiplerinin ve boyutlarinin ayarlanmasi(Alperen Cevik)
font = pygame.font.SysFont('Impact', 60)
text_font = pygame.font.SysFont('Impact', 42)
menu_font = pygame.font.SysFont('Impact', 32)

#renkleri tanimlama(Emre Kurt)
white = (255, 255, 255)
black = (0, 0, 0)
coral = (255, 105, 105)
orange = (255, 105, 30)
gray = (119, 136, 153)

#// oyun degiskenlerini tanimlama(Alperen Cevik)
flying = False
game_over = False
score = 0
death_count = 0
death_count_text = "Death Count:" #olme sayisi(alperen cevik)
score_text = "Score :" #anlik skor(Alperen)
best_text = "Best :" #yapilan en iyi skor(Alperen)
start_text = "Click Anywhere to Start" #baslamak icin herhangi bir yere tiklayin yazisi(Alperen)
scroll_speed = 4 # kusun ve ekranin kayma hizi(Alperen)
pipe_gap = 250 #boruların ortasindaki boslukların genisligi(Alperen)
pipe_frequency = 1500 #borularin spawn olma sikligi(Alperen)
ground_scroll = 0
last_pipe = pygame.time.get_ticks() - pipe_frequency #borularin spawninin algoritmasi(Alperen)
pass_pipe = False

# En yuksek skorumuzun kaydedilen kayit dosyasindan okunmasi(Alperen Cevik)
savefile = open('saves/data.txt','r') #best skorun kaydedildigi txt dosyasi(Alperen)
high_score = int(savefile.read()) #best skoru kaydetme ve txt dosyasinadn okuma komutu(Alperen)
savefile.close()

# Ses klasorunu ve icerdigi ses dosyalarini tanimlama(Alperen Cevik)
s = 'sound'

rst_snd = pygame.mixer.Sound(os.path.join(s, 'reset.wav')) #reset buyonuna basilinca cikan sesin eklenmesi(Alperen)
jmp_snd = pygame.mixer.Sound(os.path.join(s, 'jump.wav')) #ziplama ses efekti(Alperen)
hscore_snd = pygame.mixer.Sound(os.path.join(s, 'highscore.mp3'))#new high score olunca acilan ses(Alperen)
death_snd = pygame.mixer.Sound(os.path.join(s, 'death.wav')) #high score olmayinca ve olunce cikan ses(Alperen)


#Resimlerin yuklenmesi(Alperen Cevik)
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png') #zemin resmi(Alperen)
button_img = pygame.image.load('img/restart.png') #restart butonunun resmi(alperen)
gameover_img = pygame.image.load('img/gameover.png') #gameover resminin tanimlanmasi(alperen)
high_score_img = pygame.image.load('img/highscore.png')#new high score resminin tanimlanmasi(Alperen)
menu_img = pygame.image.load('img/menu.png')#menu arka plani(alperen)
leftclick = pygame.image.load('img/left2.png')#oyun baslamadan ekrana cikan click resmi(alperen)

# Ekrana metin ciktisi veren komut(Emre Kurt)
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))
# Oyunu bastan baslatmak icin gereken sifirlama komutlari(Alperen Cevik)
def reset_game():
	pipe_group.empty()
	flappy.rect.x = 100 #kusun x ekseninde tanimi(alperen)
	flappy.rect.y = int(screen_height / 2) #kusun y ekseninde tanimi(alperen)
	score = 0#yaninca skoru 0 yapan komut(Alperen)
	return score

# Kus sinifinin tanimi, ozelliklerin ve animasyonlarin olusturulmasi (yagmur umutlu)
class Bird(pygame.sprite.Sprite):

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.counter = 0
		#Kusların ekranda ki resimleri(Emre Kurt)
		for num in range (1, 4):
			img = pygame.image.load(f"img/bird{num}.png")
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.vel = 0
		self.clicked = False

		#animasyon gorsellerini tutacak self.images isimli listeyi olusturur (yagmur umutlu)

		#index , counter , velocity ve clicked'in baslangic degerleriyle tanimlanmasi (yagmur umutlu)


		#animasyonun for dongusuyle ayarlanmasi (yagmur umutlu)

	    #koordinat girisi icin hazirlik (yagmur umutlu)

	#Eger Kus ucuyorsa vel degerini 0.5 artirarak asagi dusmesini yani yercekimini saglar(Alperen cevik)
	def update(self):

		if flying == True:
			#Yercekimi uygulayan komut(Emre Kurt)
			self.vel += 0.5
			if self.vel > 8:
				self.vel = 8
			if self.rect.bottom < 768:
				self.rect.y += int(self.vel)
				
				#maximum hizi 8 , vel degerine gore yukari asagi hareketi saglayan komut satiri (yagmur umutlu)

		if game_over == False:
			#Zıplama komutu (Emre Kurt)
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				pygame.mixer.Sound.play(jmp_snd)
				self.vel = -10
			if pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False
				
				#eger yanmadiysak mause basilisini algılar, clicked degerini gunceller (yagmur umutlu)
				#kusun vel degerini degistirerek ziplamayi saglar ve ziplama sesini oynatir (yagmur umutlu)

			#Gorsellerin belirli zaman araliklariyla listeye eklenip cikarilmasiyla animasyonun olusmasi(Alperen cevik)

			flap_cooldown = 5
			self.counter += 1
			
			if self.counter > flap_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images):
					self.index = 0
				self.image = self.images[self.index]

				


			#kusun kafasinin yukari asagi bakmasini saglar(Alperen Cevik)
			self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
		else:
			#eger yandiysak kusun kafasinin yere bakmasini saglar(Alperen Cevik)
			self.image = pygame.transform.rotate(self.images[self.index], -90)

			#eger yanmadiysak kusun vel degerine gore kafasinin yukari veya asagi bakmasini saglar (yagmur umutlu)
			


# Borularin cok sayida spawn edilmesi icin sinif olarak olusturulmasi ve ayarlari(Alperen Cevik)
class Pipe(pygame.sprite.Sprite):

	def __init__(self, x, y, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/pipe.png")
		self.rect = self.image.get_rect()
		
		#pozisyon 1 ise boruyu yukaridan -1 ise asagidan spawn eder(Alperen Cevik)
		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
		elif position == -1:
			self.rect.topleft = [x, y + int(pipe_gap / 2)]

	#update konksiyonu ile ekran hizina gore yeni boru eklenir ve gecilenler silinir(Alperen Cevik)
	def update(self):
		self.rect.x -= scroll_speed
		if self.rect.right < 0:
			self.kill()

			#self.image ile boruya gorsellik saglar (yagmur umutlu)
		


# Kullanilacak butonun sinif ayarlari ve ozellikleri(Alperen Cevik)
class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
#Kullanilan butonun cizimi(Emre Kurt)
	def draw(self):
		action = False

		#pos degiskeni ile mousenin lokasyonunun atanmasi(Alperen Cevik)
		pos = pygame.mouse.get_pos()

		#Collidepoint fonksiyonu ile mouse butonun uzerinde mi kontrol edilir(Alperen Cevik)
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				action = True

		#Butonu cizdirir(Alperen Cevik)
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action

	


# Olusturdugumuz siniflar turunden yeni objeler olusturma ozellik verme ve gruplandirma(Alperen Cevik)
pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)

## Restart butonunun olusturulmasi(Alperen Cevik)
button = Button(screen_width // 2 - 60, screen_height // 2 - 21, button_img)

# Oyun calisir vaziyette iken calisacak olan sonsuz dongu(Alperen Cevik)

run = True
while run:

	clock.tick(fps)

	#Arka planı cizer(Emre Kurt)
	screen.blit(bg, (0,0))

	pipe_group.draw(screen)
	bird_group.draw(screen)
	bird_group.update()

	#Zemini cizer ve kaydırır(Emre Kurt)
	screen.blit(ground_img, (ground_scroll, 768))

	#Puanı kontrol eden algoritmanin olusturulmasi(Emre Kurt)
	if len(pipe_group) > 0:
		if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
			and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
			and pass_pipe == False:
			pass_pipe = True
		if pass_pipe == True:
			if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
				score += 1
				pass_pipe = False
	draw_text(str(score), font, white, int(screen_width / 2), 20)

	draw_text(str(death_count_text), text_font, white, 20, int(screen_height) - 60)
	draw_text(str(death_count), font, coral, 240, int(screen_height) - 75)

	#Baslatmak icin tıklama komutu(Emre Kurt)
	if pygame.mouse.get_pressed()[0] == 0 and flying == False and game_over == False:
		draw_text(str(start_text), font, white, 150, 300)
		screen.blit(leftclick, ( (screen_width / 2) + 50 , (screen_height / 2) - 80 ))

		#screen.blit fonksiyonu ile arka planin, yer yuzunun, baslangic ekranindaki yazi ve resimlerin, menu resimleri ve tesxtleri vb.seylerin cizdirilmesi (yagmur umutlu)
		#draw_text ile yazi yazdirilmasi (yagmur umutlu)
		#kusun borunun en sol koordinati ile en sag koordinati arasindaki gecis kontrol edilerek skor kazanma isleminin yapilmasi (yagmur umutlu)
		#eger mouse basili degilse, kus halihazirda ucmuyorsa ve yanmadiysak baslangic ekraninin olusturulmasi (yagmur umutlu)



	#Zorluk ayari(Emre Kurt)
	if score == 7:
		scroll_speed = 4.5
		pipe_gap = 240
	if score == 17: #zorluk seviyesinin artmasi hedeflenen skor(alperen)
		pipe_gap = 230 #pipe genisliginin azaltilmasi ile zorluk katilmasi(alperen)
		pipe_frequency = 1450 #pipe lerin olusturulma sikliginin artirilmasi(Alperen)
	if score == 27:
		scroll_speed = 5
		pipe_gap = 220
		pipe_frequency = 1400
	if score == 37:
		scroll_speed = 5.5
		pipe_gap = 200
		pipe_frequency = 1350
	if score == 47:
		scroll_speed = 6
		pipe_gap = 190
		pipe_frequency = 1200
	if score == 57:
		pipe_gap = 180
		pipe_frequency = 1200
	if score == 67:
		pipe_gap = 170
		pipe_frequency = 1100
	if score == 77:
		scroll_speed = 6.5
		pipe_gap = 170
		pipe_frequency = 1050
	if score == 87:
		scroll_speed = 7
		pipe_gap = 160
		pipe_frequency = 1000
	if score == 97:
		pipe_gap = 150
		pipe_frequency = 1000
	if score == 107:
		pipe_gap = 150
		pipe_frequency = 900
	if score == 117:
		scroll_speed = 7
		pipe_gap = 150
		pipe_frequency = 800
		
	
	#Carpma kontrolunun yapilmasi(Alperen Cevik)
	if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
		game_over = True
	#kus yere degdiginde gameover yapan satir(Alperen)
	if flappy.rect.bottom >= 768:
		game_over = True
		flying = False
		#Oyun sonu bitis müzigi(Emre Kurt)
		if high_score >= score:
			pygame.mixer.Sound.play(death_snd)


	if flying == True and game_over == False:
		#yeni borular olusturan satir(Alperen Cevik)
		time_now = pygame.time.get_ticks()
		if time_now - last_pipe > pipe_frequency:
			pipe_height = random.randint(-100, 100)
			btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
			top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
			pipe_group.add(btm_pipe)
			pipe_group.add(top_pipe)
			last_pipe = time_now
	#Update ile guncellenmesini saglar(bu komut olmadigi zaman hareket olmuyor)(Alperen Cevik)
		pipe_group.update()

		ground_scroll -= scroll_speed
		if abs(ground_scroll) > 35:
			ground_scroll = 0
	

	# oyunun bitip bitmedigini kontrol eden eger yandiysak menu cikaran (Alperen Cevik)
	# ve degerleri(skoru) hesaplayan ve sonra reset atmamizi saglayan komutlar
	if game_over == True:

		#En yüksek puan kontrolü(Emre Kurt)
		if high_score >= score:
			screen.blit(gameover_img, ( (screen_width / 2) - (426 / 2) , (screen_height / 2) - 250 ))
		else:
			screen.blit(high_score_img, ( (screen_width / 2) - (679 / 2) , (screen_height / 2) - 250 ))
			pygame.mixer.Sound.play(hscore_snd)
		
		screen.blit(menu_img, ( (screen_width / 2) - 100 , (screen_height / 2) - 50 ))
		draw_text(str(score_text), menu_font, white, (screen_width / 2)-62 , (screen_height / 2)+ 50 )
		draw_text(str(score), menu_font, gray, (screen_width / 2)+34 , (screen_height / 2) + 52)
		draw_text(str(best_text), menu_font, white, (screen_width / 2)-44, (screen_height / 2)+ 115)
		draw_text(str(high_score), menu_font, gray, (screen_width / 2)+34, (screen_height / 2) + 117)

		#reset butonu tıklama tusu(Emre Kurt)
		if button.draw():
			death_count += 1
			game_over = False

			pygame.mixer.Sound.play(rst_snd)

			#En yüksek puan ataması(Emre Kurt)
			if high_score < score:
				savefile = open('saves/data.txt','r+')
				high_score = score
				savefile.write(str(high_score))
				savefile.close()

			#Zorluk sıfırlama(Emre Kurt)
			scroll_speed = 4
			pipe_gap = 250
			pipe_frequency = 1500

			score = reset_game()

#Kusun ucmasını ve yanısını anlayan komut(Emre Kurt)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
			flying = True

	pygame.display.update()

pygame.quit()

#yuksek skoru ani elektrik kesintisi, hata durumlarinda kayit altina alinmasini saglayan satir(Alperen Cevik)
if high_score < score:
	savefile = open('saves/data.txt','r+')
	high_score = score
	savefile.write(str(high_score))
	savefile.close()

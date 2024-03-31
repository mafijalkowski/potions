import pygame
import random
import time
import pickle
import os

# Inicjalizacja Pygame
pygame.init()

# Ustawienie rozmiaru ekranu

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1024
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Poruszające się liczby")
fullscreen = False
ekran = None

# Lista przechowująca potiony
numbers = []
czastmp = time.time()
defdelay = 0.5
delay = defdelay
lvldelay = 0.3
defspeed = SCREEN_WIDTH * 0.002
potiontier = 1
kociol = None
kociol1 = 0
kociol2 = 0
enchance = 0
enchancechance = random.random()
sell = 0
sellplus = 0
hajs = 0

# Ustawienia czcionki
font = pygame.font.Font(None, 36)

# Ścieżka do pliku z zapisanym postępem gry
SAVE_FILE_PATH = "G:\VS Code\save.dat"
image_folder = "G:\VS Code"

# Klasa reprezentująca pojedynczą liczbę
class Potion:
    def __init__(self, value, tier, x, y, speed):  # Poprawiono konstruktor, dodając argumenty
        self.value = value
        self.tier = tier
        self.x = x
        self.y = y
        self.speed = defspeed
        self.click_margin = 3.5  # Margines kliknięcia
        self.image_name = f"{value}.{tier}.png"  # Nazwa pliku obrazu
        
        self.image = pygame.image.load(os.path.join("G:\VS Code", self.image_name))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # Rozszerzamy prostokąt kolizji o margines kliknięcia
        self.rect.inflate_ip(self.click_margin * 2, self.click_margin * 2)

    def update(self):
        self.x += self.speed 
        self.rect.x = self.x  # Aktualizacja prostokąta dla wykrywania kliknięcia

    def draw(self):
       # Wczytanie obrazu na podstawie nazwy pliku obrazu
        image_path = os.path.join(image_folder, self.image_name)
        image = pygame.image.load(image_path)
        screen.blit(image, (self.x, self.y))




# Funkcja do konwersji liczby całkowitej na obiekt klasy Potion
def int_to_potion(num1,num2):
    if num1 == 1:
        if num2 ==1:
            return Potion(1, 1, 0, 0, 0)  
        elif num2 ==2:
            return Potion(1, 2, 0, 0, 0)
        else:
            return Potion(1, 3, 0, 0, 0)
    elif num1 == 2:
        if num2 ==1:
            return Potion(2, 1, 0, 0, 0)  
        elif num2 ==2:
            return Potion(2, 2, 0, 0, 0)
        else:
            return Potion(2, 3, 0, 0, 0) 
    elif num1 == 3:
        if num2 ==1:
            return Potion(3, 1, 0, 0, 0)  
        elif num2 ==2:
            return Potion(3, 2, 0, 0, 0)
        else:
            return Potion(3, 3, 0, 0, 0) 
    else:
        return None  # Zwrócenie None w przypadku innej wartośc

# Funkcja do konwersji obiektu klasy Potion na liczby całkowite
def potion_to_int(potion_obj):
    value = potion_obj.value
    tier = potion_obj.tier
    
    if value == 1:
        if tier == 1:
            return 1, 1
        elif tier == 2:
            return 1, 2
        else:
            return 1, 3
    elif value == 2:
        if tier == 1:
            return 2, 1
        elif tier == 2:
            return 2, 2
        else:
            return 2, 3
    elif value == 3:
        if tier == 1:
            return 3, 1
        elif tier == 2:
            return 3, 2
        else:
            return 3, 3
    else:
        return None



# Funkcja do zapisywania postępu gry
def save_game():
    with open(SAVE_FILE_PATH, "wb") as file:
        if kociol is not None:
            kociol1, kociol2 = potion_to_int(kociol)
        else:
            kociol1, kociol2 = 0, 0
        pickle.dump((hajs, sell, sellplus, kociol1, kociol2), file)

# Funkcja do wczytywania postępu gry
def load_game():
    try:
        with open(SAVE_FILE_PATH, "rb") as file:
            saved_hajs, saved_sell, saved_sellplus, saved_kociol1, saved_kociol2 = pickle.load(file)
            return saved_hajs, saved_sell, saved_sellplus, saved_kociol1, saved_kociol2
    except FileNotFoundError:
        return None

# Wczytanie postępu gry lub ustawienie domyślnych wartości
saved_data = load_game()
if saved_data:
    hajs, sell, sellplus, kociol1, kociol2 = saved_data 
    kociol = int_to_potion(kociol1, kociol2)

    if kociol is not None:
        kociol.x = SCREEN_WIDTH / 2
        kociol.y = SCREEN_HEIGHT / 2
        kociol.update()
        kociol.draw()
else:
    hajs = 0
    sell = 0
    sellplus = 0
    kociol = None

# Główna pętla gry
running = True

while running:
    screen.fill((0, 0, 0))

    # Dodanie nowych liczb co pewien czas
    if len(numbers) < 100 and time.time() - czastmp >= delay:
        value = random.randint(1, 3)
        tier = random.randint(1, potiontier)  # Generowanie losowej wartości
        numbers.append(Potion(value, tier, SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.1, 2))  # Tworzenie nowego obiektu Potion
        czastmp = time.time()

    for potion_obj in numbers:
        potion_obj.update()
        potion_obj.draw()


        # Usunięcie liczby, gdy przekroczy ona prawą krawędź ekranu
        if potion_obj.x > SCREEN_WIDTH * 0.8:
            numbers.remove(potion_obj)

    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game()   # Zapisanie postępu gry przed wyjściem
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # jeżeli kociol jest pusty
            if kociol is None:
                for potion_obj in numbers[:]:  
                    if potion_obj.rect.collidepoint(mouse_pos):
                        numbers.remove(potion_obj)  
                        kociol = potion_obj
                        sell += int(potion_obj.value) 
                        # Ustawienie prędkości na podstawową, gdy kociol jest pusty
                        delay = defdelay

                        
            # Akcje jakie można wykonać jeżeli kociol nie jest pusty         
            else:
                for potion_obj in numbers[:]:
                    # Dodanie kolejnego składnika do kociol (sellplus)
                    if potion_obj.rect.collidepoint(mouse_pos):
                        sellplus += int(potion_obj.value)
                        numbers.remove(potion_obj)
                # Sprzedaż (sell)
                if buttonu_rect.collidepoint(mouse_pos):
                    hajs += sell + sellplus
                    sell = 0
                    sellplus = 0
                    kociol = None
                    delay = defdelay  

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                # Przełączanie między trybem pełnoekranowym a okienkowym po naciśnięciu klawisza F11
                fullscreen = not fullscreen
                if fullscreen:
                    # Zczytywanie aktualnej rozdzielczości ekranu
                    infoObject = pygame.display.Info()
                    SCREEN_WIDTH = infoObject.current_w
                    SCREEN_HEIGHT = infoObject.current_h
                    ekran = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                else:
                    ekran = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            


    # Aktualizacja i wyświetlanie liczby w kotle
    if kociol is not None:
        kociol.x = SCREEN_WIDTH/ 2
        kociol.y = SCREEN_HEIGHT/ 2
        kociol.update()
        kociol.draw()
        delay = lvldelay




    # Wyświetlanie wartości stanu hajsu
    hajs_text = font.render(f"Hajs: {hajs}", True, (255, 255, 255))
    screen.blit(hajs_text, (SCREEN_WIDTH *0.5, SCREEN_HEIGHT*0.05))


    # Przycisk usuwający zawartość kotła (sell)
    buttonu_rect = pygame.draw.rect(screen, (255, 0, 0), (SCREEN_WIDTH * 0.2, SCREEN_HEIGHT *0.8, 110, 40))
    buttonu_text = font.render(f"SELL ({sell+sellplus})", True, (255, 255, 255))
    text_rect = buttonu_text.get_rect(center=buttonu_rect.center)
    screen.blit(buttonu_text, text_rect)

    # Przycisk uleprzający/zwiękrzający wartość pota
    buttone_rect = pygame.draw.rect(screen, (255, 0, 0), (SCREEN_WIDTH * 0.8, SCREEN_HEIGHT *0.8, 110, 40))
    buttone_text = font.render(f"Enchance ({enchance})", True, (255, 255, 255))
    text_rect = buttone_text.get_rect(center=buttone_rect.center)
    screen.blit(buttone_text, text_rect)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Zakończenie Pygame
pygame.quit()

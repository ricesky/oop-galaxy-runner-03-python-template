# oop-galaxy-runner-03-python

## Capaian Pembelajaran

Setelah menyelesaikan seluruh tahapan, mahasiswa diharapkan mampu:

1. Memodelkan permainan 2D sederhana menggunakan **pemrograman berorientasi objek** (class, object, composition, encapsulation, inheritance, polymorphism) di Python.
2. Menggunakan **PyGame** untuk membangun game 2D dengan beberapa komponen: player, musuh (enemy), background, skor, dan UI dasar.
3. Menerapkan **multimedia** (gambar, sprite animation, suara) di dalam game.
4. Mengelola **beberapa screen** (main menu, game screen, high score) menggunakan Screen Manager berbasis OOP.
5. Menerapkan **perilaku AI sederhana** pada musuh (enemy) dan mengatur tingkat kesulitan permainan.

---

## Lingkungan Pengembangan

1. Platform: Python **3.12+** (boleh 3.13 selama PyGame berjalan)
2. Bahasa: Python
3. Editor/IDE yang disarankan:

   * VS Code + Python Extension
   * Terminal
4. Library:

   * `pygame 2.6.1`
   * `pytest`

---

## Cara Menjalankan Project

```bash
python -m src.main
```

---

# Tahap 3 — Sprite Animation & Sound

**Tujuan Tahap 3**

1. Mahasiswa dapat memuat **image** dari folder `assets/` dan menampilkannya dengan PyGame.
2. Mahasiswa dapat membuat **sprite animation sederhana** berbasis frame.
3. Mahasiswa dapat memainkan **efek suara** pada event tertentu (misalnya tabrakan & score).

Struktur repo mulai memakai asset:

```text
oop-galaxy-runner-python/
├─ assets/
│  ├─ images/
│  │  └─ player_sprite.png        # sprite sheet player
│  └─ sounds/
│     ├─ hit.wav                  # suara ketika kena enemy
│     └─ score.wav                # suara ketika dapat skor
└─ src/
   └─ core/
      ├─ player.py
      ├─ enemy.py
      ├─ starfield.py
      └─ game.py
```

---

## 0. Menyiapkan Asset

Sprite Animation menggunakan file image yang terdiri dari beberapa gambar yang bisa dianimasikan.

* `player_sprite.png` adalah **sprite sheet**:

  * 1 baris,
  * 4 kolom (4 frame)
  * setiap frame adalah pose pesawat yang sedikit berbeda (misal animasi thruster).
* Kita akan:

  * memotong sprite sheet menjadi list frame, lalu
  * mengganti `draw()` Player agar memakai frame sesuai waktu (animation loop).

---

## 1. Mengubah Player Menjadi Sprite Animasi

Saat ini `Player.draw()` menggambar pesawat pakai `pygame.draw.rect` + `pygame.draw.polygon`.
Di Tahap 3, kita akan:

* memuat `player_sprite.png`,
* memotongnya menjadi beberapa frame,
* menyimpan frame ke list `self.frames`,
* menambah `current_frame` dan `animation_timer`,
* menggambar sprite (frame) di `draw()` instead of rect.

---

### 1.1. Import `os` dan siapkan path dasar

**File:** `src/core/player.py`

Di paling atas (bagian import), tambahkan:

```python
import os
import pygame
```

Kalau `pygame` sudah diimport, cukup tambahkan `os`.

Lalu, di atas class `Player` (global level), tambahkan helper untuk path:

```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
PLAYER_SPRITE_PATH = os.path.join(IMAGES_DIR, "player_sprite.png")
```

---

### 1.2. Tambahkan atribut animasi di `__init__`

Masih di `player.py`, di dalam `__init__`, setelah bagian:

```python
self.width = 40
self.height = 25
self.color = (0, 220, 180)
```

Tambahkan:

```python
        # --- Sprite & Animation ---
        self.sprite_sheet = pygame.image.load(PLAYER_SPRITE_PATH).convert_alpha()

        # Misal sprite sheet 1 baris, N kolom
        self.frame_count = 4          
        self.current_frame = 0
        self.frame_duration = 0.1     # detik per frame
        self._animation_timer = 0.0

        self.frames = self._slice_frames()
```

---

### 1.3. Tambahkan method `_slice_frames`

Masih di dalam class `Player`, **di bawah `__init__` dan sebelum property `score`**, tambahkan:

```python
    def _slice_frames(self) -> list[pygame.Surface]:
        """Memotong sprite sheet menjadi list frame."""
        sheet_width = self.sprite_sheet.get_width()
        sheet_height = self.sprite_sheet.get_height()

        frame_width = sheet_width // self.frame_count
        frame_height = sheet_height  # 1 baris

        frames: list[pygame.Surface] = []
        for i in range(self.frame_count):
            frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame_surface.blit(
                self.sprite_sheet,
                (0, 0),
                pygame.Rect(i * frame_width, 0, frame_width, frame_height),
            )
            frames.append(frame_surface)

        # Sesuaikan juga ukuran hitbox (rect) dengan ukuran sprite
        self.width = frame_width
        self.height = frame_height

        return frames
```

---

### 1.4. Tambahkan method `update_animation`

Masih di dalam class `Player`, misalnya **di bawah method `update()`**:

```python
    def update_animation(self, dt: float):
        """Meng-update frame animasi berdasarkan waktu."""
        self._animation_timer += dt
        if self._animation_timer >= self.frame_duration:
            self._animation_timer -= self.frame_duration
            self.current_frame = (self.current_frame + 1) % self.frame_count
```

---

### 1.5. Panggil `update_animation` di `update`

Cari method `update(self, dt: float)` yang sekarang berisi:

```python
    def update(self, dt: float):
        self.handle_input(dt)
```

Ubah menjadi:

```python
    def update(self, dt: float):
        self.handle_input(dt)
        self.update_animation(dt)
```

---

### 1.6. Ganti isi `draw()` agar memakai sprite

Sebelumnya `draw()` menggambar rect & polygon.
Sekarang kita ganti supaya menggambar **frame sprite** di posisi player.

Cari method `draw(self, surface: pygame.Surface)` dan ubah isinya menjadi:

```python
    def draw(self, surface: pygame.Surface):
        frame = self.frames[self.current_frame]
        rect = frame.get_rect()
        rect.centerx = int(self.x)
        rect.centery = int(self.y)

        surface.blit(frame, rect)
```

---

## 2. Menambah Sound Effect ke Game

Sekarang kita tambahkan suara sederhana:

* Ketika player **tertabrak enemy** → mainkan suara `hit.wav`
* Ketika enemy **lolos lewat bawah** dan player dapat score → mainkan suara `score.wav`

Implementasi:

1. Inisialisasi `pygame.mixer`
2. Load sound file di `Game.__init__`
3. Panggil `.play()` di `_check_collisions()` dan `update()`.

---

### 2.1. Siapkan path sound

**File:** `src/core/game.py`

Di bagian import paling atas, tambahkan:

```python
import os
```

Lalu, di atas `class Game`, tambahkan path helper (mirip dengan Player):

```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")

HIT_SOUND_PATH = os.path.join(SOUNDS_DIR, "hit.wav")
SCORE_SOUND_PATH = os.path.join(SOUNDS_DIR, "score.wav")
```

---

### 2.2. Inisialisasi mixer & load sound di `__init__`

Masih di `game.py`, di dalam `Game.__init__`, setelah inisialisasi player dan enemies, tambahkan:

```python
        # --- Inisialisasi sound ---
        pygame.mixer.init()

        self.hit_sound = pygame.mixer.Sound(HIT_SOUND_PATH)
        self.score_sound = pygame.mixer.Sound(SCORE_SOUND_PATH)
```

---

### 2.3. Putar sound ketika enemy lolos (dapat skor)

Masih di `game.py`, di method `update(self, dt: float)`, kita tadi punya:

```python
        for enemy in self.enemies:
            enemy.update(dt)

            if enemy.is_off_screen():
                enemy.reset()
                self.player.add_score(10)
```

Tambahkan pemanggilan **sound** di dalam block `if enemy.is_off_screen()`:

```python
            if enemy.is_off_screen():
                enemy.reset()
                self.player.add_score(10)
                self.score_sound.play()
```

---

### 2.4. Putar sound ketika terjadi tabrakan

Masih di `game.py`, di method `_check_collisions(self)` kita punya:

```python
    def _check_collisions(self):
        player_rect = self.player.get_rect()

        for enemy in self.enemies:
            if player_rect.colliderect(enemy.get_rect()):
                self.player.lose_life(1)
                enemy.reset()
```

Tambahkan suara di dalam block if:

```python
    def _check_collisions(self):
        player_rect = self.player.get_rect()

        for enemy in self.enemies:
            if player_rect.colliderect(enemy.get_rect()):
                self.player.lose_life(1)
                enemy.reset()
                self.hit_sound.play()
```

---

## 3. Menjalankan Tahap 3

Pastikan:

* `assets/images/player_sprite.png` ada dan bisa dibaca,
* `assets/sounds/hit.wav` dan `assets/sounds/score.wav` ada.

Lalu jalankan perintah berikut:

```bash
python -m src.main
```

Observasi hal-hal berikut:

* Player sekarang digambar dengan **sprite animasi** (bukan kotak lagi).
* Ketika enemy lolos → score +10 dan ada suara (mis. “bip”/“coin”).
* Ketika enemy menabrak player → lives berkurang dan ada suara “hit”.



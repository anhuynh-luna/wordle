"""
Docstring for source.sound
File chứa đối tượng dùng để phát nhạc nền và hiệu ứng âm thanh khi thắng/thua/lỗi
"""
import pygame
from source.constant import *

class SoundEffect:
    # Dùng chung cho cả nhạc nền và hiệu ứng âm thanh. Tại đây có sử dụng AI để tham khảo cách tích hợp nhạc (pygame.mixer)
    def __init__(self):
        pygame.mixer.init()
        # có sử dụng AI để giải thích sự khác nhau giữa SFX và BGM, giữa Sound, load và play
        self.sfx = [] # danh sách các hiệu ứng âm thanh
        # thêm ba hiệu ứng âm thanh vào danh sách và chỉnh âm thanh (.Sound là đọc file âm thanh và load lên RAM)
        self.sfx.append(pygame.mixer.Sound('assets/sound/Win.wav'))
        self.sfx[-1].set_volume(1)
        self.sfx.append(pygame.mixer.Sound('assets/sound/Lose.wav'))
        self.sfx[-1].set_volume(1)
        self.sfx.append(pygame.mixer.Sound('assets/sound/Error.wav'))
        self.sfx[-1].set_volume(1)

        # danh sách các bài nhạc nền; các bài nhạc thuộc bản quyền của Monster Siren/HyperGryph và được lấy từ arknights.wiki.gg 
        self.playlist = ['assets/sound/bgm1_green.mp3', 'assets/sound/bgm2_silver.mp3', 'assets/sound/bgm3_red.mp3', 'assets/sound/bgm4_gold.mp3']
        # danh sách màu tương ứng cho mỗi bài hát để nhận biết khi đổi
        self.color = [green, silver, red, gold]
        self.track = 0 # biến dùng để đánh dấu bài hiện tại, khởi tạo là bài đầu tiên

        self.note = '\u266B' # biểu tượng note nhạc, có sử dụng AI để kiếm mã
        self.mute = '\u263C' # biểu tượng mute, có sử dụng AI để kiếm mã

        self.icon = self.note # icon hiển thị
        self.color_disp = self.color[0] # màu hiển thị

        self.play_bgm() # phát nhạc (bài số 0) ngay khi khởi tạo

    def play_win(self):
        # Phương thức dùng để phát hiệu ứng âm thanh khi thắng
        self.sfx[0].play()
    def play_lose(self):
        # Phương thức dùng để phát hiệu ứng âm thanh khi thua
        self.sfx[1].play()
    def play_error(self):
        # Phương thức dùng để phát hiệu ứng âm thanh khi lỗi (từ không có trong từ điển, phương trình sai, không phải phương trình)
        self.sfx[2].play()

    def switch_bgm(self):
        # Phương thức dùng để đổi nhạc khi nhấn icon
        self.track += 1 # biến tăng lên 1
        if self.track > len(self.playlist): # khi track == len thì vào trạng thái im lặng, nếu lớn hơn thì track trở về 0
            self.track = 0
        self.play_bgm()
    
    def play_bgm(self):
        # Phương thức dùng để phát nhạc
        if self.track == len(self.playlist): # khi track == len
            pygame.mixer.music.stop() # dừng phát nhạc
            self.icon = self.mute # icon trở thành mute
            self.color_disp = black # màu hiển thị đen
        else:
            pygame.mixer.music.load(self.playlist[self.track]) # load nhạc tương ứng với chỉ số (chuẩn bị file trong ổ cứng, không load lên RAM)
            pygame.mixer.music.play(-1) # phát bài vừa load (-1 nghĩa là nếu hết thì phát lại)
            self.icon = self.note # icon hình note nhạc
            self.color_disp = self.color[self.track] # màu hiển thị tương ứng với chỉ số

"""
Docstring for main
File chính dùng để điều khiển luồng game và xử lý sự kiện
Các phần:
1. Khởi tạo pygame và các biến cần thiết
2. Xử lý các luồng hoạt động của game
3. Xử lý logic game
4. Vẽ giao diện game
Có sử dụng AI để tìm hiểu về các module pygame, os, sys
"""
import pygame
import os
import sys
import time
# import các module từ thư mục source
import source.draw as draw
from random import randint
import source.storage as storage
from source.sound import SoundEffect
from source.data import player_list, stack
from source.logic import main_func, minor_func, check_equal, save, dictionary, tran_word
from source.constant import *

def main():

    # 1. Khởi tạo pygame và các biến cần thiết
    pygame.init()
    # tạo thư mục chứa các file save nếu chưa có
    if not os.path.exists('resume'):
        os.makedirs('resume')

    SE = SoundEffect() # tạo đối tượng để xử lý âm thanh

    screen = pygame.display.set_mode((width, height)) # tạo cửa sổ game
    pygame.display.set_caption(title) # đặt tiêu đề cửa sổ

    clock = pygame.time.Clock() # đồng hồ kiểm soát FPS, tại đây có dùng AI để giải thích và tìm hiểu

    # tạo các font chữ cần thiết
    font = pygame.font.Font("assets/font/Times New Roman Bold.ttf", 40)
    font2 = pygame.font.Font("assets/font/Times New Roman Bold.ttf", 20)
    font3 = pygame.font.Font("assets/font/DejaVuSans.ttf", 30)
    font4 = pygame.font.Font("assets/font/Times New Roman.ttf", 15)
    font5 = pygame.font.Font("assets/font/Times New Roman.ttf", 40)
    board = draw.board() # tạo bảng chơi chính
    # load dữ liệu người chơi từ file top 20
    top20_list = player_list()
    pl = storage.load_player('top20.lun')
    if pl != None: # nếu có dữ liệu thì thêm vào danh sách dưới dạng (name, time)
        for i in range(len(pl)):
            top20_list.add(pl[i][0], round(pl[i][1], 2))
    top20_list.top20() # lọc và sắp xếp top 20
    top20_board = draw.top_20_board() # khởi tạo bảng top 20
    top20_board.fill(top20_list) # điền dữ liệu vào bảng top 20

    running = True # biến điều khiển vòng lặp game, game dừng khi running == False

    cr = 0
    cc = 0
    # load các list từ từ file từ điển
    d_English = dictionary('assets/dictionary/English.txt')
    d_Vietnamese = dictionary('assets/dictionary/Vietnamese.txt')
    d_Equation = dictionary('assets/dictionary/Equation.txt')

    

    input_name = "" # biến để luư tên người chơi khi nhập ở input_name

    resumed_time = 0 # khởi tạo biến lưu thời gian đã chơi khi loadgame (sẽ thay đổi khi loadgame)

    curr_state = 'Menu' # biến để kiểm soát trạng thái hiện tại của game
    # tạo các nút bấm cần thiết
    new_game_button = draw.button(300, 300, "New Game") # nút new_game hiển thị ở menu chính, dùng để tạo 1 username mới
    top_20_button = draw.button(300, 370, "Top 20")
    resume_button = draw.button(300, 440, "Resume")
    back_button = draw.button(50, 500, "Back")
    undo_button = draw.button(570, 500, "Undo")
    redo_button = draw.button(570, 550, "Redo")
    refresh_button = draw.button(550, 500, "Refresh") # nút refresh hiển thị trong top20, dùng để tải lại bảng top20
    start_button = draw.button(550, 500, "Start Game")
    setting_button = draw.round_button(750, 10, "\u2699", width = 30, height = 30)
    timescoring_button = draw.round_button(720, 10, "\u2139", width = 30, height = 30) # nút timescoring hiển thị trong game, dùng để xem bảng các ván đã chơi của 1 username
    done_button = draw.button(310, 440, "Done")
    newgame_button = draw.button(50, 550, "New Game") # nút newgame hiển thị trong game, dùng để bắt đầu 1 ván mới
    cancel_button = draw.button(570, 500, "Cancel") # nút cancel hiển thị trong resume, dùng để hủy việc lưu game
    endgame_button = draw.button(310, 500, "End Game") # nút endgame dùng để kết thúc game của 1 username và tính điểm

    music_button = draw.round_button(750, 300, SE.icon, width = 30, height = 30) # nút nhạc nền, nhấn để thay đổi/tắt nhạc
    music_button.border = SE.color_disp # màu viền nút tròn hiển thị trạng thái nhạc nền

    # các nút bấm trong bảng setting dùng để chọn chế độ game và chế độ thời gian
    unlimited_button = draw.round_button(540, 340, width = 15, height = 15)
    unlimited_button.border = black
    daily_button = draw.round_button(540, 310, width = 15, height = 15)
    daily_button.border = black
    daily_button.color = black
    customize_button = draw.round_button(540, 370, width = 15, height = 15)
    customize_button.border = black
    English_button = draw.round_button(540, 190, width = 15, height = 15)
    English_button.border = black
    English_button.color = black
    Vietnamese_button = draw.round_button(540, 220, width = 15, height = 15)
    Vietnamese_button.border = black
    Equation_button = draw.round_button(540, 250, width = 15, height = 15)
    Equation_button.border = black
    
    # vẽ bảng setting, bảng timescoring, bảng resume và bảng lịch sử chơi
    setting_table = draw.button(100, 100, width = 630, height = 400, color = silver)
    timescoring_table = draw.button(100, 100, width = 630, height = 400, color = silver)
    resume_table = draw.resume_board()
    history_table = draw.scroll_list()

    setting_state = False # trạng thái tắt/mở bảng setting
    timescoring_state = False # trạng thái tắt/mở bảng timescoring
    x = 0 # biến để kiểm soát khi thoát game, bằng 0 thì về menu, bằng 1 thì tắt cửa sổ game
    # khởi tạo các biến cần thiết cho game
    cooldown_endtime = 0 # thời gian kết thúc cooldown, khởi tạo bằng 0, sẽ thay đổi tuỳ vào chế độ thời gian
    game_phase = 'Setup' # giai đoạn của game, gồm Setup (cài đặt), Cooldown (đang đếm ngược thời gian chờ), Ready (sẵn sàng chơi), Playing (đang chơi), khi vừa tạo username mới thì khởi tạo ở Setup
    game_state = 0 # trạng thái của ván chơi hiện tại, 0 là đang chơi, 1 là thắng, -1 là thua
    start_time = time.time() # thời gian bắt đầu ván chơi hiện tại, thay đổi phụ thuộc vào ván chơi
    target = "" # khởi tạo từ cần đoán là rỗng
    game_mode = 'English' # chế độ chơi mặc định là English, có thể thay đổi trong bảng setting
    time_mode = 'Daily' # chế độ thời gian mặc định là Daily, có thể thay đổi trong bảng setting
    pause = 0 # biến để lưu thời gian tạm dừng khi mở bảng setting hoặc bảng timescoring hoặc khi thoát game để lưu
    undo = stack() # khởi tạo ngăn xếp undo
    redo = stack() # khởi tạo ngăn xếp redo
    guess = "" # khởi tạo biến lưu từ đang đoán hiện tại

    error_endtime = time.time() # thời gian kết thúc thông báo lỗi
    error = "" # biến lưu thông báo lỗi hiện tại
    saved_name = "" # biến lưu tên người chơi hiện tại
    # các biến lưu thời gian tuỳ chỉnh khi chọn chế độ thời gian Customize
    customize_h = "0"
    customize_m = "0"
    customize_s = "0"
    customize_on = "0" # biến kiểm soát ô nhập thời gian tuỳ chỉnh đang được chọn, "0" là không chọn, "h" là giờ, "m" là phút, "s" là giây
    while running:
        # 2. Xử lý các luồng hoạt động của game
        if game_phase == 'Cooldown': # kiểm tra nếu qua giai đoạn cooldown thì chuyển sang giai đoạn ready (đối với các username đã hoàn thành ván chơi và đang đếm ngược thời gian chờ)
            if time.time() >= cooldown_endtime:
                game_phase = 'Ready'
                cooldown_dur = 0
        for event in pygame.event.get():
            # xử lý thoát game khi không ở trong game và bảng resume
            if event.type == pygame.QUIT and curr_state != 'Game' and curr_state != 'Resume':
                running = False
            # xử lý các nút bấm
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos # lấy vị trí khi bấm chuột

                if music_button.click(pos): # xử lý khi nhấn nút đổi nhạc nền
                    SE.switch_bgm()
                    music_button.text = SE.icon
                    music_button.border = SE.color_disp

                if curr_state == 'Menu': # xử lý các nút bấm trong menu chính
                    if new_game_button.click(pos):
                        curr_state = 'Input_Name' # nếu nhấn new game thì chuyển sang cửa sổ nhập tên
                    elif top_20_button.click(pos):
                        curr_state = 'Top20' # nếu nhấn top 20 thì chuyển sang cửa sổ bảng top 20
                    # nếu nhấn nút resume thì load các file save để điền vào bảng resume, sau đó chuyển sang cửa sổ resume
                    elif resume_button.click(pos): 
                        Resume = []
                        for i in range(5):
                            filename = 'resume/resume' + str(i) + '.lun'
                            sub_board = draw.board()
                            sub_history_table = draw.scroll_list()
                            Resume.append(storage.loadgame(filename, sub_board, sub_history_table))
                        resume_table.fill(Resume)
                        curr_state = 'Resume_Enter'
                        
                elif curr_state == 'Input_Name': # xử lý các nút bấm trong cửa sổ nhập tên
                    if back_button.click(pos):
                        curr_state = 'Menu' # nếu nhấn back thì về menu chính
                        input_name = "" # reset lại tên đã nhập
                    elif start_button.click(pos):
                        if input_name == "No data" or input_name == "Available": # tránh lỗi hiển thị khi resume
                            error = 'Cannot use this name!'
                            error_endtime = time.time() + 1.5
                        elif 3 <= len(input_name) <= 10: # kiểm tra độ dài tên hợp lệ
                            dup_name = False
                            # kiểm tra trùng tên trong bảng top 20
                            if top20_list.check_name(input_name):
                                dup_name = True
                            # kiểm tra trùng tên trong bảng resume bằng cách load từng file save và kiểm tra tên được lưu trong file
                            if not dup_name:
                                for i in range(5):
                                    filename = 'resume/resume' + str(i) + '.lun'
                                    try:
                                        sub_board = draw.board()
                                        sub_history_table = draw.scroll_list()
                                        match = storage.loadgame(filename, sub_board, sub_history_table)
                                        if match is not None and match[5] == input_name:
                                            dup_name = True
                                            break
                                    except:
                                        pass # nếu không có file thì bỏ qua
                            if dup_name: # nếu trùng tên thì gán lỗi và thời gian hiển thị lỗi
                                error = 'Name already exists!'
                                error_endtime = time.time() + 1.5
                            else: # nếu tên hợp lệ thì qua cửa sổ game và mở bảng setting để chọn chế độ
                                saved_name = input_name # lưu tên người chơi
                                input_name = "" # reset lại tên đăng nhập để tránh lỗi khi người khác đăng nhập
                                curr_state = 'Game'
                                game_phase = 'Setup' # game mới vào ở giai đoạn Setup
                                game_state = 0
                                setting_state = True
                                history_table.clear()

                                English_button.color = black # chế độ mặc định là tiếng Anh
                                Vietnamese_button.color = white
                                Equation_button.color = white
                                unlimited_button.color = white
                                daily_button.color = black # chế độ mặc định là hằng ngày
                                customize_button.color = white
                                
                        else: # nếu tên không hợp lệ thì gán lỗi và thời gian hiển thị lỗi
                            error = 'Name must be 3-10 characters long!'
                            error_endtime = time.time() + 1.5

                elif curr_state == 'Top20': # xử lý các nút bấm trong cửa sổ bảng top 20
                    if back_button.click(pos):
                        curr_state = 'Menu' # nếu nhấn back thì về menu chính
                    elif refresh_button.click(pos): # nếu nhấn refresh thì tải lại bảng top 20 từ file
                        top20_list.clear()
                        pl = storage.load_player('top20.lun')
                        if pl != None:
                            for i in range(len(pl)):
                                top20_list.add(pl[i][0], round(pl[i][1], 2))
                        top20_list.top20()
                        top20_board.fill(top20_list)
                
                # xử lý các nút bấm trong cửa sổ game khi không mở bảng setting và bảng timescoring
                elif curr_state == 'Game' and not setting_state and not timescoring_state:
                    if back_button.click(pos):
                        pause = time.time() # nếu nhấn back thì đánh dấu thời gian tạm dừng (để xử lý nếu người chơi trở lại game)
                        stop_time = time.time() # đánh dấu thời gian tạm dừng (để xử lý nếu người chơi muốn lưu game)
                        # load các file save để điền vào bảng resume, sau đó chuyển sang cửa sổ resume
                        Resume = []
                        for i in range(5):
                            filename = 'resume/resume' + str(i) + '.lun'
                            # tạo hai bảng con để hứng dữ liệu (tránh ảnh hưởng lên bảng gốc)
                            sub_board = draw.board()
                            sub_history_table = draw.scroll_list()
                            Resume.append(storage.loadgame(filename, sub_board, sub_history_table))
                        resume_table.fill(Resume)
                        curr_state = 'Resume'
                            
                        

                   
                    if undo_button.click(pos) and game_state == 0:
                        if undo.len != 0: # nếu nhấn undo khi đang chơi và stack undo không rỗng
                            save(redo, cc, guess, board) # lưu trạng thái hiện tại vào stack redo
                            # lấy trạng thái trước đó từ stack undo và phục hồi
                            status = undo.pop()
                            board.mainboard = status[0]
                            cc = status[1]
                            guess = status[2]
                    
                    if redo_button.click(pos) and game_state == 0:
                        if redo.len != 0: # nếu nhấn redo khi đang chơi và stack redo không rỗng
                            save(undo, cc, guess, board) # lưu trạng thái hiện tại vào stack undo
                            # lấy trạng thái trước đó từ stack redo và phục hồi
                            status = redo.pop()
                            board.mainboard = status[0]
                            cc = status[1]
                            guess = status[2]

                    if setting_button.click(pos) and game_phase != 'Cooldown': # chỉ cho phép mở bảng setting khi không đang trong giai đoạn Cooldown
                        pause = time.time() # đánh dấu thời gian tạm dừng
                        setting_state = not setting_state # chuyển trạng thái bảng setting (= True)
                    
                    if timescoring_button.click(pos):
                        pause = time.time() # đánh dấu thời gian tạm dừng
                        timescoring_state = not timescoring_state # chuyển trạng thái bảng timescoring (= True)

                    if newgame_button.click(pos) and game_phase == 'Ready': # khi trong trạng thái Ready (đã hết Cooldown)
                        # tạo màn chơi mới
                        cr = 0
                        cc = 0
                        guess = ""
                        board = draw.board()
                        undo = stack()
                        redo = stack()
                        game_state = 0
                        curr_state = 'Game'
                        start_time = time.time()
                        resumed_time = 0
                        # lấy dữ liệu chế độ chơi và chế độ thời gian từ trạng thái của bảng setting (giữ nguyên trạng thái trước đó)
                        if English_button.color == black:
                            game_mode = 'English'
                            target = d_English[randint(0, len(d_English) - 1)]
                        elif Vietnamese_button.color == black:
                            game_mode = 'Vietnamese'
                            target = d_Vietnamese[randint(0, len(d_Vietnamese) - 1)]
                        elif Equation_button.color == black:
                            game_mode = 'Equation'
                            target = d_Equation[randint(0, len(d_Equation) - 1)]
                        if unlimited_button.color == black:
                            time_mode = 'Unlimited'
                            cooldown_dur = 0
                        elif daily_button.color == black:
                            time_mode = 'Daily'
                            cooldown_dur = 86400
                        elif customize_button.color == black:
                            time_mode = 'Customize'
                            hc = int(customize_h) if customize_h != '' else 0
                            mc = int(customize_m) if customize_m != '' else 0
                            sc = int(customize_s) if customize_s != '' else 0
                            cooldown_dur = hc * 3600 + mc * 60 + sc

                        game_phase = 'Playing' # chuyển sang giai đoạn Playing

                    if endgame_button.click(pos): # nút endgame có thể nhấn bất kỳ lúc nào (miễn là không mở bảng setting hoặc bảng timescoring)
                        total_time = 0 # biến để tính tổng thời gian chơi
                        total_win = 0 # biến để tính tổng số ván thắng
                        for match in history_table.matches: # duyệt qua các ván đã chơi trong bảng lịch sử
                            total_time += match[0] # cộng dồn thời gian chơi
                            total_win += 1 if match[2] == 1 else 0 # tính tổng số ván thắng
                        if total_win != 0: # nếu có ván thắng thì tính điểm và lưu vào bảng top 20
                            score = total_time / total_win
                            top20_list.add(saved_name, round(score, 2))
                            top20_list.top20()
                            storage.save_player('top20.lun', top20_list)
                            top20_board.fill(top20_list)
                        # xoá bảng chơi và bảng lịch sử, về menu chính
                        board.clear()
                        history_table.clear()
                        curr_state = 'Menu'

                elif curr_state == 'Game' and setting_state: # xử lý các nút bấm trong bảng setting
                    if done_button.click(pos): # nhấn done thì tạo ván mới nếu đang ở giai đoạn Setup hoặc Ready (dựa vào các tuỳ chọn trong bảng setting), sau đó đóng bảng
                        if game_phase == 'Setup' or game_phase == 'Ready': # tạo ván mới dựa vào các chế độ đã chọn
                            cr = 0
                            cc = 0
                            guess = ""
                            board = draw.board()
                            undo = stack()
                            redo = stack()
                            game_state = 0
                            curr_state = 'Game'
                            start_time = time.time()
                            resumed_time = 0
                            if English_button.color == black:
                                target = d_English[randint(0, len(d_English) - 1)]
                                game_mode = 'English'
                            elif Vietnamese_button.color == black:
                                target = d_Vietnamese[randint(0, len(d_Vietnamese) - 1)]
                                game_mode = 'Vietnamese'
                            elif Equation_button.color == black:
                                target = d_Equation[randint(0, len(d_Equation) - 1)]
                                game_mode = 'Equation'
                            if unlimited_button.color == black:
                                cooldown_dur = 0
                                time_mode = 'Unlimited'
                            elif daily_button.color == black:
                                cooldown_dur = 86400 # nếu là chế độ Daily thì đặt thời gian chờ là 86400 giây (24 giờ)
                                time_mode = 'Daily'
                            elif customize_button.color == black: # nếu là chế độ Customize thì tính thời gian chờ từ các ô nhập
                                hc = int(customize_h) if customize_h != '' else 0 # chuyển sang kiểu int, nếu rỗng thì là 0
                                mc = int(customize_m) if customize_m != '' else 0
                                sc = int(customize_s) if customize_s != '' else 0
                                cooldown_dur = hc * 3600 + mc * 60 + sc # tính thời gian cooldown theo giây
                                time_mode = 'Customize'
                            game_phase = 'Playing'
                        elif game_state == 0: # nếu đang chơi thì tính tổng thời gian mở bảng setting và cộng vào start_time để không tính thời gian mở bảng setting vào thời gian chơi
                            pause = time.time() - pause # tổng thời gian mở bảng setting
                            start_time += pause # cộng vào start_time
                        setting_state = False # đóng bảng setting
                    # xử lý các nút chọn chế độ chơi và chế độ thời gian (đen là chọn, trắng là không chọn)
                    elif unlimited_button.click(pos) and game_phase != 'Playing':
                        unlimited_button.color = black
                        daily_button.color = white
                        customize_button.color = white
                    elif daily_button.click(pos) and game_phase != 'Playing':
                        daily_button.color = black
                        unlimited_button.color = white
                        customize_button.color = white
                    elif customize_button.click(pos) and game_phase != 'Playing':
                        customize_button.color = black
                        unlimited_button.color = white
                        daily_button.color = white
                    elif English_button.click(pos) and game_phase != 'Playing':
                        English_button.color = black
                        Vietnamese_button.color = white
                        Equation_button.color = white
                    elif Vietnamese_button.click(pos) and game_phase != 'Playing':
                        Vietnamese_button.color = black
                        English_button.color = white
                        Equation_button.color = white
                    elif Equation_button.click(pos) and game_phase != 'Playing':
                        Equation_button.color = black
                        English_button.color = white
                        Vietnamese_button.color = white
                    
                    # xử lý riêng cho chế độ thời gian Customize để nhập giờ, phút, giây tuỳ chỉnh
                    if customize_button.color == black:
                        if 570 <= pos[0] <= 600 and 365 <= pos[1] <= 390: # nhấn vào ô nhập giờ
                            customize_on = 'h' # đang nhập giờ
                        elif 620 <= pos[0] <= 650 and 365 <= pos[1] <= 390: # nhấn vào ô nhập phút
                            customize_on = 'm' # đang nhập phút
                        elif 670 <= pos[0] <= 700 and 365 <= pos[1] <= 390: # nhấn vào ô nhập giây
                            customize_on = 's' # đang nhập giây
                        else: # nhấn ra ngoài thì thoát khỏi các ô nhập
                            customize_on = '0'
                
                elif curr_state == 'Game' and timescoring_state: # xử lý các nút bấm trong bảng timescoring
                    if done_button.click(pos):
                        if game_state == 0: # nếu nhấn done và khi đang chơi thì tính tổng thời gian mở bảng timescoring và cộng vào start_time để không tính thời gian mở bảng timescoring vào thời gian chơi
                            pause = time.time() - pause
                            start_time += pause
                        timescoring_state = False # đóng bảng timescoring
                    i = history_table.click(pos) # kiểm tra nếu nhấn vào 1 ván trong lịch sử
                    if i != None: # nếu có nhấn
                        temp_time, temp_target, temp_game_state, temp_board = i # lấy dữ liệu màn chơi đó
                        curr_state = 'History' # chuyển sang trạng thái xem lịch sử chơi

                elif curr_state == 'Resume': # xử lý các nút bấm trong cửa sổ resume (khi từ game nhấn back hoặc thoát game)
                    if back_button.click(pos):
                        if game_state == 0: # nếu nhấn back và khi đang chơi thì tính tổng thời gian mở bảng resume và cộng vào start_time để không tính thời gian mở bảng resume vào thời gian chơi
                            pause = time.time() - pause
                            start_time += pause
                        curr_state = 'Game' # về lại game
                        x = 0 # đặt lại x = 0 (không thoát game)
                    elif cancel_button.click(pos):
                        curr_state = 'Menu' # nếu nhấn cancel thì về menu chính (không lưu dữ liệu)
                        if x == 1: running = False # nếu x == 1 (trước đó đã nhấn thoát game) thì cho dừng vòng lặp game
                    i = resume_table.click(pos) # kiểm tra nếu nhấn vào 1 ô trong bảng resume
                    if i != -1: # nếu có nhấn
                        if None in Resume and Resume[i] != None: # nếu còn slot trống mà người chơi chọn slot không trống
                            error = 'Please select an empty slot!' # thông báo chọn slot khác
                            error_endtime = time.time() + 1.5
                        else: # nếu chọn slot trống hoặc không còn slot trống
                            # lưu dữ liệu người chơi vào file (nếu slot không trống thì ghi đè và mất dữ liệu cũ)
                            filename = 'resume/resume' + str(i) + '.lun'
                            if game_state == 0: # nếu đang chơi thì tính thời gian đã chơi đến lúc nhấn nút back (hoặc thoát game) cộng với thời gian lượt lưu trước đó (nếu có)
                                saved_time = stop_time - start_time + resumed_time
                            else: # nếu ván đã xong thì thời gian lưu là thời gian đã chơi đến lúc kết thúc ván cộng với thời gian lượt lưu trước đó (nếu có)
                                saved_time = end_time - start_time + resumed_time
                            storage.savegame(filename, target, board, cr, cc, saved_time, saved_name, cooldown_endtime, game_mode, time_mode, game_state, cooldown_dur, history_table)
                            error = 'Game saved!'
                            error_endtime = time.time() + 0.5
                            curr_state = 'Menu'
                            if x == 1: running = False

                elif curr_state == 'Resume_Enter': # xử lý các nút bấm trong cửa sổ resume (khi từ menu chính nhấn resume)
                    if back_button.click(pos):
                        curr_state = 'Menu' # nếu nhấn back thì về menu chính
                    i = resume_table.click(pos) # kiểm tra nếu nhấn vào 1 ô trong bảng resume
                    if i != -1: # nếu có nhấn
                        if Resume[i] == None: # nếu slot trống thì thông báo không có dữ liệu được lưu
                            error = 'No saved game found!'
                            error_endtime = time.time() + 1.5
                        else: # nếu slot không trống thì load dữ liệu từ file và phục hồi trạng thái game
                            filename = 'resume/resume' + str(i) + '.lun' # tên file
                            # phục hồi dữ liệu từ file
                            target, cr, cc, guess, saved_time, saved_name, cooldown_endtime, game_mode, time_mode, game_state, cooldown_dur = storage.loadgame(filename, board, history_table)
                            resumed_time = saved_time # thời gian đã chơi được phục hồi
                            start_time = time.time() # tạo thời gian bắt đầu mới
                            # đặt lại các nút bấm trong bảng setting
                            if game_mode == 'English':
                                English_button.color = black
                                Vietnamese_button.color = white
                                Equation_button.color = white
                            elif game_mode == 'Vietnamese':
                                English_button.color = white
                                Vietnamese_button.color = black
                                Equation_button.color = white
                            elif game_mode == 'Equation':
                                English_button.color = white
                                Vietnamese_button.color = white
                                Equation_button.color = black
                            if time_mode == 'Unlimited':
                                unlimited_button.color = black
                                daily_button.color = white
                                customize_button.color = white
                            elif time_mode == 'Daily':
                                unlimited_button.color = white
                                customize_button.color = white
                                daily_button.color = black
                            elif time_mode == 'Customize':
                                unlimited_button.color = white
                                customize_button.color = black
                                daily_button.color = white
                                customize_m, customize_s = divmod(cooldown_dur, 60) # tính lại giờ, phút, giây tuỳ chỉnh từ cooldown_dur
                                customize_h, customize_m = divmod(customize_m, 60)
                                customize_h, customize_m, customize_s = str(customize_h), str(customize_m), str(customize_s) # chuyển về str để render text
                            if time.time() < cooldown_endtime: # nếu thời gian hiện tại chưa qua cooldown_endtime thì đang trong giai đoạn Cooldown
                                game_phase = 'Cooldown'
                                end_time = start_time # gán thời gian kết thúc ván chơi là thời gian bắt đầu (để tránh lỗi khi vẽ giao diện ở Time taken)
                                # end_time - start_time sẽ bằng 0, Time taken bằng chính xác resumed_time, dù lưu và load nhiều lần cũng không ảnh hưởng
                            elif game_state != 0: # nếu đã xong ván và đã qua cooldown_endtime thì giai đoạn là Ready
                                game_phase = 'Ready'
                                end_time = start_time # giải thích tương tự trên
                            else:
                                game_phase = 'Playing' # nếu chưa xong ván thì giai đoạn là Playing
                            # phục hồi màu sắc các ô trong bảng chơi dựa vào từ đã đoán
                            for i in range(cr):
                                # dùng minor_func vì các từ đã tô chắc chắn có trong từ điển (và phương trình đúng nếu là chế độ Equation)
                                result = minor_func(target, ''.join([board.mainboard[i][j].text for j in range(board.cols)]))
                                for j in range(len(result)):
                                    if result[j] == 'GREEN':
                                        board.mainboard[i][j].color = green
                                    elif result[j] == 'YELLOW':
                                        board.mainboard[i][j].color = yellow
                                    else:
                                        board.mainboard[i][j].color = gray
                            os.remove(filename) # xoá file save sau khi load để tránh trùng tên khi lưu lần sau
                            curr_state = 'Game' # về trạng thái game

                elif curr_state == 'History': # xử lý nút bấm trong cửa sổ xem lịch sử chơi
                    if back_button.click(pos):
                        curr_state = 'Game' # nếu nhấn back thì về lại game

                    
            
            if curr_state == 'Game' and timescoring_state: # nếu đang mở bảng timescoring thì xử lý sự kiện cho bảng lịch sử chơi
                # các phím up và down để cuộn bảng lịch sử chơi
                history_table.handle_event(event)


            if curr_state == 'Input_Name': # xử lý nhập tên người chơi
                if event.type == pygame.KEYDOWN: # lấy sự kiện nhấn phím
                    if event.unicode.isalpha(): # nếu là ký tự chữ cái
                        input_name += event.unicode # thêm vào tên đang nhập
                    elif event.key == pygame.K_BACKSPACE and len(input_name) > 0: # nếu nhấn backspace thì xoá ký tự cuối cùng nếu còn ký tự
                        input_name = input_name[:len(input_name)-1]

            # xử lý khi nhấn thoát game tương tự khi nhấn back trong game (chỉ khác là đặt x = 1 để thoát game sau khi lưu)
            if event.type == pygame.QUIT and curr_state == 'Game' and not setting_state and not timescoring_state:
                pause = time.time()
                stop_time = time.time()
                curr_state = 'Resume'
                Resume = []
                for i in range(5):
                    filename = 'resume/resume' + str(i) + '.lun'
                    sub_board = draw.board()
                    sub_history_table = draw.scroll_list()
                    Resume.append(storage.loadgame(filename, sub_board, sub_history_table))
                resume_table.fill(Resume)
                x = 1

            # xử lý nhập thời gian tuỳ chỉnh trong bảng setting khi chọn chế độ Customize
            # điều kiện là bảng setting đang mở và phải có một trong ba ô h, m, s đang được chọn
            if event.type == pygame.KEYDOWN and setting_state and customize_on != '0':
                if event.key == pygame.K_BACKSPACE: # nếu nhấn backspace thì xoá ký tự cuối cùng trong ô đang chọn
                    if customize_on == 'h' and len(customize_h) > 0:
                        customize_h = customize_h[:len(customize_h) - 1]
                    elif customize_on == 'm' and len(customize_m) > 0:
                        customize_m = customize_m[:len(customize_m) - 1]
                    elif customize_on == 's' and len(customize_s) > 0:
                        customize_s = customize_s[:len(customize_s) - 1]
                elif event.unicode.isdigit(): # nếu nhập là ký tự số
                    # mỗi ô chỉ nhập hai ký tự
                    if customize_on == 'h' and len(customize_h) < 2:
                        customize_h += event.unicode
                    # phút và giây không vượt quá 59
                    elif customize_on == 'm' and len(customize_m) < 2 and int(customize_m + event.unicode) < 60: 
                        customize_m += event.unicode
                    elif customize_on == 's' and len(customize_s) < 2 and int(customize_s + event.unicode) < 60:
                        customize_s += event.unicode

            # 3. Xử lý logic game
            # chỉ được nhập khi đang trong game (game_state = 0) và không mở bảng setting hoặc bảng time scoring
            if event.type == pygame.KEYDOWN and curr_state == 'Game' and game_state == 0 and not setting_state and not timescoring_state:
                # chế độ tiếng Anh
                if game_mode == 'English':
                    if event.unicode.isalpha(): # nếu nhập ký tự chữ cái
                        c = event.unicode.upper() # chuyển thành chữ in hoa
                        if cc < board.cols: # khi hàng chưa đầy
                            save(undo, cc, guess, board) # lưu trạng thái hiện tại vào stack undo
                            redo.clear() # xoá stack redo
                            board.mainboard[cr][cc].text = c # điền ký tự vào ô hiện tại
                            cc += 1 # chuyển sang cột tiếp theo
                            guess += c # thêm ký tự vào từ đang đoán
                    elif event.key == pygame.K_BACKSPACE: # nếu nhấn backspace
                        if cc > 0: # nếu còn ký tự ở hàng hiện tại
                            save(undo, cc, guess, board) # lưu trạng thái hiện tại vào stack undo
                            redo.clear() # xoá stack redo
                            cc -= 1 # lùi về cột trước
                            board.mainboard[cr][cc].text = "" # xoá ký tự ở ô hiện tại
                            guess = guess[:len(guess)-1] # xoá ký tự cuối cùng trong từ đang đoán
                    elif event.key == pygame.K_RETURN: # nếu nhấn return
                        if cc < board.cols: # nếu hàng chưa đủ ký tự thì báo lỗi
                            error = "Not enough letters!"
                            SE.play_error()
                            error_endtime = time.time() + 1.5
                        elif cc == board.cols: # nếu hàng đủ ký tự
                            result = main_func(target, guess, d_English) # gọi hàm chính để so sánh từ đoán với từ mục tiêu
                            if result == None: # nếu từ đoán không có trong từ điển thì báo lỗi
                                error = "Guess not in dictionary!"
                                SE.play_error()
                                error_endtime = time.time() + 1.5
                            else: # nếu từ đoán hợp lệ
                                redo.clear() # xoá stack redo khi sang hàng mới
                                undo.clear() # xoá stack undo khi sang hàng mới
                                # vòng lặp để tô màu cho các ô trong hàng
                                for i in range(len(result)):
                                    if result[i] == "GREEN":
                                        board.mainboard[cr][i].color = green
                                    elif result[i] == "YELLOW":
                                        board.mainboard[cr][i].color = yellow
                                    else: board.mainboard[cr][i].color = gray
                                # vòng lặp để kiểm tra kết quả đoán
                                for i in range(len(result)):
                                    if result[i] != "GREEN": # nếu tồn tại một ô khác xanh lá trong hàng
                                        if cr == board.rows - 1: # nếu đã là hàng cuối
                                            game_state = -1 # trạng thái game là thua
                                            SE.play_lose()
                                            end_time = time.time() # đánh dấu thời gian kết thúc
                                            history_table.add(end_time - start_time + resumed_time, target, -1, board) # lưu vào bảng lịch sử chơi
                                            if time_mode != 'Unlimited': # nếu không phải chế độ vô hạn
                                                cooldown_endtime = time.time() + cooldown_dur # đặt thời gian kết thúc cooldown bằng thời gian hiện tại cộng với thời gian cooldown
                                                game_phase = 'Cooldown' # chuyển sang giai đoạn Cooldown
                                            else: # nếu là chế độ vô hạn
                                                game_phase = 'Ready' # chuyển sang giai đoạn Ready
                                        break # thoát vòng lặp vì đã biết chắc là thua
                                    elif result[i] == "GREEN" and i == len(result) - 1: # nếu vòng lặp đi đến ô cuối cùng và ô cuối cùng là xanh lá
                                        game_state = 1 # trạng thái game là thắng
                                        SE.play_win()
                                        end_time = time.time() # đánh dấu thời gian kết thúc
                                        # giải thích tương tự như trên
                                        if time_mode != 'Unlimited':
                                            cooldown_endtime = time.time() + cooldown_dur
                                            game_phase = 'Cooldown'
                                        else:
                                            game_phase = 'Ready'
                                        history_table.add(end_time - start_time + resumed_time, target, 1, board)
                                # tăng hàng, reset cột và guess
                                cr += 1
                                cc = 0
                                guess = ""
                                

                # chế độ phương trình (các phần giải thích tương tự chế độ tiếng Anh sẽ được bỏ qua)
                elif game_mode == 'Equation':
                    if event.unicode in '0123456789+-*/=' and event.unicode != '': # nếu nhập ký tự hợp lệ
                        c = event.unicode
                        if cc < board.cols:
                            save(undo, cc, guess, board)
                            redo.clear()
                            board.mainboard[cr][cc].text = c
                            cc += 1
                            guess += c
                    elif event.key == pygame.K_BACKSPACE:
                        if cc > 0:
                            save(undo, cc, guess, board)
                            redo.clear()
                            cc -= 1
                            board.mainboard[cr][cc].text = ""
                            guess = guess[:len(guess)-1]
                    elif event.key == pygame.K_RETURN:
                        if cc < board.cols:
                            error = "Not enough characters!"
                            SE.play_error()
                            error_endtime = time.time() + 1.5
                        elif cc == board.cols:
                            if check_equal(guess) == None: # kiểm tra kết quả nhập có phải phương trình hay không
                                # nếu không thì báo lỗi
                                error = "The answer must be an equation!"
                                SE.play_error()
                                error_endtime = time.time() + 1.5
                            elif not check_equal(guess): # nếu phương trình nhập không chính xác thì báo lỗi
                                error = "Equation is not correct!"
                                SE.play_error()
                                error_endtime = time.time() + 1.5
                            else:
                                result = main_func(target, guess, d_Equation)
                                if result == None:
                                    error = "Guess not in dictionary!"
                                    SE.play_error()
                                    error_endtime = time.time() + 1.5
                                else:
                                    redo.clear()
                                    undo.clear()
                                    for i in range(len(result)):
                                        if result[i] == "GREEN":
                                            board.mainboard[cr][i].color = green
                                        elif result[i] == "YELLOW":
                                            board.mainboard[cr][i].color = yellow
                                        else: board.mainboard[cr][i].color = gray
                                    for i in range(len(result)):
                                        if result[i] != "GREEN":
                                            if cr == board.rows - 1:
                                                game_state = -1
                                                SE.play_lose()
                                                end_time = time.time()
                                                history_table.add(end_time - start_time + resumed_time, target, -1, board)
                                                if time_mode != 'Unlimited':
                                                    cooldown_endtime = time.time() + cooldown_dur
                                                    game_phase = 'Cooldown'
                                                else:
                                                    game_phase = 'Ready'
                                            break
                                        elif result[i] == "GREEN" and i == len(result) - 1:
                                            game_state = 1
                                            SE.play_win()
                                            end_time = time.time()
                                            if time_mode != 'Unlimited':
                                                cooldown_endtime = time.time() + cooldown_dur
                                                game_phase = 'Cooldown'
                                            else:
                                                game_phase = 'Ready'
                                            history_table.add(end_time - start_time + resumed_time, target, 1, board)
                                    cr += 1
                                    cc = 0
                                    guess = ""

                # chế độ tiếng Việt (các phần giải thích tương tự chế độ tiếng Anh sẽ được bỏ qua)
                elif game_mode == 'Vietnamese':
                    if event.unicode.isalpha():
                        c = event.unicode.upper()
                        if cc < board.cols:
                            save(undo, cc, guess, board)
                            redo.clear()
                            board.mainboard[cr][cc].text = c
                            cc += 1
                            guess += c
                    # xử lý nhập ký tự có dấu
                    elif event.unicode.isdigit() and len(guess) != 0: # nếu ký tự nhập là số (kiểu gõ VNI) và đã có ít nhất một ký tự trước đó
                        n = event.unicode
                        # gọi hàm tran_word để chuyển ký tự cuối của từ đoán sang ký tự có dấu tương ứng
                        temp = tran_word(guess[-1], n)
                        if temp != None: # nếu có ký tự tương ứng
                            save(undo, cc, guess, board) # lưu trạng thái hiện tại vào stack undo
                            redo.clear() # xoá stack redo
                            # thay thế ký tự cuối trong từ đoán và trong ô hiện tại bằng ký tự có dấu
                            guess = guess[:len(guess)-1] + temp
                            board.mainboard[cr][cc - 1].text = temp
                    elif event.key == pygame.K_BACKSPACE:
                        if cc > 0:
                            save(undo, cc, guess, board)
                            redo.clear()
                            cc -= 1
                            board.mainboard[cr][cc].text = ""
                            guess = guess[:len(guess)-1]
                    elif event.key == pygame.K_RETURN:
                        if cc < board.cols:
                            error = "Not enough letters!"
                            SE.play_error()
                            error_endtime = time.time() + 1.5
                        elif cc == board.cols:
                            result = main_func(target, guess, d_Vietnamese)
                            if result == None:
                                error = "Guess not in dictionary!"
                                SE.play_error()
                                error_endtime = time.time() + 1.5
                            else:
                                redo.clear()
                                undo.clear()
                                for i in range(len(result)):
                                    if result[i] == "GREEN":
                                        board.mainboard[cr][i].color = green
                                    elif result[i] == "YELLOW":
                                        board.mainboard[cr][i].color = yellow
                                    else: board.mainboard[cr][i].color = gray
                                for i in range(len(result)):
                                    if result[i] != "GREEN":
                                        if cr == board.rows - 1:
                                            game_state = -1
                                            SE.play_lose()
                                            end_time = time.time()
                                            history_table.add(end_time - start_time + resumed_time, target, -1, board)
                                            if time_mode != 'Unlimited':
                                                cooldown_endtime = time.time() + cooldown_dur
                                                game_phase = 'Cooldown'
                                            else:
                                                game_phase = 'Ready'
                                        break
                                    elif result[i] == "GREEN" and i == len(result) - 1:
                                        game_state = 1
                                        SE.play_win()
                                        end_time = time.time()
                                        if time_mode != 'Unlimited':
                                            cooldown_endtime = time.time() + cooldown_dur
                                            game_phase = 'Cooldown'
                                        else:
                                            game_phase = 'Ready'
                                        history_table.add(end_time - start_time + resumed_time, target, 1, board)
                                cr += 1
                                cc = 0
                                guess = ""
        # 4. Vẽ giao diện game
        screen.fill(white) # xoá màn hình tại mỗi vòng lặp game

        # hiển thị thông báo lỗi khi thời gian hiện tại bé hơn thời gian kết thúc lỗi
        if time.time() <= error_endtime:
            screen.blit(font.render(error, True, black), (50, 10))

        # vẽ giao diện menu
        if curr_state == 'Menu':
            new_game_button.draw(screen, font)
            top_20_button.draw(screen, font)
            resume_button.draw(screen, font)
            Game = font.render("WORDLE", True, black) # render chữ thành hình ảnh
            screen.blit(Game, (300, 200)) # vẽ chữ lên màn hình

        # vẽ giao diện bảng xếp hạng top 20
        elif curr_state == 'Top20':
            back_button.draw(screen, font)
            refresh_button.draw(screen, font)
            top20_board.draw(screen, font2, top20_list)
            text = font.render("Top 20 Players", True, black)
            screen.blit(text, (300, 50))
        
        # vẽ giao diện nhập tên người chơi
        elif curr_state == 'Input_Name':
            back_button.draw(screen, font)
            start_button.draw(screen, font)
            prompt = font.render("Enter your name (3-10 characters):", True, black)
            screen.blit(prompt, (100, 200))
            pygame.draw.line(screen, black, (220, 340), (600, 340), 2) # vẽ gạch chân chỗ nhập tên
            name = font.render(input_name, True, black)
            screen.blit(name, (410 - name.get_width() // 2, 300)) # vẽ tên người chơi đang nhập
            # 410 là trung điểm của gạch chân, trừ cho một nửa chiều rộng của tên để tên được canh giữa
            # tại đây có sử dụng AI để hỏi về phương thức get_width()
            
        # vẽ giao diện game
        elif curr_state == 'Game':
            # vẽ bảng và các nút cơ bản
            board.draw(screen, font5)
            back_button.draw(screen, font)
            undo_button.draw(screen, font)
            redo_button.draw(screen, font)
            endgame_button.draw(screen, font)
            setting_button.draw(screen, font3)
            timescoring_button.draw(screen, font3)
            newgame_button.draw(screen, font)
            if game_state == 1: # nếu thắng 
                game = "You won!"
                tex = font.render(game, True, green)
                screen.blit(tex, (50, 10))
                time_taken = round(end_time - start_time + resumed_time, 2)
                # thời gian chơi bằng thời gian bắt đầu - thời gian kết thúc cộng thêm thời gian lưu trước đó (vì mỗi lần mở file resume thì start_time = 0)
                time_text = "Time taken: " + str(time_taken) + " s"
                time_tex = font2.render(time_text, True, green)
                screen.blit(time_tex, (50, 60))
            elif game_state == -1: # nếu thua
                game = "You lost! The word was " + target
                tex = font.render(game, True, red)
                screen.blit(tex, (50, 10))
                time_taken = round(end_time - start_time + resumed_time, 2)
                time_text = "Time taken: " + str(time_taken) + " s"
                time_tex = font2.render(time_text, True, red)
                screen.blit(time_tex, (50, 60))
            elif game_state == 0 and game_phase != 'Setup': # nếu đang chơi, đặt điều kiện khác Setup để tránh các lỗi biến chưa khai báo khi chưa vào game
                 #For testing
                game = target
                tex = font4.render(game, True, black)
                screen.blit(tex, (270, 50))
                
                if setting_state or timescoring_state:
                    curr_time = pause # khi mở bảng setting hoặc bảng timescoring thì giữ thời gian lúc mới mở
                else:
                    curr_time = time.time() # nếu không thì lấy thời gian hiện tại
                time_elapsed = round(curr_time - start_time + resumed_time, 2)
                # thời gian đã trôi qua bằng thời gian hiện tại - thời gian bắt đầu cộng thêm thời gian đã lưu trước đó
                time_text = "Time elapsed: " + str(time_elapsed) + " s"
                time_tex = font2.render(time_text, True, black)
                screen.blit(time_tex, (50, 60))
            # vẽ bảng setting
            if setting_state:
                # làm mờ cửa sổ game
                filter = pygame.Surface((800, 600))
                filter.set_alpha(200)
                filter.fill(gray)
                screen.blit(filter, (0, 0))
                # vẽ bảng setting
                setting_table.draw(screen, font)
                done_button.draw(screen, font)
                setting_text = font.render("Settings", True, black)
                screen.blit(setting_text, (350, 120))

                mode_text = font2.render("Game Mode:", True, black)
                screen.blit(mode_text, (250, 160))
                pygame.draw.line(screen, black, (250, 180), (550, 180), 2)
                English_text = font4.render("English", True, black)
                screen.blit(English_text, (280, 190))
                pygame.draw.line(screen, black, (280, 207), (550, 207), 2)
                Vietnamese_text = font4.render("Vietnamese", True, black)
                screen.blit(Vietnamese_text, (280, 220))
                pygame.draw.line(screen, black, (280, 237), (550, 237), 2)
                Equation_text = font4.render("Equation", True, black)
                screen.blit(Equation_text, (280, 250))
                pygame.draw.line(screen, black, (280, 267), (550, 267), 2)

                reset_time_text = font2.render("Reset Time:", True, black)
                screen.blit(reset_time_text, (250, 280))
                pygame.draw.line(screen, black, (250, 300), (550, 300), 2)
                daily_text = font4.render("Daily", True, black)
                screen.blit(daily_text, (280, 310))
                pygame.draw.line(screen, black, (280, 327), (550, 327), 2)
                unlimited_text = font4.render("Unlimited", True, black)
                screen.blit(unlimited_text, (280, 340))
                pygame.draw.line(screen, black, (280, 357), (550, 357), 2)
                customize_text = font4.render("Customize", True, black)
                screen.blit(customize_text, (280, 370))
                pygame.draw.line(screen, black, (280, 387), (550, 387), 2)

                
                unlimited_button.draw(screen, font4)
                daily_button.draw(screen, font4)
                customize_button.draw(screen, font4)
                English_button.draw(screen, font4)
                Vietnamese_button.draw(screen, font4)
                Equation_button.draw(screen, font4)

                if customize_button.color == black: # khi nút Customize được chọn thì vẽ các ô để hiển thị h, m, s được nhập
                    # nếu ô được chọn thì viền đỏ, không được chọn thì viền đen
                    pygame.draw.rect(screen, red if customize_on == 'h' else black, (570, 365, 30, 25), 1)
                    h = font4.render(customize_h, True, black)
                    screen.blit(h, (575, 368))
                    screen.blit(font4.render('h', True, black), (602, 368))

                    pygame.draw.rect(screen, red if customize_on == 'm' else black, (620, 365, 30, 25), 1)
                    m = font4.render(customize_m, True, black)
                    screen.blit(m, (625, 368))
                    screen.blit(font4.render('m', True, black), (652, 368))

                    pygame.draw.rect(screen, red if customize_on == 's' else black, (670, 365, 30, 25), 1)
                    s = font4.render(customize_s, True, black)
                    screen.blit(s, (675, 368))
                    screen.blit(font4.render('s', True, black), (702, 368))

            # vẽ bảng timescoring
            if timescoring_state:
                filter = pygame.Surface((800, 600))
                filter.set_alpha(200)
                filter.fill(gray)
                screen.blit(filter, (0, 0))
                timescoring_table.draw(screen, font)
                done_button.draw(screen, font)
                history_table.draw(screen, font5)
                timescoring_text = font.render("History", True, black)
                screen.blit(timescoring_text, (350, 120))

            # nếu game đang cooldown thì vẽ bộ đếm thời gian cooldown và làm mờ các nút newgame, undo và redo
            if game_phase == 'Cooldown':
                remain = int(cooldown_endtime - time.time())
                m, s = divmod(remain, 60)
                h, m = divmod(m, 60)
                cd = "Cooldown: {:02d}:{:02d}:{:02d}".format(h, m, s)

                cd = font3.render(cd, True, red)
                screen.blit(cd, (270, 50))

                filter = pygame.Surface((200, 50))
                filter.set_alpha(200)
                filter.fill(gray)
                screen.blit(filter, (50, 550))
                screen.blit(filter, (570, 500))
                screen.blit(filter, (570, 550))
            
        elif curr_state == 'Resume': # vẽ giao diện resume khi thoát ra từ game
            text = "Choose a slot to save your game:"
            tex = font.render(text, True, black)
            screen.blit(tex, (140, 100))
            resume_table.draw_game(screen, font5)
            back_button.draw(screen, font)
            cancel_button.draw(screen, font)

        elif curr_state == 'Resume_Enter': # vẽ giao diện resume khi vào từ menu
            text = "Choose your saved game:"
            tex = font.render(text, True, black)
            screen.blit(tex, (140, 100))
            resume_table.draw_menu(screen, font5)
            back_button.draw(screen, font)

        elif curr_state == 'History': # vẽ giao diện khi xem lại các màn chơi trước đó
            back_button.draw(screen, font)
            temp_board.draw(screen, font5)
            if temp_game_state == 1:
                game = "You won!"
                tex = font.render(game, True, green)
                screen.blit(tex, (50, 10))
                time_taken = round(temp_time, 2)
                time_text = "Time taken: " + str(time_taken) + " s"
                time_tex = font2.render(time_text, True, green)
                screen.blit(time_tex, (50, 60))
            elif temp_game_state == -1:
                game = "You lost! The word was " + temp_target
                tex = font.render(game, True, red)
                screen.blit(tex, (50, 10))
                time_taken = round(temp_time, 2)
                time_text = "Time taken: " + str(time_taken) + " s"
                time_tex = font2.render(time_text, True, red)
                screen.blit(time_tex, (50, 60))

        music_button.draw(screen, font3) # vẽ nút bấm chuyển nhạc nền

        # cập nhật màn hình tại mỗi khung hình
        pygame.display.flip()
        clock.tick(30) # thiết lập fps
    
    pygame.quit() # tắt tất cả các module của Pygame
    sys.exit() # thoát khỏi trình thông dịch của Python
    # hai lệnh này có dùng AI để giải thích ý nghĩa

if __name__ == "__main__":
    main()


"""
Docstring for source.storage
File chứa các hàm dùng cho việc lưu dữ liệu dưới dạng nhị phân cho tính năng resume và top 20 list
"""
import struct as st
import source.draw as draw
from source.logic import minor_func
from source.constant import *
# Có sử dụng AI để hỏi về cách lưu tập tin nhị phân và module struct

def xdata(data):
    # Hàm dùng để mã hoá dữ liệu nhị phân bằng phép toán xor
    k = 228 # khoá k để xor với từng byte dữ liệu
    temp = bytearray(data) # chuyển dữ liệu thành mảng mutable để xor
    for i in range(len(temp)):
        temp[i] = temp[i] ^ k # phép toán xor từng byte dữ liệu với khoá k
    return bytes(temp) # trả về dữ liệu đã xor ở dạng các byte (immutable)
    # có dùng AI để hỏi về bytes và bytearray

def guesses_board(board):
    # Hàm dùng để trả về dữ liệu chữ của bảng hiện tại dưới dạng một list gồm các string
    guesses = [] # tạo list rỗng
    for i in range(board.rows): # duyệt hết tất cả các hàng của bảng
        guess = '' # tạo từ của mỗi hàng
        for j in range(board.cols): # duyệt qua từng ô trong bảng để cộng vào guess, nếu có ký tự thì cộng ký tự, nếu không thì cộng khoảng trắng
            if board.mainboard[i][j].text != '':
                guess += board.mainboard[i][j].text
            else:
                guess += ' '
        guesses.append(guess.encode('utf-8')) # thêm từ của hàng hiện tại (đã encode) vào list từ
    return guesses


def savegame(filename, target, board, cr, cc, time_elapsed, name, cooldown_endtime, game_mode, time_mode, game_state, cooldown_dur, history_table):
    # Hàm dùng để lưu toàn bộ trạng thái của username hiện tại
    try:
        # 1. Dữ liệu của màn chơi hiện tại đã encode thành byte
        guesses = guesses_board(board)
        target = target.encode('utf-8')
        name = name.encode('utf-8')
        game_mode = game_mode.encode('utf-8')
        time_mode = time_mode.encode('utf-8')

        # format cho màn chơi hiện tại (với các từ dùng 20 byte để đề phòng các ký tự tiếng Việt chiếm nhiều hơn 1 byte)
        fmt = '20s 20s 20s 20s 20s 20s 20s i i f 20s d 20s 20s i i'

        # đóng gói dữ liệu màn chơi hiện tại
        packed_data = st.pack(fmt, target, guesses[0], guesses[1], guesses[2], guesses[3], guesses[4], guesses[5], cr, cc, time_elapsed, name, cooldown_endtime, game_mode, time_mode, game_state, cooldown_dur)
        
        # 2. Dữ liệu của các màn chơi trong lịch sử
        history_matches = history_table.matches # lấy danh sách của các màn chơi trong lịch sử
        temp_cnt_data = st.pack('i', len(history_matches)) 
        packed_data += temp_cnt_data # đóng gói tổng số màn chơi trong lịch sử để thuận tiện cho việc loadgame

        # format cho một màn chơi trong lịch sử
        temp_fmt = 'f 20s i 20s 20s 20s 20s 20s 20s'

        # duyệt qua từng màn chơi trong lịch sử sau đó encode và đóng gói
        for match in history_matches:
            temp_time, temp_target, temp_wl, temp_board = match
            temp_target = temp_target.encode('utf-8')
            temp_guesses = guesses_board(temp_board)
            packed_data += st.pack(temp_fmt, temp_time, temp_target, temp_wl, temp_guesses[0], temp_guesses[1], temp_guesses[2], temp_guesses[3], temp_guesses[4], temp_guesses[5])

        # mã hoá dữ liệu bằng hàm xor
        xored_data = xdata(packed_data)
        # lưu dữ liệu vào file
        with open(filename, 'wb') as f:
            f.write(xored_data)
    except Exception as e:
        print(f"Error saving game: {e}")


def loadgame(filename, board, history_table):
    # Hàm dùng để load game của một username từ file resume
    try:
        # đọc dữ liệu từ file sau đó đem xor lại để trả về dữ liệu gốc
        with open(filename, 'rb') as f:
            xored_data = f.read()
        packed_data = xdata(xored_data)

        # 1. Lấy trạng thái màn chơi hiện tại
        # format của màn chơi hiện tại
        fmt = '20s 20s 20s 20s 20s 20s 20s i i f 20s d 20s 20s i i'
        # tách dữ liệu của màn chơi hiện tại bằng cách tính kích thước vùng nhớ dựa vào format, sau đó unpack dữ liệu
        curr_packed_data = packed_data[:st.calcsize(fmt)]
        unpacked_data = st.unpack(fmt, curr_packed_data)

        # lấy dữ liệu đã lưu thông qua ký tự trong format
        # với 20s thì cần xoá các ký tự null (\x00) do python tự thêm vào để lấp đầy 20 byte
        # tại đây có sử dụng AI để hỏi về cách Python lấp đầy 20 byte
        target = unpacked_data[0].decode('utf-8').rstrip('\x00')
        guesses = [unpacked_data[i].decode('utf-8').rstrip('\x00') for i in range(1, 7)]
        cr = unpacked_data[7]
        cc = unpacked_data[8]
        time_elapsed = unpacked_data[9]
        name = unpacked_data[10].decode('utf-8').rstrip('\x00')
        cooldown_endtime = unpacked_data[11]
        game_mode = unpacked_data[12].decode('utf-8').rstrip('\x00')
        time_mode = unpacked_data[13].decode('utf-8').rstrip('\x00')
        game_state = unpacked_data[14]
        cooldown_dur = unpacked_data[15]

        # điền vào bàn cờ
        guess = '' # khởi tạo guess bằng chuỗi rỗng, từ đang đoán dở của người chơi

        board.clear() # xoá sạch bàn cờ trước để tránh bị ghi đè

        # thiết lập số hàng cần điền, nếu game đã kết thúc thì điền đúng cr hàng, nếu chưa thì cr + 1 (do hàng cuối cùng vẫn chưa được tăng chỉ số lên)
        fill_row = cr + 1 if game_state == 0 else cr
        for i in range(fill_row):
            if i == cr: # nếu i bằng cr (tức hàng đang được viết dở) thì chỉ điền đến cột đang được viết dở (cc)
                for j in range(cc):
                    guess += guesses[i][j] # từ đang đoán dở của người chơi
                    board.mainboard[i][j].text = guesses[i][j]
            else: # nếu i < cr tức hàng đã hoàn thành thì điền hết hàng
                for j in range(board.cols):
                    board.mainboard[i][j].text = guesses[i][j]

        # 2. Lấy lại dữ liệu của các màn chơi trong lịch sử của username

        # xoá sạch bảng lịch sử trước để tránh bị ghi đè dữ liệu
        history_table.clear()
        # lấy số màn chơi trong lịch sử
        start_history = st.calcsize(fmt) # bắt đầu tại fmt
        history = packed_data[start_history:start_history + 4] # vì dữ liệu kiểu int nên là 4 byte
        temp_cnt = st.unpack('i', history)[0] # vì unpack trả về tuple nên phải có chỉ số 0 để lấy int, tại đây có dùng AI để giải thích lý do bug nếu không có chỉ số
        start_history += 4 # cộng thêm 4 byte để bắt đầu lấy các màn chơi

        temp_fmt = 'f 20s i 20s 20s 20s 20s 20s 20s' # format cho 1 màn chơi trong lịch sử
        temp_size = st.calcsize(temp_fmt) # kích thước dữ liệu cho một màn chơi trong lịch sử

        # duyệt qua các màn chơi trong lịch sử dựa vào số đếm số màn chơi
        for i in range(temp_cnt):
            packed_match = packed_data[start_history:start_history + temp_size] # dữ liệu của 1 màn chơi
            start_history += temp_size # tăng vị trí con trỏ byte

            match = st.unpack(temp_fmt, packed_match) # unpack dữ liệu để trả về một tuple

            # lấy các dữ liệu trong tuple, tương tự các dữ liệu được lưu 20s sẽ được loại bỏ ký tự null dư thừa
            temp_time = match[0]
            temp_target = match[1].decode('utf-8').rstrip('\x00')
            temp_wl = match[2]
            temp_guesses = [match[j].decode('utf-8').rstrip('\x00') for j in range(3, 9)]

            # khởi tạo một bảng trống để ghi dữ liệu, vì mỗi lần khởi tạo là vùng nhớ mới nên không cần deepcopy, tại đây có sử dụng AI để hỏi về sự cần thiết của deepcopy
            temp_board = draw.board()
            
            # cài đặt điểm dừng, nếu thắng thì chạy đến hàng có target, nếu thua thì chạy hết bảng
            stop = temp_guesses.index(temp_target) + 1 if temp_wl == 1 else 6
            for j in range(stop):
                temp_guess = temp_guesses[j]
                temp_result = minor_func(temp_target, temp_guess) # lấy danh sách màu để tô lại bảng

                # vòng lặp để điền chữ và tô mỗi hàng
                for k in range(len(temp_guess)):
                    temp_board.mainboard[j][k].text = temp_guess[k]
                    if temp_result[k] == "GREEN":
                        temp_board.mainboard[j][k].color = green
                    elif temp_result[k] == "YELLOW":
                        temp_board.mainboard[j][k].color = yellow
                    else:
                        temp_board.mainboard[j][k].color = gray

            # thêm trạng thái màn chơi vào history table
            history_table.add(temp_time, temp_target, temp_wl, temp_board)

        # trả về các thông tin cần thiết để vào lại màn chơi cho username
        return target, cr, cc, guess, time_elapsed, name, cooldown_endtime, game_mode, time_mode, game_state, cooldown_dur
            
    # nếu không có file thì return None để tránh bị crash hoặc in nhiều ra terminal
    except FileNotFoundError:
        return None
    except Exception as e:
        print('Error loading game:', e)
        return None

def save_player(filename, player_list):
    # Hàm dùng để lưu danh sách top 20 người chơi
    try:
        player = [] # tạo list chứa danh sách người chơi

        # duyệt qua từng người chơi trong Linked List để lưu tuple chứa (name, time) vào list
        curr = player_list.head
        for i in range(player_list.len):
            player.append((curr.name.encode('utf-8'), curr.time))
            curr = curr.next
        
        # format cho một người chơi nhân cho số người chơi
        fmt = '20s f' * player_list.len
        # đóng gói dữ liệu
        # for p in player là từng tuple (name, time); for data in p là từng phần tử trong tuple đó
        # dấu * để giải tách các phần tử của tuple lớn ra
        packed_data = st.pack(fmt, *(data for p in player for data in p))

        # xor dữ liệu rồi ghi vào file
        xored_data = xdata(packed_data)

        with open(filename, 'wb') as f:
            f.write(xored_data)
    except Exception as e:
        print(f"Error saving player data: {e}")

def load_player(filename):
    # Hàm dùng để load danh sách các player đã lưu và trả về list
    player_list = []
    try:
        # đọc dữ liệu và xor ngược lại để trả về dữ liệu gốc
        with open(filename, 'rb') as f:
            xored_data = f.read()

        packed_data = xdata(xored_data)

        # format của một người chơi nhân cho số người chơi
        # vì một người chơi chiếm 24 byte (20 byte cho tên và 4 byte cho thời gian) nên số người chơi là tổng số byte chia 24
        # dùng // để trả về số nguyên để nhân với chuỗi
        fmt = '20s f' * (len(xored_data) // 24)

        # unpack dữ liệu tạo thành một tuple
        player = st.unpack(fmt, packed_data)

        # duyệt qua các phần tử chẵn (là name) và các phần tử lẻ liền kề sau nó là time ứng với name
        # sau đó thêm tuple (name, time) vào list, cuối cùng trả về list
        for i in range(0, len(player), 2):
            name = player[i].decode('utf-8').rstrip('\x00')
            time = player[i + 1]
            player_list.append((name, time))
        return player_list
        
    except Exception as e:
        print(f"Error loading player data: {e}")

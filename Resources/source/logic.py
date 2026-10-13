"""
Docstring for source.logic
File chứa các hàm logic chính dùng cho các vận hành cốt lõi của game
"""
import copy

def main_func(target, guess, d):
    # Hàm dùng để xác định màu để tô
    if not binary_search(guess, d):
        return None # Nếu từ đoán (guess) không có trong từ điển thì trả về None để báo lỗi
    
    return minor_func(target, guess) # Trả về kết quả của minor_func

def minor_func(target, guess):
    # Hàm dùng để xác định màu tô khi đã biết chắc từ có trong từ điển, dùng khi load lên lại lịch sử các trận đấu từ file resume và đoạn sau của main_func
    target = list(target) # list các ký tự trong mục tiêu
    guess = list(guess) # list các ký tự trong từ đoán
    result = [None] * len(guess) # list kết quả

    for i in range(len(guess)): # vòng lặp thứ nhất duyệt qua các ký tự đúng và đúng vị trí
        if guess[i] == target[i]:
            result[i] = "GREEN" # kết quả tại i màu xanh
            target[i] = None 
            guess[i] = None
            # gán ký tự thứ i của target và result là None để tránh việc đếm thừa cho các ký tự sai vị trí

    for i in range(len(guess)): # vòng lặp thứ hai duyệt các ký tự còn lại
        if guess[i] == None:
            continue # bỏ qua nếu đã màu xanh 
        else:
            if guess[i] in target: # nếu ký tự trong mục tiêu thì trả về màu vàng
                result[i] = "YELLOW"
                target[target.index(guess[i])] = None # đặt ký tự đã có là None để tránh bị đếm thừa
            else:
                result[i] = "GRAY" # nếu không có trong mục tiêu thì trả về xám
    return result # trả về danh sách màu để tô

def save(do, cc, guess, board):
    # Hàm để lưu trạng thái bàn chơi vào undo/redo, chỉ lưu cột (cc) mà không lưu hàng vì undo/redo chỉ có hiệu lực trọng phạm vi một hàng, qua hàng mới thì bị reset
    status = (copy.deepcopy(board.mainboard), cc, guess) # đặt trạng thái là một tuple, dùng deepcopy với mainboard vì bản thân mainboard là list để tránh tạo view thay vì copy
    do.push(status) # push status vào stack

def check_equal(guess):
    # Hàm dùng để kiếm tra phương trình (dùng cho chế độ Equation)
    if '=' not in guess or guess.count('=') > 1:
        return None # nếu số dấu = trong guess khác 1 thì trả về None để thông báo guess phải là phương trình
    i = guess.index('=') # lấy chỉ số của dấu bằng
    if i == 0 or i == 4: # kiểm tra nếu dấu = ở đầu hoặc cuối
        return None
    if eval(guess[:i]) == eval(guess[i + 1:]): # kiếm tra tính đúng đắn của phương trình
        return True
    return False

def dictionary(filename):
    # Hàm dùng để tạo danh sách từ từ file
    d = []
    with open(filename, "r", encoding = 'utf-8') as f: # đọc file
        for line in f: # đọc từng dòng trong file
            word = line.strip().upper() # cắt bỏ đi \n và viết hoa các ký tự
            word = word.replace(' ', '') # bỏ đi các dấu cách nếu có
            if len(word) == 5: # nếu từ có 5 ký tự thì thêm vào danh sách
                d.append(word)
    return quick_sort(d) # trả về danh sách được sắp xếp để thuận tiện cho việc tìm kiếm bằng binary search

def binary_search(g, d):
    # Hàm dùng để tìm kiếm từ trong danh sách
    start = 0 # đầu danh sách
    end = len(d) - 1 # cuối danh sách
    while start <= end: # thu hẹp phạm vi tìm kiếm
        mid = (start + end)//2 # đặt mốc so sánh ở giữa danh sách
        if g == d[mid]:
            return True # nếu mục tiêu cần tìm bằng d[mid], trả về True
        elif g > d[mid]:
            start = mid + 1 # nếu mục tiêu cần tìm lớn hơn d[mid], tìm kiếm ở nửa sau của danh sách
        else:
            end = mid - 1 # nếu mục tiêu cần tìm nhỏ hơn d[mid], tìm kiếm ở nửa trước của danh sách
    return False # nếu duyệt hết mà không tìm thấy thì trả về False

def quick_sort(d):
    # Hàm dùng để sắp xếp lại danh sách, có tham khảo AI để lựa chọn thuật toán sắp xếp tối ưu
    if len(d) <= 1:
        return d # Nếu danh sách rỗng hoặc có 1 phần tử thì trả về chính nó
    l = [] # phần bé hơn mốc chọn
    m = [] # phần bằng mốc chọn
    r = [] # phần lớn hơn mốc chọn
    for i in range(len(d)): # chọn mốc là phần tử chính giữa, duyệt qua từng phần tử để thêm vào từng list phù hợp khi so sánh với phần tử giữa
        if d[i] == d[len(d) // 2]:
            m.append(d[i])
        elif d[i] < d[len(d) // 2]:
            l.append(d[i])
        else: r.append(d[i])

    return quick_sort(l) + m + quick_sort(r) # gọi đệ quy cho các danh sách l và r để tiếp tục sắp xếp



def tran_word(a, n):
    # Hàm dùng để gõ ký tự tiếng Việt bằng bộ gõ VNI giới hạn (gõ số n chỉ có hiệu lực lên ký tự cuối cùng a)
    a = a.lower() # chuyển về ký tự thường để tìm kiếm
    # Bảng tìm kiếm các nguyên âm và thanh điệu của nó với thứ tự ngang-sắc-huyền-hỏi-ngã-nặng, phù hợp với thứ tự số của kiểu gõ VNI
    tran = ['aáàảãạ', 'ăắằẳẵặ', 'âấầẩẫậ', 'eéèẻẽẹ', 'êếềểễệ', 'iíìỉĩị', 'oóòỏõọ', 'ôốồổỗộ', 'ơớờởỡợ', 'uúùủũụ', 'ưứừửữự', 'yýỳỷỹỵ']
    if (a == 'd' or a == 'đ') and n == '9':
        return 'Đ' # trường hợp đặc biệt chữ Đ
    def seek(a): # hàm dùng để tìm kiếm vị trí của a trong tran, nếu không có thì trả về None
        for i in range(12):
            for j in range(6):
                if a == tran[i][j]:
                    return i, j
        return None
    add = seek(a)
    if add == None:
        return None # nếu không tìm ra thì không hợp lệ, trả vê None
    else:
        i, j = add # gán i, j là vị trí của a
        if '0' <= n <= '5': # nếu n thuộc từ 0 đến 5 (tức là thanh điệu) thì trả về cùng ký tự nhưng thanh điệu theo số (đã được sắp xếp trong tran)
            return tran[i][int(n)].upper()
        elif n == '6': # nếu n bằng 6, thành ký tự dấu mũ
            if i in [0, 1, 2]: # a, ă, â chuyển thành â, giữ nguyên thanh điệu
                return tran[2][j].upper()
            elif i in [3, 4]: # e, ê chuyển thành ê, giữ nguyên thanh điệu
                return tran[4][j].upper()
            elif i in [6, 7, 8]: # o, ô, ơ chuyển thành ô, giữ nguyên thanh điệu
                return tran[7][j].upper()
            else: # nếu không hợp lệ, trả về None
                return None
        elif n == '7': # nếu n bằng 7, thành ký tự dấu móc
            if i in [6, 7, 8]: # o, ô, ơ chuyển thành ơ, giữ nguyên thanh điệu
                return tran[8][j].upper()
            elif i in [9, 10]: # u, ư chuyển thành ư, giữ nguyên thanh điệu
                return tran[10][j].upper()
            else: # nếu không hợp lệ, trả về None
                return None
        elif n == '8': # nếu n bằng 8, chuyển thành ký tự dấu trăng
            if i in [0, 1, 2]: # a, ă, â chuyển thành ă, giữ nguyên thanh điệu
                return tran[1][j].upper()
            else:
                return None # nếu không hợp lệ, trả về None
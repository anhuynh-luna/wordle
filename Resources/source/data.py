"""
Docstring for source.data
File chứa hai cấu trúc dữ liệu Linked List gồm player_list dùng cho Top 20 và stack dùng cho các tính năng undo và redo
"""

class Node_player_list():
    def __init__(self, name, time):
        self.name = name    # tên người chơi
        self.time = time    # thời gian chơi: được tính bằng tổng thời gian chơi / tổng số ván thắng
        self.next = None
    
class player_list():
    def __init__(self):
        self.head = None
        self.len = 0 # độ dài danh sách
    
    def add(self, name, time):
        # Phương thức thêm người chơi mới vào danh sách (bằng cách thêm vào đầu danh sách)
        new = Node_player_list(name, time)
        if self.len == 0:
            self.head = new # nếu danh sách đang rỗng thì new chính là head
        else:
            new.next = self.head # nếu danh sách không rỗng thì new.next là head hiện tại
            self.head = new # head mới sẽ là new
        self.len += 1 # tăng độ dài danh sách

    def sort(self):
        # Phương thức để sắp xếp danh sách (dùng bubble sort)
        curr = self.head # biến curr để đánh dấu Node hiện tại (khởi đầu là head)
        for i in range(self.len - 1, 0, -1): #số lần duyệt i khi sắp xếp
            for j in range(i):
                if curr.time > curr.next.time: # thời gian của Node hiện tại lớn hơn Node sau
                    curr.name, curr.next.name = curr.next.name, curr.name # hoán đổi tên người chơi
                    curr.time, curr.next.time = curr.next.time, curr. time # hoán đổi thời gian chơi (càng nhỏ càng ở trước)
                curr = curr.next # đi tới Node tiếp theo
            curr = self.head # khi hết vòng lặp của i hiện tại thì curr quay về Node đầu để tiếp tục i tiếp theo

    def top20(self):
        # Phương thức để lấy top 20
        self.sort() # sắp xếp lại danh sách theo thời gian từ nhỏ đến lớn
        # Lọc top 20 nếu danh sách có nhiều hơn 20 người
        i = 0 # đếm số Node đã đi hiện tại
        curr = self.head # khởi tạo ở head
        if self.len > 20: 
            while i < 19: # khi i == 19 (tức đã đủ 20 người do đếm từ 0) thì vòng lặp dừng lại
                curr = curr.next
                i += 1
            curr.next = None # xoá những người ở top sau
            self.len = 20 #đặt lại độ dài danh sách là 20

    def check_name(self, name):
        # Phương thức dùng để kiểm tra nếu tên có trong top 20
        curr = self.head # khởi tạo curr ở head
        while curr != None: # duyệt đến cuối danh sách
            if curr.name == name:
                return True # nếu gặp tên trùng, sẽ trả về True
            curr = curr.next
        return False # nếu không thì trả về False
    
    def clear(self):
        # Phương thức dùng để xoá danh sách
        self.head = None
        self.len = 0
    

class Node_stack():
    def __init__(self, data):
        self.data = data # dữ liệu được lưu
        self.next = None


class stack():
    def __init__(self):
        self.head = None
        self.len = 0

    def push(self, item):
        # Phương thức dùng để thêm vào stack (ở đây xem ngăn xếp trên cùng là đầu của Linked list để tối ưu tốc độ)
        new = Node_stack(item)
        if self.len == 0:
            self.head = new # nếu stack rỗng thì head chính là Node mới
        else:
            new.next = self.head
            self.head = new # nếu stack không rỗng thì thì thêm Node mới vào đầu
        self.len += 1 # tăng độ dài lên 1 đơn vị
    
    def pop(self):
        # Phương thức dùng để lấy ra ngăn xếp cuối cùng
        if self.len == 0:
            return None # nếu stack rỗng thì trả về None
        else:
            top = self.head # đặt top là head
            self.head = top.next # gán head mới chính là top.next
            self.len -= 1 # trừ độ dài đi 1 đơn vị
            return top.data # trả về dữ liệu của top
    
    def clear(self):
        # Phương thức dùng để xoá sạch stack khi qua ván mới/dòng mới
        self.head = None 
        self.len = 0
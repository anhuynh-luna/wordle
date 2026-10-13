"""
Docstring for source.draw
File chứa các đối tượng dùng cho việc vẽ đồ hoạ cho game
"""
import pygame
from source.constant import *

class tile():
    # Class dùng để vẽ các ô vuông trên bảng
    def __init__(self, x, y, text = "", color = white):
        self.x = x
        self.y = y
        self.text = text
        self.color = color # màu nền mặc định là trắng
        self.border = black # màu viền là đen
        self.width = 60
        self.height = 60
        # tạo đối tượng hình chữ nhật để thuận tiện cho việc vẽ/hiển thị chữ
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, font):
        # Phương thức dùng để vẽ một ô vuông
        # vẽ nền và viền của ô
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.border, self.rect, 2)

        # nếu chữ cái khác rỗng thì vẽ chữ ở giữa ô
        if self.text != "":
            text_surface = font.render(self.text, True, black)
            # căn giữa ký tự trong ô vuông một cách tự động, tại đây có sử dụng AI để hỏi về lệnh rect.center
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
            

class board():
    # Class dùng để vẽ và quản lý bảng
    def __init__(self):
        self.rows = 6 # số hàng
        self.cols = 5 # số cột
        self.xs = 250 # toạ độ x bắt đầu
        self.ys = 120 # toạ độ y bắt đầu
        # tạo mảng hai chiều với các phần tử là các tile
        self.mainboard = [[tile(self.xs + col*60, self.ys + row*60) for col in range(self.cols)] for row in range(self.rows)]
    
    def draw(self, screen, font):
        # Phương thức dùng để vẽ bảng bằng cách duyệt qua và gọi phương thức draw của từng tile
        for row in range(self.rows):
            for col in range(self.cols):
                self.mainboard[row][col].draw(screen, font)

    def clear(self):
        # Phương thức dùng để xoá bảng bằng cách duyệt qua từng tile và gán text bằng rỗng, màu nền bằng white
        for row in range(self.rows):
            for col in range(self.cols):
                self.mainboard[row][col].text = ""
                self.mainboard[row][col].color = white


class button():
    # Class dùng để vẽ và xử lý nhấn chuột các nút bấm có dạng hình chữ nhật
    def __init__(self, x, y, text = "", width = 200, height = 50, color = white):
        self.x = x
        self.y = y
        self.text = text # text mặc định là rỗng
        self.color = color
        self.border = black
        self.width = width
        self.height = height
        # tạo đối tượng hình chữ nhật để thuận tiện cho vẽ và xử lý nhấn chuột
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, font):
        # Phương thức dùng để vẽ nút
        # vẽ nền và viền của nút
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.border, self.rect, 2)

        # nếu text khác rỗng thì vẽ text ở ngay giữa nút
        if self.text != "":
            text_surface = font.render(self.text, True, black)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def click(self, pos):
        # Phương thức dùng để xử lý nhấn chuột bằng cách kiểm tra toạ độ nhấn chuột có nằm trong vùng của nút hay không
        # dùng phương thức collidepoint của đối tượng hình chữ nhật với pos là toạ độ vị trí nhấn chuột
        if self.rect.collidepoint(pos):
            return True
        return False

class top_20_board():
    # Class dùng để vẽ bảng xếp hạng top 20
    def __init__(self):
        self.rows = 5 # 5 hàng
        self.cols = 4 # 4 cột
        self.xs = 40 # toạ độ x bắt đầu
        self.ys = 120 # toạ độ y bắt đầu
        # tạo mảng hai chiều với các phần tử là các button
        self.mainboard = [[button(self.xs + col*180, self.ys + row*60, width = 180, height = 60) for col in range(self.cols)] for row in range(self.rows)]

    def fill(self, player_list):
        # Phương thức dùng để điền dữ liệu vào bảng xếp hạng từ danh sách người chơi
        curr = player_list.head
        for i in range(player_list.len): # chỉ điền số người chơi hiện có
            # điền text vào từng button trong mảng, với số thứ tự hàng là i // self.cols, cột là i % self.cols (dựa trên kiến thức về modulo)
            self.mainboard[i // self.cols][i % self.cols].text = str(i + 1) + '. ' + curr.name + ': ' + str(curr.time) + 's'
            curr = curr.next

    def draw(self, screen, font, player_list):
        # Phương thức dùng để vẽ bảng xếp hạng bằng cách duyệt qua và gọi phương thức draw của từng button
        for i in range(player_list.len): # chỉ vẽ những ô có text khác rỗng
            self.mainboard[i // self.cols][i % self.cols].draw(screen, font)

class round_button():
    # Class dùng để vẽ và xử lý nhấn chuột các nút bấm có nội dung là các icon đặc biệt
    def __init__(self, x, y, text = "", width = 100, height = 50, color = white):
        self.x = x
        self.y = y
        self.text = text # mặc định là rỗng, dùng để điền icon
        self.color = color
        self.border = white # viền trắng để làm nổi bật icon bên trong
        self.width = width
        self.height = height
        # tạo đối tượng hình chữ nhật để thuận tiện cho vẽ và xử lý nhấn chuột
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, font):
        # Phương thức dùng để vẽ một nút tròn
        pygame.draw.ellipse(screen, self.color, self.rect)
        pygame.draw.ellipse(screen, self.border, self.rect, 2)

        # nếu text khác rỗng thì vẽ text ở giữa nút
        if self.text != "":
            text_surface = font.render(self.text, True, black)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def click(self, pos):
        # Phương thức dùng để xử lý nhấn chuột
        if self.rect.collidepoint(pos):
            return True
        return False
    
class resume_board():
    # Class dùng để vẽ bảng lưu và tiếp tục trò chơi
    def __init__(self):
        self.len = 5 # có 5 slot để lưu
        self.xs = 300
        self.ys = 220
        # tạo list có 5 phần tử là các button
        self.mainboard = [button(self.xs, self.ys + i*70) for i in range(self.len)]
    
    def draw_menu(self, screen, font):
        # Phương thức dùng để vẽ bảng khi từ menu vào nút resume
        # duyệt qua từng button để vẽ, nếu text bằng rỗng thì vẽ "No data", khác rỗng thì vẽ text
        for i in range(self.len):
            if self.mainboard[i].text == "":
                self.mainboard[i].text = "No data"
                self.mainboard[i].draw(screen, font)
                self.mainboard[i].text = ""
            else:
                self.mainboard[i].draw(screen, font)
    
    def draw_game(self, screen, font):
        # Phương thức dùng để vẽ bảng khi thoát ra khỏi game đang chơi
        # duyệt qua từng button để vẽ, nếu text bằng rỗng thì vẽ "Available", khác rỗng thì vẽ text
        for i in range(self.len):
            if self.mainboard[i].text == "":
                self.mainboard[i].text = "Available"
                self.mainboard[i].draw(screen, font)
                self.mainboard[i].text = ""
            else:
                self.mainboard[i].draw(screen, font)
    
    def click(self, pos):
        # Phương thức dùng để xử lý nhấn chuột thông qua phương thức click của từng button
        # nếu button nào được nhấn thì trả về chỉ số của nó, nếu nhấn ở ngoài thì trả về -1
        if self.mainboard[0].click(pos):
            return 0
        elif self.mainboard[1].click(pos):
            return 1
        elif self.mainboard[2].click(pos):
            return 2
        elif self.mainboard[3].click(pos):
            return 3
        elif self.mainboard[4].click(pos):
            return 4
        return -1
    
    def fill(self, Resume):
        # Phương thức dùng để điền dữ liệu username vào từng button thông qua list Resume khi load từ các file
        for i in range(5):
            if Resume[i] != None:
                self.mainboard[i].text = Resume[i][5]
            else:
                self.mainboard[i].text = ""

class scroll_list:
    # Class dùng để vẽ và xử lý danh sách lịch sử các trận đấu của một username
    # tại đây có dùng AI để hỏi về cách làm thanh cuộn
    def __init__(self):
        # toạ độ và kích thước của vùng nhìn được
        self.xs = 310
        self.ys = 200
        self.width = 200
        self.height = 175

        self.gap = 5 # khoảng cách giữa các nút
        self.buttons = [] # danh sách các nút
        self.matches = [] # danh sách các trận đấu tương ứng với mỗi nút
        self.y_start = 0 # vị trí cuộn hiện tại (0 là ở đầu danh sách)
        self.y_end = 0 # giới hạn cuộn tối đa (tổng chiều cao nội dung - chiều cao vùng nhìn được)
        self.view = pygame.Rect(310, 200, 200, 175) # vùng nhìn được

    def add(self, time, target, wl, board):
        # Phương thức dùng để thêm một trận đấu mới vào danh sách
        new_match = button(0, 0, target) # nút mới, toạ độ x, y ban đầu là (0, 0) và sẽ được tạo mới khi vẽ, target là từ cần đoán ở ván đó
        self.buttons.append(new_match) # thêm nút mới vào danh sách nút
        self.matches.append((time, target, wl, board)) # thêm trận đấu vào danh sách trận đấu
        self.update_height() # gọi hàm cập nhật chiều cao nội dung

    def update_height(self):
        # Phương thức dùng để cập nhật giới hạn cuộn tối đa
        total_height = len(self.buttons) * 55 # tổng chiều cao nội dung (mỗi nút cao 50 + khoảng cách 5)
        self.y_end = max(0, total_height - self.height) # giới hạn cuộn tối đa phải lớn hơn hoặc bằng 0

    def handle_event(self, event):
        # Phương thức để xử lý sự kiện cuộn
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: # khi nhấn lên thì cuộn lên
                self.y_start -= 20 # vị trí cuộn giảm
            elif event.key == pygame.K_DOWN: # khi nhấn xuống thì cuộn xuống
                self.y_start += 20 # vị trí cuộn tăng
            # đặt giới hạn cho vị trí cuộn (bé nhất bằng 0, lớn nhất bằng giới hạn cuộn)
            if self.y_start < 0:
                self.y_start = 0
            if self.y_start > self.y_end:
                self.y_start = self.y_end
        

    def draw(self, screen, font):
        # Phương thức dùng để vẽ scroll_list

        # set_clip dùng để cắt, chỉ vẽ những gì nằm trong vùng self.view
        # tại đây có sử dụng AI để hỏi về cách dùng set_clip
        screen.set_clip(self.view)

        for i, match in enumerate(self.buttons):
            # toạ độ y để vẽ = vị trí gốc + thứ tự nút * 55 - vị trí cuộn hiện tại
            draw_y = self.ys + i * 55 - self.y_start
            # vị trí toạ độ cho mỗi button
            match.rect.x = self.xs
            match.rect.y = draw_y

            # chỉ vẽ nút nằm trong vùng nhìn thấy được
            # self.ys - 50 thay vì self.ys để nếu đầu của button ra khỏi vùng nhìn thấy nhưng đuôi thì chưa thì vẫn cần vẽ
            # self.ys + self.height là giới hạn ở đuôi (vì draw_y là tính ở đầu nút nên không cần cộng thêm 50 ở phần này)
            if self.ys - 50 < draw_y < self.ys + self.height:
                match.draw(screen, font)
        # khi vẽ xong thì huỷ bỏ chế độ cắt view
        screen.set_clip(None)

    def click(self, pos):
        # Phương thức dùng để xử lý nhấn chuột ở mỗi nút
        if self.view.collidepoint(pos): # kiểm tra chuột nằm ở trong vùng xem được
            for i, match in enumerate(self.buttons): # lấy số thứ tự và nút trong list nút
                if match.click(pos): # nếu nút bị nhấn thì trả về màn chơi tương ứng với số thứ tự đó
                    return self.matches[i]
        return None
    
    def clear(self):
        # Phương thức dùng để xoá danh sách
        self.buttons.clear() # xoá list nút
        self.matches.clear() # xoá list trận đấu
        self.y_start = 0 # đặt lại vị trí cuộn hiện tại
        self.y_end = 0 # đặt lại giới hạn cuộn bằng 0
    


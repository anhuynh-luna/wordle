=================================================================================
TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN - ĐẠI HỌC QUỐC GIA THÀNH PHỐ HỒ CHÍ MINH
KHOA CÔNG NGHỆ THÔNG TIN
MÔN HỌC: CƠ SỞ LẬP TRÌNH CHO TRÍ TUỆ NHÂN TẠO
MÃ LỚP: 25TNT2
---------------------------------------------------------------------------------
ĐỒ ÁN MÔN HỌC: TRÒ CHƠI ĐOÁN TỪ (WORDLE)
=================================================================================

I. Thông tin sinh viên
---------------------------------------------------------------------------------
- Họ và tên: Huỳnh Tường Ân
- MSSV: 25122058

II. Cấu trúc thư mục Resources
---------------------------------------------------------------------------------
1. main.py
    - File chính để điều khiển vòng lặp game (dựa vào thư viện pygame).
    - Xử lý các sự kiện nhập phím và quản lý luồng hoạt động của game.
2. source/
    Chứa các file .py để quản lý mảng riêng biệt, cụ thể:
    - constant.py: Chứa các hằng số về màu sắc và cửa sổ game.
    - data.py: Chứa cấu trúc dữ liệu Linked List phục vụ cho stack undo, redo và
    top 20.
    - draw.py: Chứa các class và các phương thức ở mỗi class phục vụ cho mục
    đích vẽ các đối tượng và quản lý click chuột.
    - logic.py: Chứa các hàm dùng để xử lý logic game (tô màu, lấy từ điển, sắp xếp,
    tìm kiếm, bộ gõ VNI giới hạn).
    - sound.py: Chứa class dùng để quản lý hiệu ứng âm thanh và nhạc nền.
    - storage.py: Chứa các hàm dùng để lưu và load file nhị phân (dùng cho resume
    và top 20).
    - __init__.py: Dùng để định nghĩa thư mục source là một package.
3. assets/
    Chứa các thư mục tài nguyên:
    - dictionary/: Chứa ba file txt gồm English, Vietnamese, Equation để lấy target
    và tra cứu guess.
    - font/: Chứa các file font chữ dùng cho game.
    - sound/: Chứa các file nhạc nền (.mp3) và các file hiệu ứng âm thanh (.wav).

Ngoài ra, khi game vận hành còn có các tập tin sau đây:
4. top20.py
    - Chứa dữ liệu xếp hạng top 20 người chơi đã được mã hoá.
5. resume/
    - Chứa các file resume đã được mã hoá.

III. Luồng hoạt động của game
------------------------------------------------------------------------------
1. Luồng game chính
    - Khởi tạo: Khi mở game, chương trình nạp từ điển vào các list, đọc file 
    top 20 và lưu vào Linked List
    - Cửa sổ Menu: Khi mở game thì cửa sổ đầu tiên là menu, để tạo một username
    mới, nhấn vào "New Game", sẽ chuyển sang cửa sổ Input Name.
    - Cửa sổ Input Name: Người chơi cần nhập tên, nếu tên đạt độ dài hợp lệ và 
    không trùng trong danh sách top 20 và các file resume, nhấn nút "Start" thì
    sẽ chuyển sang cửa sổ Game.
    - Cửa sổ Game: Khi vừa mở cửa sổ Game, game đang trong giai đoạn Setup, người
    chơi có thể tuỳ chỉnh chế độ chơi và chế độ thời gian, Khi nhấn "Done" thì sẽ
    tạo một ván chơi mới, game chuyển sang giai đoạn Playing. Trong ván chơi sẽ có 
    bộ đếm thời gian liên tục (sẽ tạm ngừng khi người chơi mở bảng settings/timescoring
    hoặc qua cửa sổ Resume/History).
        Trong quá trình chơi, người chơi nhập ký tự từ bàn phím, dùng các chức năng
    undo/redo trong cùng một hàng thông qua hai nút bấm trên màn hình. Người chơi có
    thể mở bảng settings để xem nhưng không được chỉnh lại. Nút "New Game" cũng sẽ bị
    khoá khi đang chơi.
        Khi kết thúc ván chơi, nếu chế độ thời gian người chơi chọn khác Vô hạn thì sẽ
    đếm ngược Cooldown, game sang giai đoạn Cooldown, trong giai đoạn này, người chơi
    không thể mở bảng settings hoặc nhấn các nút "New Game", "Undo" và "Redo".
        Nếu hết thời gian Cooldown hoặc chế độ vô hạn, game chuyển sang giai đoạn Ready,
    lúc này người chơi có hai lựa chọn: Nhấn "New Game" để bắt đầu ván mới theo setting
    cũ, hoặc mở bảng settings để chọn lại settings mới (khi vừa đóng bảng settings là
    ngay lập tức tạo ván mới).
        Người chơi có thể nhấn nút "End Game" bất cứ lúc nào nó xuất hiện, khi nhấn, 
    game sẽ điểm dựa trên tổng thời gian chơi chia tổng số ván thắng (nếu số ván thắng
    bằng 0 thì không được tính điểm) để xếp hạng vào top 20 và ngay lập tức về cửa sổ Menu.
    Người chơi không thể vào lại username một khi đã nhấn "End Game".
2. Các luồng phụ khác
    - Bảng top 20: Tại cửa sổ Menu, nếu nhấn vào "Top 20" thì sẽ chuyển sang cửa sổ 
top 20, nếu nhấn "Refresh" thì game sẽ load và đọc lại file top 20, nếu nhấn "Back" thì về
lại cửa sổ Menu.
    - Xem lịch sử trận đấu của một username: Trong cửa sổ Game, nếu nhấn nút Timescoring
(biểu tượng chữ i) thì sẽ mở bảng danh sách trận chơi, các trận chơi sẽ hiển thị bằng một
danh sách cuộn dọc (với chữ hiển thị là target của trận chơi đó), người chơi trượt lên/xuống
bằng hai phím lên/xuống của bàn phím. Nếu người chơi nhấn vào một nút nào, sẽ chuyển qua cửa
sổ History, hiển thị màn chơi đó, nhấn "Back" để quay trở lại, nhấn "Done" để thoát khỏi bảng
Timescoring. Trong toàn bộ quá trình mở bảng Timescoring và qua cửa sổ History, nếu đang chơi,
thời gian sẽ được tạm ngưng.
    - Chức năng resume: Gồm hai phần:
        Thoát từ cửa sổ Game: khi nhấn "Back" hoặc thoát cửa sổ, sẽ chuyển sang cửa sổ Resume
    hiển thị 5 slot để người chơi chọn lưu. Nếu các slot chưa full thì người chơi bắt buộc phải
    chọn slot trống (Available), nếu tất cả slot đã full thì người chơi có thể chọn slot và ghi
    đè lên dữ liệu cũ. Ngoài ra, nếu nhấn "Back", người chơi sẽ quay về cửa sổ Game và tiếp tục,
    nếu nhấn "Cancel" thì sẽ thoát ra khỏi username mà không lưu.
        Vào từ cửa sổ Menu: khi nhấn "Resume", người chơi sẽ vào cửa sổ "Resume_Enter", hiển thị
    5 slot để người chơi chọn, người chơi chỉ có thể chọn slot có dữ liệu (hiển thị bằng username)
    để tiếp tục trò chơi trước đó. Nếu nhấn "Back" thì quay về cửa sổ Menu.
        !Lưu ý: Khi resume game: Nếu game đang chơi thì thời gian của bộ đếm sẽ tạm ngưng, nếu game
    đang cooldown thì bộ đếm cooldown sẽ tiếp tục đếm.
    - Chức năng chỉnh nhạc: Người chơi có thể đổi/tắt nhạc nền bằng cách nhấn vào nút có icon note
    nhạc hiển thị ở tất cả cửa sổ.

IV. Các nguồn tài nguyên sử dụng và chú thích về việc sử dụng AI
---------------------------------------------------------------------------------
1. Các tài nguyên sử dụng
    - Danh sách các từ: các từ tiếng Việt và tiếng Anh được lấy trên Github, các
phương trình được tạo bằng hàm random số nguyên và toán tử sau đó được lưu vào file
txt.
    Đường link của danh sách từ tiếng Anh: 
    https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b
    Đường link của danh sách từ tiếng Việt: 
    https://github.com/duyet/vietnamese-wordlist/blob/master/Viet11K.txt
    - Các file font chữ: hai font Times New Roman được copy trực tiếp từ thư viện font
mặc định của MacOS, font DejaVuSans được tải về từ Github.
    Đường link của font DejaVuSans: 
    https://github.com/prawnpdf/prawn/blob/master/data/fonts/DejaVuSans.ttf
    - Các file âm thanh:
    Các âm thanh sfx (file .wav) được lấy từ bfxr.net.
    Đường link: https://www.bfxr.net
    Các âm thanh bgm (file .mp3) là nhạc nền thuộc quyền sở hữu của Monster Siren/Hypergryph
    và được lấy từ arknights.wiki.gg (dưới dạng file .ogg) sau đó được giảm chất lượng
    và chuyển thành .mp3 qua online-audio-converter để giảm dung lượng.
    Các đường link tải nhạc:
    https://arknights.wiki.gg/wiki/Ideal_City/BGM
    https://arknights.wiki.gg/wiki/The_Masses%27_Travels/BGM
    https://arknights.wiki.gg/wiki/Such_is_the_Joy_of_Our_Reunion/BGM
    https://arknights.wiki.gg/wiki/Lone_Trail/BGM
    Đường link nén nhạc:
    https://online-audio-converter.com/vi/#google_vignette
2. Chú thích về việc sử dụng AI
    2.1. constant.py
    - Dùng AI để hỏi về các chỉ số màu cần thiết.
    2.2. data.py (Không có)
    2.3. draw.py
    - Dùng AI để hỏi về cách căn giữa hình chữ nhật (rect.center).
    - Dùng AI để hỏi về cách tạo và xử lý thanh cuộn (cụ thể về vùng nhìn thấy,
    phương thức set_clip(), cách xử lý kéo lên xuống y_start và y_end).
    2.4. logic.py
    - Dùng AI để hỏi về việc lựa chọn thuật toán sắp xếp để tối ưu thời gian và logic của 
    thuật toán đó.
    2.5. sound.py
    - Dùng AI để hỏi về cách sử dụng pygame.mixer và các phương thức trong nó (gồm
    .Sound, .play và .load).
    - Dùng AI để hỏi mã của icon note nhạc và icon mute.
    2.6. storage.py
    - Dùng AI để hỏi về cách dùng module struct (các lệnh pack và unpack, format).
    - Dùng AI để hỏi về sự mutable giữa bytes và bytearray.
    - Dùng AI để hỏi về cách Python lấp đầy 20 byte, cách tính độ dài bằng calcsize và sự
    cần thiết của deepcopy.
    2.7. main.py
    - Sử dụng AI để tìm hiểu về vòng lặp game và cơ chế FPS của pygame.
    - Sử dụng AI để hỏi về cách tính độ rộng văn bản hiển thị (get_width()).
    - Sử dụng AI để hỏi về các lệnh tạo file và xoá file của module os.
    - Sử dụng AI để hỏi về cách thoát game (pygame.quit() và sys.exit()).
    2.8. Khác
    - Dùng AI để tìm kiếm nguồn sfx, website để nén nhạc và font chữ.
    - Dùng AI để tham khảo về cách tổ chức cây thư mục.
3. Các tài liệu tham khảo
    - Pygame Documentation: https://www.pygame.org/docs/

V. Các lưu ý cho người chấm
---------------------------------------------------------------------------------
- Cài đặt thư viện pygame theo hướng dẫn sau:
    https://www.pygame.org/wiki/GettingStarted
- Giữ nguyên cấu trúc cây thư mục Resources và chạy file main.py.
- Trong file main.py khoảng dòng 850 có ba dòng comment đánh dấu "For testing", 
nếu người chấm muốn test các tính năng chấm điểm khi đúng có thể tắt comment ở 
ba dòng này để target hiển thị trên màn hình.

VI. Bảng tự đánh giá các chức năng hiện có
---------------------------------------------------------------------------------
| STT | Chức năng                       | Đánh giá  | Ghi chú
|-----|---------------------------------|-----------|----------------------------
| 1   | Giao diện đồ hoạ                | 70%       | Đạt ở mức đủ, nhưng chưa được
|     |                                 |           | sáng tạo, bắt mắt.
| 2   | Logic tô màu                    | 100%      | Đúng luật tô màu.
| 3   | Chế độ tiếng Anh                | 100%      | Hoàn thiện.
| 4   | Chế độ tiếng Việt               | 80%       | Chưa xử lý các từ có dấu cách,
|     |                                 |           | bộ gõ VNI chỉ giới hạn ký tự trước.
| 5   | Chế độ phương trình             | 80%       | Phương trình ngắn nên cấu trúc
|     |                                 |           | đơn giản.
| 6   | Bảng top 20                     | 100%      | Hoàn thiện đầy đủ cơ chế.
| 7   | Tính năng Resume                | 100%      | Hoàn thiện đầy đủ cơ chế, có lưu
|     |                                 |           | file nhị phân được mã hoá.
| 8   | Nhập tên người chơi             | 90%       | Giới hạn ký tự nhỏ.
| 9   | Các tính năng Undo/Redo         | 100%      | Hoàn thiện đầy đủ cơ chế.
| 10  | Tính năng xem lịch sử           | 100%      | Hoàn thiện đầy đủ cơ chế.
| 11  | Tính năng bảng settings         | 70%       | Chưa cấu hình được nhiều thứ,
|     |                                 |           | chưa có bàn phím ảo.
| 12  | Tính năng End Game và tính điểm | 90%       | Logic tính điểm và xếp hạng tốt,
|     |                                 |           | nhưng chưa có thông báo khi nhấn.
| 13  | Logic tính và hiển thị thời gian| 100%      | Hoàn thiện đầy đủ cơ chế.
| 14  | Tính năng nhạc nền              | 100%      | Vận hành tốt.

---------------------------------------------------------------------------------
Người thực hiện: Huỳnh Tường Ân


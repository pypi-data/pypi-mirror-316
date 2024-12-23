import cv2
import time
import os
import shutil
import curses
from datetime import datetime
from . import camera_module as camera
from . import file_management as file_manager
from .qr_scanner import detect_and_track_qr
from . import sound_module as sound
from . import overlay_module as overlay
from . import motion_detector
from . import cache_cleaner
from . import display_tracking_id_on_frame

def detect_motion(cap, min_area=500):
    """
    Phát hiện chuyển động bằng cách so sánh sự thay đổi giữa khung hình hiện tại và khung hình trước.
    """
    ret, frame1 = cap.read()
    if not ret:
        return False

    ret, frame2 = cap.read()
    if not ret:
        return False

    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)
    gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

    diff = cv2.absdiff(gray1, gray2)

    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > min_area:
            return True

    return False

# def start_packing_process(data_dir, cache_dir):
#     cap = camera.init_camera()
#     if cap is None:
#         # print("Không tìm thấy camera.")
#         return  # Không tìm thấy camera

#     recording = False
#     current_tracking_id = None
#     writer = None
#     last_motion_time = None

#     # Cấu hình video ghi lại
#     video_resolution = (1920, 1080)  # Độ phân giải HD
#     original_fps = 60  # FPS gốc của camera (có thể kiểm tra bằng camera thực tế)
#     speed_up_factor = 0.4  # Tăng tốc 1.4 lần (nhanh hơn 0.4 lần)
#     adjusted_fps = int(original_fps * speed_up_factor)  # FPS ghi video sau khi tăng tốc
#     codec = cv2.VideoWriter_fourcc(*'mp4v')  # Codec cho MP4

#     try:
#         while True:
#             # Đọc frame từ camera
#             ret, frame = camera.read_frame(cap)
#             if not ret:
#                 break

#             # Hiển thị khung hình realtime
#             frame_with_timestamp = overlay.overlay_datetime(frame.copy())  # Gắn timestamp vào khung hình

#             # Phát hiện và theo dõi mã QR
#             label_text, qr_roi = detect_and_track_qr(frame_with_timestamp)

#             # Nếu phát hiện mã QR và dữ liệu hợp lệ
#             if label_text:
#                 if current_tracking_id != label_text:
#                     print(f"Quét thành công đơn hàng: {label_text}")

#                     # Kết thúc ghi hình video hiện tại (nếu đang ghi)
#                     if writer:
#                         writer.release()
#                         recording = False

#                     # Tạo thư mục lưu trữ
#                     tracking_dir = file_manager.create_tracking_directory(data_dir, label_text)

#                     # Lưu ảnh với tên mã vận đơn
#                     image_filename = os.path.join(tracking_dir, f"{label_text}.jpg")
#                     frame_with_timestamp = display_tracking_id_on_frame.display_tracking_id_on_frame(
#                         frame_with_timestamp, label_text
#                     )
#                     cv2.imwrite(image_filename, frame_with_timestamp)

#                     # Tạo file video để ghi lại quá trình
#                     video_filename = os.path.join(tracking_dir, f"{label_text}.mp4")
#                     writer = cv2.VideoWriter(video_filename, codec, adjusted_fps, video_resolution)

#                     # Bắt đầu ghi hình video mới
#                     recording = True
#                     current_tracking_id = label_text
#                     last_motion_time = time.time()
#                     sound.play_success_sound()

#             # Hiển thị mã vận đơn nếu đã quét thành công
#             if current_tracking_id:
#                 frame_with_timestamp = display_tracking_id_on_frame.display_tracking_id_on_frame(
#                     frame_with_timestamp, current_tracking_id
#                 )

#             # Ghi lại video khi đang ghi
#             if recording:
#                 # Resize frame sang độ phân giải HD để ghi video
#                 frame_for_recording = cv2.resize(frame, video_resolution)

#                 # Gắn timestamp và mã vận đơn vào frame ghi
#                 frame_for_recording = overlay.overlay_datetime(frame_for_recording)
#                 frame_for_recording = display_tracking_id_on_frame.display_tracking_id_on_frame(
#                     frame_for_recording, current_tracking_id
#                 )

#                 writer.write(frame_for_recording)  # Ghi khung hình vào video

#                 # Kiểm tra phát hiện chuyển động
#                 if motion_detector.detect_motion(cap):
#                     last_motion_time = time.time()
#                 elif last_motion_time is not None and time.time() - last_motion_time > 45:
#                     print("\nKhông phát hiện chuyển động trong 45s, dừng ghi hình.")
#                     writer.release()
#                     recording = False
#                     break

#             # Hiển thị khung hình realtime (không resize để tiết kiệm hiệu năng)
#             cv2.imshow('E-commerce Packing Process', frame_with_timestamp)
#             if cv2.waitKey(1) & 0xFF == 27:  # Nhấn ESC để thoát
#                 break

#     finally:
#         if writer:
#             writer.release()
#         camera.release_camera(cap)
#         cv2.destroyAllWindows()
#         cache_cleaner.clear_cache(cache_dir)
#         if os.path.exists(cache_dir):
#             shutil.rmtree(cache_dir)


import threading
import queue
from datetime import datetime
import curses
import cv2
import os
import time
import shutil
from collections import deque  # Thêm deque để quản lý danh sách mã đơn hàng

def start_packing_process(data_dir, cache_dir):
    cap = camera.init_camera()
    if cap is None:
        return  # Không tìm thấy camera

    recording = False
    current_tracking_id = None
    writer = None
    last_motion_time = None
    scanned_orders = deque(maxlen=10)  # Dùng deque với kích thước tối đa là 10
    scanned_orders_queue = queue.Queue()
    display_queue = queue.Queue()  # Hàng đợi để quản lý mã vận đơn hiển thị trên camera
    stop_event = threading.Event()

    orders_before_14 = 0
    orders_after_14 = 0

    video_resolution = (1920, 1080)
    original_fps = 60
    speed_up_factor = 0.4
    adjusted_fps = int(original_fps * speed_up_factor)
    codec = cv2.VideoWriter_fourcc(*'mp4v')

    def update_ui(stdscr):
        curses.curs_set(1)  # Hiển thị con trỏ khi nhập liệu
        stdscr.nodelay(True)
        stdscr.timeout(100)

        def draw_frame(user_input):
            stdscr.clear()
            max_y, max_x = stdscr.getmaxyx()

            # Vẽ tiêu đề chương trình
            title = "E-COMMERCE PACKING PROCESS"
            stdscr.addstr(1, (max_x - len(title)) // 2, title, curses.A_BOLD | curses.A_UNDERLINE)

            # Hiển thị tổng số đơn hàng đã quét trước và sau 14 giờ
            stdscr.addstr(3, 2, f"Orders before 14:00: {orders_before_14}")
            stdscr.addstr(4, 2, f"Orders after 14:00: {orders_after_14}")

            # Vẽ khung danh sách mã vận đơn
            list_title = "Scanned Orders"
            box_width = max(50, len(max(scanned_orders, key=len, default="")) + 4)
            box_start_x = (max_x - box_width) // 2
            stdscr.addstr(6, box_start_x, f"+{'-' * (box_width - 2)}+")
            stdscr.addstr(7, box_start_x, f"| {list_title.center(box_width - 4)} |")
            stdscr.addstr(8, box_start_x, f"+{'-' * (box_width - 2)}+")

            # Hiển thị danh sách mã vận đơn (giới hạn 10 dòng)
            y_offset = 9
            for idx in range(10):  # Giới hạn số lượng mã vận đơn hiển thị là 10
                if idx < len(scanned_orders):
                    stdscr.addstr(y_offset + idx, box_start_x, f"| {scanned_orders[idx].ljust(box_width - 4)} |")
                else:
                    stdscr.addstr(y_offset + idx, box_start_x, f"| {' '.ljust(box_width - 4)} |")
            stdscr.addstr(y_offset + 10, box_start_x, f"+{'-' * (box_width - 2)}+")

            # Vẽ khung nhập liệu
            input_start_y = y_offset + 11
            stdscr.addstr(input_start_y, 2, "Enter Tracking ID: " + user_input)
            stdscr.refresh()

        user_input = ""
        while not stop_event.is_set():
            draw_frame(user_input)
            try:
                key = stdscr.getch()
                if key == 10:  # Enter key
                    if user_input.strip():
                        scanned_orders_queue.put(user_input.strip())
                        user_input = ""
                elif key in range(32, 127):  # Printable characters
                    user_input += chr(key)
                elif key in (curses.KEY_BACKSPACE, 127):  # Backspace key
                    user_input = user_input[:-1]
            except Exception:
                pass

    ui_thread = threading.Thread(target=lambda: curses.wrapper(update_ui))
    ui_thread.daemon = True
    ui_thread.start()

    try:
        while not stop_event.is_set():
            ret, frame = camera.read_frame(cap)
            if not ret:
                break

            frame_with_timestamp = overlay.overlay_datetime(frame.copy())
            label_text, qr_roi = detect_and_track_qr(frame_with_timestamp)

            if label_text and label_text not in scanned_orders:
                print(f"Quét thành công đơn hàng: {label_text}")
                scanned_orders.append(label_text)  # Dùng append để thêm mã mới vào deque
                scanned_orders_queue.put(label_text)  # Thêm vào hàng đợi

                # Tăng bộ đếm trước hoặc sau 14 giờ
                current_time = datetime.now().time()
                if current_time.hour < 14:
                    orders_before_14 += 1
                else:
                    orders_after_14 += 1

                if writer:
                    writer.release()
                    recording = False
                tracking_dir = file_manager.create_tracking_directory(data_dir, label_text)
                image_filename = os.path.join(tracking_dir, f"{label_text}.jpg")
                frame_with_timestamp = display_tracking_id_on_frame.display_tracking_id_on_frame(
                    frame_with_timestamp, label_text
                )
                cv2.imwrite(image_filename, frame_with_timestamp)
                video_filename = os.path.join(tracking_dir, f"{label_text}.mp4")
                writer = cv2.VideoWriter(video_filename, codec, adjusted_fps, video_resolution)
                recording = True
                current_tracking_id = label_text
                last_motion_time = time.time()
                sound.play_success_sound()

                # Thêm mã đơn vào hàng đợi hiển thị trên màn hình camera
                if not display_queue.empty():
                    display_queue.queue.clear()
                display_queue.put(label_text)

            if recording:
                frame_for_recording = cv2.resize(frame, video_resolution)
                frame_for_recording = overlay.overlay_datetime(frame_for_recording)
                frame_for_recording = display_tracking_id_on_frame.display_tracking_id_on_frame(
                    frame_for_recording, current_tracking_id
                )
                writer.write(frame_for_recording)
                if motion_detector.detect_motion(cap):
                    last_motion_time = time.time()
                elif last_motion_time and time.time() - last_motion_time > 45:
                    writer.release()
                    recording = False
                    break

            try:
                manual_tracking_id = scanned_orders_queue.get_nowait()
                if manual_tracking_id and manual_tracking_id not in scanned_orders:
                    print(f"Thêm thủ công đơn hàng: {manual_tracking_id}")
                    scanned_orders.append(manual_tracking_id)  # Thêm mã vận đơn thủ công vào deque
                    current_time = datetime.now().time()
                    if current_time.hour < 14:
                        orders_before_14 += 1
                    else:
                        orders_after_14 += 1

                    tracking_dir = file_manager.create_tracking_directory(data_dir, manual_tracking_id)
                    image_filename = os.path.join(tracking_dir, f"{manual_tracking_id}.jpg")
                    frame_with_timestamp = display_tracking_id_on_frame.display_tracking_id_on_frame(
                        frame_with_timestamp, manual_tracking_id
                    )
                    cv2.imwrite(image_filename, frame_with_timestamp)
                    video_filename = os.path.join(tracking_dir, f"{manual_tracking_id}.mp4")
                    writer = cv2.VideoWriter(video_filename, codec, adjusted_fps, video_resolution)
                    recording = True
                    last_motion_time = time.time()
                    sound.play_success_sound()

                    # Thêm mã đơn vào hàng đợi hiển thị trên màn hình camera
                    if not display_queue.empty():
                        display_queue.queue.clear()
                    display_queue.put(manual_tracking_id)
            except queue.Empty:
                pass

            if not display_queue.empty():
                current_display_text = display_queue.queue[0]
                frame_with_display = display_tracking_id_on_frame.display_tracking_id_on_frame(
                    frame_with_timestamp, current_display_text
                )
            else:
                frame_with_display = frame_with_timestamp

            cv2.imshow('E-commerce Packing Process', frame_with_display)
            if cv2.waitKey(1) & 0xFF == 27:  # ESC
                stop_event.set()
                break

    finally:
        if writer:
            writer.release()
        camera.release_camera(cap)
        cv2.destroyAllWindows()
        cache_cleaner.clear_cache(cache_dir)
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)

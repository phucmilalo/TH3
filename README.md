# Thực hành IoT với giao thức CoAP

## Mục lục

- [a. Thông tin sinh viên thực hiện](#a-thông-tin-sinh-viên-thực-hiện)
- [b. Phiên bản Python và thư viện](#b-phiên-bản-python-và-thư-viện)
- [c. Cài đặt môi trường](#c-cài-đặt-môi-trường)
- [d. Cách chạy](#d-cách-chạy)
- [e. IP, cổng và URI](#e-ip-cổng-và-uri)
- [f. Kết quả đạt được](#f-kết-quả-đạt-được)
- [g. Log minh chứng](#g-log-minh-chứng)

## a. Thông tin sinh viên thực hiện

Họ và tên: Nguyễn Văn Phúc  
Mã sinh viên: B23DCCN957

## b. Phiên bản Python và thư viện

Đã xác nhận trong môi trường chạy:

```text
Python 3.12.10
Name: aiocoap
Version: 0.4.17
```

Chương trình dùng `aiocoap` và thư viện chuẩn Python. Phiên bản thư viện được ghim trong [requirements.txt](requirements.txt).

## c. Cài đặt môi trường

Mở terminal tại thư mục chứa dự án, sau đó chạy `cd TH1_EX3`.

Windows PowerShell:

```powershell
cd TH1_EX3
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Linux hoặc macOS:

```sh
cd TH1_EX3
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## d. Cách chạy

Mở terminal trong thư mục `TH1_EX3`. Luôn chạy server trước. Các chương trình nhận tham số `--host`; mặc định là `127.0.0.1`.

### Bài 1

Hai terminal:

```powershell
# Terminal 1
python bai1/coap_server_bai1.py
# Terminal 2
python bai1/coap_client_bai1.py --count 2 --test-missing
```

`--count 2` gửi hai POST; `--test-missing` thử URI không tồn tại để nhận `4.04`.

### Bài 2

Hai terminal:

```powershell
# Terminal 1
python bai2/sensor_server_bai2.py
# Terminal 2
python bai2/monitor_client_bai2.py
```

### Bài 3

Terminal 1 chạy server, Terminal 2 chạy monitor, Terminal 3 chạy controller. Để thử nhiều observer, mở terminal khác và chạy thêm monitor thứ hai.

```powershell
# Terminal 1
python bai3/light_server_bai3.py
# Terminal 2
python bai3/light_monitor_bai3.py
# Terminal 3
python bai3/light_controller_bai3.py
# Terminal khác, observer thứ hai
python bai3/light_monitor_bai3.py
```

Trong controller, nhập `ON`, `ON` lần nữa, `STATUS`, `OFF`, một lệnh sai như `BOGUS`, rồi `EXIT`. Controller từ chối lệnh sai tại chỗ. Payload sai được gửi bằng client thử nghiệm tạm thời ngoài dự án để kiểm tra phản hồi `4.00`. Dừng server và monitor bằng Ctrl+C; controller nhận `EXIT` hoặc Ctrl+C.

## e. IP, cổng và URI

Mặc định là `127.0.0.1`, UDP cổng `5683`.

| Bài | URI | Phương thức | Content-Format | Mô tả |
|---|---|---|---|---|
| 1 | `coap://127.0.0.1:5683/iot/lab/message` | GET, POST | Không đặt | GET trả lời chào hoặc POST gần nhất; POST nhận thông điệp |
| 2 | `coap://127.0.0.1:5683/iot/lab/sensor01/data` | GET | application/json | Dữ liệu nhiệt độ, độ ẩm và mã thiết bị |
| 3 | `coap://127.0.0.1:5683/iot/lab/light01/status` | GET, PUT, GET Observe | application/json | Đọc trạng thái, điều khiển đèn và nhận cập nhật Observe |

Chạy trên hai máy: khởi động server với `--host 0.0.0.0`, rồi truyền IP máy server cho client, ví dụ `python bai1/coap_client_bai1.py --host 192.168.1.10`. Mở firewall cho UDP cổng `5683` trên máy server.

## f. Kết quả đạt được

### Bài 1 (5 điểm)

- [x] Khởi tạo và chạy Server. [Log server](evidence/bai1_server.log).
- [x] Client gửi GET và POST. [Log client](evidence/bai1_client.log).
- [x] Server xử lý đúng từng phương thức. [Log server](evidence/bai1_server.log).
- [x] Payload và phản hồi hiển thị chính xác. [Log client](evidence/bai1_client.log).
- [x] Chạy ổn định, xử lý lỗi kết nối cơ bản khi server tắt. [Log khi server tắt](evidence/bai1_timeout.log).

### Bài 2 (6 điểm)

- [x] Server cung cấp dữ liệu qua URI. [Log server](evidence/bai2_server.log) và [log monitor](evidence/bai2_regression_monitor.log).
- [x] Server cập nhật định kỳ 3 giây. [Log monitor](evidence/bai2_regression_monitor.log) có các lần đọc cách nhau 3 giây.
- [x] Payload JSON đúng định dạng; client GET và phân tích dữ liệu. [Log monitor](evidence/bai2_regression_monitor.log).
- [x] Cảnh báo đúng điều kiện nhiệt độ trên 35°C và độ ẩm dưới 40%. [Log monitor](evidence/bai2_regression_monitor.log).
- [x] Xử lý server không phản hồi và thử lại. [Log khi server tắt](evidence/bai2_server_off_monitor.log).

### Bài 3 (7 điểm)

- [x] Server quản lý tài nguyên thiết bị. [Log server](evidence/bai3_server.log).
- [x] Client gửi GET và PUT. [Log phiên controller](evidence/bai3_regression_controller_session.log).
- [x] Đèn đổi trạng thái đúng lệnh. [Log server](evidence/bai3_server.log).
- [x] Monitor đăng ký Observe thành công. [Monitor 1](evidence/bai3_monitor1.log) và [monitor 2](evidence/bai3_monitor2.log).
- [x] Server gửi thông báo khi trạng thái đổi; lệnh ON lặp lại không tạo cập nhật. [Log server](evidence/bai3_server.log) và hai log monitor ở trên.
- [x] Hỗ trợ đồng thời điều khiển và giám sát. [Controller](evidence/bai3_regression_controller_session.log), [monitor 1](evidence/bai3_monitor1.log), [monitor 2](evidence/bai3_monitor2.log).
- [x] Payload sai trả `4.00`; xử lý lỗi giao tiếp cơ bản. [Kiểm tra payload](evidence/bai3_payload_validation.log), [controller khi server tắt](evidence/bai3_controller_server_off.log), [monitor khi server tắt](evidence/bai3_monitor_server_off.log).

### Mở rộng đã làm

Monitoring Client Bài 3 dùng CoAP Observe thật (`observe=0`, vòng lặp `async for`), không dùng GET định kỳ. Đã xác minh trong `light_monitor_bai3.py`, hàm `main`.

## g. Log minh chứng

Đây là các log của lần chạy thật. Các đoạn rút gọn có liên kết tới file đầy đủ trong `evidence/`.

### Bài 1

#### Server

(rút gọn, đầy đủ ở [evidence/bai1_server.log](evidence/bai1_server.log))

```text
CoAP Server started on port 5683
GET request received: /iot/lab/message
POST request received:
Payload: Xin chao tu CoAP Client - B23DCCN957 - Nguyen Van Phuc
Time: 00:52:23
```

#### Client: GET, hai POST và URI sai

(rút gọn, đầy đủ ở [evidence/bai1_client.log](evidence/bai1_client.log))

```text
Sending GET request...
URI: coap://127.0.0.1:5683/iot/lab/message
Response:
Code: 2.05 Content
Payload: Xin chao tu CoAP Server
Sending POST request...
Payload: Xin chao tu CoAP Client - B23DCCN957 - Nguyen Van Phuc
Response:
Code: 2.04 Changed
Payload: Server da nhan thong diep
Missing URI Code: 4.04 Not Found
```

#### Client khi server tắt

(rút gọn, đầy đủ ở [evidence/bai1_timeout.log](evidence/bai1_timeout.log))

```text
Sending GET request...
URI: coap://127.0.0.1:5683/iot/lab/message
Loi ket noi/timeout CoAP: Network error: NetworkError
```

### Bài 2

#### Server

(rút gọn, đầy đủ ở [evidence/bai2_server.log](evidence/bai2_server.log))

```text
Sensor CoAP Server started: sensor01
```

#### Monitor ngẫu nhiên bình thường và cảnh báo

(rút gọn, đầy đủ ở [evidence/bai2_regression_monitor.log](evidence/bai2_regression_monitor.log))

Log này được ghi ở chế độ ngẫu nhiên mặc định, không dùng chế độ ép ngưỡng.

```text
[23:38:21] Received sensor data
Device: sensor01
Temperature: 30.5 C
Humidity: 40.7 %
Trang thai: Binh thuong
------------------------------
[23:38:27] Received sensor data
Device: sensor01
Temperature: 38.1 C
Humidity: 74.0 %
CANH BAO: Nhiet do cao
------------------------------
[23:38:39] Received sensor data
Device: sensor01
Temperature: 30.2 C
Humidity: 34.0 %
CANH BAO: Do am thap
------------------------------
```

#### Monitor khi server tắt

(rút gọn, đầy đủ ở [evidence/bai2_server_off_monitor.log](evidence/bai2_server_off_monitor.log))

```text
Loi doc du lieu: Network error: NetworkError; thu lai sau 3 giay
```

### Bài 3

#### Server

(rút gọn, đầy đủ ở [evidence/bai3_server.log](evidence/bai3_server.log))

```text
CoAP Smart Light Server started...
Resource: /iot/lab/light01/status
New Observe registration received
New Observe registration received
PUT request received:
Device: light01
Command: ON
Light state changed: OFF -> ON
Notify observers: ON
PUT request received:
Device: light01
Command: ON
PUT request received:
Device: light01
Command: OFF
Light state changed: ON -> OFF
Notify observers: OFF
```

#### Controller: ON, ON lặp, STATUS, OFF, lệnh sai và EXIT

(rút gọn, đầy đủ ở [evidence/bai3_regression_controller_session.log](evidence/bai3_regression_controller_session.log))

Đầu vào được gửi theo thứ tự: `ON`, `ON`, `STATUS`, `OFF`, `BOGUS`, `EXIT`.

```text
Commands supplied to controller stdin: ON, ON, STATUS, OFF, BOGUS, EXIT
Nhap lenh (ON/OFF/STATUS/EXIT): Sending PUT request...
Response Code: 2.04 Changed
Da bat den light01
Nhap lenh (ON/OFF/STATUS/EXIT): Sending PUT request...
Response Code: 2.04 Changed
Da bat den light01
Nhap lenh (ON/OFF/STATUS/EXIT): Sending GET request...
Response:
{"device_id": "light01", "status": "ON"}
Nhap lenh (ON/OFF/STATUS/EXIT): Sending PUT request...
Response Code: 2.04 Changed
Da tat den light01
Nhap lenh (ON/OFF/STATUS/EXIT): Lenh khong hop le. Hay nhap ON, OFF, STATUS hoac EXIT.
```

#### Monitor 1 và Monitor 2

(rút gọn, đầy đủ ở [evidence/bai3_monitor1.log](evidence/bai3_monitor1.log) và [evidence/bai3_monitor2.log](evidence/bai3_monitor2.log))

```text
Registering CoAP Observe...
Observe registration successful
[00:52:06] Initial State
Device: light01
Status: OFF
[00:52:09] State Updated
Device: light01
Status: ON
[00:52:09] State Updated
Device: light01
Status: OFF
```

Không có cập nhật trạng thái cho lệnh ON bị lặp.

#### Payload sai trả 4.00

(rút gọn, đầy đủ ở [evidence/bai3_payload_validation.log](evidence/bai3_payload_validation.log))

```text
Response Code: 4.00 Bad Request
Payload: Payload khong phai JSON hop le
Response Code: 4.00 Bad Request
Payload: Thieu truong device_id hoac command
Response Code: 4.00 Bad Request
Payload: device_id khong hop le
Response Code: 4.00 Bad Request
Payload: command phai la ON hoac OFF
Final State: {"device_id": "light01", "status": "OFF"}
```

#### Lỗi giao tiếp khi server tắt

(rút gọn, đầy đủ ở [evidence/bai3_controller_server_off.log](evidence/bai3_controller_server_off.log) và [evidence/bai3_monitor_server_off.log](evidence/bai3_monitor_server_off.log))

```text
Loi ket noi/timeout CoAP: Network error: NetworkError
Observe loi/mat ket noi: Network error: NetworkError; dang thu dang ky lai
```

Monitor thử đăng ký lại sau lỗi mạng; log không có traceback.

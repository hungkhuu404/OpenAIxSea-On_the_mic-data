# Cổng tra cứu công khai cho TPBVSK — kiểm tra ngày 21/10/2026

Kiểm từ máy ở Việt Nam (mạng VN). Chỉ dùng chức năng công khai: không đăng nhập, không vượt captcha. Tổng cộng khoảng 260 request, cách nhau ≥1,2 giây; log ở `_raw/_requests.log`.

> **Công dụng đã công bố có tra công khai được không: KHÔNG.**
> Bằng chứng: API tra cứu công khai của cổng mới (`/api/attp/tra-cuu-giay-phep/*`) chỉ trả về các trường: tên SP, chủ thể pháp lý, cơ sở SX, số giấy, ngày cấp, trạng thái và vài trường thu hồi. Không có công dụng, thành phần hay nội dung quảng cáo được xác nhận. Trang `/tra-cuu-ho-so` (bundle `chunk-7YACEOZS.js`) chỉ hiển thị danh sách, không có màn chi tiết hay nút tải file; nút duy nhất trên mỗi dòng là "Gửi phản ánh kiến nghị". Trường `fileDinhKemHoSo` rỗng ở tất cả 66+ bản ghi đã xem. Cổng cũ congbosanpham và xacnhanquangcao không truy cập được. Ngoại lệ không áp dụng cho TPBVSK: tra cứu *mã định danh UDI* của sản phẩm **tự công bố** có trả `moTaSanPham.thanhPhan` (thành phần), nhưng không có công dụng, và TPBVSK không thuộc diện tự công bố.

---

## 1. Cổng thông tin ATTP quốc gia — `https://antoanthucpham.moh.gov.vn/`

- **Truy cập:** được (HTTP 200). Frontend dùng Angular SSR (Express). API nằm ở host riêng **`https://gateway-api-antoanthucpham.moh.gov.vn`** (Kestrel/ABP), lấy từ `chunk-OICHJF64.js` (`apis.default.url`). Gọi `/api/...` trên host frontend thì chỉ nhận lại HTML của SPA.
- **Lưu ý kỹ thuật:** Python `requests` (OpenSSL) lỗi `DH_KEY_TOO_SMALL` khi kết nối host này. PowerShell `Invoke-WebRequest` (Windows SChannel) thì kết nối bình thường. Tôi **không** hạ mức bảo mật TLS. Muốn gọi từ Python/Node thì phải dùng một TLS stack chấp nhận được tham số DH của server.
- **Điều khoản sử dụng** (`/dieu-khoan-su-dung`, trích từ `chunk-KHZL4OPD.js`): *"Bạn có thể tra cứu nhiều thông tin trên Cổng mà không cần đăng nhập"*. Phần tra cứu tự do gồm *"Sản phẩm đã được cấp phép công bố, xác nhận quảng cáo"* và *"Sản phẩm đã tự công bố và mã số nhận diện sản phẩm"*. Khi dùng lại thông tin thì *"cần ghi rõ nguồn là Cổng thông tin An toàn thực phẩm Quốc gia"* và *"Không được chỉnh sửa, xuyên tạc nội dung"*. Cổng tự nêu giới hạn: *"Thông tin trên Cổng được … cập nhật định kỳ nên có thể có độ trễ nhất định so với thực tế."* Cổng không có robots.txt (trả về trang SPA).
- **Giới hạn quan sát được:** không captcha, không cần token. Khoảng 70 request vào gateway ở tốc độ 1 request/1,2 giây không bị chặn. Tôi có gửi header `Origin`/`Referer` của cổng nhưng không thử gọi khi thiếu chúng.

### 1.1 Endpoint công khai do trang `/tra-cuu-ho-so` gọi (mã nguồn `chunk-EIKMPEEC.js`)

Tất cả là `GET`. Tham số chung: `skipCount`, `maxResultCount`, `sanPham` (tên SP, khớp chuỗi con, không phân biệt hoa thường), `tenDoanhNghiep`, `soGiayPhep` (**khớp chuỗi con**: `838/2024` khớp cả 1838, 2838…), `tenCoSoSanXuat`, `nhomSanPhamId`, `xaPhuongId`, `ngayCapTu`, `ngayCapDen` (ISO-8601).

| Endpoint (trên gateway) | Nội dung | totalCount 21/10 |
|---|---|---|
| `/api/attp/tra-cuu-giay-phep/giay-tiep-nhan-cong-bo` | Giấy tiếp nhận đăng ký bản công bố (ĐKSP) | 68.688 |
| `/api/attp/tra-cuu-giay-phep/giay-xac-nhan-quang-cao` | Giấy xác nhận nội dung quảng cáo (GXNQC) | 14.738 (trang thống kê `csdl` ghi 11.841) |
| `/api/attp/tra-cuu-giay-phep/giay-chung-nhan-co-so` | Giấy chứng nhận cơ sở đủ điều kiện | – |
| `/api/nghiep-vu/ho-so-tu-cong-bo/portal/giay-tiep-nhan-cong-bo` | Hồ sơ tự công bố | – |
| `/api/nghiep-vu/ho-so-tu-cong-bo/portal/tra-cuu/ma-dinh-danh?maUDI=` | Tra mã UDI (tự công bố) | – |
| `/api/attp/tra-cuu-giay-phep/filter-dropdowns` | 34 tỉnh, 3.321 xã, 42 nhóm SP (gồm "Thực phẩm bảo vệ sức khỏe") | – |
| `/api/portal/public/csdl` | Thống kê số lượng theo năm | – |

**Trường trả về của ĐKSP:** `id, tenSanPham, chuThePhapLy, tenCoSoSanXuat, soGiayPhep, ngayCap, ngayCongBo, trangThai, choXacNhanThuHoi, daThuHoi, ngayThuHoi, userThuHoiId, tenUserThuHoi, loaiNguoiThuHoi, thuHoiTepId, danhSachTuocQuyen[], fileDinhKemHoSo[]`.
**Trường của GXNQC:** như trên, thêm `soGiayTiepNhanCongBo` (số ĐKSP liên kết) và `soBanCongBo`.

Ví dụ rút gọn (GXNQC, `sanPham=Betics`):
```json
{"totalCount":4,"items":[{"tenSanPham":"Thực phẩm bảo vệ sức khoẻ DK-BETICS GOLD","chuThePhapLy":"CÔNG TY CỔ PHẦN DƯỢC KHOA",
 "soGiayPhep":"3433/2020/XNQC-ATTP","soGiayTiepNhanCongBo":"7615/2020/ĐKSP","soBanCongBo":"4/2020/0101326329-DKCB",
 "ngayCap":"2020-10-23T00:00:00","trangThai":0,"daThuHoi":false,"ngayThuHoi":null,"danhSachTuocQuyen":[],"fileDinhKemHoSo":[]}]}
```

### 1.2 Phát hiện quan trọng cho Lớp 1
1. **Không có công dụng, thành phần hay nội dung QC đã xác nhận.** Không có file đính kèm tải công khai. Trang công khai không gọi endpoint chi tiết nào. Endpoint chi tiết hoặc tải file của module tự công bố (`/portal/{id}`, `/tai-lieu/{id}/download`, `/xuat-pdf`) chỉ được gọi từ các route có guard đăng nhập. Tôi **không** thử gọi chúng.
2. **Dữ liệu dừng ở 2024.** Lọc `ngayCapTu=2024-09-02` trả 0 bản ghi; ngày cấp mới nhất là 2024-09-01 (ĐKSP) và 2024-08-31 (GXNQC). Endpoint `csdl` ghi rõ `giayTiepNhanCongBo.years: {2025: 0, 2026: 0}` và `giayXacNhanQuangCao.years: {2025: 0, 2026: 0}`. Trong khi đó vẫn có ĐKSP cấp năm 2025: QĐ 125/QĐ-ATTP thu hồi `856/2025/ĐKSP`, QĐ 126 thu hồi `92/2025/ĐKSP`. Nghĩa là giấy cấp từ 09/2024 trở đi **không** có trên cổng.
3. **Trạng thái thu hồi không đáng tin.** `3984/2019/ĐKSP` (PROJEL GLUTATHIONE WHITE) đã bị thu hồi theo QĐ 136/QĐ-ATTP ngày 17/06/2026, nhưng API vẫn trả `trangThai:0` (UI hiển thị "Còn hiệu lực") và `daThuHoi:false`. Không thấy bản ghi nào có `daThuHoi=true`. Muốn kiểm R "bị thu hồi?" thì phải dùng `recalls.jsonl`.
4. **Số giấy phải so khớp cả hậu tố.** `3433/2020/XNQC-ATTP` là GXNQC của DK-BETICS GOLD, còn `3433/2020/ĐKSP` là ĐKSP của VIMIRADS MULTIVITAMIN (DANSON GROUP).
5. Văn bản (`/api/portal/public/docs`) và tin tức (`/api/portal/public/article`): không có quyết định thu hồi. Chuyên mục "Cảnh báo về an toàn thực phẩm" chỉ có vài bài (năm 2026).

### 1.3 Kết quả tra 3 SKU (chi tiết trong `sku_lookups.json`)
| SKU | ĐKSP | GXNQC | Ghi chú |
|---|---|---|---|
| DK-Betics Gold | **7615/2020/ĐKSP** (13/08/2020), CTCP Dược Khoa | **3433/2020/XNQC-ATTP** (23/10/2020) | Không có trong recalls |
| Non Alco | **4993/2024/ĐKSP** (19/06/2024), CTCP Dược phẩm VITATH | **không tìm thấy** (API + danh sách VFA đến 15/05/2025) | GXNQC sau 15/05/2025: không có nguồn công khai |
| Slimaura Care x3 | "Slimaura": **0 kết quả** | 0 | Tên gần nhất: **SLIMMING CARE X3**, 1665/2021/ĐKSP, GXNQC 1245/2024/XNQC-ATTP (18/06/2024), Cty TNHH TM&DV Slimming Care VN. *Chưa xác nhận là cùng sản phẩm* |
| Số `838/2024/ĐKSP` | thuộc **LEKITER CALZBONE KIDDY** (Leking Pharma, 23/01/2024) | `838/2024/XNQC-ATTP` là SP khác | Không khớp SKU nào đã tra |
| Số `3433/2020` | ĐKSP: VIMIRADS MULTIVITAMIN | GXNQC: DK-BETICS GOLD | Mơ hồ nếu thiếu hậu tố |

## 2. Hệ thống DVC Bộ Y tế — `https://dichvucong.moh.gov.vn/`
- **Truy cập:** được (200, Liferay).
- **Tra cứu công khai:** (a) *"Tra cứu hồ sơ DVC"*: POST form, yêu cầu **mã số biên nhận và captcha** (`_trangchu_WAR_bytedvcportlet_mahoso`, `captchaText`). Tôi dừng ở đây. Chức năng này không dùng để tra theo SKU. (b) *"Tra cứu DVC trực tuyến"*: danh mục thủ tục hành chính (tên/mã thủ tục, lĩnh vực, mức độ), không có dữ liệu sản phẩm.
- Danh sách lĩnh vực trên trang `/web/guest/dichvucong` (theo HTML server trả về) **không có An toàn thực phẩm**: chỉ có Bảo trợ XH, Phòng bệnh, KCB, YDCT, Dược phẩm, TBYT, KHCN&ĐT, Mỹ phẩm, Thi đua.
- Dù vậy, VFA ghi rằng hồ sơ QC 2024–2025 được xử lý trên dichvucong.moh.gov.vn. File danh sách 9/2024–5/2025 có tiêu đề nguồn `https://mcdt.moh.gov.vn`. Không có endpoint công khai nào trả về giấy đã cấp.
- **Kết luận:** không có tra cứu công khai theo sản phẩm, không trả công dụng.

## 3. Cổng cũ (thử lại 21/10/2026)
| Host | DNS | https | http | www |
|---|---|---|---|---|
| congkhaiyte.moh.gov.vn | 103.124.60.94 | không kết nối được | không kết nối được | không có bản ghi DNS |
| xacnhanquangcao.vfa.gov.vn | 103.124.60.74 | không kết nối được | kết nối bị đóng ("unexpected error on receive") | không có bản ghi DNS |
| congbosanpham.vfa.gov.vn | 103.124.60.73 | **HTTP 500** | **HTTP 500** | không có bản ghi DNS |

Không có redirect hay header `Location` nào chỉ sang domain mới. Trang "Hệ thống tra cứu" của vfa.gov.vn không liên kết sang domain mới. Thực tế, kho ĐKSP/GXNQC cũ (2018 → 08/2024) đã có mặt trên antoanthucpham.moh.gov.vn. vfa.gov.vn cũng đăng *"Thông báo về việc nộp hồ sơ thông báo bổ sung sau công bố trên Cổng thông tin An toàn thực phẩm Quốc gia"*. Tuy vậy tôi **không** tìm thấy thông báo chính thức nói rằng domain cũ đã chuyển sang domain mới.

## 4. vfa.gov.vn — quyết định thu hồi (→ `recalls.jsonl`)
- **Văn bản, phân loại "Quyết định thu hồi CBSP"** (`/vanban-search?g=194`): 17 QĐ, từ 123 đến 140/QĐ-ATTP (22/05 → 17/06/2026), mỗi QĐ có PDF ở `/van-ban/tai-tep-<hash>.html`. Link menu `/quyet-dinh-thu-hoi-cbsp/` bị hỏng (redirect về trang chủ).
- **Tin tức "Thu hồi hiệu lực …"** (`/tim-kiem/?p=thu hồi hiệu lực`, đã quét 9 trang): 30 bài đăng từ 26/04 → 11/07/2025 (29 bài trong danh sách tìm kiếm cộng bài HIUP), kèm 63 PDF. Bài trước đó gần nhất là 19/04/2023.
- PDF đều có lớp text tốt (PyMuPDF, không cần OCR). Số và ngày QĐ lấy từ dấu chữ ký số. 6 PDF có số QĐ lệch hoặc không có trong bài đăng; đã ghi trong trường `note`.
- **Kết quả:** 77 QĐ (60 năm 2025, 17 năm 2026), 312 dòng (290 thu hồi ĐKSP, 22 thu hồi GXNQC, đều thuộc QĐ 215/QĐ-ATTP – Abbott/Glomed). 8 dòng GXNQC thiếu tên SP do ô gộp trong bảng.
- **Khoảng trống:** không tìm thấy QĐ thu hồi nào đăng trên vfa.gov.vn trong các giai đoạn 01/2024–04/2025, 07/2025–05/2026 và sau 17/06/2026. Có thể do không đăng, hoặc do tìm kiếm của site không bắt được. Ngoài QĐ 215, không thấy QĐ thu hồi GXNQC nào trong giai đoạn 2024–2026.
- Lý do thu hồi phổ biến: doanh nghiệp *tự nguyện xin thu hồi / xin rút hồ sơ*. QĐ 215 thì thu hồi GXNQC *căn cứ QĐ 209 đã thu hồi ĐKSP*.

## 5. vfa.gov.vn — danh sách GXNQC đã cấp (có số GXNQC)
| Bài đăng (ngày) | File | Có số GXNQC? | Số dòng |
|---|---|---|---|
| DS SP được cấp GXNQC tháng 9/2024 (15/10/2024) | `/storage/upload/thang-9.xlsx` | Có (cột "Số Giấy XNQC") | 24 |
| … tháng 9,10,11/2024 (17/01/2025) | `/upload/files/DS HO SO CAP PHEP 9,10,11 2024.xlsx` | Có (số/2024/XNQC-ATTP + ngày) | 1.218 |
| … tháng 11,12/2024 (06/01/2025) | `/upload/files/DS GIAY XNQC TH 11_12 NAM_2024.xlsx` | Có (mã hồ sơ, số, ngày cấp) | 1.142 |
| … tháng 1,2,3/2025 (04/04/2025) | `/upload/files/DS XNQC TH QUY 1_2025.xlsx` | Có | 965 |
| DS 2020–2025 (10/10/2024, đã cập nhật) | `…/DS CAP CAP HS QC 1_12_2023 - 31_8_2024.xlsx` | **Không** (chỉ có DN, SP, ngày nộp/trả, trạng thái) | 1.997 |
|  | `/upload/files/DS CAP CAP HS QC 1_9_2024 den 15_5_2025 (1).xls` | **Không** (mã hồ sơ, trích yếu, chủ hồ sơ) | 1.216 |

Ngoài ra còn 3 file 2020–2023 (`DS CAP CAP HS QC …`) chưa tải. Kết quả cho 3 SKU: chỉ có **SLIMMING CARE X3** xuất hiện, ở file 12/2023–8/2024 (dòng 1504, "Hồ sơ đã hoàn tất", file này không có cột số). Số `1245/2024/XNQC-ATTP` lấy từ API cổng mới. Không có dòng nào cho Betics hay Non Alco. Các danh sách này không có công dụng hay nội dung QC.

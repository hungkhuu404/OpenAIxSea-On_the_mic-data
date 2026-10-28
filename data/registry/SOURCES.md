# Nguồn — data/registry (truy xuất 21/10/2026, mạng VN)

Độ tin cậy: **A** = dữ liệu gốc của cơ quan nhà nước, lấy trực tiếp; **B** = dữ liệu gốc nhưng có lỗi hoặc thiếu đã biết; **C** = suy luận hoặc chưa xác minh.

| # | URL | Dùng cho | Bản thô | Độ tin cậy |
|---|---|---|---|---|
| 1 | https://antoanthucpham.moh.gov.vn/ (+ bundle `main-25V2JBQI.js`, `chunk-*.js`) | Tìm route và endpoint; điều khoản sử dụng (`chunk-KHZL4OPD.js`) | `_raw/attp_index.html`, `_raw/attp_js/` | A |
| 2 | https://gateway-api-antoanthucpham.moh.gov.vn/api/attp/tra-cuu-giay-phep/giay-tiep-nhan-cong-bo | Tra ĐKSP theo SKU/số | `_raw/attp_api/gtncb_*.json` | B: dữ liệu dừng ở 01/09/2024; trạng thái thu hồi không cập nhật |
| 3 | …/giay-xac-nhan-quang-cao | Tra GXNQC | `_raw/attp_api/gxnqc_*.json` | B: dừng ở 31/08/2024 |
| 4 | …/filter-dropdowns, /api/portal/public/csdl, /api/portal/public/docs, /api/portal/public/article | Danh mục, thống kê theo năm, văn bản, tin | `_raw/attp_api/` | A |
| 5 | https://dichvucong.moh.gov.vn/ , /web/guest/dichvucong | Chức năng tra cứu (cần mã biên nhận + captcha) | `_raw/dvc/` | A |
| 6 | congkhaiyte.moh.gov.vn, xacnhanquangcao.vfa.gov.vn, congbosanpham.vfa.gov.vn (http/https, có/không www) | Thử lại | `_raw/_requests.log` (không có body nào để lưu) | A (lỗi kết nối hoặc 500 tại thời điểm thử) |
| 7 | https://vfa.gov.vn/vanban-search?g=194 và 17 trang `/van-ban/quyet-dinh-ve-viec-thu-hoi-…html` → `/van-ban/tai-tep-<hash>.html` (PDF) | QĐ thu hồi 2026 (123–140/QĐ-ATTP) | `_raw/vfa/vanban194/`, `_raw/vfa/pdf2026/*.pdf` + `.txt` | A |
| 8 | https://vfa.gov.vn/tim-kiem/?p=thu+hồi+hiệu+lực (trang 1–9) và 30 bài `/tin-tuc/thu-hoi-hieu-luc-…html` (26/04–11/07/2025) → `/upload/files/*.pdf` | QĐ thu hồi 2025 | `_raw/vfa/tim-kiem_*.html`, `_raw/vfa/articles/`, `_raw/vfa/lists/recall_hiup.html`, `_raw/vfa/pdf2025/` | A; số QĐ ở 6 PDF lệch hoặc không có trong bài đăng (B, xem `note`) |
| 9 | https://vfa.gov.vn/tin-tuc/danh-sach-…-quang-cao-….html (5 bài) và các file xlsx/xls | Danh sách GXNQC đã cấp (9/2024–Q1/2025 có số) | `_raw/vfa/lists/`, `_raw/vfa/gxnqc_lists/` | A; file .xls được Excel chuyển sang .xlsx (đã tắt macro), bản gốc ở `_orig_xls/` |
| 10 | `team archive: research-data-2026-10-21/qd136.txt` (mẫu có sẵn) | Đối chiếu QĐ 136 | — | B: text trong file mẫu mất dấu tiếng Việt; PDF gốc ở #7 đọc đúng |

## Cách tạo các file đầu ra
- `recalls.jsonl`: text lấy từ lớp text của PDF bằng PyMuPDF (không OCR). Số và ngày QĐ lấy từ dấu chữ ký số trên PDF (với QĐ năm 2026 thì lấy theo bảng văn bản VFA, hai nguồn khớp nhau). `reason_excerpt` = các đoạn "Căn cứ …" nguyên văn, bỏ căn cứ thẩm quyền 3668/QĐ-BYT, khoảng trắng gộp lại. `url` = link PDF; `source_page` = trang đăng. Các trường thêm: `type` (`thu_hoi_giay_tiep_nhan_DKSP` | `thu_hoi_GXNQC`) và `note` (ô gộp, lệch số QĐ, trùng ĐKSP 5803/2019).
- `sku_lookups.json`: chỉ dựng lại từ các JSON thô đã lưu, không gửi request mới.
- Script tải và dựng dữ liệu chạy cục bộ, không đưa vào repo này: tải chậm có log, dựng và hoàn thiện `recalls.jsonl`, dựng `sku_lookups.json`, đọc file Excel.

## Chưa kiểm được / hạn chế
- Giấy ĐKSP và GXNQC cấp **từ 09/2024 đến nay**: không có nguồn công khai nào để tra (cổng mới không có; danh sách GXNQC của VFA dừng ở 15/05/2025).
- Quyết định thu hồi năm **2024** và giai đoạn **07/2025–05/2026**: không tìm thấy trên vfa.gov.vn. Chưa loại trừ khả năng có nhưng tìm kiếm của site không trả về.
- Chưa xác nhận "Slimaura Care x3" có phải là "SLIMMING CARE X3" hay không.
- Không thử các endpoint chi tiết hoặc tải file nằm sau đăng nhập. Không thử gọi gateway khi thiếu header Origin.

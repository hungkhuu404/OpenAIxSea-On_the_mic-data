# Ghi chú về số ĐKSP trong registry, kiểm ngày 22/10/2026

Dữ liệu: `cbsp_2018_2025.csv`, 72.766 dòng, 72.444 số khác nhau. Tất cả là bản công bố TPBVSK từ 2018 tới 31/5/2025.

## Bốn điểm cần biết khi tra số ĐKSP

1. **Số không phải khoá duy nhất.**
   - 296 số (0,4%) ứng với 2–3 tên sản phẩm khác nhau. Phần lớn thuộc các năm 2018 (228), 2019 (244) và 2024 (107).
   - Ví dụ: `838/2024/ĐKSP` ứng với **LEKITER CALZBONE KIDDY** (Leking Pharma) **và** **CALCI LIPOCAN 700** (Medicophar).
   - → Một tên sản phẩm chỉ "không khớp" số đó khi nó không khớp với **dòng nào** của số.
2. **Định dạng số không thống nhất.** 95 số lệch mẫu `N/YYYY/ĐKSP`:
   - `ÐKSP` dùng chữ Ð (U+00D0, Eth của tiếng Iceland), không phải Đ (U+0110);
   - `DKSP` không dấu;
   - mẫu cũ `…/ATTP-XNCB`.
   - → Chuẩn hoá trước khi tra: NFC, đổi Ð→Đ, `DKSP`→`ĐKSP`, viết hoa.
3. **Cùng chuỗi số, khác loại giấy.**
   - `3433/2020/ĐKSP` là VIMIRADS MULTIVITAMIN, còn `3433/2020/XNQC-ATTP` là GXNQC của DK-BETICS GOLD.
   - → Luôn giữ hậu tố. API cổng mới khớp `soGiayPhep` theo **chuỗi con**, nên cũng phải lọc lại theo hậu tố.
4. **Dữ liệu không phủ hết.**
   - Registry dừng ở 31/5/2025. API cổng mới dừng ở 01/09/2024, và **không cập nhật thu hồi**: `3984/2019/ĐKSP` đã bị thu hồi theo QĐ 136 ngày 17/06/2026 mà API vẫn báo còn hiệu lực.
   - → Số **không có** trong registry không chứng minh số đó là giả. Thu hồi lấy từ `recalls.jsonl` (312 dòng, 77 quyết định, 26/04/2025 → 17/06/2026), không lấy từ API.

## Kết quả tra cho ba sản phẩm (registry local và API cổng mới)

| Sản phẩm | ĐKSP | GXNQC |
|---|---|---|
| DK-Betics Gold | `7615/2020/ĐKSP`, CTCP Dược Khoa: khớp tên | `3433/2020/XNQC-ATTP` |
| Non Alco | `4993/2024/ĐKSP`, CTCP DP VITATH: khớp tên | Không tìm thấy trong các danh sách có số (đến 15/05/2025). Cảnh báo VFA 19/08/2026 nói sản phẩm chưa được cấp GXNQC |
| Slimaura Care x3 | Không có trong registry. Số người bán đưa ra, `838/2024/ĐKSP`, thuộc hai sản phẩm khác. Tên gần nhất là SLIMMING CARE X3 (`1665/2021/ĐKSP`), **chưa xác nhận là cùng sản phẩm** | Không có |

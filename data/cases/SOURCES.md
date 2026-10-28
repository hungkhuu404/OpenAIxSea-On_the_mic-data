# SOURCES — evidence pack và bộ ca

Ngày lấy: 21–22/10/2026, từ máy ở VN (PowerShell `Invoke-WebRequest`, Python `requests`). Một số trang lấy qua WebFetch (máy chủ Mỹ), có ghi rõ. Bản tải thô nằm trong `data/evidence/_raw/` và `data/cases/_raw/`. Phụ đề YouTube nằm trong `data/cases/_raw/youtube/yt_<id>.json`.

Độ tin cậy: **cao** = văn bản cơ quan nhà nước (trang/PDF gốc) · **trung bình** = báo chí trích dẫn, mô tả video, ảnh chụp do báo/cơ quan đăng · **thấp** = trang bán hàng tự viết lại, phụ đề ASR tự động, tiêu đề khôi phục từ slug URL.

## 1. Cơ quan nhà nước (vfa.gov.vn)

| Nội dung | URL | Ngày đăng | Độ tin cậy | Ghi chú |
|---|---|---|---|---|
| Non Alco + DK-Betics Gold | https://vfa.gov.vn/tin-tuc/khan-truong-xac-minh-xu-ly-vi-pham-quang-cao-san-pham-vien-ngam-giai-ruou-non-alco-va-dk-betics-gold.html | 19/08/2026 | cao | Số ĐKSP, GXNQC 3433/2020, "chưa được cấp GXNQC" |
| CV 1667/ATTP-NĐTT (DK-Betics, gửi SYT HN) | …/Tuan%2010/CV%20gui%20SYT%20H%C3%80%20N%20I%202_signed.pdf | 20/08/2026 | cao | PDF có lớp chữ; thay CV 1647 ngày 18/8 |
| CV 1658/ATTP-NĐTT (Non Alco, gửi Cục PTTH&TTĐT) | …/Tuan%2010/CV%20gui%20Cuc%20PTTH-TTDT(sua)_signed_1.pdf | 19/08/2026 | cao | Nguồn phản ánh: tạp chí Thương hiệu và Công luận |
| Slimaura — yêu cầu gỡ | https://vfa.gov.vn/tin-tuc/yeu-cau-go-bo-ngung-kinh-doanh-san-pham-slimaura-care-x3-do-vi-pham-phap-luat.html | 04/08/2026 | cao | Số 838/2024/ĐKSP ngày 23/02/2024 "không cấp" |
| CV 1539/ATTP-SP gửi Shopee | …/Tuan%208/CV%20gui%20shopee%2031_7_2025_signed.pdf | 04/08/2026 | cao | Tên file ghi "31_7_2025" nhưng nội dung ngày 04/8/2026 |
| Slimaura — gửi Chi cục HN | https://vfa.gov.vn/tin-tuc/khan-truong-kiem-tra-xac-minh-hoat-dong-san-xuat-kinh-doanh-quang-cao-san-pham-slimaura-care-x3.html | 06/08/2026 | cao | CV 1565/ATTP-SP |
| Sausando — Shopee | https://vfa.gov.vn/tin-tuc/yeu-cau-shopee-ngung-kinh-doanh-san-pham-sausando-slimming-capsule.html | 16/10/2026 | cao | Số 5218/2023/ĐKSP "không cấp" |
| Sausando — TikTok | https://vfa.gov.vn/tin-tuc/ra-soat-go-bo-thong-tin-san-pham-sausando-slimming-capsule-tren-tiktok.html | 17/10/2026 | cao | + PDF CV 2210/ATTP-SP |
| Love World Nutrition Coffee | https://vfa.gov.vn/xu-ly-vi-pham-attp/xac-minh-xu-ly-vi-pham-quang-cao-san-pham-love-world-nutrition-coffee-tren-san-thuong-mai-dien-tu.html | 30/08/2026 | cao | Mục "Xử lý vi phạm ATTP", không nằm trong mục Cảnh báo |
| CV 1782/ATTP-NĐTT + phụ lục ảnh | …/Tuan%2012/CV%201782%20ve%20Coffee%20Love%20World_signed.pdf | 30/08/2026 | cao (văn bản) / trung bình (chữ chép từ ảnh) | 2 ảnh listing Shopee trích ra: `evidence/_raw/cv_loveworld_1782_img0.png`, `_img1.jpeg`. 11 ca love_world_coffee chép tay từ ảnh này |
| BONMAX JOINT | https://vfa.gov.vn/tin-tuc/canh-bao-thuc-pham-bao-ve-suc-khoe-bonmax-joint-co-noi-dung-quang-cao-vi-pham-quy-dinh-cua-phap-luat.html | 29/04/2025 | cao | |
| SELODERMA + Morimon | https://vfa.gov.vn/tin-tuc/canh-bao-thuc-pham-bao-ve-suc-khoe-seloderma-psc-300-plus-va-thuc-pham-bao-ve-suc-khoe-bot-chiet-xuat-xuong-ngua-morimon-co-noi-dung-quang-cao-vi-pham-quy-dinh-cua-phap-luat.html | 04/04/2025 | cao | |
| Fanpage "Dược phẩm Hoàng Hường – Meli" (có Morimon) | https://vfa.gov.vn/tin-tuc/canh-bao-fanpage-co-ten-duoc-pham-hoang-huong--meli-noi-dung-quang-cao-vi-pham-quy-dinh-cua-phap-luat-ve-quang-cao.html | 29/05/2025 | cao | |
| Cao Việt Hoàng | https://vfa.gov.vn/tin-tuc/canh-bao-thuc-pham-bao-ve-suc-khoe-cao-viet-hoang-dang-quang-cao-vi-pham-quy-dinh-phap-luat.html | 17/06/2025 | cao | |
| Khác đã tải để tham khảo (chưa dùng làm ca) | Crilin women Health (31/03/2025, có ví dụ GXNQC 2288/2021 bị thu hồi bằng QĐ 134/QĐ-ATTP); CONDITION LET'S C / LIVER (14/05/2025); Life-Space (16/03/2023); "Người dân cần lưu ý…" (18/04/2025) | | cao | `evidence/_raw/vfa_crilin.*`, `vfa_condition.*`, `vfa_canhbao_tpbvsk_qc.*`, `vfa_luuy_tpbvsk.*` |

Lưu ý kỹ thuật: Python `requests` bị lỗi TLS `DH_KEY_TOO_SMALL` với vfa.gov.vn; KHÔNG hạ mức bảo mật TLS, mà dùng PowerShell `Invoke-WebRequest` (vào được).

## 2. Registry

| File | Dùng cho | Ghi chú |
|---|---|---|
| `research-data-2026-10-21/cbsp_2018_2025.csv` | số ĐKSP ↔ tên ↔ công ty | Kết quả tra: `evidence/_raw/registry_lookup_by_name_2026-10-21.json`, `registry_lookup_by_number_company_2026-10-22.json`. **Phát hiện:** số 838/2024/ĐKSP xuất hiện 2 dòng (STT 64704 LEKITER CALZBONE KIDDY – LEKING PHARMA; STT 72092 CALCI LIPOCAN 700 – MEDICOPHAR) |
| `research-data-2026-10-21/qc_2023_2024.csv` | có hồ sơ GXNQC hay không | Không có số GXNQC. Có dòng ' BONMAX JOINT' (28/3/2024, "Hồ sơ đã hoàn tất") và 'SLIMMING CARE X3' (5/6/2024); không có Non Alco, Slimaura, Sausando |

## 3. Báo chí

| Báo | URL | Ngày | Độ tin cậy | Dùng cho |
|---|---|---|---|---|
| Thương hiệu và Công luận | https://thuonghieucongluan.com.vn/vien-ngam-giai-ruou-non-alco-quang-cao-giam-nhanh-nong-do-con-chi-sau-40-phut-can-cu-tu-dau-a325093.html | 04/07/2026 | trung bình | 19 ca Non Alco: trích trong bài + **chép tay từ 5 ảnh chụp màn hình** báo đăng (`cases/_raw/thcl_img*.jpg`: landing nonalcovitath.vn, fanpage NON ALCO ngày 4/12/2025 và 22/1/2026). Các câu chép từ ảnh không kiểm tự động được → cần người đối chiếu ảnh |
| VOV | https://vov.vn/thi-truong/dk-betics-gold-thuc-pham-bao-ve-suc-khoe-quang-cao-tac-dung-nhu-thuoc-chua-benh-post1307684.vov | 19/06/2026 | trung bình–thấp | **403 từ máy VN**; đọc qua WebFetch (công cụ tóm tắt, chỉ trả đoạn trích). Ghi chép: `cases/_raw/press_vov_dkbetics_WEBFETCH_NOTES.txt`. 6 ca DK-Betics + câu GXNQC trong evidence |
| Báo Pháp luật VN (Doanh nhân) | https://doanhnhan.baophapluat.vn/vien-tieu-duong-dk-betics-gold-vi-pham-quy-dinh-vi-quang-cao-nhu-thuoc-chua-benh-348a9daa.html | 20/08/2026 | trung bình | 5 ca DK-Betics (gói liệu trình) |
| Tiền Phong, Báo Lào Cai, VietnamPlus, Thời báo Tài chính, Báo Pháp luật (Non Alco) | tienphong.vn …post1869353.tpo; baolaocai.vn …post906519.html; vietnamplus.vn …post1131267.vnp; thoibaotaichinhvietnam.vn …202582.html; doanhnhan.baophapluat.vn …264abab3.html | 20/08/2026 | trung bình | Đối chiếu, không lấy ca |
| VTC News, Viettimes (phạt Vitath 110 triệu) | https://vtcnews.vn/cong-ty-co-phan-duoc-pham-vitath-bi-phat-110-trieu-dong-ar1035575.html ; https://viettimes.vn/duoc-pham-vitath-bi-phat-110-trieu-dong-sau-vu-quang-cao-non-alco-post204832.html | 21/08/2026 | trung bình | Quyết định xử phạt Sở Y tế HN (R06 + R03), lưu ở `evidence/_raw/press_*_vitath_phat.*` |
| Tuổi Trẻ, VnBusiness, Nhân Dân, Thời báo TC (Slimaura) | tuoitre.vn …100260805091646511.htm; vnbusiness.vn …slimaura-care-x3.html; nhandan.vn …post980253.html | 05/08/2026 | trung bình | Ảnh hộp ghi "Thực phẩm bổ sung" (VnBusiness) |
| Tuổi Trẻ, Thời báo TC, Đại biểu Nhân dân, Tạp chí KT-TC Thuế Hải quan (Cao Việt Hoàng) | tuoitre.vn …20250617152125422.htm; thoibaotaichinhvietnam.vn …178483.html; daibieunhandan.vn …10389002.html; thuehaiquan.tapchikinhtetaichinh.vn …96425.html | 17–18/06/2025; 26/9 (ĐBND) | trung bình | Công dụng "được cấp phép" chỉ có ở bài Thuế Hải quan |
| Kera: VnExpress (bản án), SGGP (phạt 70tr/người), VietNamNet (phạt 125tr, thu hồi bản tự công bố; kết quả kiểm định), Tuổi Trẻ (03/04/2026), Luật sư VN (cáo trạng), Znews (06/03/2025; 04/04/2025), Nông nghiệp & MT (19/09/2025), Báo Văn hoá (xin lỗi) | xem `cases/_raw/kera_*.html` | 03/2025 – 04/2026 | trung bình | Câu claim là lời nói do báo/bản án trích, không có bản ghi livestream gốc |

## 4. Trang bán hàng / nhà thuốc

| Trang | URL | Ngày trên trang | Độ tin cậy | Ghi chú |
|---|---|---|---|---|
| Trung Tâm Thuốc — DK-Betics Gold | https://trungtamthuoc.com/dk-betics-gold | đăng 27/11/2023, cập nhật 28/07/2026 | thấp | **Ghi sai số ĐKSP 3833/2018** (số của Trà túi lọc DK-BETICS) |
| Trung Tâm Thuốc — Non Alco | https://trungtamthuoc.com/vien-ngam-giai-ruou-non-alco | 12/08/2026 | thấp | Công dụng do nhà thuốc viết lại |
| Trung Tâm Thuốc — Slimming Care X3 | https://trungtamthuoc.com/slimming-care-x3 | 23–27/10/2025 | thấp | Sản phẩm KHÁC (1665/2021/ĐKSP) — dùng làm đối chứng |
| Chiaki — DK-Betics Gold | https://chiaki.vn/vien-uong-ho-tro-on-dinh-duong-huyet-dk-betics-gold | không ghi | thấp | |
| Chiaki — Cao Việt Hoàng | https://chiaki.vn/cao-viet-hoang-ho-tro-bao-ve-niem-mac-da-day-hop-100g | không ghi (bình luận 08–10/2026) | thấp | Có bình luận người mua — KHÔNG lấy làm ca (người dùng cá nhân) |
| Shopee/Lazada listing do VFA nêu | xem `evidence/slimaura_care_x3.json`, `sausando_slimming_capsule.json` | — | thấp | Không mở (cần JS/đăng nhập; đã bị yêu cầu gỡ). Chỉ dùng tiêu đề khôi phục từ slug URL |

## 5. YouTube (trang công khai, không đăng nhập, không tải video)

Siêu dữ liệu (tiêu đề, kênh, ngày đăng, mô tả) lấy từ trang xem video; phụ đề qua `youtube-transcript-api` (cài `--user`). Phụ đề đều là **ASR tự động của YouTube** (tiếng Việt, "được tạo tự động"), chất lượng thấp. Sau khoảng 30 video, YouTube trả `IpBlocked` → các video Morimon, BONMAX, 4 video GREEN BEAUTY/PHẠM VIỆT HOÀNG chỉ có tiêu đề + mô tả.

| SKU | Video (id — kênh — ngày đăng) |
|---|---|
| DK-Betics Gold | C2vnrj4Nb4E — Sàn Thuốc — 09/08/2023 · lc5AGpkh1l0 — Dk-Betics Gold - Hỗ Trợ Ổn Định Đường Huyết — 04/08/2026 · vpaarEqzvbE — DK Betics Gold - Hỗ trợ điều trị tiểu đường — 14/08/2025 · iZRSVNws4tY — 31/07/2025 · iYoV6bvGW3E — Hệ thống nhà thuốc Pharmart — 02/07/2021 · SOU3eHAbQn8 — 13/05/2022 · 1grxOWIm-_Y — 22/06/2023 · sNq6zrtMIjI — DKSG — 12/02/2025 · _GfWLJe4NfM — 18/10/2023 (đã tải thêm, chưa dùng: cEcuEFRi6mE, Dx5Vrg1TwI0 [DK-Betics thường, khác SKU], VYNGhJvEbAo) |
| Non Alco | kênh "Viên Ngậm Giải Rượu NON ALCO": sI_jtRof2x0 (21/12/2025), D5m43hHzzEs (10/11/2025), DN4t39pIrPI (07/04/2026), Cs8eEy1DQd0, vRigeYdhNHI, r9lS_tFO9Ks (14/11/2025), yAUdET3F6gA, SSGl502oVmg (10/11/2025) · xtdfxqNXoVw — "Phiên bản giới hạn" — 05/03/2025 · _FTlXzU5kU4 — Lượn Lờ Phố — 25/08/2026 (tin phạt 110 triệu, không lấy ca) |
| Kera | duMFht7DXRw — VTC NEWS — 14/03/2025 · XBuJKFnEx1o — VTV24 — 06/04/2025 · (tải thêm: lBmIVXfIVW4, vpjurGthF0Q) |
| Cao Việt Hoàng | Jo_tOyjRCTs — Cao Việt Hoàng Chính Hãng — 27/11/2024 · Ti6cqDGvo0U — Đơn Vị Cao Việt Hoàng Chính Hãng — 14/10/2025 · C_8LiKcErDQ — Cliptrangphuc — 20/11/2024 · 7btXszpLe5A, RMdijna6wbw, R-HGdo2gfbo — GREEN BEAUTY — 10/2025–05/2026 |
| Morimon | kênh "CAO NGỰA MÔNG CỔ - MORIMON": cUg0j8MZZsE, VtxdCG6n9Lo, tpahB_UC6cE, xq6HhkNJbM8, tm3dgzauEbU (09–12/2023) |
| BONMAX | 4_uSRq1KBcU — Bác Sĩ 4.0 — 06/05/2025 (hashtag #bonmax, SKU không xác định) |

Tìm video bằng trang kết quả tìm kiếm công khai của YouTube (`youtube.com/results`, không đăng nhập).

## 6. Nguồn chết / không vào được (22/10/2026)

| Nguồn | Tình trạng |
|---|---|
| vitath.vn/vien-ngam-giai-ruou-non-alco.html | Chuyển hướng về trang chủ Vitath (trang đã gỡ) |
| nonalcovitath.vn (và /vienngamgiairuou, /duocphamvitath) | Không kết nối được |
| tieuduong.asia | Không kết nối được |
| hotrotieuduong.asia | Lỗi chứng chỉ TLS — không vượt |
| caonguamongco.com/san-pham-bot-cao-ngua-mong-co-morimon | Lỗi chứng chỉ TLS — không vượt |
| doctor.tuvanwebsite.com/product/dr-michaels-psc-300/ | Không phân giải DNS |
| caoviethoang.com | Tên miền nay là trang cờ bạc spam (đã lưu `site_caoviethoang*.html` làm bằng chứng, không dùng) |
| caoviethoang-chinhhang.com | Không kết nối được |
| phattriencaoviethoang.com (website chính thức theo công ty) | Không phân giải DNS |
| vov.vn (bài DK-Betics) | 403 từ máy VN; chỉ đọc qua WebFetch |
| archive.org / web.archive.org | Hết thời gian kết nối từ VN; WebFetch không được phép truy cập → không dùng được bản lưu |
| Facebook (fanpage NON ALCO, @Caonguamorimon, xuongkhopbonmaxjoint) | Cần đăng nhập — không thử |
| Shopee / Lazada / TikTok listing do VFA nêu | Cần JS/đăng nhập, đã bị yêu cầu gỡ — không thử |
| Tìm kiếm DuckDuckGo HTML / Bing từ máy VN | Không trả kết quả dùng được (DDG trống; Bing trả kết quả rác) |

## 7. Chưa kiểm được

- Bản gốc Quyết định 2941/QĐ-SYT (Sở Y tế HN, 21/8/2026) và 12/QĐ-XPHC (Cục ATTP, 20/6/2025) — chỉ thấy qua báo.
- Cảnh báo VFA ngày 06/08/2021 về DK-BETICS GOLD (VOV nhắc) — chưa tìm thấy trên vfa.gov.vn.
- Ảnh nhãn thật của mọi SKU — chưa có ảnh nào đủ rõ phần công dụng.

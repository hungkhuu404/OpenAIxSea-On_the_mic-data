# Nguồn của corpus luật (`data/law/`)

- **Ngày tải.** Tất cả bản tải thô lấy ngày **2026-10-21**, khoảng 21:40–22:01 giờ VN, từ máy ở Việt Nam bằng Python `requests`. Mỗi request cách nhau ít nhất 1,5 giây và thử lại tối đa 3 lần.
- **Ngày dựng corpus và kiểm.** 2026-10-22.
- **Bổ sung 2026-10-23 (NĐ 115/2018 Điều 20, 22).** Bản tải thô của NĐ 115/2018, NĐ 124/2021 và các tệp kiểm tình trạng lấy ngày **2026-10-23** bằng PowerShell `Invoke-WebRequest` (Python `requests` lỗi TLS với trang .gov.vn), mỗi request cách nhau ít nhất 1,5 giây. Dựng và kiểm cùng ngày, cùng hàm tách đoạn PDF và cùng quy tắc anchor như đợt 22/10 (đã chạy lại trên corpus cũ: dựng lại đúng 302 anchor).
- **Bản thô.** Nằm trong `_raw/` (giữ cục bộ, không đưa lên repo). Tên file theo dạng `<văn bản>__<nguồn>.<đuôi>`.
- **Log so sánh.** Log so sánh từng điều giữa các nguồn nằm ở `_build/*.diff.txt` (giữ cục bộ, không đưa lên repo).
- **Script.** Script tải và dựng corpus chạy cục bộ, không đưa vào repo này: tải trang, tìm văn bản trên Công báo, tách điều/khoản, dựng `index.json`, kiểm hợp lệ, kiểm câu trích.

## Cách lấy và mức tin cậy

| Mã nguồn (`kind`) | Là gì | Độ tin cậy |
|---|---|---|
| `cong_bao` | Tệp đính kèm trên **congbao.chinhphu.vn** (Công báo nước CHXHCN Việt Nam, VPCP). PDF có chữ ký số "CÔNG BÁO NƯỚC CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM". Một số văn bản có thêm .docx. URL tệp lấy từ API tìm kiếm công khai của chính trang (`api-searchcongbao.chinhphu.vn/search/van-ban`) hoặc từ trang chi tiết `/van-ban/...htm` | **Cao nhất.** Đây là bản chính thức. Văn bản hợp nhất (VBHN) của Văn phòng Quốc hội đăng Công báo cũng thuộc nhóm này |
| `luatvietnam` | Trang toàn văn luatvietnam.vn (HTML) | Trung bình–cao. Dùng làm **nguồn đối chiếu thứ hai**. Trang có chèn ghi chú biên tập (khối "Nội dung tham chiếu", chú thích VBHN). Script đã loại các khối này khi so sánh. Đã phát hiện 1 lỗi gõ của luatvietnam (NĐ 87 Đ50 k1) |
| `local_txt` | `team archive: research-data-2026-10-21/nd87.txt`, `luat75.txt` có sẵn trên máy | Dùng làm nguồn thứ ba. `nd87.txt` trùng Công báo. `luat75.txt` khác Công báo 2 chỗ về kiểu bỏ dấu ("hàng hoá") |

**Cách dựng body**

- **Nguồn chính và trích xuất.** Lấy từ nguồn chính, ưu tiên .docx của Công báo. Nếu không có .docx thì dùng PDF Công báo. PDF được dựng lại đoạn theo thụt đầu dòng.
- **Phần bỏ khỏi PDF.** Script bỏ:
  - dòng đầu trang "CÔNG BÁO/Số…", số trang, khối chữ ký số;
  - với VBHN: chú thích cuối trang và số chú thích (superscript).
- **Đối chiếu.** Sau đó so với từng nguồn phụ theo từng đoạn, sau chuẩn hoá (`normalize.md`).
- **Kết quả kiểm.** Thông tin nguồn và kết quả so sánh của từng điều nằm trong front matter của file điều đó.

## Theo văn bản

| Văn bản | File trong corpus | Nguồn chính | Nguồn đối chiếu | Kết quả đối chiếu |
|---|---|---|---|---|
| **Luật TMĐT 122/2025/QH15** (hiệu lực 01/7/2026) | `luat-122-2025-qh15/dieu-3, 22, 23, 24` | Công báo số 41, .docx | luatvietnam; PDF ký số Công báo | **Khớp hoàn toàn** cả 4 điều |
| **NĐ 248/2026/NĐ-CP** (ký 30/6/2026, hiệu lực 01/7/2026) | `nd-248-2026/dieu-12, 17`, `phu-luc-ii-mau-05` (trích mục 3) | Công báo số 407 ngày 18/7/2026, PDF (trang Công báo không có .docx) | luatvietnam | **Khớp hoàn toàn** |
| **NĐ 15/2018/NĐ-CP** (còn hiệu lực theo NQ 15/2026/NQ-CP) | `nd-15-2018/dieu-26, 27` | Công báo số 375+376 (2018), PDF | luatvietnam | **Khớp** phần lời văn điều luật. luatvietnam chèn 2 ghi chú biên tập, cả hai dẫn NQ 21/2026/NQ-CP về phân cấp thẩm quyền (ở Đ26 và Đ27 k5). Đã loại khi so |
| Tình trạng NĐ 15 | (không dựng thành file điều) | NQ 15/2026/NQ-CP, Công báo số 242, PDF; NQ 09/2026/NQ-CP, .docx; NĐ 46/2026/NĐ-CP, .docx | — | Dùng làm căn cứ cho `status_note` |
| **NĐ 342/2025/NĐ-CP** (hiệu lực 15/02/2026) | `nd-342-2025/dieu-5` | Công báo số 26, .docx | PDF ký số Công báo; luatvietnam | **Khớp hoàn toàn** |
| **Luật Dược 105/2016/QH13**, VBHN **76/VBHN-VPQH** (xác thực 25/3/2026) | `luat-duoc-2016/dieu-6` | Công báo số 201 ngày 10/4/2026, PDF | luatvietnam (VBHN 76); VBHN cũ 39/VBHN-VPQH (Công báo 2025); luatvietnam bản gốc 2016 | VBHN 76: **khớp hoàn toàn**. VBHN 39: khác đúng 1 chỗ ở điểm a khoản 17 (do Luật Phòng bệnh 114/2025). Bản 2016: khác ở k2, k5i, k8 và chưa có k17–19 (do Luật 44/2024). **Khoản 15 giống nhau ở mọi bản** |
| **Luật Quảng cáo 16/2012/QH13**, VBHN **88/VBHN-VPQH** (2025, đã gồm Luật 75/2025) | `luat-quang-cao-2012-sua-2025/dieu-8, 15a, 19` | Công báo số 1243+1244 ngày 05/9/2025, PDF | Bản dựng độc lập từ Luật 16/2012 (Công báo 2012, PDF) cộng Luật 75/2025 (Công báo 2025, PDF); `luat75.txt` | **Khớp hoàn toàn** với bản dựng. `luat75.txt`: Điều 19 k3a ghi "hàng hoá" (2 chỗ) trong khi Công báo ghi "hàng hóa" |
| **NĐ 87/2026/NĐ-CP** (ký 27/3/2026, hiệu lực 15/5/2026) | `nd-87-2026/dieu-6, 50, 51, 53, 68, 69, 71` | Công báo số 243 ngày 22/4/2026, PDF | luatvietnam; `nd87.txt` | `nd87.txt`: **khớp hoàn toàn** cả 7 điều. luatvietnam khác 2 chỗ, xem bên dưới |
| **BLHS 100/2015/QH13**, VBHN **135/VBHN-VPQH** (2025) | `blhs-2015/dieu-198` | Công báo số 1353+1354 ngày 20/9/2025, PDF (phần 2/4 của VBHN) | luatvietnam (BLHS 2015) | **Khớp hoàn toàn**. Điều 198 không có chú thích sửa đổi trong VBHN |
| **NĐ 115/2018/NĐ-CP** (xử phạt VPHC về an toàn thực phẩm, hiệu lực 20/10/2018), bản áp dụng từ 01/01/2022 gồm sửa đổi bởi **NĐ 124/2021/NĐ-CP** (hiệu lực 01/01/2022). Đây là bản áp dụng ngày 12/12/2024 | `nd-115-2018/dieu-20, 22` | Bản dựng từ Công báo: NĐ 115/2018 (Công báo số 907+908 ngày 14/9/2018, PDF) áp các đoạn sửa đổi trích nguyên văn từ NĐ 124/2021 (Công báo số 39+40 ngày 08/01/2022, PDF). Tệp .doc cùng số Công báo dùng để dò chuỗi | luatvietnam VBHN 02/VBHN-BYT (2022); luatvietnam NĐ 115/2018 bản gốc; luatvietnam NĐ 124/2021 | **Khoản 3 Điều 22 khớp ở mọi nguồn.** Khoản này giữ nguyên từ 2018, NĐ 124 không sửa. luatvietnam khác Công báo ở vài đoạn khác, xem bên dưới |
| Tình trạng NĐ 115 | (không dựng thành file điều) | API tìm kiếm Công báo, 14 truy vấn (lưu ở `_raw/status__nd-115-2018__congbao-search-2026-10-23.json`); NĐ 147/2025, NĐ 148/2025, NQ 21/2026/NQ-CP (PDF Công báo) | luatvietnam ("Ngày hết hiệu lực: Đang cập nhật"); baochinhphu.vn 29/10/2025 (tin về dự thảo sửa đổi) | **Còn hiệu lực tại 23/10/2026.** Không có văn bản thay thế hoặc sửa đổi sau NĐ 124/2021. Dùng làm căn cứ cho `status_note` |

**Hai chỗ luatvietnam khác Công báo ở NĐ 87**

- **Đ50 k1.** luatvietnam ghi "dán, **về** các", Công báo ghi "dán, **vẽ** các". Đây là lỗi gõ của luatvietnam.
- **Đ53 k3 điểm b.** luatvietnam ghi "**kể** từ", Công báo và `nd87.txt` ghi "**kề** từ". Đây là lỗi có sẵn trong bản Công báo. Corpus giữ nguyên văn Công báo.

**Các chỗ luatvietnam khác Công báo ở NĐ 115/2018 Điều 20, 22 (bản áp dụng từ 01/01/2022)**

Không chỗ nào nằm ở khoản 3 Điều 22. Ở mọi chỗ khác nhau, tệp .doc cùng số Công báo đều khớp PDF Công báo.

- **Đ22 k2 điểm l (đoạn do NĐ 124/2021 bổ sung).** luatvietnam ghi "duy trì thường xuyên **hoạt động tự kiểm tra** để giám sát", ở cả trang VBHN 02/VBHN-BYT và trang NĐ 124/2021. Công báo NĐ 124/2021 ghi "duy trì thường xuyên để giám sát". Trên Công báo không tìm thấy văn bản đính chính NĐ 124/2021. Corpus giữ Công báo.
- **Đ20 k6 điểm c.** Công báo ghi "điểm **bkhoản** 4", dính chữ, có trong cả PDF và .doc. luatvietnam ghi "điểm b khoản 4". Corpus giữ nguyên văn Công báo.
- **Đ22 k4 điểm đ, k5 điểm b, k8 điểm b và c.** luatvietnam ghi "hoá chất", "sản xuất gia công", "hóa chất phụ gia". Công báo ghi "hóa chất", "sản xuất, gia công", "hóa chất, phụ gia".
- **Dấu câu do VBHN biên tập.** Điểm cuối cũ đổi "." thành ";" khi có điểm bổ sung phía sau (Đ20 k2 điểm đ; Đ22 k2 điểm g, k11 điểm d). Corpus giữ dấu câu Công báo.
- **Điểm d khoản 10 Điều 22.** Bị bãi bỏ bởi khoản 2 Điều 3 NĐ 124/2021. Body ghi `d) (được bãi bỏ)` theo cách ghi của VBHN, giống Luật QC Điều 8 khoản 13. VBHN trên luatvietnam ghi "(được bãi bỏ);".

## URL nguồn chính

- **Luật 122/2025.**
  - .docx: https://congbaocdn.chinhphu.vn/180507251028987904/2026/1/27/122-1769482625737929639063.docx
  - PDF: https://congbaocdn.chinhphu.vn/180507251028987904/2026/1/27/122signed-17694826033991158478619.pdf
- **NĐ 248/2026.**
  - PDF: https://congbaocdn.chinhphu.vn/180507251028987904/2026/7/18/469983-1784195076_v1_1784336573_signed.pdf
  - Trang chi tiết: https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-248-2026-nd-cp-469983.htm
- **NĐ 15/2018.** PDF: https://congbaocdn.chinhphu.vn/CongBaoCP/VanBan/2018/2/25858/21320-1-2018375-37615-2018-nd-cp.pdf
- **NQ 15/2026/NQ-CP.**
  - PDF: https://congbaocdn.chinhphu.vn/180507251028987904/2026/4/22/469344-1776837714_v1_1776849804_signed.pdf
  - Trang chi tiết: https://congbao.chinhphu.vn/van-ban/nghi-quyet-so-15-2026-nq-cp-469344.htm
- **NQ 09/2026/NQ-CP.** .docx: https://congbaocdn.chinhphu.vn/180507251028987904/2026/2/26/09-17720683407421791166195.docx
- **NĐ 46/2026.** .docx: https://congbaocdn.chinhphu.vn/180507251028987904/2026/2/11/46-17708023867031006725357.docx
- **NĐ 342/2025.**
  - .docx: https://congbaocdn.chinhphu.vn/180507251028987904/2026/1/22/342cp-17690650314311267364841.docx
  - PDF: https://congbaocdn.chinhphu.vn/180507251028987904/2026/1/22/342cpsigned-1769065009231106015785.pdf
- **VBHN 76/VBHN-VPQH (Luật Dược).**
  - PDF: https://congbaocdn.chinhphu.vn/180507251028987904/2026/4/10/469206-1775705438_v1_1775787513_signed.pdf
  - Trang chi tiết: https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-76-vbhn-vpqh-469206.htm
- **VBHN 39/VBHN-VPQH (Luật Dược, 2025, phần 1).** PDF: https://congbaocdn.chinhphu.vn/CongBaoCP/VanBan/2025/2/44498/55554-1-2025559-56039-vbhn-vpqh.pdf
- **VBHN 88/VBHN-VPQH (Luật Quảng cáo).** PDF: https://congbaocdn.chinhphu.vn/CongBaoCP/VanBan/2025/8/45976/58538-1-20251243-124488-vbhn-vpqh.pdf
- **Luật 16/2012 (gốc).** PDF: https://congbaocdn.chinhphu.vn/CongBaoCP/VanBan/2012/6/3433/11328-1-2012481-482-162012qh13pdf
- **Luật 75/2025.** PDF: https://congbaocdn.chinhphu.vn/CongBaoCP/VanBan/2025/6/45566/57708-1-2025967-96875-2025-qh15.pdf
- **NĐ 87/2026.**
  - PDF: https://congbaocdn.chinhphu.vn/180507251028987904/2026/4/23/469359-1776912733_v1_1776913093_signed.pdf
  - Trang chi tiết: https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-87-2026-nd-cp-469359.htm
- **VBHN 135/VBHN-VPQH (BLHS, phần chứa Điều 198).** PDF: https://congbaocdn.chinhphu.vn/CongBaoCP/VanBan/2025/9/46165/58888-1-20251353-1354135-vbhn-vpqh.pdf
- **NĐ 115/2018.**
  - PDF: https://congbaocdn.chinhphu.vn/CongBaoCP/VanBan/2018/9/27230/23678-1-2018907-908115-2018-nd-cp.pdf
  - .doc: https://congbaocdn.chinhphu.vn/CongBaoCP/VanBan/2018/9/27230/23679-1-2018907-908115-2018-nd-cp.doc
- **NĐ 124/2021.**
  - PDF: https://congbaocdn.chinhphu.vn/CongBaoCP/VanBan/2021/12/36406/39137-1-202239-40124-2021-nd-cp.pdf
  - .doc: https://congbaocdn.chinhphu.vn/CongBaoCP/VanBan/2021/12/36406/39138-1-202239-40124-2021-nd-cp.doc
- **Kiểm tình trạng NĐ 115/2018.**
  - API: `POST https://api-searchcongbao.chinhphu.vn/search/van-ban`
  - NĐ 147/2025: https://congbaocdn.chinhphu.vn/CongBaoCP/VanBan/2025/6/45091/56785-1-2025787-788147-2025-nd-cp.pdf
  - NĐ 148/2025: https://congbaocdn.chinhphu.vn/CongBaoCP/VanBan/2025/6/45158/56913-1-2025815-816148-2025-nd-cp.pdf và https://congbaocdn.chinhphu.vn/CongBaoCP/VanBan/2025/6/45158/56916-1-2025817-818148-2025-nd-cp.pdf
  - NQ 21/2026/NQ-CP: https://congbaocdn.chinhphu.vn/180507251028987904/2026/5/15/469468-1778579173_v1_1778807093_signed.pdf

URL luatvietnam của từng văn bản được ghi trong front matter (`source_secondary`) của từng file điều.

## Chưa lấy được, hoặc đã lấy nhưng không dùng (và lý do)

| Nguồn / tệp | Tình trạng | Lý do |
|---|---|---|
| **thuvienphapluat.vn** | Không dùng | Trả HTTP 403 (chặn bot). Theo yêu cầu, không vượt qua cơ chế này |
| **vbpl.vn** | Không dùng | Trang mới chạy Next.js, nội dung tải bằng JS. Đã có Công báo là nguồn chính thức hơn nên không tốn công khai thác |
| .docx Công báo cho NĐ 248/2026, NĐ 87/2026, VBHN 76/2026, NQ 15/2026 | Không có | Trang chi tiết Công báo chỉ đính kèm PDF ký số. Đã dùng PDF |
| `nd-15-2018__congbao.doc`, `luat-75-2025-qh15__congbao.doc`, `luat-duoc-…vbhn-39…doc`, `luat-quang-cao__vbhn-88…doc` | Đã tải, **không dùng** | Định dạng Word 97 nhị phân. Chuyển bằng Word COM bị treo (đã dừng tiến trình Word mình tạo). Bản PDF cùng số Công báo đã đủ dùng |
| `luat-duoc-2016__congbao-goc-2016.pdf` | Đã tải, **không dùng** | PDF scan, gần như không có lớp chữ (khoảng 5.000 ký tự cho 73 trang). Bản gốc 2016 chỉ dùng để đối chiếu lịch sử, lấy từ luatvietnam |
| `blhs-2015__vbhn-135…luatvietnam.html`, `luat-quang-cao__vbhn-88…luatvietnam.html` | Đã tải, **không dùng** | Trang luatvietnam của hai VBHN này không hiển thị toàn văn inline. BLHS đối chiếu bằng trang BLHS 2015 của luatvietnam. Luật QC đối chiếu bằng bản dựng từ Công báo |
| BLHS phần 1, 3, 4 (`…58885`, `…58891`, `…58894`.pdf) | Đã tải, **không dùng** | Điều 198 nằm ở phần 58888 |
| **NQ 21/2026/NQ-CP** (phân cấp thẩm quyền GXNQC) | **Đã tải 23/10/2026** (`_raw/status__nq-21-2026-nq-cp__congbao-signed.pdf`, Công báo số 275 ngày 15-05-2026). Điều 6: NQ hiệu lực từ 29/4/2026 đến 01/01/2028; **riêng Điều 2 hiệu lực từ 01/7/2026** | Tải để kiểm tình trạng NĐ 115/2018 (không dẫn NĐ 115). Điều 2 khoản 1 điểm a: việc cấp GXNQC TPBVSK theo khoản 5 Điều 27 NĐ 15/2018 "thuộc thẩm quyền của Chủ tịch Ủy ban nhân dân cấp tỉnh", khớp ghi chú luatvietnam. `status_note` của các file NĐ 15 đã cập nhật ngày 24/10/2026 |
| **VBHN 02/VBHN-BYT (2022)**, bản chính thức | Không có trên Công báo | API Công báo chỉ có 02/VBHN-BYT năm 2014 và 2015. Chỉ dùng bản luatvietnam để đối chiếu. PDF tĩnh của luatvietnam tải về 0 byte (đã xoá) |
| `nd-115-2018__congbao.doc`, `nd-124-2021__congbao.doc` | Đã tải, chỉ dùng để dò chuỗi | Word 97 nhị phân. Dò chuỗi UTF-16 ở các chỗ PDF khác luatvietnam: đều khớp PDF |
| `status__nd-147-2025…`, `status__nd-148-2025…` | Đã tải, chỉ dùng để kiểm tình trạng | Nghị định phân quyền, phân cấp và phân định thẩm quyền lĩnh vực y tế năm 2025. Không dẫn NĐ 115/2018 hay NĐ 124/2021 |
| Dự thảo NĐ sửa đổi NĐ 115/2018 (Bộ Y tế, tin baochinhphu.vn 29/10/2025) | **Chưa lấy** | Dự thảo sửa Điều 4, 6, 16, không đụng Điều 20, 22. Tại 23/10/2026 chưa thấy ban hành trên Công báo. Nếu ban hành trước D-Day thì cần kiểm lại |
| **Dự thảo Luật TMĐT (06/2025)** | **Chưa lấy** | Ngoài phạm vi |
| **Luật An toàn thực phẩm (sửa đổi)** | Không tồn tại trên Công báo tại 22/10/2026 | Đã xem danh mục Luật 01–24/2026/QH16. Nếu luật này có hiệu lực thì NĐ 15/2018 hết được áp dụng, cần kiểm lại trước D-Day |

**Các điểm còn rủi ro**

1. **PDF dựng lại đoạn bằng heuristic thụt dòng.** Mọi điều lấy từ PDF đều đã khớp từng đoạn với ít nhất một nguồn độc lập (luatvietnam hoặc bản dựng Công báo), nên rủi ro thấp.
2. **Có thể có văn bản sửa đổi ban hành sau ngày lập VBHN mà chưa được hợp nhất.**
   - Luật Dược: VBHN ngày 25/3/2026.
   - Luật QC: VBHN 2025.
   - BLHS: VBHN 2025.
   - Đã lọc theo tiêu đề danh mục Luật 2026 trên Công báo. Luật 20/2026 (Tần số, Viễn thông, Giao dịch điện tử, Chuyển giao công nghệ) và Luật 21/2026 (10 luật lĩnh vực nông nghiệp và môi trường) **không nhắm tới** các luật trên.
   - Chưa đọc toàn văn từng luật 2026 để loại trừ tuyệt đối.

## SHA-256 của bản tải thô (`_raw/`)

| Tệp | Byte | SHA-256 |
|---|---|---|
| `blhs-2015__luatvietnam.html` | 7829210 | `35f3396a5992a551c3e3286b1569d80ec0f8b11d3d9cbd43a0ba12a5df0fca7f` |
| `blhs-2015__vbhn-135-2025-vpqh__congbao-58885.pdf` | 479031 | `3ccccc060c2c3685416a8244ba4f234fc1af5216928a3b71afe653178b556f94` |
| `blhs-2015__vbhn-135-2025-vpqh__congbao-58888.pdf` | 664849 | `ffc622b508ea5631c5ca7052df7002f461a3c02538b1b6046416d1d34fb6f49a` |
| `blhs-2015__vbhn-135-2025-vpqh__congbao-58891.pdf` | 831399 | `f5b6c20da0d4f99e8fba32114d21c02011069d82d97e80b0ce8968a50c476234` |
| `blhs-2015__vbhn-135-2025-vpqh__congbao-58894.pdf` | 830536 | `84b7b2afda3eb97f6ad1ce158c05afd339197654ed196a04770823f3d64a5ef6` |
| `blhs-2015__vbhn-135-2025-vpqh__luatvietnam.html` | 1747581 | `23fd28bda763354edd84315575be48486a532aa2386ada1584096aeb9998aa1a` |
| `luat-122-2025-qh15__congbao-signed.pdf` | 578020 | `d7ed3ddf521daf234f05be33d4247b0b4118321fa703e5f64ec8b08490af7afd` |
| `luat-122-2025-qh15__congbao.docx` | 72283 | `da1b3752010e23fa085f694f56e8c663675e293a9932372909235331a49f4c43` |
| `luat-122-2025-qh15__luatvietnam.html` | 752328 | `6a7d643956bfb9ac109eb8903234944dde8689522b5d932fae883889ce251e4a` |
| `luat-75-2025-qh15__congbao.doc` | 544256 | `375d6e197e00f7149a860116443546880a6d3e6b65d67e95705e92f703632838` |
| `luat-75-2025-qh15__congbao.pdf` | 314018 | `2e59f02d0fb2822d98c6386e07a9bce272726e379e72c40eb0c3e04ed9e670c6` |
| `luat-duoc-2016__congbao-goc-2016.pdf` | 37125146 | `e05b1ce42e57dbd0dfe5b7bf5f81ee08138d3b1378908e0977bd8abf7c328e62` |
| `luat-duoc-2016__luatvietnam-goc.html` | 2223897 | `4416e24f72c6d91212c520f1e4b9cdadf67638ce228c4c7eb9c614e28a10d63c` |
| `luat-duoc-2016__vbhn-39-2025-vpqh__congbao-p1.doc` | 720896 | `ec14cfc4dc30a0799510bd99f49543da618ae1326f842ac6597c7d437c44794a` |
| `luat-duoc-2016__vbhn-39-2025-vpqh__congbao-p1.pdf` | 746208 | `74ac9f512b1872ea2e9acb4364725fc98697a2818f2270ca2692e4ca05bdffdb` |
| `luat-duoc-2016__vbhn-76-2026-vpqh__congbao-detail.html` | 148104 | `0eb36b52d6703db72e9afc25a510ec1952d9976caedf3e10b6efd520aa8f96f2` |
| `luat-duoc-2016__vbhn-76-2026-vpqh__congbao-signed.pdf` | 1905116 | `61f5ac57014a5be2ddda28f12d2b0d8392e6482d63071e593d2f78656c9616e2` |
| `luat-duoc-2016__vbhn-76-2026-vpqh__luatvietnam.html` | 2205680 | `196cccd9f6494c071f5dc9d1f0cc97f987bb5a2dcf6e6e7d911a3683167f52a0` |
| `luat-quang-cao-2012__congbao-goc-2012.pdf` | 353234 | `70d5c4a05f3830249d56c2fedded59e80fa1c4dc0fabdf4ac0964e67f5d3549f` |
| `luat-quang-cao__vbhn-88-2025-vpqh__congbao.doc` | 249856 | `a8158629ce9fc5bc643fdc0481deedfaf2b0a5b0f7106307aa3ca909fe304d1f` |
| `luat-quang-cao__vbhn-88-2025-vpqh__congbao.pdf` | 649570 | `3e99b0c3b679f94177f7612ab7cab0e7d0088fadd49a3b05729e17bc1ca96676` |
| `luat-quang-cao__vbhn-88-2025-vpqh__luatvietnam.html` | 372678 | `f21bdc0dfc1099d2d35578571f85ed290bb2351b244d03d1423eff1e97364023` |
| `nd-115-2018__congbao.doc` | 835584 | `4db59488e8cee4a7dff1d5d9ddb57b6f77158ab8ce5df7fa978a686c3a11a496` |
| `nd-115-2018__congbao.pdf` | 645964 | `c4d3397b5435f080bbe53ec48cc28d550b8c78d5688f0b46bf79c3701cc09448` |
| `nd-115-2018__luatvietnam.html` | 1073051 | `21605f41a35a2b017496829ec83c068f8e4d1b026cc69eb4216933d7bd2440ac` |
| `nd-115-2018__vbhn-02-2022-byt__luatvietnam.html` | 411989 | `93deebc00a3b8fb4b7e37f4b375041f9820a40a569b66191384a14320225578d` |
| `nd-124-2021__congbao.doc` | 771072 | `c5b2bf5fc5d9a25ef8ebec8fe3ad2a85724cf89e6e8753ac839c5b13b37a2193` |
| `nd-124-2021__congbao.pdf` | 880938 | `b1dad4ab3e1960f3e8b2718608e41998f91bce64250da0b2d5cb2fd2b010adea` |
| `nd-124-2021__luatvietnam.html` | 964422 | `31e33aa6144fc449167f75380d321fab6b8334ad819f48c5b183fd6bfcffedc8` |
| `nd-15-2018__congbao.doc` | 1163264 | `ff7b51dd1154fb1fcd6af30486bf207392248270d3093f4d01001dd8cf22695c` |
| `nd-15-2018__congbao.pdf` | 807646 | `9dec41b53cb1568a50fc3a98b41a95df2e6595341e5dd8dcf5926d22dde4b1b2` |
| `nd-15-2018__luatvietnam.html` | 1161122 | `2ef7a16a4bae7d9af1f809dc44fb34367eeb7d2a92690afb1fa1f1a3ebd4923f` |
| `nd-248-2026__congbao-detail.html` | 149056 | `ff59981b4fe25e88db98b73122c0761f1bf8173c835b785b8373f9098a7102d8` |
| `nd-248-2026__congbao-signed.pdf` | 1701095 | `e5bace31e4f5820d8ac7847e7b2eed7d52e2a57b8314b7c1260ede11fb349693` |
| `nd-248-2026__luatvietnam.html` | 1609662 | `6351a28589912e6c8ea166175a52107996ac33e505cc8d49fcee96e239a298b5` |
| `nd-342-2025__congbao-signed.pdf` | 781685 | `c6878dc1fd2755ae0975c581182540d06cb1da80ae63e430465b0144931fb3c3` |
| `nd-342-2025__congbao.docx` | 97818 | `81121bed039928dff6805974765970f67047e3cc7afd2ac829564565666dea3a` |
| `nd-342-2025__luatvietnam.html` | 627509 | `59e289e14f6270caae7807c61f6ee6f306747e087734f48752cd3f628361ebbe` |
| `nd-87-2026__congbao-detail.html` | 149004 | `79baef9c9eb8f57a8885f46837741796db2ad76aaf8efb5d9522cb7af70e54fb` |
| `nd-87-2026__congbao-signed.pdf` | 1199649 | `89d3ba1f60b2e1382173c0e3a995b68725c797f7b476bd0906b6e7f06554ce2a` |
| `nd-87-2026__luatvietnam.html` | 2040280 | `41e8e069be34a2749de092f8dcfb7c94e20753e2004338c17cff6f1b0b3d30c0` |
| `status__nd-115-2018__congbao-search-2026-10-23.json` | 439773 | `4d79cc135e8f76eeca9cd2a057646bfb1695aa6ca951b26b011348f7bf69477a` |
| `status__nd-147-2025__congbao.pdf` | 593643 | `1d31abf946a1ea7a873f7df9a16e36b090a5e38f2d48335a2e85b76f5029c57e` |
| `status__nd-148-2025__congbao-p1.pdf` | 739479 | `8946af0d6eda9f9bef6348e0eedaa401897f2b2828888c3269369bb88e069ee9` |
| `status__nd-148-2025__congbao-p2.pdf` | 678132 | `61b58f16cb751134133df1b5e5e905d40bc2eba55341b9981ba9cb34f59fe03b` |
| `status__nd-46-2026__congbao.docx` | 225231 | `de25d466542968e06f326cd8af1340785845dca03b670559b3e79a50ab52c1eb` |
| `status__nq-09-2026-nq-cp__congbao.docx` | 32508 | `221335f5d141e35955843623c961950be32f1f1ddfe545c27ae7e58e4a1cf0fd` |
| `status__nq-15-2026-nq-cp__congbao-detail.html` | 150351 | `545e61fad52b024da075008a04a6393ff9b4ea31693a590325ea93799fc7fe18` |
| `status__nq-15-2026-nq-cp__congbao-signed.pdf` | 592776 | `f76f585b4a3066bf9ae1511deff62690bf03fc88eca3eeddfc1fb922543689ec` |
| `status__nq-21-2026-nq-cp__congbao-signed.pdf` | 937930 | `5fede70adab1500693534a00e7fc3d78ff6e1ed413e5da72e0114e5a60e2c334` |

# Kera: bản tin video có trích âm thanh livestream gốc

Lấy ngày 22/10/2026 từ máy ở VN. Chỉ đọc trang xem video công khai và phụ đề tự động qua `youtube-transcript-api` (1.2.4). Không tải video hay audio. JSON thô (siêu dữ liệu và phụ đề có mốc thời gian) nằm ở `_raw/youtube/yt_<id>.json`.

Người nói ghi theo vai: [KOL 1] là KOL nam, chủ phiên live; [KOL 2] là KOL nữ, chủ phiên live; [KOL 3] là hoa hậu, khách mời.

## Đọc trước khi dùng

- Mọi câu dưới đây là **phụ đề tự động (ASR) của YouTube**, chưa có người nghe lại. Phụ đề có lỗi chính tả, ví dụ "chất sơ" thay cho "chất xơ", "kê ra" thay cho "Kera".
- Việc một đoạn là **tiếng livestream gốc** (chứ không phải giọng phát thanh viên) là **suy luận từ chữ**: xưng "mình", gọi "mọi người", có "nha/nhá/luôn đấy", nằm ở đầu bản tin trước lời dẫn, và nội dung khớp câu báo chí đã trích. **Phải nghe để xác nhận**, kể cả xác nhận ai đang nói.
- Không đoán người nói trong clip. Cột "Người nói" ghi `[không rõ]` khi bản tin không nói rõ.
- **YouTube chặn IP (`IpBlocked`) sau 12 video ngày 22/10.** Thử lại sau khoảng 20 phút vẫn bị chặn. Các video ở mục 4 chưa được kiểm tra.

## 1. Clip có tiếng livestream gốc (suy luận từ phụ đề)

| # | Video | Kênh | Đăng | Dài | Mốc | Dài đoạn | Người nói | Phụ đề tự động (nguyên văn ASR) | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|
| A1 | https://www.youtube.com/watch?v=URORib01rbA | Báo Thanh Niên | 07/04/2025 | 12:05 | **00:00.0 – 00:20.3** | ~20 s | [không rõ] (có thể 2 giọng, câu "Đúng rồi" ở 00:10.9 giống lời đáp) | "Từng cái loại rau củ ở đây á, mọi người, sẽ được xuất phát từ Đà Lạt và đạt chuẩn VietGAP, mọi người nhá. Và thực chất Kera là có sử dụng một cái công nghệ là sấy thăng hoa để có thể giữ được dưỡng chất của rau củ nha, mọi người. Đúng rồi. Rau của nó là như một viên là mình nói đấy, một đĩa rau của mọi người đang ăn đấy. Tại vì thực chất là cái một viên này ấy, một viên này nó sẽ tương ứng với một đĩa rau." | Đoạn liền dài nhất (~20 s), mở đầu bản tin nên khả năng cao là tiếng gốc. Phụ đề có dấu câu và ít lỗi, gợi ý giọng rõ. Chứa 3 loại claim: nguồn gốc (Đà Lạt, VietGAP), công nghệ (sấy thăng hoa), tương đương "một đĩa rau". Chưa nghe kiểm tra nhạc nền. |
| A2 | https://www.youtube.com/watch?v=URORib01rbA | Báo Thanh Niên | 07/04/2025 | 12:05 | **03:58.4 – 04:04.9** | ~6,5 s | [không rõ] | "Một viên này ấy thì nó sẽ nó sẽ tương ứng với một đĩa rau luộc, đĩa rau luộc thông thường của mọi người hay ăn ấy." | Ngắn. Khớp ý câu kera-q-001/q-002 của [KOL 1]. |
| B1 | https://www.youtube.com/watch?v=EoMCBfIr6Y4 | VTV24 | 12/03/2025 | 13:12 | **00:02.8 – 00:12.9** | ~10 s | [không rõ], có thể 2 giọng | "Một ngày chỉ cần ăn hai đến ba viên là có thể là bổ sung chất xơ cho một người bình thường luôn. Một hộp này là một bó rau luôn đấy. Một bó rau luộc của mọi người là một đĩa rau luôn đấy." (00:00.0 "Quảng cáo là" có lẽ là lời dẫn) | Dưới 20 s. Nội dung khớp kera-q-022 ([KOL 3] đáp "Một ngày chỉ cần ăn 2-3 viên…") và kera-q-007/q-008 ([KOL 1] "bó rau"). Đoạn 00:24–00:31 sau đó là sản phẩm khác (yến), **không dùng**. |
| C1 | https://www.youtube.com/watch?v=adrRcdXl9ho | Báo Thanh Niên | 24/02/2025 | 8:35 | **00:02.1 – 00:13.7** | ~11,5 s | [không rõ] | "[âm nhạc] mọi người một ngày thì quy định của nó là cũng là tầm hai ba viên thôi mà Cái này là ba tuổi đ lên ă được nhá mọi người xem xét về cái sản phẩm này để mua cho con cái với là cho những người mà gọi là k ăn rau" | Có nhạc nền (ASR ghi [âm nhạc]), ngắn. Nội dung đáng chú ý: liều "hai ba viên" và "ba tuổi trở lên". |
| C2 | https://www.youtube.com/watch?v=P5MTIDtDoxM | Báo Thanh Niên | 07/03/2025 | 7:53 | **03:55.8 – 04:08.7** | ~13 s | [không rõ] | "sau mọi người một ngày thì quy định của nó là cũng là tầm hai ba viên thôi mà Cái này là ba tuổi tr Lên M ăn được nhá Giờ mọi người xem xét về cái sản phẩm này để mua cho con cái với là cho những người mà gọi là ké ăn rau" | Cùng đoạn C1, phát lại trong bản tin khác. |

**Tóm tắt:** chỉ A1 (URORib01rbA, 00:00–00:20) có tiếng gốc chạy liền khoảng 20 giây. Các clip còn lại ngắn hơn hoặc có nhạc nền.

## 2. Clip phát biểu sau sự việc (họp báo, phiên tòa), không phải livestream

Vẫn là phụ đề tự động và chưa nghe lại.

| # | Video | Kênh | Đăng | Mốc | Người nói (theo lời dẫn) | Phụ đề tự động | Ghi chú |
|---|---|---|---|---|---|---|---|
| D1 | https://www.youtube.com/watch?v=duMFht7DXRw | VTC NEWS | 14/03/2025 | **01:20.9 – 01:35.6** (~15 s) | [KOL 1], họp báo 14/3/2025 (lời dẫn ở 01:14 giới thiệu đây là lời [KOL 1]) | "Tôi nghĩ thuật ngữ của mình trên livestream gây hiểu lầm về thông tin sản phẩm với khách hàng công chúng trong thời gian vừa qua tôi xin lỗi vì sơ suất sử dụng sai hai thuật ngữ kẹo K bổ sung dinh dưỡng từ rau xanh tại vì thành phần chính của K là từ rau" | Có lẽ là tiếng gốc vì câu lặp lại sau lời dẫn. |
| D2 | https://www.youtube.com/watch?v=duMFht7DXRw | VTC NEWS | 14/03/2025 | **00:40.8 – 00:49.6** (~9 s) | [KOL 1] (có thể là lời dẫn đọc lại) | "kẹo kera không thay thế được rau khi chúng ta ăn rau cùng kẹo kera sẽ bổ sung dinh dưỡng cho cơ thể của chúng ta tôi chưa từng nói sản phẩm này thay thế được rau trên mạng xã hội" | Câu "không thay thế được rau… bổ sung dinh dưỡng" hợp với phân loại thực phẩm bổ sung. Đã có trong `cases/candidates.jsonl` (kera-010). |
| D3 | https://www.youtube.com/watch?v=S6pwLTCqU_A | Báo Thanh Niên | 19/11/2025 | **00:00.0 – 00:08** | hỏi đáp tại phiên tòa; người trả lời là [KOL 3] theo tiêu đề và lời dẫn | "Một ngày bị cáo sử dụng bao nhiêu sản phẩm? >> Đúng theo liều khuyến cáo sử dụng là hai ba viên một ngày ạ. >> Ồ. Tại sao bị cáo lại sử dụng kẹo kera ra? >> Tại vì bị cáo không biết ăn rau." | Gián tiếp cho thấy có "liều khuyến cáo 2–3 viên/ngày", nhưng chưa thấy chữ này in trên nhãn. Ở 02:50 lời dẫn nói: "toàn bộ thông tin mà bị cáo [KOL 3] nói trên các phiên livestream đều là kịch bản có sẵn" (tên đã thay bằng vai). |

## 3. Bản tin đã đọc phụ đề, không thấy tiếng livestream

Các bản tin này chỉ có lời dẫn hoặc phỏng vấn chuyên gia. Không dùng cho clip ASR.

| Video | Kênh | Đăng | Dài | Ghi chú |
|---|---|---|---|---|
| https://www.youtube.com/watch?v=MLGRZEWy3hM | Báo Sức khỏe & Đời sống | 06/03/2025 | 9:17 | lời dẫn và chuyên gia |
| https://www.youtube.com/watch?v=4-AeN8paS5I | Báo Sức khỏe & Đời sống | 06/03/2025 | 8:33 | lời dẫn; đọc lại bài xin lỗi ngày 24/2 của [KOL 1] (05:22–05:45) |
| https://www.youtube.com/watch?v=pLsQlbxnq3s | Báo Pháp Luật TP HCM | 07/03/2025 | 11:37 | lời dẫn |
| https://www.youtube.com/watch?v=_mU5LnZgZjk | Chuyển động 24h | 07/03/2025 | 13:46 | bản tin tổng hợp; đoạn Kera ngắn, chỉ có lời dẫn |
| https://www.youtube.com/watch?v=LKihZlBbgaI | VTV24 | 05/04/2025 | 11:29 | bình luận cuối tuần |
| https://www.youtube.com/watch?v=XBuJKFnEx1o | VTV24 | 06/04/2025 | 13:15 | phỏng vấn đại diện cơ quan điều tra; 05:57 có câu thuật lại "một viên kẹo tương ứng với một đĩa rau cần tây" (lời người được phỏng vấn) |
| https://www.youtube.com/watch?v=eXSqIsCx1co | VTC NEWS | 07/09/2025 | 11:33 | lời dẫn đọc kết luận điều tra |
| https://www.youtube.com/watch?v=piW25h2VSMk | VTC NEWS | 09/09/2025 | 10:16 | lời dẫn đọc kết luận điều tra (05:27–05:50 đọc lại câu của [KOL 1] và [KOL 3]) |
| https://www.youtube.com/watch?v=lBmIVXfIVW4 | Cần Thơ - Báo & PTTH | 05/09/2025 | 3:25 | lời dẫn |
| https://www.youtube.com/watch?v=vpjurGthF0Q | Nguyễn Duy Cương (kênh bác sĩ, không phải báo) | 17/03/2025 | 4:07 | bình luận chuyên môn |

## 4. Chưa kiểm tra được (YouTube chặn IP lúc lấy phụ đề)

Danh sách lấy từ trang tìm kiếm YouTube công khai ngày 22/10/2026. Ngày đăng ở đây là ngày tương đối do trang tìm kiếm hiển thị. Tiêu đề rút gọn, tên người thật thay bằng "…" hoặc vai; tiêu đề đầy đủ xem file kết quả tìm kiếm. Tiêu đề gợi ý các video này có thể chứa đoạn livestream. Nên thử lại `yt_fetch.py` sau vài giờ hoặc từ IP khác:

| Video | Kênh | Dài | Tiêu đề (rút gọn) |
|---|---|---|---|
| https://www.youtube.com/watch?v=vs91twQkahY | Báo Thanh Niên (đăng 07/09/2025) | 6:28 | "Dành tặng kẹo Kera cho [KOL 3]"… (tiêu đề đầy đủ ở SOURCES.md) (đã lấy được siêu dữ liệu, chưa có phụ đề) |
| https://www.youtube.com/watch?v=JbggegfpsM8 | Tạp chí Diễn đàn doanh nghiệp | 5:10 | Ngay sau phiên livestream bán kẹo Kera thu về 400 triệu… |
| https://www.youtube.com/watch?v=C7cTPGKYYwc | Báo Người Lao Động | 11:17 | Sau livestream 400 triệu, Hoa hậu … đề nghị tăng cổ phần |
| https://www.youtube.com/watch?v=tTmFFVbk0w8 | VTC NEWS | 21:00 | … đòi tăng cổ phần Kẹo Kera sau khi bán được 400 triệu chỉ qua 1 livestream |
| https://www.youtube.com/watch?v=djllXAP0z1A | VTC NEWS | 18:31 | Người viết kịch bản khiến … "diễn" lừa 17,5 tỷ là ai? |
| https://www.youtube.com/watch?v=NdBdazT59PE | VTC NEWS | 19:07 | Chiêu 've sầu thoát xác' … |
| https://www.youtube.com/watch?v=bNNhYSmNrkA | Báo Thanh Niên | 14:12 | Hoa hậu … khai gì khi hưởng lợi 7 tỉ đồng từ kẹo rau Kera? |
| https://www.youtube.com/watch?v=Va1PMEoCbSo | Báo Pháp luật Việt Nam | 12:17 | Một TikToker đình đám 'sập bẫy' kẹo rau củ Kera… |
| https://www.youtube.com/watch?v=m82wh6czXCg | Báo Dân Việt | 10:22 | Công bố kết quả kiểm nghiệm viên kẹo rau củ Kera… |
| https://www.youtube.com/watch?v=FpGuNci88sc | Tiền Phong TV | 11:31 | TikToker nổi tiếng bất ngờ xin lỗi… |
| https://www.youtube.com/watch?v=MWzTm2SrqWE | Tiền Phong TV | 11:05 | Bất ngờ trước thông tin 'cực sốc' về kẹo rau củ… |
| https://www.youtube.com/watch?v=7Dw3Fw2nwzU | VTC NEWS | 10:37 | … kiếm bao nhiêu nhờ bán kẹo Kera? |
| https://www.youtube.com/watch?v=b1Ns9ljokic | VTC NEWS | 9:26 | … Bộ Công an công bố thành phần kẹo Kera… |
| https://www.youtube.com/watch?v=X4TJx1gXals | Báo Pháp Luật TP HCM | 28:58 | Tin nóng 9-3: Tiết lộ bằng chứng … 'kẹo rau' Kera |
| https://www.youtube.com/watch?v=WPug1iYGkOk | VTV24 | 2:58 | Kẹo rau củ Kera chứa chất tạo ngọt Sorbitol nhưng không ghi trên nhãn |
| https://www.youtube.com/watch?v=PKjBV9YMDE0 | VTV24 | 2:28 | Bán kẹo Kera lợi nhuận hơn 17 tỷ đồng… |
| https://www.youtube.com/watch?v=iSVTPSQdb6o | VTV24 | 42:00 | TSTC tối 15/3: Từ vụ kẹo rau củ Kera… |
| https://www.youtube.com/watch?v=rWnB9kPZJE0 | VTV24 | 36:53 | Thời sự toàn cảnh tối 20/3… |
| https://www.youtube.com/watch?v=BUXuLYVnITQ | VTV24 | 29:28 | TSTC 4/4: … bắt tạm giam … |
| https://www.youtube.com/watch?v=MqhtTTbs0Zc | VTV24 | 29:02 | TSTC 19/5: … bị khởi tố |
| https://www.youtube.com/watch?v=03FRGCPKgJ8 | Chuyển động 24h | 9:05 | Bị can … khai gì khi bị bắt… |
| https://www.youtube.com/watch?v=au3JOJY7HX8 | Chuyển động 24h | 8:43 | Đề nghị truy tố 5 bị can vụ kẹo Kera… |
| https://www.youtube.com/watch?v=jcehkukPfU0 | Báo Tuổi Trẻ | 1:30 | … 'bỏ túi' gần 7 tỉ đồng… |
| https://www.youtube.com/watch?v=VWYaPHoRqRo | Báo Tuổi Trẻ | 1:09 | … nhận sai khi quảng cáo lố kẹo rau củ Kera… |
| https://www.youtube.com/watch?v=u58LSsHj3FQ | Báo Pháp Luật TP HCM | 9:20 | Sự thật về chất trong kẹo rau củ Kera không được ghi trên nhãn |

## 5. Cách lấy lại

Script lấy phụ đề: `tools/yt_fetch.py`. Cách chạy: `python -I -X utf8 tools/yt_fetch.py <thư_mục_ra> <id1> <id2> …` (cần `pip install --user youtube-transcript-api requests`). Script không tải video/audio, và tự dừng khi YouTube chặn IP.

- Tìm video: `yt_search.py <out.jsonl> "truy vấn" …` đọc trang `youtube.com/results` công khai. Kết quả ngày 22/10 nằm ở `ytsearch.jsonl` cùng thư mục.
- Lấy siêu dữ liệu và phụ đề: `yt_fetch.py <out_dir> <id…>`. Script tự dừng khi gặp `IpBlocked` và không vượt chặn.
- Xem phụ đề theo mốc thời gian: `yt_dump.py <json> [giây/dòng] [từ] [đến]`. Tìm đoạn có dấu hiệu tiếng livestream: `yt_fp.py <dir>`.

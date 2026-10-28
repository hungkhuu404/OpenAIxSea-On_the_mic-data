# Thử ASR tiếng Việt

**Mục đích:** chọn cấu hình ASR **trước** D-Day. Đây là thử nghiệm giảm rủi ro, được build trước và **không được chấm**.

**Trạng thái (21/10):**
- Script đã chạy hết luồng trên mock server cục bộ. Đã kiểm: cắt audio, multipart UTF-8, lỗi 400, chế độ hybrid, báo cáo, `--dry-run`.
- **Chưa gọi API thật**, vì máy soạn chưa có `OPENAI_API_KEY` và chưa có video.

## Chạy

```powershell
python -m pip install --user requests imageio-ffmpeg   # hoặc có sẵn ffmpeg trên PATH
$env:OPENAI_API_KEY = "sk-..."                          # key của một thành viên
# 1) Kiểm setup, không tốn tiền
python asr_probe.py "D:\path\video.mp4" --start 300 --duration 120 --dry-run
# 2) Chạy thật: 6 cấu hình × 2 phút ≈ $0.06
python asr_probe.py "D:\path\video.mp4" --start 300 --duration 120
# 3) Sửa tay runs\<thời điểm>\reference.todo.txt cho đúng từng chữ, lưu thành ref.txt, rồi chạy lại để có CER
python asr_probe.py "D:\path\video.mp4" --start 300 --duration 120 --reference ref.txt
```

- Chọn đoạn 2 phút **khó nhất** của video: có nhạc nền, hai người nói, có tên sản phẩm và câu công dụng. Không chọn đoạn chào hỏi.
- Sửa `keywords.txt` theo video: tên SKU, hoạt chất, các cụm bắt buộc.
- Nếu một biến thể trả HTTP 400, đọc lỗi trong `report.md`, sửa tên tham số trong `variants.json`, rồi chạy lại với `--only <id>`. Tên tham số của `gpt-transcribe` **chưa được xác minh**.

## Sáu cấu hình

| id | Model | Trả lời câu hỏi gì |
|---|---|---|
| `diarize_vi` | `gpt-4o-transcribe-diarize`, `language=vi` | **Mã `vi` có được nhận không?** Có người nói + timestamp |
| `diarize_auto` | như trên, tự nhận ngôn ngữ | Dự phòng nếu `vi` bị từ chối |
| `transcribe_vi` | `gpt-transcribe` | Chất lượng chữ của model khuyến nghị (không có người nói) |
| `transcribe_vi_kw` | `gpt-transcribe` + `keywords` | Tên SKU, hoạt chất có ra đúng không |
| `whisper_vi_ts` | `whisper-1` `verbose_json` | Dự phòng: có timestamp theo segment, không có người nói (deprecated) |
| `hybrid_kw` | Lượt nói và timestamp lấy từ diarize; chữ của mỗi lượt chép lại bằng `gpt-transcribe` + keywords | Ghép điểm mạnh của hai model |

## Báo cáo đo gì

- **Syllable ER** (tỉ lệ lỗi theo âm tiết; tiếng Việt tách âm tiết bằng dấu cách), **CER**, và CER khi bỏ dấu. Chỉ tính khi có `--reference`.
- **Keyword hits**: khớp đúng dấu / khớp khi bỏ dấu.
- Số segment, số người nói, có timestamp không, độ trễ, chi phí ước tính.

## Quy tắc ra quyết định [KN, ngưỡng do đội tự đặt, không phải chuẩn ngành]

| Kết quả | Quyết định |
|---|---|
| `diarize_*` đạt syllable ER ≤ 20%, keyword hits ≥ 80%, người nói tách hợp lý (kiểm tay 5 lượt) | **Chỉ dùng diarize.** Pipeline đơn giản nhất |
| Chữ của diarize kém (ER > 20%) nhưng `hybrid_kw` đạt | **Hybrid.** Phải tính thêm chi phí: số lời gọi bằng số lượt nói |
| Mọi cấu hình đều có ER > 35% | **Không cấu hình nào đủ dùng** cho audio này: dùng transcript sửa tay |
| `vi` bị từ chối ở mọi model | Dùng tự nhận ngôn ngữ |

## Không đưa lên repo public

- `runs/` chứa audio cắt từ video của shop thật. **Không commit** (đã có `.gitignore`).
- Chỉ commit `report.md` sau khi đã che tên shop và tên người, kèm cấu hình đã chọn.

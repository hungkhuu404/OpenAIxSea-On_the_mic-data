# Hàm chuẩn hoá cho kiểm tra "docstring là substring nguyên văn"

Áp dụng cho: kiểm tra trong CI (docstring của predicate phải là chuỗi con của file luật), cột `text` trong `index.json`, và trường `body_sha256` trong front matter.

## Định nghĩa (theo đúng thứ tự)

1. **Unicode NFC.** Gộp các ký tự tiếng Việt đang ở dạng tổ hợp (NFD) về dạng dựng sẵn.
2. **Ngoặc kép cong thành ngoặc thẳng.** `“ ” „ ‟ ″ « »` thành `"`. Ngoặc đơn cong `‘ ’ ‚ ‛ ′` thành `'`.
3. **Gạch ngang thành `-`.** Các ký tự `‐ ‑ ‒ – — ― −` (U+2010 đến U+2015, U+2212) đều đổi thành `-` (U+002D).
4. **Xoá ký tự vô hình.** Bỏ U+200B, U+200C, U+200D, U+2060, U+FEFF (BOM) và U+00AD (soft hyphen).
5. **Dấu ba chấm.** `…` (U+2026) đổi thành `...`.
6. **Gộp khoảng trắng.** Mọi chuỗi khoảng trắng Unicode (`\s+` của Python `re`: dấu cách, tab, xuống dòng, NBSP U+00A0, U+2000 đến U+200A, U+3000…) gộp thành **một dấu cách**, rồi `strip()` hai đầu.

**Những gì hàm này KHÔNG làm** (cố ý, để không làm sai lệch nguyên văn):
- **Không** đổi chữ hoa/thường. Ví dụ: Luật QC Điều 15a khoản 3 điểm b bắt đầu bằng "Thông báo", **T hoa**.
- **Không** thống nhất kiểu bỏ dấu thanh. `hoá`/`hóa`, `khoẻ`/`khỏe`, `thuỷ`/`thủy` là các chuỗi khác nhau. Corpus chứa **cả hai kiểu**, đúng như văn bản gốc. Ví dụ: NĐ 342/2025 Điều 5 khoản 2 viết "bảo vệ sức khoẻ" ở vế đầu nhưng viết "Thực phẩm bảo vệ sức khỏe" trong ngoặc kép. NĐ 87/2026 Điều 68 viết "hàng hoá, dịch vụ đặc biệt". Docstring phải chép đúng kiểu bỏ dấu trong file.
- **Không** sửa lỗi chính tả có trong văn bản gốc. Ví dụ: NĐ 87/2026 Điều 53 khoản 3 điểm b viết "kề từ"; NĐ 15/2018 viết "bác sỹ", "dược sỹ".
- **Không** bỏ dấu câu. Dấu `;`, `.`, `:` ở cuối khoản/điểm vẫn là một phần của chuỗi.

## Tham chiếu Python (5 dòng, đã kiểm cho kết quả trùng với script build trên cả 26 file)

```python
import re, unicodedata
_T = str.maketrans({**dict.fromkeys("“”„‟″«»", '"'), **dict.fromkeys("‘’‚‛′", "'"), **dict.fromkeys("‐‑‒–—―−", "-"), **dict.fromkeys("​‌‍⁠﻿­", None)})
def normalize(s: str) -> str:
    s = unicodedata.normalize("NFC", s).translate(_T).replace("…", "...")
    return re.sub(r"\s+", " ", s).strip()
```

Kiểm tra substring: `normalize(docstring_quote) in normalize(law_body)`.

## Quy ước dùng trong CI

- **Phần body của file.** Là toàn bộ nội dung nằm sau dòng `---` đóng front matter. Front matter không thuộc body, nên không được khớp vào đó.
- **`body_sha256`** = `hashlib.sha256(normalize(body).encode("utf-8")).hexdigest()`. Nếu sha không khớp thì file luật đã bị sửa tay.
- **Ranh giới khoản/điểm.** Trong file, mỗi khoản/điểm là một đoạn, các đoạn cách nhau bằng một dòng trống. Sau chuẩn hoá, ranh giới này chỉ còn là một dấu cách. Vì vậy một câu trích dài qua hai điểm liên tiếp vẫn khớp. Không được ghép hai đoạn không liền nhau.
- **Lược bỏ bằng `…`.** Nếu docstring dùng `…` hoặc `...` để đánh dấu chỗ lược bỏ, CI phải tách theo dấu đó rồi kiểm **từng mảnh**. Mỗi mảnh phải là substring, và các mảnh phải xuất hiện đúng thứ tự trong cùng một file. Không được kiểm cả chuỗi có dấu lược.
- **Tham chiếu anchor.** Nên tham chiếu bằng `id` trong `index.json`, ví dụ `ND87-2026/D71/K2/b`. Trường `text` của anchor là nguyên văn khoản/điểm, các đoạn nối với nhau bằng `\n`.
  - Anchor khoản (`.../K5`) chứa cả các điểm thuộc khoản đó.
  - Anchor điểm (`.../K5/b`) chứa thêm các đoạn không đánh số nằm giữa điểm đó và điểm kế tiếp.
  - Với điểm cuối của một khoản, anchor điểm chỉ chứa thêm các dòng gạch đầu dòng (`- …`). Đoạn không đánh số đứng sau điểm cuối chỉ thuộc anchor khoản.
  - `.../intro` là đoạn dẫn không đánh số nằm trước khoản 1.
  - Anchor điều (`.../D27`) là toàn bộ điều, kể cả dòng tên điều.

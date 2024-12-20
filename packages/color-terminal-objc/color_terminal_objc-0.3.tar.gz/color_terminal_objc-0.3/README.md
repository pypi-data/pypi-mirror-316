# color_terminal_objc - Thư viện Python đơn giản để in màu trong terminal

`color_terminal_objc` là một thư viện Python cho phép bạn in văn bản với các màu sắc khác nhau cho văn bản và nền trong terminal. Thư viện này cung cấp một giao diện đơn giản để thêm màu vào các ứng dụng dòng lệnh của bạn.

## Cài đặt

### Cài đặt thông qua `pip`

Để cài đặt thư viện `color_terminal_objc`, bạn có thể sử dụng `pip` trực tiếp từ terminal:

```bash
pip install color_terminal_objc
```
Điều này sẽ cài đặt phiên bản mới nhất của thư viện cùng với các phụ thuộc.

Cách sử dụng
Sau khi cài đặt thư viện, bạn có thể dễ dàng sử dụng nó để in các thông báo với màu sắc khác nhau trong terminal. Đây là cách bạn có thể sử dụng thư viện trong mã Python của mình:

Ví dụ
```python
# Nhập thư viện color_terminal_objc
import color_terminal_objc

# In các thông báo với màu văn bản khác nhau
color_terminal_objc.red("Đây là thông báo màu đỏ")
color_terminal_objc.green("Đây là thông báo màu xanh lá")
color_terminal_objc.yellow("Đây là thông báo màu vàng")
color_terminal_objc.blue("Đây là thông báo màu xanh dương")
color_terminal_objc.purple("Đây là thông báo màu tím")
color_terminal_objc.cyan("Đây là thông báo màu cyan")
color_terminal_objc.white("Đây là thông báo màu trắng")
color_terminal_objc.black("Đây là thông báo màu đen")
color_terminal_objc.gray("Đây là thông báo màu xám")
color_terminal_objc.brown("Đây là thông báo màu nâu")
# Đặt lại màu sắc về mặc định
color_terminal_objc.reset("Đây là thông báo với màu mặc định")
```
Các phương thức có sẵn
Dưới đây là danh sách tất cả các phương thức có sẵn mà bạn có thể sử dụng để in các thông báo với màu sắc:

Phương thức màu văn bản:
```python
color_terminal_objc.red(message)
```
Mô tả: In thông báo với màu đỏ.
```python
color_terminal_objc.green(message)
```
Mô tả: In thông báo với màu xanh lá.
```python
color_terminal_objc.yellow(message)
```
Mô tả: In thông báo với màu vàng.
```python
color_terminal_objc.blue(message)
```
Mô tả: In thông báo với màu xanh dương.
```python
color_terminal_objc.purple(message)
```
Mô tả: In thông báo với màu tím.
```python
color_terminal_objc.cyan(message)
```
Mô tả: In thông báo với màu cyan.
```python
color_terminal_objc.white(message)
```
Mô tả: In thông báo với màu trắng.
```python
color_terminal_objc.black(message)
```
Mô tả: In thông báo với màu đen.
```python
color_terminal_objc.gray(message)
```
Mô tả: In thông báo với màu xám.
```python
color_terminal_objc.brown(message)
```
Mô tả: In thông báo với màu nâu.
Đặt lại màu sắc:
```python
color_terminal_objc.reset(message)
```
Mô tả: Đặt lại màu sắc về mặc định.
Kết quả ví dụ
Khi bạn chạy đoạn mã ví dụ trên, terminal của bạn sẽ hiển thị các thông báo với màu sắc như sau (màu sắc sẽ thay đổi tùy thuộc vào cấu hình của terminal):

"Đây là thông báo màu đỏ" sẽ xuất hiện với màu đỏ.
"Đây là thông báo màu xanh lá" sẽ xuất hiện với màu xanh lá.
"Đây là thông báo màu vàng" sẽ xuất hiện với màu vàng.
"Đây là thông báo với nền màu đỏ" sẽ có nền đỏ và văn bản màu trắng.
Bằng cách sử dụng thư viện này, bạn có thể dễ dàng thêm màu vào các thông báo trong terminal để làm nổi bật thông tin và cải thiện trải nghiệm người dùng.

### Giải thích:

- **Các phương thức màu sắc (text color)**: Bao gồm các màu như đỏ, xanh lá, vàng, xanh dương, tím, cyan, trắng, đen, xám, nâu.
- **Các phương thức nền màu (background color)**: Các phương thức cho phép bạn thay đổi nền của văn bản với các màu sắc tương tự.
- **Phương thức reset**: Đặt lại màu sắc về mặc định của terminal.

Với cách sử dụng này, bạn có thể tạo các thông báo trong terminal có màu sắc và nền khác nhau để làm nổi bật thông tin.
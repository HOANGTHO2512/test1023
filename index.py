import tkinter as tk
import sqlite3
from tkinter import messagebox # Import thư viện messagebox để hiển thị thông báo pop-up

# --- Cấu hình Cơ sở dữ liệu SQLite ---

# Kết nối đến cơ sở dữ liệu có tên 'Student.db'. 
# Nếu file không tồn tại, nó sẽ được tạo mới.
conn = sqlite3.connect('Student.db')
cursor = conn.cursor() # Tạo đối tượng cursor để thực thi các lệnh SQL

# Tạo bảng DB_student nếu nó chưa tồn tại.
# Cột 'db_student_id' được đặt là INTEGER PRIMARY KEY.
cursor.execute('''CREATE TABLE IF NOT EXISTS DB_student (
                    db_student_id INTEGER PRIMARY KEY,
                    db_student_name TEXT)''')
conn.commit() # Lưu thay đổi (tạo bảng) vào database

# --- Định nghĩa các Hàm Chức năng ---

def clear_entries():
    """Xóa nội dung trong các ô nhập liệu sau khi thực hiện xong thao tác."""
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)

def print_student():
    """Lấy dữ liệu từ ô nhập liệu và in ra Console."""
    student_id = entry_id.get()
    student_name = entry_name.get()

    if not student_id or not student_name:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ ID và Tên.")
        return

    # In ra console/terminal
    print('Student ID: {}'.format(student_id))
    print('Student Name: {}'.format(student_name))
    print('-'*30)
    
    messagebox.showinfo("Thông báo", "Đã in thông tin ra Console.")

def create_student():
    """Lấy dữ liệu, chèn vào cơ sở dữ liệu SQLite và hiển thị thông báo."""
    student_id = entry_id.get()
    student_name = entry_name.get().strip().lower() # Lấy tên, loại bỏ khoảng trắng thừa và chuyển thành chữ thường

    if not student_id or not student_name:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ ID và Tên.")
        return

    try:
        # Chèn dữ liệu sinh viên mới vào bảng DB_student
        cursor.execute('INSERT INTO DB_student(db_student_id, db_student_name) VALUES(?,?)', (student_id, student_name))
        conn.commit() # Xác nhận và lưu thay đổi vào database

        # In thông tin đã lưu ra console
        print(f"✅ Đã thêm sinh viên: ID {student_id}, Tên: {student_name}")
        print('-'*30)

        messagebox.showinfo("Thành công", f"Đã thêm sinh viên {student_name} (ID: {student_id}) vào database!")
        clear_entries()

    except sqlite3.IntegrityError:
        # Xử lý lỗi nếu ID sinh viên bị trùng (vì db_student_id là PRIMARY KEY)
        messagebox.showerror("Lỗi", f"ID sinh viên {student_id} đã tồn tại!")
    except Exception as e:
        # Xử lý các lỗi khác
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

def overview_student():
    """Truy vấn tất cả dữ liệu từ database và hiển thị trong một cửa sổ mới (hoặc in ra console)."""
    cursor.execute('SELECT * FROM DB_student')
    overview_data = cursor.fetchall() # Lấy tất cả các hàng dữ liệu

    if not overview_data:
        messagebox.showinfo("Thông báo", "Cơ sở dữ liệu sinh viên đang trống.")
        return

    # In ra console/terminal
    print("\n--- BẢNG SINH VIÊN ---")
    for row in overview_data:
        print(f"ID: {row[0]}, Tên: {row[1]}")
    print("----------------------\n")
    
    # Hiển thị dữ liệu trong một cửa sổ Tkinter đơn giản
    top = tk.Toplevel(root)
    top.title("Tổng quan Sinh viên")
    top.geometry("250x200")
    
    data_text = "ID | Tên\n"
    for row in overview_data:
        data_text += f"{row[0]}  | {row[1]}\n"

    label_overview = tk.Label(top, text=data_text, justify=tk.LEFT, font=('Courier', 10))
    label_overview.pack(padx=10, pady=10)

# --- Cấu hình Giao diện Tkinter (Main Window) ---

root = tk.Tk()
root.title('Ứng dụng Quản lý Sinh viên')
root.geometry('300x400') # Điều chỉnh kích thước cửa sổ lớn hơn một chút

# 1. Nhập Student ID
label_id = tk.Label(root, text='Student ID (Khóa Chính)')
label_id.pack(pady=(15,5)) # độ rộng phía trên 15, phía dưới 5
entry_id = tk.Entry(root, width=25) # độ rộng ô nhập
entry_id.pack()

# 2. Nhập Student Name
label_name = tk.Label(root, text='Student Name')  
label_name.pack(pady=(15,5))
entry_name = tk.Entry(root, width=25)
entry_name.pack()

# --- Các Nút Chức năng ---

# Nút 'Print': Chỉ in dữ liệu ra Console
button_print = tk.Button(root, text='1. In ra Console', command=print_student, width=20)  
button_print.pack(pady=15)

# Nút 'Create': Thêm dữ liệu vào SQLite
button_create = tk.Button(root, text='2. Thêm vào Database', command=create_student, width=20)
button_create.pack(pady=10)

# Nút 'Overview': Xem tất cả dữ liệu từ SQLite
botton_overview = tk.Button(root, text='3. Xem Tổng quan', command=overview_student, width=20)  
botton_overview.pack(pady=10)

# Chạy vòng lặp chính của Tkinter để hiển thị cửa sổ và lắng nghe sự kiện
root.mainloop()

# Đảm bảo đóng kết nối database khi ứng dụng kết thúc
conn.close()
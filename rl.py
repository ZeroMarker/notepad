import tkinter as tk
from tkinter import font, filedialog, messagebox

class VerticalTextEditor:
    LANGUAGES = {
        'en': {
            'file': 'File',
            'new': 'New',
            'open': 'Open',
            'save': 'Save',
            'exit': 'Exit',
            'edit': 'Edit',
            'copy': 'Copy',
            'paste': 'Paste',
            'language': 'Language',
            'saved': 'File saved successfully',
            'unsaved': 'Unsaved changes',
            'confirm_save': 'Save unsaved changes?'
        },
        'zh-CN': {
            'file': '文件',
            'new': '新建',
            'open': '打开',
            'save': '保存',
            'exit': '退出',
            'edit': '编辑',
            'copy': '复制',
            'paste': '粘贴',
            'language': '语言',
            'saved': '文件保存成功',
            'unsaved': '未保存的修改',
            'confirm_save': '是否保存未保存的修改？'
        },
        'zh-TW': {
            'file': '檔案',
            'new': '新增',
            'open': '開啟',
            'save': '儲存',
            'exit': '離開',
            'edit': '編輯',
            'copy': '複製',
            'paste': '貼上',
            'language': '語言',
            'saved': '檔案儲存成功',
            'unsaved': '未儲存的修改',
            'confirm_save': '是否儲存未儲存的修改？'
        },
        'ja': {
            'file': 'ファイル',
            'new': '新規',
            'open': '開く',
            'save': '保存',
            'exit': '終了',
            'edit': '編集',
            'copy': 'コピー',
            'paste': 'ペースト',
            'language': '言語',
            'saved': 'ファイルを保存しました',
            'unsaved': '未保存の変更',
            'confirm_save': '未保存の変更を保存しますか？'
        },
        'ko': {
            'file': '파일',
            'new': '새 파일',
            'open': '열기',
            'save': '저장',
            'exit': '종료',
            'edit': '편집',
            'copy': '복사',
            'paste': '붙여넣기',
            'language': '언어',
            'saved': '파일 저장 성공',
            'unsaved': '저장되지 않은 변경 사항',
            'confirm_save': '저장되지 않은 변경 사항을 저장하시겠습니까?'
        }
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Vertical Text Editor")
        self.current_lang = 'en'

        # 配置参数
        self.font_size = 28
        self.column_width = 60
        self.line_spacing = 10
        self.max_lines = 25
        self.clipboard = ""

        # 初始化数据
        self.reset_data()

        # 界面初始化
        self.init_ui()

    def reset_data(self):
        """重置编辑器数据"""
        self.columns = [[]]  # 从右到左存储，索引0为最右侧列
        self.current_col = 0
        self.cursor_pos = 0
        self.filename = None

    def get_font_family(self):
        """根据当前语言返回合适字体"""
        if self.current_lang in ['ja', 'ko']:
            return "Meiryo"
        elif self.current_lang == 'zh-TW':
            return "MingLiU"
        elif self.current_lang == 'zh-CN':
            return "SimSun"
        return "Arial Unicode MS"

    def init_ui(self):
        # 字体设置
        self.cjk_font = font.Font(
            family=self.get_font_family(),
            size=self.font_size
        )

        # 主画布
        self.canvas = tk.Canvas(self.root, bg="#f0e8d5")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 初始化菜单
        self.init_menu()

        # 事件绑定
        self.root.bind("<Key>", self.on_key_press)
        self.root.bind("<BackSpace>", self.on_backspace)
        self.root.bind("<Configure>", self.redraw)
        self.root.bind("<Control-c>", self.copy_text)
        self.root.bind("<Control-v>", self.paste_text)

        # 光标动画
        self.cursor_visible = True
        self.blink_cursor()
        self.redraw()

    def init_menu(self):
        """初始化多语言菜单系统"""
        self.menubar = tk.Menu(self.root)

        # 文件菜单
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.tr('file'), menu=self.file_menu)

        # 编辑菜单
        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.tr('edit'), menu=self.edit_menu)

        # 语言菜单
        self.lang_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.tr('language'), menu=self.lang_menu)

        # 更新菜单项
        self.update_menu_items()

        self.root.config(menu=self.menubar)

    def tr(self, key):
        """多语言翻译方法"""
        return self.LANGUAGES[self.current_lang].get(key, key)

    def update_menu_items(self):
        """更新多语言菜单内容"""
        # 清除旧菜单项
        self.file_menu.delete(0, tk.END)
        self.edit_menu.delete(0, tk.END)
        self.lang_menu.delete(0, tk.END)

        # 文件菜单
        self.file_menu.add_command(label=self.tr('new'),
                                   command=self.new_file,
                                   accelerator="Ctrl+N")
        self.file_menu.add_command(label=self.tr('open'),
                                   command=self.open_file,
                                   accelerator="Ctrl+O")
        self.file_menu.add_command(label=self.tr('save'),
                                   command=self.save_file,
                                   accelerator="Ctrl+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label=self.tr('exit'),
                                   command=self.root.quit)

        # 编辑菜单
        self.edit_menu.add_command(label=self.tr('copy'),
                                   command=self.copy_text,
                                   accelerator="Ctrl+C")
        self.edit_menu.add_command(label=self.tr('paste'),
                                   command=self.paste_text,
                                   accelerator="Ctrl+V")

        # 语言菜单
        for lang_code in self.LANGUAGES:
            self.lang_menu.add_command(
                label=self.LANGUAGES[lang_code]['language'],
                command=lambda l=lang_code: self.change_language(l)
            )

        # 绑定快捷键
        self.root.bind_all("<Control-n>", lambda e: self.new_file())
        self.root.bind_all("<Control-o>", lambda e: self.open_file())
        self.root.bind_all("<Control-s>", lambda e: self.save_file())

    def change_language(self, lang_code):
        """切换界面语言"""
        self.current_lang = lang_code
        self.cjk_font.configure(family=self.get_font_family())
        self.update_menu_items()
        self.redraw()

    def new_file(self):
        """新建文件"""
        if self.check_unsaved_changes():
            self.reset_data()
            self.redraw()

    def open_file(self):
        """打开文件"""
        if not self.check_unsaved_changes():
            return

        filename = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    lines = f.read().split('\n')
                self.columns = [list(line) for line in reversed(lines)]
                self.current_col = 0
                self.cursor_pos = len(self.columns[0]) if self.columns else 0
                self.filename = filename
                self.redraw()
            except Exception as e:
                messagebox.showerror("Error", f"Open failed: {str(e)}")

    def save_file(self):
        """保存文件"""
        if not self.filename:
            self.filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if not self.filename:
                return

        try:
            text = '\n'.join(''.join(col) for col in reversed(self.columns))
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo(self.tr('saved'), self.tr('saved'))
        except Exception as e:
            messagebox.showerror("Error", f"Save failed: {str(e)}")

    def check_unsaved_changes(self):
        """检查未保存的修改"""
        if any(len(col) > 0 for col in self.columns):
            response = messagebox.askyesnocancel(
                self.tr('unsaved'),
                self.tr('confirm_save')
            )
            if response is None:
                return False
            if response:
                self.save_file()
        return True

    def copy_text(self, event=None):
        """复制选中的文本"""
        if self.columns and self.columns[self.current_col]:
            start = max(0, self.cursor_pos - 1)
            end = self.cursor_pos
            selected = self.columns[self.current_col][start:end]
            self.clipboard = "".join(selected)
            self.root.clipboard_clear()
            self.root.clipboard_append(self.clipboard)

    def paste_text(self, event=None):
        """粘贴文本"""
        try:
            text = self.root.clipboard_get()
        except tk.TclError:
            return

        for char in text:
            self.columns[self.current_col].insert(self.cursor_pos, char)
            self.cursor_pos += 1

            if len(self.columns[self.current_col]) >= self.max_lines:
                self.add_column()

        self.redraw()

    def on_key_press(self, event):
        """处理字符输入事件"""
        if len(event.char) == 0 or event.keysym in ['Up', 'Down', 'Left', 'Right']:
            return

        current_col = self.columns[self.current_col]
        current_col.insert(self.cursor_pos, event.char)
        self.cursor_pos += 1

        if len(current_col) >= self.max_lines:
            self.add_column()

        self.redraw()

    def on_backspace(self, event):
        """处理退格删除事件"""
        if not self.columns:
            return

        current_col = self.columns[self.current_col]

        if self.cursor_pos > 0:
            del current_col[self.cursor_pos - 1]
            self.cursor_pos -= 1
        elif self.current_col > 0:
            self.current_col -= 1
            self.cursor_pos = len(self.columns[self.current_col])

        # 清理空列（保留至少一列）
        self.columns = [col for col in self.columns if col]
        if not self.columns:
            self.add_column()

        self.redraw()

    def redraw(self, event=None):
        """窗口重绘方法"""
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()

        for col_idx, column in enumerate(self.columns):
            x = canvas_width - (col_idx + 1) * self.column_width
            y = self.line_spacing

            self.canvas.create_line(x, 0, x, self.canvas.winfo_height(),
                                    fill="#999", dash=(2, 2))

            for char in column:
                self.canvas.create_text(
                    x - 5, y,
                    text=char,
                    font=self.cjk_font,
                    anchor=tk.NE
                )
                y += self.font_size + self.line_spacing

        self.update_cursor()

    def add_column(self):
        """在左侧添加新列"""
        new_col_idx = self.current_col + 1
        self.columns.insert(new_col_idx, [])
        self.current_col = new_col_idx
        self.cursor_pos = 0

    def update_cursor(self):
        """更新光标位置"""
        self.canvas.delete("cursor")
        if self.cursor_visible and self.columns:
            canvas_width = self.canvas.winfo_width()
            x = canvas_width - (self.current_col + 1) * self.column_width
            y = self.line_spacing + self.cursor_pos * (self.font_size + self.line_spacing)

            self.canvas.create_line(
                x - 10, y - self.font_size,
                x - 10, y,
                fill="red",
                width=2,
                tags="cursor"
            )

    def blink_cursor(self):
        """光标闪烁动画"""
        self.cursor_visible = not self.cursor_visible
        self.update_cursor()
        self.root.after(500, self.blink_cursor)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1400x900")
    editor = VerticalTextEditor(root)
    root.mainloop()
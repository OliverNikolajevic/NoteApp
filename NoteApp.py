import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

class Note:
    def __init__(self, title, content, date=None):
        self.title = title
        self.content = content
        self.date = date if date else datetime.now()

    def __str__(self):
        return f"{self.title} ({self.date.strftime('%Y-%m-%d %H:%M')})"

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NoteApp - Белешки")
        self.notes = []

        self.setup_gui()

    def setup_gui(self):
        # Горен дел со копчиња
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Креирај", command=self.create_note).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Уреди", command=self.edit_note).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Избриши", command=self.delete_note).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Сортирај по датум", command=self.sort_notes).grid(row=0, column=3, padx=5)
        self.note_listbox = tk.Listbox(self.root, width=50)
        self.note_listbox.pack(pady=5)
        self.note_listbox.bind('<<ListboxSelect>>', self.display_note)
        self.note_text = tk.Text(self.root, height=12, width=50, wrap="word")
        self.note_text.pack(pady=5)

    def refresh_listbox(self):
        self.note_listbox.delete(0, tk.END)
        for note in self.notes:
            self.note_listbox.insert(tk.END, str(note))

    def create_note(self):
        def save():
            title = title_entry.get()
            content = content_text.get("1.0", tk.END).strip()
            if title and content:
                note = Note(title, content)
                self.notes.append(note)
                self.refresh_listbox()
                win.destroy()
            else:
                messagebox.showerror("Грешка", "Насловот и содржината се задолжителни.")

        win = tk.Toplevel(self.root)
        win.title("Нова белешка")

        tk.Label(win, text="Наслов:").pack()
        title_entry = tk.Entry(win, width=50)
        title_entry.pack(pady=5)

        tk.Label(win, text="Содржина:").pack()
        content_text = tk.Text(win, height=10, width=50)
        content_text.pack(pady=5)

        tk.Button(win, text="Зачувај", command=save).pack(pady=10)

    def edit_note(self):
        selected = self.note_listbox.curselection()
        if not selected:
            return
        index = selected[0]
        note = self.notes[index]

        def save():
            new_title = title_entry.get()
            new_content = content_text.get("1.0", tk.END).strip()
            if new_title and new_content:
                note.title = new_title
                note.content = new_content
                self.refresh_listbox()
                self.display_note()
                win.destroy()
            else:
                messagebox.showerror("Грешка", "Потребен е наслов и содржина.")

        win = tk.Toplevel(self.root)
        win.title("Уреди белешка")

        tk.Label(win, text="Наслов:").pack()
        title_entry = tk.Entry(win, width=50)
        title_entry.insert(0, note.title)
        title_entry.pack(pady=5)

        tk.Label(win, text="Содржина:").pack()
        content_text = tk.Text(win, height=10, width=50)
        content_text.insert("1.0", note.content)
        content_text.pack(pady=5)

        tk.Button(win, text="Зачувај", command=save).pack(pady=10)

    def delete_note(self):
        selected = self.note_listbox.curselection()
        if selected:
            index = selected[0]
            confirm = messagebox.askyesno("Бришење", "Дали сте сигурни дека сакате да ја избришете белешката?")
            if confirm:
                del self.notes[index]
                self.refresh_listbox()
                self.note_text.delete("1.0", tk.END)

    def display_note(self, event=None):
        selected = self.note_listbox.curselection()
        if selected:
            index = selected[0]
            note = self.notes[index]
            self.note_text.delete("1.0", tk.END)
            self.note_text.insert(tk.END, f"{note.title}\n\n{note.content}\n\nКреирано: {note.date.strftime('%Y-%m-%d %H:%M')}")

    def sort_notes(self):
        self.notes.sort(key=lambda note: note.date)
        self.refresh_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import scrolledtext
import requests
import re

class PikiIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("PikiScript Editor")
        self.root.geometry("900x600")

        self.theme_dark = True

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Open .apiki", command=self.load_file)
        file_menu.add_command(label="Save .apiki", command=self.save_file)
        self.menu.add_cascade(label="File", menu=file_menu)

        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(fill=tk.X)
        self.run_button = ttk.Button(self.toolbar, text=" Run PikiScript", command=self.run_script)
        self.run_button.pack(side=tk.LEFT, padx=5)
        self.theme_button = ttk.Button(self.toolbar, text="Toggle Theme", command=self.toggle_theme)
        self.theme_button.pack(side=tk.LEFT, padx=5)

        self.paned = tk.PanedWindow(self.root, orient=tk.VERTICAL)
        self.paned.pack(fill=tk.BOTH, expand=True)

        self.editor = scrolledtext.ScrolledText(self.paned, font=("Courier New", 12), wrap=tk.WORD, undo=True)
        self.paned.add(self.editor)

        self.output = scrolledtext.ScrolledText(self.paned, font=("Courier New", 10), height=10)
        self.paned.add(self.output)

        self.editor.bind("<KeyRelease>", self.autocomplete)

        self.autocomplete_words = [
            "init():", "end", "getuser.from(", "style.output:",
            "print.age(", "print.own(", "print.cont(", "print.likes(", "print.url(", "print_sep("
        ]

        self.set_theme()

    def run_script(self):
        self.output.delete(1.0, tk.END)
        script = self.editor.get("1.0", tk.END)

        if "init():" in script and "end" in script:
            username_match = re.search(r'getuser\.from\((.*?)\)', script)
            if username_match:
                url = username_match.group(1).strip().strip('"').strip("'")
                try:
                    response = requests.get(url)
                    data = response.json()
                    posts = data.get("posts", [])

                    for post in posts:
                        if "print.age" in script:
                            self.output.insert(tk.END, f"AGE: {post.get('createdAt', 'N/A')}\n")
                        if "print.own" in script:
                            self.output.insert(tk.END, f"BY: {post.get('author', 'N/A')}\n")
                        if "print.cont" in script:
                            self.output.insert(tk.END, f"{post.get('content', '')}\n")
                        if "print.likes" in script:
                            self.output.insert(tk.END, f"Likes: {post.get('likes', 0)}\n")
                        if "print.url" in script:
                            self.output.insert(tk.END, f"URL: {post.get('url', '')}\n")
                        if "print_sep" in script:
                            self.output.insert(tk.END, "-----------------------------\n")
                except Exception as e:
                    self.output.insert(tk.END, f"Error: {str(e)}\n")
            else:
                self.output.insert(tk.END, "No valid 'getuser.from(URL)' found.\n")
        else:
            self.output.insert(tk.END, "Missing init(): or end\n")

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PikiScript Files", "*.piki")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.editor.delete("1.0", tk.END)
                self.editor.insert("1.0", content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".apiki", filetypes=[("Pikiscript Files", "*.apiki")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.editor.get("1.0", tk.END))

    def toggle_theme(self):
        self.theme_dark = not self.theme_dark
        self.set_theme()

    def set_theme(self):
        if self.theme_dark:
            self.editor.config(bg="#1e1e1e", fg="white", insertbackground="white")
            self.output.config(bg="black", fg="white", insertbackground="white")
        else:
            self.editor.config(bg="white", fg="black", insertbackground="black")
            self.output.config(bg="#f0f0f0", fg="black", insertbackground="black")

    def autocomplete(self, event):
        word = self.editor.get("insert linestart", "insert")
        matches = [w for w in self.autocomplete_words if word.strip() in w]
        if matches and len(word.strip()) > 2:
            self.output.insert(tk.END, f"[Suggest: {matches[0]}]\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = PikiIDE(root)
    root.mainloop()

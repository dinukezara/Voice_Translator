import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from config import LANGUAGE_MAP, LANGUAGE_CODE_MAP, DEFAULT_TARGET, get_logger
from database import Database
from speech_to_text_whisper import WhisperSTT
from text_to_speech import TextToSpeech
from translator import TranslatorService

logger = get_logger(__name__)


class VoiceTranslatorGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Voice-Based Multilingual Translator")
        self.root.geometry("1100x760")
        self.root.resizable(False, False)

        self.stt = WhisperSTT()
        self.translator = TranslatorService()
        self.tts = TextToSpeech()
        self.db = Database()

        self.dark_mode = False

        self.build_ui()
        self.apply_light_theme()
        self.refresh_history()

    # -------------------------------------------------
    # UI BUILD
    # -------------------------------------------------
    def build_ui(self) -> None:
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ---------------- Header ----------------
        self.header_frame = tk.Frame(self.main_frame)
        self.header_frame.pack(fill="x", pady=5)

        self.title_label = tk.Label(
            self.header_frame,
            text="Voice-Based Multilingual Speech Translator",
            font=("Arial", 20, "bold"),
        )
        self.title_label.pack(side="left", padx=10)

        self.theme_button = tk.Button(
            self.header_frame,
            text="Toggle Dark Mode",
            font=("Arial", 10, "bold"),
            command=self.toggle_theme,
            width=16,
        )
        self.theme_button.pack(side="right", padx=10)

        # ---------------- Top Controls ----------------
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.pack(fill="x", pady=10)

        self.language_frame = tk.LabelFrame(
            self.top_frame,
            text="Language Settings",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10,
        )
        self.language_frame.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(
            self.language_frame,
            text="Detected Source Language:",
            font=("Arial", 11, "bold"),
        ).grid(row=0, column=0, padx=10, pady=8, sticky="e")

        self.source_var = tk.StringVar(value="Not detected yet")
        self.source_entry = tk.Entry(
            self.language_frame,
            textvariable=self.source_var,
            width=28,
            state="readonly",
            readonlybackground="white",
        )
        self.source_entry.grid(row=0, column=1, padx=10, pady=8)

        tk.Label(
            self.language_frame,
            text="Target Language:",
            font=("Arial", 11, "bold"),
        ).grid(row=1, column=0, padx=10, pady=8, sticky="e")

        self.target_combo = ttk.Combobox(
            self.language_frame,
            values=list(LANGUAGE_MAP.keys()),
            state="readonly",
            width=25,
        )
        self.target_combo.grid(row=1, column=1, padx=10, pady=8)
        self.target_combo.set(DEFAULT_TARGET)

        # ---------------- Buttons ----------------
        self.button_frame = tk.LabelFrame(
            self.top_frame,
            text="Actions",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10,
        )
        self.button_frame.pack(side="right", fill="y", padx=5)

        self.translate_button = tk.Button(
            self.button_frame,
            text="Speak and Translate",
            font=("Arial", 11, "bold"),
            width=18,
            command=self.start_translation_thread,
        )
        self.translate_button.grid(row=0, column=0, padx=6, pady=6)

        self.replay_button = tk.Button(
            self.button_frame,
            text="Replay Audio",
            font=("Arial", 11),
            width=18,
            command=self.replay_audio_thread,
        )
        self.replay_button.grid(row=1, column=0, padx=6, pady=6)

        self.export_button = tk.Button(
            self.button_frame,
            text="Export CSV",
            font=("Arial", 11),
            width=18,
            command=self.export_csv,
        )
        self.export_button.grid(row=2, column=0, padx=6, pady=6)

        self.refresh_button = tk.Button(
            self.button_frame,
            text="Refresh History",
            font=("Arial", 11),
            width=18,
            command=self.refresh_history,
        )
        self.refresh_button.grid(row=3, column=0, padx=6, pady=6)

        self.clear_button = tk.Button(
            self.button_frame,
            text="Clear",
            font=("Arial", 11),
            width=18,
            command=self.clear_text,
        )
        self.clear_button.grid(row=4, column=0, padx=6, pady=6)

        # ---------------- Status Section ----------------
        self.status_frame = tk.Frame(self.main_frame)
        self.status_frame.pack(fill="x", pady=8)

        self.status_label = tk.Label(
            self.status_frame,
            text="Status: Ready",
            font=("Arial", 11, "bold"),
            fg="blue",
            anchor="w",
        )
        self.status_label.pack(fill="x", padx=5)

        self.progress = ttk.Progressbar(
            self.status_frame,
            orient="horizontal",
            mode="indeterminate",
            length=300,
        )
        self.progress.pack(fill="x", padx=5, pady=5)

        # ---------------- Text Areas ----------------
        self.text_frame = tk.Frame(self.main_frame)
        self.text_frame.pack(fill="x", pady=10)

        self.original_frame = tk.LabelFrame(
            self.text_frame,
            text="Original Text",
            font=("Arial", 11, "bold"),
            padx=5,
            pady=5,
        )
        self.original_frame.pack(side="left", fill="both", expand=True, padx=5)

        self.original_box = tk.Text(self.original_frame, height=10, width=55, wrap="word")
        self.original_box.pack(fill="both", expand=True)

        self.translated_frame = tk.LabelFrame(
            self.text_frame,
            text="Translated Text",
            font=("Arial", 11, "bold"),
            padx=5,
            pady=5,
        )
        self.translated_frame.pack(side="right", fill="both", expand=True, padx=5)

        self.translated_box = tk.Text(self.translated_frame, height=10, width=55, wrap="word")
        self.translated_box.pack(fill="both", expand=True)

        # ---------------- History Viewer ----------------
        self.history_frame = tk.LabelFrame(
            self.main_frame,
            text="Translation History",
            font=("Arial", 11, "bold"),
            padx=5,
            pady=5,
        )
        self.history_frame.pack(fill="both", expand=True, pady=10)

        columns = ("id", "timestamp", "source", "target", "original", "translated")
        self.history_table = ttk.Treeview(
            self.history_frame,
            columns=columns,
            show="headings",
            height=12,
        )

        self.history_table.heading("id", text="ID")
        self.history_table.heading("timestamp", text="Timestamp")
        self.history_table.heading("source", text="Source")
        self.history_table.heading("target", text="Target")
        self.history_table.heading("original", text="Original Text")
        self.history_table.heading("translated", text="Translated Text")

        self.history_table.column("id", width=50, anchor="center")
        self.history_table.column("timestamp", width=160, anchor="center")
        self.history_table.column("source", width=90, anchor="center")
        self.history_table.column("target", width=90, anchor="center")
        self.history_table.column("original", width=320, anchor="w")
        self.history_table.column("translated", width=320, anchor="w")

        self.history_scroll = ttk.Scrollbar(
            self.history_frame,
            orient="vertical",
            command=self.history_table.yview,
        )
        self.history_table.configure(yscrollcommand=self.history_scroll.set)

        self.history_table.pack(side="left", fill="both", expand=True)
        self.history_scroll.pack(side="right", fill="y")

    # -------------------------------------------------
    # PHASE 7: STATUS SYSTEM
    # -------------------------------------------------
    def set_status(self, text: str, color: str = "blue", busy: bool = False) -> None:
        self.status_label.config(text=f"Status: {text}", fg=color)

        if busy:
            self.progress.start(10)
        else:
            self.progress.stop()

        self.root.update_idletasks()

    def set_buttons_state(self, state: str) -> None:
        self.translate_button.config(state=state)
        self.replay_button.config(state=state)
        self.export_button.config(state=state)
        self.refresh_button.config(state=state)
        self.clear_button.config(state=state)
        self.theme_button.config(state=state)

    # -------------------------------------------------
    # PHASE 8: UI IMPROVEMENTS
    # -------------------------------------------------
    def apply_light_theme(self) -> None:
        bg = "#f4f6f8"
        card = "#ffffff"
        fg = "#111111"

        self.root.configure(bg=bg)
        self.main_frame.configure(bg=bg)
        self.header_frame.configure(bg=bg)
        self.top_frame.configure(bg=bg)
        self.status_frame.configure(bg=bg)
        self.text_frame.configure(bg=bg)

        self.title_label.configure(bg=bg, fg=fg)
        self.status_label.configure(bg=bg)

        for frame in [
            self.language_frame,
            self.button_frame,
            self.original_frame,
            self.translated_frame,
            self.history_frame,
        ]:
            frame.configure(bg=card, fg=fg)

        for widget in self.language_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=card, fg=fg)

        for btn in [
            self.translate_button,
            self.replay_button,
            self.export_button,
            self.refresh_button,
            self.clear_button,
            self.theme_button,
        ]:
            btn.configure(bg="#e9ecef", fg=fg, activebackground="#dfe3e6")

        self.original_box.configure(bg="white", fg="black", insertbackground="black")
        self.translated_box.configure(bg="white", fg="black", insertbackground="black")

        self.source_entry.configure(
            readonlybackground="white",
            fg="black",
        )

    def apply_dark_theme(self) -> None:
        bg = "#1e1e1e"
        card = "#2b2b2b"
        fg = "#f1f1f1"

        self.root.configure(bg=bg)
        self.main_frame.configure(bg=bg)
        self.header_frame.configure(bg=bg)
        self.top_frame.configure(bg=bg)
        self.status_frame.configure(bg=bg)
        self.text_frame.configure(bg=bg)

        self.title_label.configure(bg=bg, fg=fg)
        self.status_label.configure(bg=bg)

        for frame in [
            self.language_frame,
            self.button_frame,
            self.original_frame,
            self.translated_frame,
            self.history_frame,
        ]:
            frame.configure(bg=card, fg=fg)

        for widget in self.language_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=card, fg=fg)

        for btn in [
            self.translate_button,
            self.replay_button,
            self.export_button,
            self.refresh_button,
            self.clear_button,
            self.theme_button,
        ]:
            btn.configure(bg="#444444", fg=fg, activebackground="#555555")

        self.original_box.configure(bg="#111111", fg="white", insertbackground="white")
        self.translated_box.configure(bg="#111111", fg="white", insertbackground="white")

        self.source_entry.configure(
            readonlybackground="#111111",
            fg="white",
        )

    def toggle_theme(self) -> None:
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

    def clear_text(self) -> None:
        self.original_box.delete("1.0", tk.END)
        self.translated_box.delete("1.0", tk.END)
        self.source_var.set("Not detected yet")
        self.set_status("Cleared", color="blue", busy=False)

    def refresh_history(self) -> None:
        for row in self.history_table.get_children():
            self.history_table.delete(row)

        rows = self.db.fetch_all()
        for row in rows:
            self.history_table.insert("", tk.END, values=row)

        self.set_status("History refreshed", color="blue", busy=False)

    # -------------------------------------------------
    # THREADS
    # -------------------------------------------------
    def start_translation_thread(self) -> None:
        thread = threading.Thread(target=self.translate_speech, daemon=True)
        thread.start()

    def replay_audio_thread(self) -> None:
        thread = threading.Thread(target=self.replay_audio, daemon=True)
        thread.start()

    # -------------------------------------------------
    # MAIN FLOW
    # -------------------------------------------------
    def translate_speech(self) -> None:
        try:
            self.set_buttons_state("disabled")
            self.original_box.delete("1.0", tk.END)
            self.translated_box.delete("1.0", tk.END)

            target_lang = self.target_combo.get()

            try:
                target_translate = LANGUAGE_MAP[target_lang]["translate"]
                target_tts = LANGUAGE_MAP[target_lang]["tts"]
            except KeyError:
                self.set_status("Invalid target language", color="red", busy=False)
                messagebox.showerror("Language Error", "Invalid target language selected.")
                return

            self.set_status("Listening...", color="orange", busy=True)
            result_stt = self.stt.transcribe()

            if not result_stt.get("success"):
                self.set_status("Speech recognition failed", color="red", busy=False)
                messagebox.showerror("Speech Recognition Error", result_stt.get("error"))
                return

            original_text = result_stt.get("text", "").strip()
            detected_language_code = result_stt.get("language", "").strip().lower()
            source_lang = LANGUAGE_CODE_MAP.get(detected_language_code, "Unknown")

            self.source_var.set(f"{source_lang} ({detected_language_code})")
            self.original_box.insert(tk.END, original_text)

            self.set_status("Translating...", color="purple", busy=True)
            result_translate = self.translator.translate(
                text=original_text,
                source="auto",
                target=target_translate,
            )

            if not result_translate.get("success"):
                self.set_status("Translation failed", color="red", busy=False)
                messagebox.showerror("Translation Error", result_translate.get("error"))
                return

            translated_text = result_translate.get("text", "").strip()
            self.translated_box.insert(tk.END, translated_text)

            self.db.insert(
                source_lang=source_lang,
                target_lang=target_lang,
                original_text=original_text,
                translated_text=translated_text,
            )

            self.refresh_history()

            self.set_status("Speaking...", color="green", busy=True)
            result_tts = self.tts.speak(translated_text, lang=target_tts)

            if not result_tts.get("success"):
                self.set_status("TTS failed", color="red", busy=False)
                messagebox.showerror("TTS Error", result_tts.get("error"))
                return

            self.set_status("Completed successfully", color="green", busy=False)

        except Exception as e:
            logger.exception("Unexpected GUI error.")
            self.set_status("Unexpected error", color="red", busy=False)
            messagebox.showerror("Unexpected Error", str(e))

        finally:
            self.set_buttons_state("normal")

    def replay_audio(self) -> None:
        try:
            self.replay_button.config(state="disabled")
            self.set_status("Replaying audio...", color="orange", busy=True)

            result = self.tts.replay()

            if not result.get("success"):
                self.set_status("Replay failed", color="red", busy=False)
                messagebox.showerror("Replay Error", result.get("error"))
                return

            self.set_status("Replay completed", color="green", busy=False)

        except Exception as e:
            logger.exception("Replay thread failed.")
            self.set_status("Replay failed", color="red", busy=False)
            messagebox.showerror("Replay Error", str(e))

        finally:
            self.replay_button.config(state="normal")

    def export_csv(self) -> None:
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Save Translation History As",
            )

            if not file_path:
                return

            self.set_status("Exporting CSV...", color="orange", busy=True)
            result = self.db.export_csv(file_path)

            if result.get("success"):
                self.set_status("CSV exported successfully", color="green", busy=False)
                messagebox.showinfo(
                    "Export Success",
                    f"Translation history exported to:\n{result.get('filename')}",
                )
            else:
                self.set_status("CSV export failed", color="red", busy=False)
                messagebox.showerror("Export Error", result.get("error"))

        except Exception as e:
            logger.exception("Export CSV failed.")
            self.set_status("CSV export failed", color="red", busy=False)
            messagebox.showerror("Export Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceTranslatorGUI(root)
    root.mainloop()
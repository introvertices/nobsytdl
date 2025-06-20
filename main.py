###--- IMPORTS

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import yt_dlp                                           # REQUIRED: pip install yt-dl
from pathlib import Path




class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("NoBSYTDL - by Introvertices.github.io")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        
        self.colours = {
            'bg': "#dedfd3",           # Dark blue-gray background
            'fg': "#1c1e1f",           # Light blue-white text
            'select_bg': "#bddae4",    # Medium blue-gray for selections
            'select_fg': "#1C1E1D",    # Pure white for selected text
            'entry_bg': "#9fb5cb",     # Darker blue-gray for entries
            'entry_fg': "#1C1E1D",     # Very light blue-white for entry text
            'button_bg': "#6dc4c2",    # Medium pastel blue for buttons
            'button_fg': '#1C1E1D',    # White button text
            'accent': "#2d8f86"        # Light pastel blue accent
        }
        
        # Configure root window
        self.root.configure(bg=self.colours['bg'])
        
        # Vars
        self.url_var = tk.StringVar()
        self.download_path_var = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.format_var = tk.StringVar(value="best")
        self.audio_only_var = tk.BooleanVar(value=False)
        self.convert_mp3_var = tk.BooleanVar(value=False)
        
        self.setup_dark_theme()
        self.setup_gui()
        
    def setup_dark_theme(self):
        
        style = ttk.Style()
        
        # Configure colour theme
        style.theme_use('clam')

        style.configure('TLabel', 
                       background=self.colours['bg'], 
                       foreground=self.colours['fg'])
        
        style.configure('TFrame', 
                       background=self.colours['bg'])
        
        style.configure('TLabelFrame', 
                       background=self.colours['bg'],
                       foreground=self.colours['fg'],
                       bordercolor=self.colours['select_bg'],
                       darkcolor=self.colours['select_bg'],
                       lightcolor=self.colours['select_bg'],
                       borderwidth=1)
        
        style.configure('TEntry', 
                       fieldbackground=self.colours['entry_bg'],
                       foreground=self.colours['entry_fg'],
                       bordercolor=self.colours['select_bg'],
                       insertcolor=self.colours['fg'])
        
        style.configure('TButton', 
                       background=self.colours['button_bg'],
                       foreground=self.colours['button_fg'],
                       borderwidth=0,
                       relief='flat')
        
        style.map('TButton',
                 background=[('active', self.colours['select_bg']),
                            ('pressed', self.colours['accent'])],
                 relief=[('pressed', 'flat')])
        
        style.configure('Accent.TButton', 
                       background=self.colours['accent'],
                       foreground='white',
                       borderwidth=0,
                       relief='flat')
        
        style.map('Accent.TButton',
                 background=[('active', '#106ebe')],
                 relief=[('pressed', 'flat')])
        
        style.configure('TCombobox', 
                       fieldbackground=self.colours['entry_bg'],
                       foreground=self.colours['entry_fg'],
                       bordercolor=self.colours['select_bg'],
                       arrowcolor=self.colours['fg'])
        
        style.map('TCombobox',
                 fieldbackground=[('readonly', self.colours['entry_bg'])],
                 selectbackground=[('readonly', self.colours['select_bg'])])
        
        style.configure('TCheckbutton', 
                       background=self.colours['bg'],
                       foreground=self.colours['fg'],
                       focuscolor=self.colours['accent'])
        
        style.configure('TProgressbar',
                       background=self.colours['accent'],
                       troughcolor=self.colours['select_bg'],
                       bordercolor=self.colours['bg'])
        
        style.configure('Vertical.TScrollbar',
                       background=self.colours['button_bg'],
                       troughcolor=self.colours['bg'],
                       bordercolor=self.colours['bg'],
                       arrowcolor=self.colours['fg'],
                       darkcolor=self.colours['button_bg'],
                       lightcolor=self.colours['button_bg'])
        
        style.map('Vertical.TScrollbar',
                 background=[('active', self.colours['select_bg'])])
        
    def setup_gui(self):
        # Main frame and grid weighting
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # URL input
        ttk.Label(main_frame, text="YouTube URL:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=50)
        url_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Download path
        ttk.Label(main_frame, text="Download Path:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        path_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(path_frame, textvariable=self.download_path_var, width=40).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(path_frame, text="Browse", command=self.browse_folder).grid(row=0, column=1, padx=(5, 0))
        
        # Audio only checkbox
        audio_frame = ttk.Frame(main_frame)
        audio_frame.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))
        
        ttk.Checkbutton(audio_frame, text="Audio Only", 
                       variable=self.audio_only_var, 
                       command=self.toggle_audio_only).grid(row=0, column=0, sticky=tk.W)
        
        self.convert_mp3_var = tk.BooleanVar(value=True)
        self.convert_checkbox = ttk.Checkbutton(audio_frame, text="Convert to MP3 (requires FFmpeg)", 
                                              variable=self.convert_mp3_var)
        self.convert_checkbox.grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        
        # Quality selection
        ttk.Label(main_frame, text="Video Quality:").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        self.quality_combo = ttk.Combobox(main_frame, textvariable=self.format_var, 
                                         values=["best", "worst", "720p", "480p", "360p", "144p"], 
                                         state="readonly", width=20)
        self.quality_combo.grid(row=3, column=1, sticky=tk.W, pady=(0, 5))
        
        # Get info button
        ttk.Button(main_frame, text="Get Video Info", 
                  command=self.get_video_info).grid(row=4, column=0, columnspan=3, pady=(10, 5))
        
        # Video info display
        info_frame = ttk.LabelFrame(main_frame, text="Video Information", padding="5")
        info_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 10))
        info_frame.columnconfigure(0, weight=1)
        
        self.info_text = tk.Text(info_frame, height=8, wrap=tk.WORD,
                                bg=self.colours['entry_bg'],
                                fg=self.colours['entry_fg'],
                                insertbackground=self.colours['fg'],
                                selectbackground=self.colours['select_bg'],
                                selectforeground=self.colours['select_fg'],
                                borderwidth=1,
                                relief='solid')
        scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        info_frame.rowconfigure(0, weight=1)
        
        # Download button
        self.download_btn = ttk.Button(main_frame, text="Download", 
                                      command=self.start_download, style="Accent.TButton")
        self.download_btn.grid(row=6, column=0, columnspan=3, pady=(0, 10))
        
        # Progress
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Ready")
        self.status_label.grid(row=8, column=0, columnspan=3, pady=(0, 5))
        
        # Config row weighting
        main_frame.rowconfigure(5, weight=1)
        

    ###--- HELPERS

    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_path_var.get())
        if folder:
            self.download_path_var.set(folder)
    
    def toggle_audio_only(self):
        if self.audio_only_var.get():
            self.quality_combo.configure(state="disabled")
            self.format_var.set("audio")
            self.convert_checkbox.configure(state="normal")
        else:
            self.quality_combo.configure(state="readonly")
            self.format_var.set("best")
            self.convert_checkbox.configure(state="disabled")
    
    def get_video_info(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        def fetch_info():
            try:
                self.status_label.config(text="Fetching video information...")
                self.progress.start()
                
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                    # Format info display
                    info_text = f"Title: {info.get('title', 'N/A')}\n"
                    info_text += f"Duration: {self.format_duration(info.get('duration', 0))}\n"
                    info_text += f"Upload Date: {info.get('upload_date', 'N/A')}\n"
                    info_text += f"Uploader: {info.get('uploader', 'N/A')}\n"
                    info_text += f"View Count: {info.get('view_count', 'N/A'):,}\n"
                    info_text += f"Description: {info.get('description', 'N/A')[:200]}..."
                    
                    # Available formats
                    if info.get('formats'):
                        info_text += f"\n\nAvailable Formats:\n"
                        formats = []
                        for f in info['formats']:
                            if f.get('height'):
                                formats.append(f"{f.get('height')}p - {f.get('ext', 'unknown')}")
                        
                        unique_formats = list(set(formats))
                        unique_formats.sort(key=lambda x: int(x.split('p')[0]) if 'p' in x else 0, reverse=True)
                        info_text += "\n".join(unique_formats[:10])             # Show top 10
                    
                    self.info_text.delete(1.0, tk.END)
                    self.info_text.insert(1.0, info_text)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to get video info: {str(e)}")
            finally:
                self.progress.stop()
                self.status_label.config(text="Ready")
        
        threading.Thread(target=fetch_info, daemon=True).start()
    
    def format_duration(self, seconds):
        if not seconds:
            return "N/A"
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def start_download(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        download_path = self.download_path_var.get()
        if not os.path.exists(download_path):
            messagebox.showerror("Error", "Download path does not exist")
            return
        
        # Disable download button during download
        self.download_btn.configure(state="disabled")
        
        def download():
            try:
                self.status_label.config(text="Downloading...")
                self.progress.start()
                
                # Configure yt-dlp options
                if self.audio_only_var.get():
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                    }
                    
                    # Only add post-processor if user wants MP3 conversion
                    if self.convert_mp3_var.get():
                        ydl_opts['postprocessors'] = [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }]
                else:
                    format_selector = self.format_var.get()
                    if format_selector == "best":
                        format_str = "best[height<=1080]"
                    elif format_selector == "worst":
                        format_str = "worst"
                    else:
                        # Extract height from format 
                        height = format_selector.replace('p', '')
                        format_str = f"best[height<={height}]"
                    
                    ydl_opts = {
                        'format': format_str,
                        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                    }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                self.status_label.config(text="Download completed successfully!")
                messagebox.showinfo("Success", "Download completed successfully!")
                
            except Exception as e:
                error_msg = f"Download failed: {str(e)}"
                self.status_label.config(text="Download failed")
                messagebox.showerror("Error", error_msg)
            finally:
                self.progress.stop()
                self.download_btn.configure(state="normal")
        
        threading.Thread(target=download, daemon=True).start()


###--- Ya boi, main

def main():
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()

if __name__ == "__main__":
    main()
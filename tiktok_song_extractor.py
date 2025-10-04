#!/usr/bin/env python3
"""
TikTok Song Extractor
A tool to extract song names from TikTok profiles with GUI and CLI support.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import json
import csv
import os
import re
from urllib.parse import urlparse
import threading
from datetime import datetime
import time

class TikTokSongExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def extract_username_from_url(self, url):
        """Extract username from TikTok URL"""
        if not url:
            return None
            
        # Handle different TikTok URL formats
        patterns = [
            r'tiktok\.com/@([^/?]+)',
            r'tiktok\.com/([^/?]+)',
            r'@([^/?]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        # If no @ symbol, assume it's just a username
        if not url.startswith('http'):
            return url.replace('@', '')
        
        return None
    
    def get_user_videos(self, username, max_videos=50):
        """Get user's videos (simulated - TikTok API requires authentication)"""
        print(f"Fetching videos for user: {username}")
        
        # Note: This is a simplified version. Real TikTok API requires authentication
        # For demonstration, we'll simulate the data structure
        
        # In a real implementation, you would:
        # 1. Use TikTok's official API with proper authentication
        # 2. Or use web scraping (which may violate ToS)
        # 3. Or use third-party services
        
        simulated_videos = [
            {
                'id': f'video_{i}',
                'description': f'Sample video {i}',
                'music': {
                    'title': f'Song Title {i}',
                    'author': f'Artist {i}',
                    'duration': 30
                },
                'created_time': datetime.now().isoformat()
            }
            for i in range(1, min(max_videos + 1, 11))
        ]
        
        return simulated_videos
    
    def extract_songs_from_videos(self, videos):
        """Extract unique songs from video data"""
        songs = []
        seen_songs = set()
        
        for video in videos:
            if 'music' in video and video['music']:
                music = video['music']
                song_key = f"{music.get('title', '')}-{music.get('author', '')}"
                
                if song_key not in seen_songs and music.get('title'):
                    songs.append({
                        'title': music.get('title', 'Unknown'),
                        'artist': music.get('author', 'Unknown'),
                        'duration': music.get('duration', 0),
                        'video_id': video.get('id', ''),
                        'video_description': video.get('description', '')[:100] + '...' if len(video.get('description', '')) > 100 else video.get('description', ''),
                        'created_time': video.get('created_time', '')
                    })
                    seen_songs.add(song_key)
        
        return songs

class TikTokGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok Song Extractor")
        self.root.geometry("800x600")
        
        self.extractor = TikTokSongExtractor()
        self.songs_data = []
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="TikTok Song Extractor", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Username input
        ttk.Label(main_frame, text="TikTok Username or URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(main_frame, textvariable=self.username_var, width=50)
        username_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Max videos input
        ttk.Label(main_frame, text="Max Videos:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.max_videos_var = tk.StringVar(value="50")
        max_videos_entry = ttk.Entry(main_frame, textvariable=self.max_videos_var, width=10)
        max_videos_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        # Extract button
        self.extract_btn = ttk.Button(buttons_frame, text="Extract Songs", 
                                     command=self.extract_songs_threaded)
        self.extract_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Export buttons
        ttk.Button(buttons_frame, text="Export CSV", 
                  command=self.export_csv).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Export JSON", 
                  command=self.export_json).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Export TXT", 
                  command=self.export_txt).pack(side=tk.LEFT, padx=(0, 10))
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.progress_var).grid(row=4, column=0, columnspan=3, pady=5)
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Extracted Songs", padding="5")
        results_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(20, 0))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Treeview for results
        columns = ('Title', 'Artist', 'Duration', 'Video ID')
        self.tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.tree.heading('Title', text='Song Title')
        self.tree.heading('Artist', text='Artist')
        self.tree.heading('Duration', text='Duration (s)')
        self.tree.heading('Video ID', text='Video ID')
        
        self.tree.column('Title', width=200)
        self.tree.column('Artist', width=150)
        self.tree.column('Duration', width=80)
        self.tree.column('Video ID', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure main frame row weight
        main_frame.rowconfigure(6, weight=1)
        
    def extract_songs_threaded(self):
        """Extract songs in a separate thread to prevent GUI freezing"""
        thread = threading.Thread(target=self.extract_songs)
        thread.daemon = True
        thread.start()
        
    def extract_songs(self):
        """Extract songs from TikTok profile"""
        try:
            self.extract_btn.config(state='disabled')
            self.progress_bar.start()
            self.progress_var.set("Extracting songs...")
            
            username = self.username_var.get().strip()
            if not username:
                messagebox.showerror("Error", "Please enter a TikTok username or URL")
                return
            
            try:
                max_videos = int(self.max_videos_var.get())
            except ValueError:
                max_videos = 50
            
            # Extract username from URL if needed
            username = self.extractor.extract_username_from_url(username)
            if not username:
                messagebox.showerror("Error", "Invalid username or URL format")
                return
            
            # Get videos
            videos = self.extractor.get_user_videos(username, max_videos)
            
            # Extract songs
            songs = self.extractor.extract_songs_from_videos(videos)
            self.songs_data = songs
            
            # Update GUI
            self.root.after(0, self.update_results_display)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
        finally:
            self.root.after(0, self.reset_ui_state)
    
    def update_results_display(self):
        """Update the results display in the GUI"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add new items
        for song in self.songs_data:
            self.tree.insert('', 'end', values=(
                song['title'],
                song['artist'],
                song['duration'],
                song['video_id']
            ))
        
        self.progress_var.set(f"Found {len(self.songs_data)} unique songs")
    
    def reset_ui_state(self):
        """Reset UI state after extraction"""
        self.progress_bar.stop()
        self.extract_btn.config(state='normal')
    
    def export_csv(self):
        """Export songs to CSV file"""
        if not self.songs_data:
            messagebox.showwarning("Warning", "No songs to export. Please extract songs first.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['title', 'artist', 'duration', 'video_id', 'video_description', 'created_time']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for song in self.songs_data:
                        writer.writerow(song)
                
                messagebox.showinfo("Success", f"Songs exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export CSV: {str(e)}")
    
    def export_json(self):
        """Export songs to JSON file"""
        if not self.songs_data:
            messagebox.showwarning("Warning", "No songs to export. Please extract songs first.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as jsonfile:
                    json.dump(self.songs_data, jsonfile, indent=2, ensure_ascii=False)
                
                messagebox.showinfo("Success", f"Songs exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export JSON: {str(e)}")
    
    def export_txt(self):
        """Export songs to TXT file"""
        if not self.songs_data:
            messagebox.showwarning("Warning", "No songs to export. Please extract songs first.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as txtfile:
                    txtfile.write("TikTok Songs Extracted\n")
                    txtfile.write("=" * 50 + "\n\n")
                    
                    for i, song in enumerate(self.songs_data, 1):
                        txtfile.write(f"{i}. {song['title']} - {song['artist']}\n")
                        txtfile.write(f"   Duration: {song['duration']}s\n")
                        txtfile.write(f"   Video ID: {song['video_id']}\n")
                        txtfile.write(f"   Description: {song['video_description']}\n")
                        txtfile.write(f"   Created: {song['created_time']}\n\n")
                
                messagebox.showinfo("Success", f"Songs exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export TXT: {str(e)}")

def main():
    """Main function to run the application"""
    import sys
    
    if len(sys.argv) > 1:
        # Command line mode
        username = sys.argv[1]
        max_videos = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        
        extractor = TikTokSongExtractor()
        username = extractor.extract_username_from_url(username)
        
        if not username:
            print("Error: Invalid username or URL format")
            return
        
        print(f"Extracting songs from @{username}...")
        videos = extractor.get_user_videos(username, max_videos)
        songs = extractor.extract_songs_from_videos(videos)
        
        print(f"\nFound {len(songs)} unique songs:")
        print("-" * 50)
        
        for i, song in enumerate(songs, 1):
            print(f"{i}. {song['title']} - {song['artist']}")
            print(f"   Duration: {song['duration']}s")
            print(f"   Video ID: {song['video_id']}")
            print()
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tiktok_songs_{username}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(songs, f, indent=2, ensure_ascii=False)
        
        print(f"Songs saved to: {filename}")
        
    else:
        # GUI mode
        root = tk.Tk()
        app = TikTokGUI(root)
        root.mainloop()

if __name__ == "__main__":
    main()
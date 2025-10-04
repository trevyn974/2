# TikTok Song Extractor

A Python tool to extract song names from TikTok profiles with both GUI and command-line interfaces.

## Features

- 🎵 Extract unique songs from TikTok profiles
- 🖥️ User-friendly GUI interface
- 💻 Command-line interface for automation
- 📊 Export results in multiple formats (CSV, JSON, TXT)
- 🔍 Support for various TikTok URL formats
- ⚡ Multi-threaded processing to prevent GUI freezing

## Installation

1. Install Python 3.7 or higher
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### GUI Mode (Recommended)

Run the application with the graphical interface:

```bash
python tiktok_song_extractor.py
```

1. Enter a TikTok username or URL in the input field
2. Set the maximum number of videos to process (default: 50)
3. Click "Extract Songs" to start the extraction
4. View results in the table
5. Export results using the export buttons (CSV, JSON, or TXT)

### Command Line Mode

Extract songs from command line:

```bash
# Basic usage
python tiktok_song_extractor.py username

# With custom video limit
python tiktok_song_extractor.py username 100

# Examples
python tiktok_song_extractor.py @username
python tiktok_song_extractor.py https://www.tiktok.com/@username
python tiktok_song_extractor.py username 25
```

## Supported Input Formats

The tool accepts various TikTok input formats:

- `@username`
- `username`
- `https://www.tiktok.com/@username`
- `https://tiktok.com/@username`

## Output Formats

### CSV Export
Contains columns: title, artist, duration, video_id, video_description, created_time

### JSON Export
Structured JSON with all song metadata

### TXT Export
Human-readable text format with numbered list

## Important Notes

⚠️ **Disclaimer**: This tool is for educational purposes only. The current implementation uses simulated data as TikTok's official API requires authentication and may have usage restrictions. For production use, you would need to:

1. Obtain proper TikTok API credentials
2. Implement proper authentication
3. Respect TikTok's Terms of Service and rate limits
4. Consider using official TikTok Research API or third-party services

## Legal Considerations

- Always respect TikTok's Terms of Service
- Ensure you have permission to extract data from profiles
- Consider rate limiting to avoid overwhelming TikTok's servers
- Use this tool responsibly and ethically

## Troubleshooting

### Common Issues

1. **"Invalid username or URL format"**
   - Make sure the username doesn't contain special characters
   - Try different URL formats

2. **"No songs to export"**
   - Ensure the extraction completed successfully
   - Check if the profile has videos with music

3. **GUI not responding**
   - The extraction runs in a separate thread
   - Wait for the process to complete

## Development

To extend this tool:

1. Implement real TikTok API integration
2. Add more export formats
3. Add batch processing for multiple profiles
4. Implement caching to avoid re-extracting data
5. Add filtering options (date range, song duration, etc.)

## License

This project is for educational purposes. Please ensure compliance with TikTok's Terms of Service when using.
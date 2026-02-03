---
name: audio-to-subtitles
description: Convert audio files to subtitle files using OpenAI Whisper AI transcription. Generates SRT, FCPXML (for Final Cut Pro), and plain text formats. Use when you need to create subtitles, captions, or transcripts from audio or video files.
homepage: https://github.com/openai/whisper
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "bins": ["python3"], "python": ["openai-whisper"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": "openai-whisper",
              "label": "Install Whisper (pip3 install openai-whisper)",
            },
          ],
      },
  }
---

# Audio to Subtitles Generator

Convert audio files to subtitle files using OpenAI Whisper AI transcription. Supports SRT and FCPXML formats for use in Final Cut Pro and other video editing software.

## Features

- 🤖 AI-powered transcription using OpenAI Whisper
- 📝 Multiple output formats: SRT, FCPXML, plain text
- 🎯 Optimized for Final Cut Pro workflow
- 🌍 Automatic language detection
- ⚡ Fast processing with GPU acceleration (if available)

## Prerequisites

```bash
pip3 install openai-whisper
```

**Note:** First run will download the AI model (base model ~150MB, large model ~3GB).

## Quick Start

### Generate all formats

```bash
{baseDir}/scripts/audio-to-subtitles.py audio.mp3
```

This creates:
- `audio.srt` - Standard subtitle format
- `audio.fcpxml` - Final Cut Pro import format
- `audio.txt` - Plain text transcript

### Specific format only

```bash
{baseDir}/scripts/audio-to-subtitles.py audio.mp3 -f srt
{baseDir}/scripts/audio-to-subtitles.py audio.mp3 -f fcpxml
```

### Custom output location

```bash
{baseDir}/scripts/audio-to-subtitles.py audio.mp3 -o ~/Desktop/my-subtitles.srt
```

## Usage

```
audio-to-subtitles.py [-h] [-o OUTPUT] [-f {srt,fcpxml,txt,all}]
                      [-m {tiny,base,small,medium,large}]
                      [-l LANGUAGE] [--fps FPS]
                      input
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `input` | Audio file path | (required) |
| `-o, --output` | Output file path | Auto-generated |
| `-f, --format` | Output format (srt/fcpxml/txt/all) | all |
| `-m, --model` | Whisper model size | base |
| `-l, --language` | Language code (zh/en/ja/ko) | Auto-detect |
| `--fps` | Frame rate for FCPXML | 30 |

## Model Sizes

| Model | Speed | Accuracy | Size | Best For |
|-------|-------|----------|------|----------|
| `tiny` | Fastest | Basic | 39MB | Quick tests |
| `base` | Fast | Good | 74MB | General use ⭐ |
| `small` | Medium | Better | 244MB | Better accuracy |
| `medium` | Slow | Great | 769MB | Professional |
| `large` | Slowest | Best | 3GB | Maximum quality |

## Supported Audio Formats

- MP3, WAV, M4A, FLAC, OGG, OPUS
- AAC, WMA
- Video files (MP4, MOV) - extracts audio automatically

## Output Formats

### SRT (SubRip Subtitle)
Standard subtitle format supported by:
- Final Cut Pro (File → Import → Captions)
- Adobe Premiere Pro
- DaVinci Resolve
- YouTube, Vimeo
- VLC, IINA, and most players

**Format:**
```
1
00:00:01,000 --> 00:00:04,000
Hello, this is the first subtitle.

2
00:00:05,000 --> 00:00:08,000
This is the second subtitle.
```

### FCPXML (Final Cut Pro XML)
Native Final Cut Pro format that imports as titles.

**Usage in Final Cut Pro:**
1. File → Import → XML...
2. Select the .fcpxml file
3. Subtitles appear as titles in your timeline
4. Customize font, size, position as needed

### TXT (Plain Text)
Simple transcript without timestamps.

## Examples

### Basic transcription

```bash
{baseDir}/scripts/audio-to-subtitles.py recording.mp3
```

### Chinese audio with large model

```bash
{baseDir}/scripts/audio-to-subtitles.py interview.m4a -m large -l zh
```

### YouTube video to subtitles

```bash
# First extract audio
video-audio-extractor "https://youtube.com/watch?v=..." -o video.mp3

# Then generate subtitles
audio-to-subtitles.py video.mp3
```

### Bilibili video workflow

```bash
# Extract audio from Bilibili
yt-dlp "https://bilibili.com/video/..." --extract-audio --audio-format mp3

# Generate subtitles
audio-to-subtitles.py *.mp3 -f fcpxml
```

## Language Codes

Common language codes:
- `zh` - Chinese (中文)
- `en` - English
- `ja` - Japanese
- `ko` - Korean
- `es` - Spanish
- `fr` - French
- `de` - German

Leave blank for automatic detection.

## Performance Tips

1. **Use smaller models for quick drafts**: `-m tiny` or `-m base`
2. **Use larger models for final output**: `-m medium` or `-m large`
3. **Specify language** for better accuracy: `-l zh`
4. **GPU acceleration**: Whisper automatically uses GPU if available

## Troubleshooting

### Slow transcription
- Use smaller model: `-m base` instead of `-m large`
- Check if GPU is being used (should show in console)

### Poor accuracy
- Try larger model: `-m medium` or `-m large`
- Specify language explicitly: `-l zh`
- Check audio quality (noisy audio reduces accuracy)

### Out of memory
- Use smaller model: `-m tiny` or `-m base`
- Process shorter audio segments

### Missing dependencies
```bash
pip3 install --upgrade openai-whisper
```

## Workflow Example

Complete workflow from video to Final Cut Pro subtitles:

```bash
# Step 1: Extract audio from video
video-audio-extractor video.mp4 -o audio.mp3

# Step 2: Generate subtitles
audio-to-subtitles.py audio.mp3 -f fcpxml

# Step 3: Import to Final Cut Pro
# File → Import → XML → select video.fcpxml
```

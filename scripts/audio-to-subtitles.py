#!/usr/bin/env python3
"""
Audio to Subtitles Generator
Converts audio files to subtitle files using OpenAI Whisper.
Supports SRT and FCPXML formats for Final Cut Pro.
"""

import argparse
import sys
import os
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from datetime import timedelta

# Check for whisper
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("Warning: OpenAI Whisper not installed. Install with: pip3 install openai-whisper", file=sys.stderr)


def format_time_srt(seconds):
    """Format seconds to SRT time format: HH:MM:SS,mmm"""
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int(td.microseconds / 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def format_time_fcpxml(seconds):
    """Format seconds to FCPXML time format: HH:MM:SS.mmm"""
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int(td.microseconds / 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def seconds_to_fcpxml_timecode(seconds, fps=30):
    """Convert seconds to FCPXML timecode format (10s/1s)"""
    # FCPXML uses rational time format
    # For simplicity, we'll use seconds with decimal
    return f"{seconds:.3f}s"


def generate_srt(segments, output_path):
    """Generate SRT subtitle file from Whisper segments."""
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(segments, 1):
            start_time = format_time_srt(segment['start'])
            end_time = format_time_srt(segment['end'])
            text = segment['text'].strip()
            
            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")
    
    return output_path


def generate_fcpxml(segments, output_path, video_duration=None, fps=30):
    """
    Generate FCPXML subtitle file for Final Cut Pro.
    This creates a format that can be imported as titles/subtitles.
    """
    # Calculate total duration
    if segments:
        total_duration = max(seg['end'] for seg in segments)
    else:
        total_duration = video_duration or 60
    
    # Create FCPXML structure
    fcpxml = ET.Element('fcpxml', version='1.9')
    
    # Resources
    resources = ET.SubElement(fcpxml, 'resources')
    format_elem = ET.SubElement(resources, 'format', {
        'id': 'r1',
        'name': 'FFVideoFormat1080p30',
        'frameDuration': '1/30s',
        'width': '1920',
        'height': '1080'
    })
    
    # Library and Event
    library = ET.SubElement(fcpxml, 'library')
    event = ET.SubElement(library, 'event', {'name': 'Subtitles'})
    
    # Project
    project = ET.SubElement(event, 'project', {'name': 'Auto Subtitles'})
    sequence = ET.SubElement(project, 'sequence', {
        'duration': seconds_to_fcpxml_timecode(total_duration, fps),
        'format': 'r1'
    })
    spine = ET.SubElement(sequence, 'spine')
    
    # Add each segment as a title
    for i, segment in enumerate(segments):
        start = segment['start']
        duration = segment['end'] - segment['start']
        text = segment['text'].strip()
        
        # Create title element
        title = ET.SubElement(spine, 'title', {
            'name': f'Subtitle {i+1}',
            'lane': '1',
            'offset': seconds_to_fcpxml_timecode(start, fps),
            'duration': seconds_to_fcpxml_timecode(duration, fps),
            'start': '0s'
        })
        
        # Add text style
        text_elem = ET.SubElement(title, 'text')
        text_elem.text = text
        
        # Add text style definition
        text_style = ET.SubElement(title, 'text-style-def', {'id': f'ts{i+1}'})
        text_style_elem = ET.SubElement(text_style, 'text-style', {
            'font': 'PingFang SC',
            'fontSize': '48',
            'fontFace': 'Regular',
            'fontColor': '1 1 1 1',
            'bold': '0',
            'italic': '0',
            'underline': '0',
            'strike': '0',
            'alignment': 'center'
        })
    
    # Write to file
    tree = ET.ElementTree(fcpxml)
    ET.indent(tree, space='  ')
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    
    return output_path


def generate_txt(segments, output_path):
    """Generate plain text transcript."""
    with open(output_path, 'w', encoding='utf-8') as f:
        full_text = ' '.join(seg['text'].strip() for seg in segments)
        f.write(full_text)
    return output_path


def transcribe_audio(audio_path, model_size='base', language=None):
    """
    Transcribe audio file using OpenAI Whisper.
    
    Args:
        audio_path: Path to audio file
        model_size: Whisper model size (tiny, base, small, medium, large)
        language: Language code (e.g., 'zh', 'en', 'ja') or None for auto-detect
    
    Returns:
        List of segments with start, end, and text
    """
    if not WHISPER_AVAILABLE:
        raise RuntimeError("OpenAI Whisper not installed. Run: pip3 install openai-whisper")
    
    print(f"Loading Whisper model: {model_size}...")
    model = whisper.load_model(model_size)
    
    print(f"Transcribing: {audio_path}")
    print("This may take a few minutes depending on file length...")
    
    # Transcribe
    options = {}
    if language:
        options['language'] = language
    
    result = model.transcribe(audio_path, **options)
    
    segments = result.get('segments', [])
    detected_language = result.get('language', 'unknown')
    
    print(f"✓ Transcription complete!")
    print(f"  Detected language: {detected_language}")
    print(f"  Segments: {len(segments)}")
    
    return segments, detected_language


def main():
    parser = argparse.ArgumentParser(
        description="Generate subtitles from audio files using AI transcription"
    )
    parser.add_argument(
        "input",
        help="Input audio file path"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output subtitle file path (default: auto-generated)"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["srt", "fcpxml", "txt", "all"],
        default="all",
        help="Output format (default: all)"
    )
    parser.add_argument(
        "-m", "--model",
        choices=["tiny", "base", "small", "medium", "large"],
        default="base",
        help="Whisper model size (default: base). Larger = more accurate but slower"
    )
    parser.add_argument(
        "-l", "--language",
        help="Language code (e.g., zh, en, ja, ko). Auto-detect if not specified"
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=30,
        help="Frame rate for FCPXML (default: 30)"
    )
    
    args = parser.parse_args()
    
    # Check input file
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    # Check file extension
    valid_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg', '.opus', '.mp4', '.mov', '.aac', '.wma']
    input_ext = Path(args.input).suffix.lower()
    if input_ext not in valid_extensions:
        print(f"Warning: File extension {input_ext} may not be supported. Supported: {', '.join(valid_extensions)}")
    
    # Transcribe
    try:
        segments, detected_lang = transcribe_audio(args.input, args.model, args.language)
    except Exception as e:
        print(f"Transcription failed: {e}", file=sys.stderr)
        sys.exit(1)
    
    if not segments:
        print("No speech detected in audio file.", file=sys.stderr)
        sys.exit(1)
    
    # Generate output files
    input_stem = Path(args.input).stem
    output_dir = os.path.dirname(args.input) or '.'
    
    generated_files = []
    
    # Determine which formats to generate
    formats_to_generate = ['srt', 'fcpxml', 'txt'] if args.format == 'all' else [args.format]
    
    for fmt in formats_to_generate:
        if args.output and args.format != 'all':
            output_path = args.output
        else:
            output_path = os.path.join(output_dir, f"{input_stem}.{fmt}")
        
        try:
            if fmt == 'srt':
                result = generate_srt(segments, output_path)
                print(f"✓ SRT subtitles: {result}")
                generated_files.append(result)
                
            elif fmt == 'fcpxml':
                result = generate_fcpxml(segments, output_path, fps=args.fps)
                print(f"✓ FCPXML subtitles: {result}")
                generated_files.append(result)
                
            elif fmt == 'txt':
                result = generate_txt(segments, output_path)
                print(f"✓ Text transcript: {result}")
                generated_files.append(result)
                
        except Exception as e:
            print(f"Error generating {fmt}: {e}", file=sys.stderr)
    
    print(f"\n✓ Success! Generated {len(generated_files)} file(s)")
    for f in generated_files:
        print(f"  - {f}")
    
    # Print usage tips
    if 'fcpxml' in formats_to_generate:
        print("\n📌 To use in Final Cut Pro:")
        print("   1. Open Final Cut Pro")
        print("   2. File → Import → XML...")
        print("   3. Select the .fcpxml file")
        print("   4. The subtitles will appear as titles in your timeline")
    
    if 'srt' in formats_to_generate:
        print("\n📌 SRT file can be used in:")
        print("   - Final Cut Pro (File → Import → Captions)")
        print("   - Premiere Pro")
        print("   - DaVinci Resolve")
        print("   - YouTube/Vimeo uploads")


if __name__ == "__main__":
    main()

# Audio to Subtitles

從音頻文件提取字幕的 OpenClaw Skill，使用 OpenAI Whisper AI 進行語音識別。

## 功能特點

- 🤖 OpenAI Whisper AI 語音識別
- 📝 支持多種輸出格式：SRT、FCPXML、TXT
- 🎬 專為 Final Cut Pro 優化
- 🌍 自動語言檢測（支持中文、英文、日文等）
- ⚡ 可選模型大小（tiny 到 large）

## 安裝需求

```bash
# 安裝 OpenAI Whisper
pip3 install openai-whisper

# 確保 ffmpeg 已安裝（macOS）
brew install ffmpeg
```

## 使用方法

### 基本用法

```bash
# 生成所有格式（SRT + FCPXML + TXT）
python3 audio-to-subtitles.py audio.mp3

# 僅生成 SRT 字幕
python3 audio-to-subtitles.py audio.mp3 -f srt

# 僅生成 FCPXML（Final Cut Pro）
python3 audio-to-subtitles.py audio.mp3 -f fcpxml

# 僅生成純文字轉錄稿
python3 audio-to-subtitles.py audio.mp3 -f txt
```

### 指定語言

```bash
# 指定中文
python3 audio-to-subtitles.py audio.mp3 -l zh

# 指定英文
python3 audio-to-subtitles.py audio.mp3 -l en

# 指定日文
python3 audio-to-subtitles.py audio.mp3 -l ja
```

### 選擇模型大小

```bash
# 使用小模型（速度快，準確度較低）
python3 audio-to-subtitles.py audio.mp3 -m tiny

# 使用中等模型（平衡速度和準確度）
python3 audio-to-subtitles.py audio.mp3 -m medium

# 使用大模型（最準確，速度慢）
python3 audio-to-subtitles.py audio.mp3 -m large
```

### 指定幀率（FCPXML）

```bash
# 24fps 項目
python3 audio-to-subtitles.py audio.mp3 --fps 24

# 60fps 項目
python3 audio-to-subtitles.py audio.mp3 --fps 60
```

## 完整參數說明

```
audio-to-subtitles.py [-h] [-f {srt,fcpxml,txt,all}] [-o OUTPUT] [-m {tiny,base,small,medium,large}] [-l LANGUAGE] [--fps FPS] input

位置參數:
  input                 音頻文件路徑

選項參數:
  -h, --help            顯示幫助信息
  -f, --format          輸出格式: srt, fcpxml, txt, all (默認: all)
  -o, --output          輸出目錄 (默認: 與輸入文件同目錄)
  -m, --model           Whisper 模型大小 (默認: base)
  -l, --language        語言代碼 (默認: 自動檢測)
  --fps                 視頻幀率，用於 FCPXML (默認: 30)
```

## 輸出格式說明

### SRT 格式
- 標準字幕格式
- 支持幾乎所有視頻播放器
- 可用於 YouTube/Vimeo 上傳

### FCPXML 格式
- Final Cut Pro XML 格式
- 可直接導入 Final Cut Pro
- 字幕以標題形式呈現在時間軸上

### TXT 格式
- 純文字轉錄稿
- 無時間戳
- 適合閱讀和編輯

## 在 Final Cut Pro 中使用

### 導入 SRT 字幕
1. 打開 Final Cut Pro
2. File → Import → Captions...
3. 選擇 `.srt` 文件
4. 字幕會出現在時間軸的專用軌道上

### 導入 FCPXML 字幕
1. 打開 Final Cut Pro
2. File → Import → XML...
3. 選擇 `.fcpxml` 文件
4. 字幕會以標題形式出現在時間軸上
5. 可調整字體、顏色、位置等樣式

## 示例流程

### 從 YouTube 視頻生成字幕

```bash
# 1. 先下載音頻
yt-dlp -x --audio-format mp3 "https://youtube.com/watch?v=..." -o video.mp3

# 2. 生成字幕
python3 audio-to-subtitles.py video.mp3 -f all -m medium

# 3. 在 Final Cut Pro 中使用生成的 .srt 或 .fcpxml 文件
```

### 從 Bilibili 視頻生成字幕

```bash
# 1. 提取音頻（使用 video-audio-extractor Skill）
python3 extract-audio.py "https://bilibili.com/video/BV..." -f mp3

# 2. 生成字幕
python3 audio-to-subtitles.py bilibili_audio.mp3 -l zh

# 3. 在剪輯軟件中使用
```

## 模型選擇建議

| 模型 | 準確度 | 速度 | 建議用途 |
|------|--------|------|----------|
| tiny | ⭐⭐ | ⚡⚡⚡ | 快速測試、對準確度要求不高 |
| base | ⭐⭐⭐ | ⚡⚡ | 日常使用、平衡選擇 |
| small | ⭐⭐⭐⭐ | ⚡ | 較高準確度需求 |
| medium | ⭐⭐⭐⭐⭐ | 🐢 | 專業用途 |
| large | ⭐⭐⭐⭐⭐ | 🐢🐢 | 最高準確度、後期製作 |

## 注意事項

⚠️ **第一次運行**：需要下載模型文件，根據模型大小可能需要幾分鐘。

⚠️ **顯存需求**：大模型需要較多顯存，如果出現 OOM 錯誤，請使用較小的模型。

⚠️ **語言檢測**：自動檢測通常準確，但混合語言音頻建議手動指定 `-l` 參數。

## 常見問題

### Q: 為什麼生成的字幕時間不準確？
A: 確保提供的 `--fps` 參數與視頻實際幀率一致。

### Q: 中文識別效果不佳？
A: 嘗試使用更大的模型（medium 或 large），或確保音質清晰。

### Q: FCPXML 導入後字幕位置不對？
A: 在 Final Cut Pro 中選中字幕，調整 Inspector 中的 Position 參數。

### Q: 如何批量處理多個音頻文件？
A: 目前需要逐個處理，批量功能正在開發中。

## 相關 Skill

- [video-audio-extractor](https://github.com/kantylee/video-audio-extractor) - 從視頻提取音頻
- 兩個 Skill 配合使用可完成「視頻 → 音頻 → 字幕」的完整流程

## 作為 OpenClaw Skill 使用

```bash
# 安裝 Skill
openclaw skills install /path/to/audio-to-subtitles.skill

# 或在 OpenClaw 對話中使用
"幫我從這個音頻文件生成字幕: audio.mp3"
```

## 開發者

Created by [kantylee](https://github.com/kantylee) for OpenClaw

## 許可證

MIT License

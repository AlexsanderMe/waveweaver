# WaveWeaver - Audio Stem Separation Application 🎵

A audio stem separation application powered by Demucs AI models.

## Features

- 🎵 High-quality audio stem separation
- 🚀 GPU acceleration support
- 🎨 Intuitive interface
- 📁 Drag & drop file support
- 🔧 Multiple AI models (HTDemucs, MDX-Extra, etc.)
- 📊 Progress tracking

## Installation

### From Source
```bash
git clone https://github.com/AlexsanderMe/waveweaver.git
cd waveweaver
pip install -r requirements.txt
python main.py
```

## Usage

1. Select an audio file (MP3, WAV, FLAC, M4A, OGG)
2. Choose your preferred AI model
3. Select output folder
4. Pick stems to extract
5. Click "Extract Stems"

## System Requirements

- Python 3.8+
- 4GB RAM minimum (8GB+ recommended)
- CUDA-compatible GPU (optional, for faster processing)

## Project Structure

```
waveweaver/
├── README.md
├── LICENSE
├── requirements.txt
├── setup.py
├── pyproject.toml
├── .env
├── .gitignore
├── main.py
│
├── src/
│   └── waveweaver/
│       ├── __init__.py
│       ├── app.py
│       ├── config/
│       │   ├── __init__.py
│       │   └── settings.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   └── stem_separator.py
│       ├── gui/
│       │   ├── __init__.py
│       │   ├── main_window.py
│       │   ├── components/
│       │   │   ├── __init__.py
│       │   │   ├── audio_section.py
│       │   │   ├── model_selection.py
│       │   │   ├── stem_selection.py
│       │   │   ├── output_section.py
│       │   │   └── progress_section.py
│       │   └── styles/
│       │       ├── __init__.py
│       │       └── theme.py
│       └── utils/
│           ├── __init__.py
│           ├── file_handler.py
│           └── helpers.py
│
├── assets/
│   ├── icons/
│   │   ├── ico.ico
│   │   └── github.png
│   └── images/
│
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_core/
    │   ├── __init__.py
    │   └── test_stem_separator.py
    ├── test_gui/
    │   ├── __init__.py
    │   └── test_main_window.py
    └── test_utils/
        ├── __init__.py
        └── test_file_handler.py
        └── test_helpers.py
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Credits

Created by [AlexsanderMe](https://github.com/AlexsanderMe)
Powered by [Demucs](https://github.com/facebookresearch/demucs)
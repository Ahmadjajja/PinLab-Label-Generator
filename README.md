# 📦 PinLab Label Generator

**PinLab Label Generator** is a modern desktop application built in Python for creating and printing scientific labels, originally designed for entomological and field collection purposes.

It is the upgraded version of the legacy software *PinLab v1.0* written over 20 years ago by **Daniel L. Gustafson, Ph.D.** in **Fortran + WINTERACTER**, which had limitations like PCL-only output, lack of Unicode support, and no direct printing or editing interface.

This new version **v2.0**, developed by **Ahmad Jajja**, solves those limitations using modern technologies and provides both **PDF generation** and **direct printer output**, while supporting all ASCII and Unicode characters.


## 🚀 Features

- 📂 **Load structured `.txt` label files** - Import your label data from text files
- 📝 **View and edit label content directly** - Built-in editor for real-time modifications
- ⚙️ **Validate and process input files** - Comprehensive error checking with line feedback
- 📄 **Generate high-resolution PDFs** - Create professional printable documents
- 🖨️ **Direct printer output** - Send labels straight to your default printer
- ❓ **Help & About dialogs** - Guided usage instructions and version information
- 🎨 **Modern GUI interface** - Clean, intuitive design built with Tkinter
- 🧠 **Full Unicode support** - Monospaced fonts for perfectly aligned output


## 📁 Input File Format

Your `.txt` label files should follow this specific structure:

```
25
30
MONT: Lincoln Co.
Scenery Mountain Trail
48.4160°N,115.7173°W
09 JULY 2024, 2101m
J.Vega,J.Vargas, net
15
...
```

**Format Explanation:**
- **Line 1:** Maximum character width per label
- **Line 2:** Number of times to repeat the following label block  
- **Next lines:** The actual label content (variable number of lines)
- **Next number:** Repeat count for the subsequent label block
- **Continue pattern:** Alternating counts and label blocks

✅ **Note:** Each label block can contain any number of lines, and special characters like degree symbols (°) are fully supported.


## 🛠️ Installation

### Option 1: Windows Executable (Recommended for End Users)

1. Download the latest `.exe` file from the [Releases](https://github.com/Ahmadjajja/PinLab-Label-Generator/releases) page
2. No Python installation required - just run the executable
3. Perfect for researchers and lab technicians who need the tool without development setup

### Option 2: Developer Setup (Source Code)

**Prerequisites:**
- Python 3.7 or higher
- Git

**Installation Steps:**

```bash
# Clone the repository
git clone https://github.com/ahmadcodes/pinlab-label-generator.git
cd pinlab-label-generator

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux  
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python pinlab_gui.py
```


## 🖨️ Printing Setup & Requirements

### System Requirements
- **Windows:** Windows 7 or later (recommended: Windows 10+)
- **Printer:** Any Windows-compatible printer set as default
- **PDF Reader:** Adobe Acrobat Reader (for direct printing functionality)

### Printing Configuration
1. Ensure your printer is **connected** and **powered on**
2. Set your desired printer as the **system default**
3. Install **Adobe Acrobat Reader** and set it as the default PDF application
4. The application uses `os.startfile()` for seamless printing integration


## 💻 Usage Guide

### Basic Workflow
1. **Launch** the PinLab Label Generator
2. **Load** your structured `.txt` file using the "Load File" button
3. **Review** and edit the label content in the built-in editor
4. **Validate** the file format using the validation feature
5. **Generate** PDF output or send directly to printer
6. **Print** your professional scientific labels

### File Validation
The application provides comprehensive validation including:
- Format structure verification
- Character width compliance checking  
- Error reporting with specific line numbers
- Unicode character compatibility testing


## 🧠 Technical Architecture

### Core Technologies
- **Python 3.x** - Primary development language
- **Tkinter** - Cross-platform GUI framework
- **ReportLab** - Professional PDF generation and rendering
- **PyInstaller** - Executable packaging for distribution
- **win32api/win32print** - Native Windows printing integration

### Key Components
- `pinlab_gui.py` - Main application interface
- Label parsing and validation engine
- PDF generation and formatting system
- Direct printer communication module
- Error handling and user feedback system


## 🧑‍💻 Developer Information

**Developed by:** Ahmad Jajja

🌐 **Website:** [ahmad-jajja.com](https://ahmad-jajja.com)  
🔗 **LinkedIn:** [linkedin.com/in/ahmad-jajja](https://linkedin.com/in/ahmad-jajja)  
🐙 **GitHub:** [github.com/Ahmadjajja](https://github.com/Ahmadjajja)


## 📜 License & Usage

```
© 2025 Ahmad Jajja. All Rights Reserved.

This software is provided "as is" without warranty of any kind. 
Redistribution and use in source or binary forms, with or without 
modification, are not permitted without explicit written permission 
from the author.

Licensed for educational, research, and internal laboratory use only.
```


## 📌 Version History

| Version | Developer | Release Date | Key Features |
|---------|-----------|--------------|--------------|
| **v1.0** | Daniel L. Gustafson, Ph.D. | 2004 | Original Fortran + WINTERACTER implementation |
| **v2.0** | Ahmad Sultan | 2025 | Modern Python GUI with PDF/printer support |

### Legacy Version Limitations (v1.0)
- PCL-only output format
- No Unicode character support
- Limited editing capabilities
- No direct printing interface
- Platform compatibility issues

### Modern Version Improvements (v2.0)
- ✅ Full Unicode support
- ✅ PDF and direct printing
- ✅ Modern GUI interface
- ✅ Real-time editing
- ✅ Comprehensive validation
- ✅ Cross-platform compatibility


## 🤝 Contributing

We welcome contributions from the scientific and development communities!

### How to Contribute
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 Python coding standards
- Include comprehensive docstrings
- Add unit tests for new functionality
- Update documentation as needed


## 🐛 Issues & Support

### Reporting Issues
- **Bug Reports:** Use the [Issues](https://github.com/Ahmadjajja/PinLab-Label-Generator/issues) page
- **Feature Requests:** Submit detailed enhancement proposals
- **Questions:** Connect via LinkedIn or open a discussion

### Common Troubleshooting
- **Printing Issues:** Verify default printer settings and Adobe Reader installation
- **File Format Errors:** Check input file structure against the documented format
- **Unicode Problems:** Ensure your system supports the required character sets


## 🔗 Repository Links

**Main Repository:** [github.com/Ahmadjajja/PinLab-Label-Generator](https://github.com/Ahmadjajja/PinLab-Label-Generator)

**Quick Links:**
- [📥 Download Latest Release](https://github.com/Ahmadjajja/PinLab-Label-Generator/releases)
- [🐛 Report Issues](https://github.com/Ahmadjajja/PinLab-Label-Generator/issues)
- [📚 Documentation](https://github.com/Ahmadjajja/PinLab-Label-Generator/wiki)
- [💬 Discussions](https://github.com/Ahmadjajja/PinLab-Label-Generator/discussions)


## 🏆 Acknowledgments

Special thanks to **Daniel L. Gustafson, Ph.D.** for the original PinLab concept and vision that inspired this modern implementation.


*Built with ❤️ for the scientific research community*

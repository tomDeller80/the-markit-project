# Security Policy

## Supported Versions
Currently, only the latest release is supported for security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability
I take the security of this project seriously. If you find a potential security flaw, please do not report it via a public Issue. Instead:

1. **Email me:** tom@deller.co
2. **Response Time:** On a best-effort basis.
3. **Disclosure:** Once a fix is applied, a new version will be released with a patch note.

## Local-First Privacy
MarkIt! is designed with a "Zero-Network" architecture. 
- **No Data Collection:** The application does not phone home, track usage, or upload images to any server.
- **Local Processing:** All image manipulation happens entirely within your computer's RAM/Disk.
- **Dependency Auditing:** This project uses `Pillow` for image parsing. I recommend always using the latest release to ensure you have the most recent security patches from the Pillow team.

## 🛡️ Executable Integrity & Antivirus Flags

- Because **The Markit! Project** is an independent, open-source tool, the Windows executables are currently unsigned.

- **Heuristic Flags:** Some aggressive antivirus engines (notably **Bkav Pro** and **SecureAge**) may flag the .exe as "Malicious" or "AIDetect." These are **potentially false positives** common with unrecognized software that performs local file operations (like saving watermarked images).

- **Transparency:** While it is believed these flags to be incorrect based on our code audits, it is encouraged that users to treat all software with caution.

- **Verification:** Always verify the SHA-256 Checksum provided in the Latest Release notes before running the application.

- **Audit:** If you have security concerns, you are encouraged to audit the source code or build the executable yourself from the repository.
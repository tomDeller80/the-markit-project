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
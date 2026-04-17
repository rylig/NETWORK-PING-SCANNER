# 🚀 Rylig CDIR Scanner

[English](README.md) | [فارسی](README-FA.md)

![rylig CDIR Scanner Screenshot](https://github.com/rylig/rylig-CDIR-scanner/blob/main/screenshot.jpg?raw=true)

A fast, efficient, multi-threaded IP ping scanner written in Python. Designed for simplicity, performance, and practical network analysis.

---

## ✨ Features

- **Multi-threaded Scanning** – Scan large IP ranges quickly with adjustable thread count  
- **CIDR Range Support** – Easily scan full subnets (e.g., `/24`)  
- **Auto-Save** – Active IPs are automatically saved to `active.txt`  

---

## 🛠 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/rylig/rylig-CDIR-scanner.git
cd rylig-CDIR-scanner
````

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

---

## ⚙️ Usage

### 1. Prepare Your IP Ranges

Create a file (e.g., `range.txt`) and add your IP ranges.

Each line should contain one CIDR range:

```
8.6.112.0/24
8.6.144.0/24
8.6.145.0/24
```

---

### 2. Run the Scanner

Run the script:

```bash
python scanner.py
```

You will be prompted to:

* Enter the path to your range file (e.g., `range.txt`)
* Enter the number of concurrent threads (how many IPs to scan at the same time)

---

### 3. View Results

* All responsive IPs will be saved automatically in:

```
active.txt
```

---

## 📌 Notes

* Higher thread counts = faster scans, but more network load
* Use responsibly and only on networks you own or have permission to scan
* Works best on stable network connections

---

## ⚠️ Disclaimer

This tool is intended for educational and authorized network testing purposes only. Unauthorized scanning of networks may be illegal in your jurisdiction.

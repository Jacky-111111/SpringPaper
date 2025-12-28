# 🌸 SpringPaper — Chinese Papercut Art Simulator

SpringPaper is an interactive digital simulator inspired by **traditional Chinese papercutting art** commonly seen during the Spring Festival.

By simulating the real-world **folding-and-cutting process** used to create symmetrical paper decorations, SpringPaper allows users to design their own papercut artworks through simple clicks and drags — combining cultural heritage with computational creativity.

---

## 🎯 Project Motivation

Traditional Chinese papercutting is a cultural art form that relies heavily on spatial symmetry, folding logic, and manual craftsmanship.  
SpringPaper aims to:

- Preserve and reimagine traditional papercutting techniques in a digital format  
- Help users intuitively understand symmetry and geometric patterns  
- Provide a playful, creative tool that blends art, culture, and programming  

---

## ✂️ How It Works

SpringPaper simulates the **sector-based folding model** used in real papercutting:

1. The paper is conceptually folded into equal angular sectors  
2. Users draw cut paths within a single sector  
3. The system mirrors and rotates the cuts across all folds  
4. A full symmetrical papercut pattern is generated in real time  

This approach closely mirrors real-life papercutting logic while remaining intuitive for users.

---

## 🧠 Key Features

- **Symmetry-Based Papercut Simulation**  
  Automatically mirrors user-drawn cuts across multiple folds

- **Interactive Drawing Interface**  
  Create designs using mouse clicks and drag gestures

- **Configurable Folding Parameters**  
  Adjust number of folds and paper radius to explore different symmetry styles

- **Instant Visual Feedback**  
  See the complete papercut pattern update dynamically as you draw

- **Instruction & Sample Modes**  
  Includes usage instructions and example designs for exploration

---

## 🏗️ System Design

- Each papercut is defined by a sequence of user-drawn paths  
- Paths are stored in a base sector and transformed via rotation  
- The simulator ensures all cuts remain within valid paper boundaries  
- The final rendering overlays all symmetric copies to form the artwork  

---

## ⚙️ Tech Stack

- **Language:** Python  
- **Graphics Framework:** `cmu_graphics` (CMU CS Academy)  
- **Math Utilities:** Trigonometry and geometric transformations  
- **Environment:** Designed to run in CMU CS Academy or compatible Python environments  

---

## ▶️ How to Run

This project is designed to run in **CMU CS Academy**.

1. Open CMU CS Academy  
2. Create a new Python project  
3. Paste the contents of `main.py` into the editor  
4. Run the program and start creating papercut designs  

> 💡 No additional libraries are required beyond `cmu_graphics`.

---

## 📚 Educational Value

SpringPaper demonstrates:

- Computational geometry and symmetry  
- Event-driven programming  
- Object-oriented design for graphical systems  
- Cultural computing through code  

It serves as both a creative tool and an educational example of how programming can model real-world artistic processes.

---

## 🌱 Future Improvements

- Export papercuts as images or SVG files  
- Support free-form folding angles  
- Add color and layering options  
- Enable saving and loading designs  

---

## 📄 Notes

This project was coded to be run in **CMU CS Academy**  
and was developed as a creative programming project exploring cultural art simulation.

---

## 📜 License

This project is intended for educational and non-commercial use.

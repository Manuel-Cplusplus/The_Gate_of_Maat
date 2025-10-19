# The Gate of Maat  
### Formal Methods Laboratory  

This repository contains all files used for the development of a **Formal Methods laboratory exercise** within the *Computer Science* degree program at the **University of Bari “Aldo Moro”**.

---

## Table of Contents
1. [Description](#description)  
2. [Installation](#installation)  
3. [Running the Project](#running-the-project)  
4. [Notes](#notes)  
5. [License and Author](#license-and-author)

---

## Description  

**The Gate of Maat** is a *Finite State Machine (FSM)* integrated with a *Large Language Model (LLM)* simulating a mythological entity — the **Sphinx** — whose purpose is to test the user’s *worthiness* through an interactive dialogue.  

During the conversation, the user faces a sequence of **conceptual trials** designed to evaluate logic, intuition, and humility.  
Each response contributes to an **internal score**; at the end of the dialogue, the Sphinx determines whether the user is *worthy to cross the gate* or should be *rejected*.  

From a technical perspective, the project demonstrates the integration of:  
- **Formal Methods and FSMs**, to model deterministic transitions and behaviors.  
- **Large Language Models (LLMs)**, to dynamically generate dialogue and evaluate user's responses.  

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Manuel-Cplusplus/The_Gate_of_Maat.git
```

2. Move into the project folder:
```bash
cd The_Gate_of_Maat
```

3. Copy the environment file:
```bash
cp .env.example .env
```

4. Inside the .env file, insert your valid OpenAI API key to enable language model access.

5. Create a virtual environment
- Windows:
```bash
python -m venv myenv
```
- Linux/MacOS:
```bash
python3 -m venv venv
```

6. Activate the virtual environment
- Windows:
```bash
myenv\Scripts\activate
```
- Linux/MacOS:
```bash
source venv/bin/activate
```

7. Install dependencies:
```bash
pip install -r requirements.txt
```
If required, also install the custom FSM package:
```bash
pip install fsm-llm
```

---

## Running the Project
To start the simulation:
```bash
python src/TheGateOfMaat.py
```

Once launched, the system initiates an interactive session with the Sphinx.
The user must respond to each trial, and the final outcome — Grace or Condemnation — will be revealed based on the accumulated score.


___
## Note
If you add new dependencies, update the requirements.txt file:
```bash
pip freeze > requirements.txt
```

In case of errors, you could try to install the the custom FSM package:
```bash
pip install fsm-llm
```

[Custom FSM package reference](https://github.com/jsz-05/LLM-State-Machine)

---
## License and Author

**Author:** Manuel Carlucci  
**Year:** 2025  
**Project:** *The Gate of Maat*  

This project is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** license.  

---

### You are free to:
- **Share** — copy and redistribute the material in any medium or format  
- **Adapt** — remix, transform, and build upon the material  

### Under the following terms:
- You must give **appropriate credit**  
- You may not use the material for **commercial purposes**  
- Any derivative works must be distributed under the **same license**  

[View the full license here](https://creativecommons.org/licenses/by-nc-sa/4.0/)


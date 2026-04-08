# 🚀 Chitti AI – Emergent Multi-Agent MCP System

> **“We don’t orchestrate intelligence — we let it emerge.”**

---

## 🧠 Overview

**Chitti AI** is a **multi-agent system built on MCP (Model Context Protocol)** where multiple AI agents collaboratively solve problems by interacting through a **shared memory (MCP)**.

Unlike traditional systems:

* ❌ No fixed roles (planner, critic, etc.)
* ❌ No linear pipelines
* ✅ Agents self-organize
* ✅ Intelligence **emerges over iterations**

---

## 🎯 Problem Statement

Modern AI systems are:

* Static
* Pipeline-based
* Role-dependent

👉 We aim to build a system where:

* Multiple agents **think together**
* Improve each other’s ideas
* Produce **better structured solutions over time**

---

## 🧬 Core Concept

Inspired by **Swarm Intelligence** 🐜

| Nature          | Chitti AI             |
| --------------- | --------------------- |
| Ants            | AI Agents             |
| Pheromones      | MCP Shared Memory     |
| Colony Behavior | Emergent Intelligence |

---

## ⚙️ System Architecture

```text
User Input
   ↓
MCP Initialized (Shared Memory)
   ↓
Iteration 1 → Raw Ideas
   ↓
Iteration 2 → Improved Ideas
   ↓
Iteration 3 → Structured Ideas
   ↓
Scoring + Voting
   ↓
Final Output (Clean Plan)
```

---

## 🧠 How It Works

### 🔹 1. Shared Memory (MCP)

* Stores:

  * Problem
  * Ideas
  * Iterations
  * Scores & votes
* Acts as a **communication layer**

---

### 🔹 2. Agents (Role-Free)

Each agent:

* Reads MCP
* Writes improvements

Agents can:

* Add ideas
* Refine ideas
* Combine ideas
* Critique ideas

👉 Roles are **not assigned** — they **emerge**

---

### 🔹 3. Iterative Refinement

#### Iteration 1

* Raw, unstructured ideas

#### Iteration 2

* Improvements + combinations

#### Iteration 3

* Structured + refined solutions

---

### 🔹 4. Scoring & Voting

Ideas are evaluated based on:

* Clarity
* Practicality
* Completeness

Best ideas are selected and merged into final output.

---


## 🏗️ Tech Stack

### 🔹 Backend

* Python
* MCP Server (FastMCP)
* Custom Orchestrator

### 🔹 AI / Agents

* (Upcoming) LangChain + Gemini API
* Multi-agent simulation

### 🔹 Memory

* In-memory state (current)
* (Planned) Vector DB (pgvector)

### 🔹 Frontend (In Progress)

* React.js
* Tailwind CSS

---

## 📂 Project Structure

```text
Chitti-AI/
│
├── backend/
│   ├── server.py
│   ├── chitti/
│   │   ├── orchestrator.py
│   │   ├── memory.py
│   │   ├── agents.py
│   │   └── scorer.py
│
├── frontend/ (WIP)
│
├── screenshots/
│
└── README.md
```

---

## 📸 Demo Screenshots

> Add your screenshots here

```markdown
![Initialize](screenshots/init.png)
![Iteration1](screenshots/iteration1.png)
![Iteration2](screenshots/iteration2.png)
![Iteration3](screenshots/iteration3.png)
![Final Output](screenshots/final.png)
```

---

## 🚀 How to Run

```bash
git clone https://github.com/Shrinivas-py/Chitti-AI.git
cd Chitti-AI
pip install -r requirements.txt
python server.py
```

---

## 🧠 Example Output

```text
Day 1: Learn HTML basics + build a simple page  
Day 2: Learn CSS + responsive design  
Day 3: Practice JavaScript fundamentals  
...
```

---

## 💡 Unique Selling Point

> **Emergent Intelligence Architecture**

* No predefined roles
* No fixed pipelines
* Agents evolve behavior dynamically

👉 This mimics **real-world collaborative thinking**

---

## 🔥 Why This Stands Out

* Goes beyond chatbots ❌
* Demonstrates real **multi-agent coordination**
* Implements **MCP as infrastructure layer**
* Shows **emergent intelligence**, not scripted logic

---

## 🧠 Future Scope

* Self-learning agents (feedback loop)
* Digital twin systems
* Autonomous decision engines
* Integration with real-world tools/APIs


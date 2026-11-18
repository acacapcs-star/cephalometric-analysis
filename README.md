# 側顱頭影測量與誤差分析 · Cephalometric Measurement & Error Analysis

從 2D 側顱 X 光的**標記點座標**計算頭影測量角度/距離,含 **Monte Carlo 誤差分析**與**幾何自檢**。跨校牙醫 × 資工研究合作的一部分(2026/09 起,進行中)。

> 本 repo **只包含我自己的程式**,以**自編座標**示範。不含任何病人 X 光、座標或臨床結果;病人資料僅在研究團隊內、依院方規定處理。

---

## 中文

### 我的分工
量測計算與誤差分析(CS 側):把標記點座標換算成標準頭影測量角度與距離,並量化標記誤差會讓每一項偏多少。

### 這個程式在做什麼
給定解剖標記點(Sella、Nasion、A 點、B 點…)的 (x, y),計算標準頭影測量(SNA、SNB、ANB、FMA、Y-axis、Interincisal、FMIA…),並回答**每個數字有多可信**。

**1 · 三個幾何基礎運算**:三點夾角、兩線夾角、點到線距離 —— 所有測量都由這三個組出來(`measure.py`)。

**2 · 三個「會錯但不報錯」的陷阱**(特意記錄,因為它們都是靜默出錯):

| 陷阱 | 為什麼會錯 |
|---|---|
| ANB 必須用 `SNA − SNB` | 直接取 A–N–B 三點夾角是無正負號的,Class III 會被讀成 Class II |
| 角度尺度無關,距離不是 | 角度可跨機器比較;mm 距離要校正 —— 片上尺規兩端相距 20 mm,用它把像素換算成毫米 |
| 影像 y 軸向下 | 所有幾何推導要跟著翻,否則上下顛倒 |

**3 · Monte Carlo 誤差傳播**:標記不可能像素級精確。把每個點按其 σ 擾動、重算 2000 次,得到每項測量的標準差與 95% 區間。

**4 · Tweed 幾何自檢**:FMA + FMIA + IMPA 必須 = 180°(三角形內角和),自動檢查以抓出公式的正負/慣例錯誤。

### 一個方法主張
標記誤差傳到角度是**不均勻**的:模擬中(每點 ±1.5 px),同樣的點誤差在臂長較長的角度影響小、臂長較短的被放大。所以「平均誤差幾 mm」說不出任一項能不能用 —— 醫師讀的是角度,誤差棒就該放在角度上。(此為模擬下的推論,下一步用人工修正過的真實標記驗證。)同理,評估基準應是 **inter-observer variability** 而非絕對誤差。

### 執行 demo(假資料)
```bash
pip install numpy
python demo.py
```
輸出:自編標記點的各項測量 + ±2σ 誤差棒,以及 Tweed 自檢(= 180.0)。

### 檔案
| 檔案 | 內容 |
|---|---|
| `measure.py` | 各項測量 + 三個幾何基礎運算 |
| `demo.py` | 假座標的完整 demo(Monte Carlo + Tweed) |
| `measurement_definitions.md` | 每項測量:用哪些點、公式、意義 |

---

## English

### My role
Measurement computation and error analysis (CS side): turning annotated landmark coordinates into standard cephalometric angles and distances, and quantifying how much landmark-placement error moves each measurement.

### What it does
Given landmark (x, y) positions, compute standard cephalometric measurements (SNA, SNB, ANB, FMA, Y-axis, Interincisal, FMIA, …) and **how trustworthy each number is**.

**1 · Three geometry primitives** — angle-at-a-point, angle-between-two-lines, point-to-line distance (`measure.py`).

**2 · Three traps that give wrong numbers without any error:**

| Trap | Why it goes wrong |
|---|---|
| ANB must be `SNA − SNB` | The raw A–N–B angle is unsigned, so a Class III reads as Class II |
| Angles are scale-invariant, distances are not | Angles compare across machines; mm distances need calibration — the film ruler is 20 mm, used for pixels → mm |
| Image y-axis points down | Every geometric derivation must follow, or it flips upside-down |

**3 · Monte Carlo error propagation** — jitter each landmark by its σ, recompute 2000 times, report each measurement's standard deviation and 95% interval.

**4 · Tweed geometric self-check** — FMA + FMIA + IMPA must equal 180°, checked automatically to catch sign/convention errors.

### A methodological point
Landmark error propagates into angles **unevenly**: the same point error is small on long-armed angles and amplified on short-armed ones. So a single "average error in mm" cannot say whether any measurement is usable; the benchmark should be **inter-observer variability**, not absolute error.

### Run the demo (synthetic data)
```bash
pip install numpy
python demo.py
```

### Files
| File | What it is |
|---|---|
| `measure.py` | The measurements + three geometry primitives |
| `demo.py` | End-to-end demo on synthetic coordinates (Monte Carlo + Tweed) |
| `measurement_definitions.md` | Each measurement: landmarks, formula, meaning |

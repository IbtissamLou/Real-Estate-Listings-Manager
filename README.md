# 🏘️ Quick Shop

## 📌 Project Description
**Quick Shop** is a housing marketplace management application that enables users to **collect, process, and interact with real estate listings** from multiple sources.

The system allows users to **upload listings, and manage housing advertisements** within a unified environment. It also provides **personalized tracking features**, such as wishlists and historical activity, to improve the overall user experience.

---

## 🎯 Target Users
- Individuals searching for housing opportunities  
- Users who want to track and compare real estate listings  
- Data-driven users interested in aggregating listings from multiple sources  

---

## ✅ Key Guarantees
- Centralized management of housing listings  
- Persistent user data (favorites & history)  
- Structured data ingestion pipeline (upload + scraping)  
- Reliable filtering and search capabilities  

---

## 🚀 Main Features
- 📥 Upload and manage housing listings  
- 🌐 Web scraping integration for listing aggregation  
- ❤️ Wishlist system for saving favorite properties  
- 📜 User history tracking  
- 🔎 Advanced filtering and search (`RechercheFiltre`)  

---

## 🧠 System Architecture
The application follows a modular architecture:

- **Data Ingestion Layer**  
  → Upload + web scraping  

- **Processing Layer**  
  → Filtering, transformation, business logic (`RechercheFiltre`)  

- **Storage Layer**  
  → Database (ENSAI environment required)  

- **Application Layer**  
  → Main execution via `main.py`  

---

## ⚙️ Local Installation & Execution

### Prerequisites
- Python **3.10+**  
- Updated `pip`  

⚠️ **Database Access Requirement**  
- ENSAI Wi-Fi  
**OR**  
- ENSAI Virtual Machine (VMware Horizon Client)  

⚠️ **Compatibility Note**  
- Recommended: **Windows 10 or higher**  
- May not work properly on Linux / macOS / Apple Silicon  

### Installation
```bash
pip install -r requirements.txt
```

### Run the Application
python main.py

---

## 🎯 API Usage / 🖥️ User Interface (Streamlit)
- Current version: CLI-based application
- No API or Streamlit UI yet
- Planned: Web interface in future versions

---

## ⏱️ Performance Goals
- Efficient filtering over large datasets
- Fast retrieval of wishlist and user history
- Scalable data ingestion (scraping + upload)

---

## 📊 Evaluation & Metrics (Planned)
- Filtering accuracy and relevance
- Data completeness from scraping
- System responsiveness (latency)

---

## 🔐 Privacy & Security
- User data (favorites, history) is securely stored
- Database access restricted to ENSAI infrastructure
- No external exposure of sensitive data

---

## 🧪 🔁 Continuous Testing & Integration
- Testing framework: unittest

Run tests:

```bash
python -m unittest
```

- RechercheFiltre is thoroughly tested on real datasets
- Combination of multiple functions validated
- Code is documented for maintainability

---
  
## 🚚 🚀 Continuous Delivery
- Manual delivery process
- Reproducible setup via requirements.txt

---

## 🚀 Continuous Deployment 
- Not deployed yet
- Architecture compatible with future cloud deployment

---

## 🔥 Future Improvements
🌍 Web interface (Streamlit or React)
🔗 Public API
☁️ Cloud deployment (Azure / AWS)
📊 Advanced analytics & recommendations
🧠 AI-powered listing ranking

---

## 🏁 Vision
Build a smart real estate assistant that helps users make better housing decisions through data, automation, and AI.

---

## 🧑‍💻 Authors
ENSAI Project Contributors

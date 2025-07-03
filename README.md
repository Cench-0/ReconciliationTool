# 🧾 Reconciliation Tool – Transaction Comparator

A lightweight Flask web application that compares financial transactions from two sources:  
- **Internal System Export** (your platform's records)  
- **Provider Statement** (your payment processor's records)

This tool helps identify **matched**, **missing**, and **mismatched** transactions — making it useful for reconciling payments, spotting errors, and ensuring financial accuracy.

## 🚀 Features
- Upload two CSV files (internal & provider)
- Compare using `transaction_reference`
- Categorize into:
  - ✅ Matched transactions
  - ⚠️ Present only in internal file
  - ❌ Present only in provider file
- Bonus: Highlight mismatched `amount` or `status`
- Download results in separate CSVs

## 📂 How It Works
1. Upload your two transaction CSVs
2. Click **Compare Transactions**
3. View categorized results instantly
4. Download clean CSVs of each result set

## 💡 Example Use Case
A fintech ops team uploads:
- Their platform’s export
- The payment provider’s report

→ Within seconds, they can see discrepancies and export clean, reconciled results.

## 🛠 Tech Stack
- Python (Flask)
- HTML/CSS + Bootstrap
- Pandas for CSV processing
- Replit-hosted (live URL)

## 📁 Sample CSV Format
```csv
transaction_reference,amount,status
TX001,1000,success
TX002,2500,failed

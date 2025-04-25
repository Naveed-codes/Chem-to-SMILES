# 🔬 Chemical Name to SMILES Converter

This is a command-line Python script that converts a list of **chemical names to their SMILES** representations using the **PubChem PUG REST API**.

---

## 📄 Features

- 📥 Accepts a `.txt` file of chemical names (one per line)
- 🖼️ Generate and save 2D structure images
- 🔄 Fetches SMILES using PubChem's public API
- 🧠 Intelligent error handling (invalid names, no results)
- ⚡ Batch processing with optional multi-threading for speed
- 📤 Saves results as a `.csv` file: `Name,SMILES`
- 💻 Easy to use from terminal or integrate into pipelines
- 🖥️ Can be run entirely from the terminal

## ⚙️ Requirements

- Python ≥ 3.6
- [RDKit](https://www.rdkit.org/)
- [PubChemPy](https://github.com/mcs07/PubChemPy)

🚀 Usage

📌 Single Chemical Name

python chemname2smiles.py "glucose"
  

📌 Save SMILES to a File

python chemname2smiles.py "glucose" -o output.txt


📌 Save 2D Molecule Image

python chemname2smiles.py "glucose" -i glucose.png


📌 Batch Mode (From File)

python chemname2smiles.py chemicals.txt -b -o smiles_output.tsv

📌 Optional multi-threading (e.g., 8 threads):

python3 chem2smiles.py --input chemicals.txt --output smiles.csv --threads 8


📂 Input File Format (batch mode)
A plain text file with one chemical name per line:

Glutamic acid
Ferulic acid
Niacin

✅ Output Format
You’ll get a .csv file:


Name	SMILES
Glutamic acid	C(CC(=O)O)C(C(=O)O)N
Ferulic acid	COc1cc(C=CC(=O)O)ccc1O
Niacin	C5H4N(CO)OH
If a name fails to resolve, it will be marked as "Not Found".

🧑‍💻 Author
Naveed Hasan
📧 naveedhasan2000@gmail.com
🐙 @Naveed-codes

# 🧬 Protein Structure and Coevolution Analysis Workflow

Follow this step-by-step guide to analyze protein structures and coevolution data.

## 1. **AlphaFold Structure Prediction**
   - Go to [AlphaFold Colab Notebook](https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/AlphaFold2.ipynb).
   - Input your sequence(s) in the provided input box. For complexes, separate sequences with a colon `:`.
   - Default settings are usually sufficient. Optionally, use the relaxation option.
   - Ensure you're using a T4 GPU for faster processing.
   - After completion, download the results and extract the desired `.pdb` file.

## 2. **Coevolution Analysis**
   - Go to [Categorical Jacobian gLM2 Colab Notebook](https://colab.research.google.com/github/sokrypton/ColabBio/blob/main/categorical_jacobian/gLM2.ipynb).
   - For multimers, separate each chain into its own input. For homomers, input the sequence once.
   - Add a code cell with the following command to save the results as a CSV:
     ```python
     sub_df.to_csv("coevolution.csv")
     ```
   - Download the `coevolution.csv` file.

## 3. **Interface Summary Generation**
   - Open the `create_interface_summary.py` script.
   - Insert the file path to your `.pdb` file in the script.
   - This script will:
     - Identify interfaces using a 5 Ångström cutoff by default.
     - Cluster the interfaces using K-means clustering.
     - Generate a summary file in the format: `Chain id, cluster id, residue position`.

## 4. **Visualization and Analysis**
   - Open the `Analyse.ipynb` notebook.
   - Insert the file paths to your interface summary CSV and coevolution CSV.
   - The notebook will visualize the data for further analysis!

🎉 You're done! Now you can analyze the protein structure and coevolution data visually.

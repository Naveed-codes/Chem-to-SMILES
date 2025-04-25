#!/usr/bin/env python
"""
Chemical Name to SMILES Converter

This script converts chemical names to SMILES notation using PubChemPy and RDKit.
"""

import sys
import argparse
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit import RDLogger

# Suppress RDKit warnings
RDLogger.DisableLog('rdApp.*')

def name_to_smiles(chemical_name):
    """
    Convert a chemical name to SMILES notation.
    
    Args:
        chemical_name (str): The chemical name to convert
        
    Returns:
        str: SMILES notation if successful, None otherwise
    """
    try:
        # Check if input is already a SMILES string
        mol = Chem.MolFromSmiles(chemical_name)
        if mol is not None:
            return chemical_name
        
        # Try with PubChem (requires internet connection)
        try:
            from pubchempy import get_compounds
            compounds = get_compounds(chemical_name, 'name')
            if compounds:
                return compounds[0].canonical_smiles
            else:
                print(f"No compounds found for '{chemical_name}' in PubChem")
        except ImportError:
            print("PubChemPy not installed. Installing it with: pip install pubchempy")
            try:
                import subprocess
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pubchempy"])
                # Try again after installation
                from pubchempy import get_compounds
                compounds = get_compounds(chemical_name, 'name')
                if compounds:
                    return compounds[0].canonical_smiles
            except Exception as e:
                print(f"Failed to install or use PubChemPy: {e}")
        except Exception as e:
            print(f"PubChem lookup failed: {e}")
        
        return None
    except Exception as e:
        print(f"Error processing {chemical_name}: {e}")
        return None

def save_molecule_image(smiles, output_file):
    """
    Generate and save a 2D structure image of the molecule.
    
    Args:
        smiles (str): SMILES notation of the molecule
        output_file (str): Path to save the image
    """
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            img = Draw.MolToImage(mol, size=(400, 400))
            img.save(output_file)
            print(f"Molecular structure saved to {output_file}")
        else:
            print("Could not generate molecular structure image")
    except Exception as e:
        print(f"Error generating image: {e}")

def main():
    parser = argparse.ArgumentParser(description='Convert chemical names to SMILES notation')
    parser.add_argument('input', nargs='?', help='Chemical name or path to a file with one name per line')
    parser.add_argument('-o', '--output', help='Output file for results (default: stdout)')
    parser.add_argument('-i', '--image', help='Generate and save molecular structure image')
    parser.add_argument('-b', '--batch', action='store_true', help='Process input as a file with one name per line')
    
    args = parser.parse_args()
    
    if not args.input:
        # Interactive mode
        print("Enter chemical names (Ctrl+D or Ctrl+Z to exit):")
        try:
            for line in sys.stdin:
                name = line.strip()
                if not name:
                    continue
                smiles = name_to_smiles(name)
                if smiles:
                    print(f"{name} → {smiles}")
                else:
                    print(f"Could not convert: {name}")
        except KeyboardInterrupt:
            pass
        return
    
    if args.batch:
        try:
            results = []
            with open(args.input, 'r') as f:
                for line in f:
                    name = line.strip()
                    if not name:
                        continue
                    smiles = name_to_smiles(name)
                    results.append((name, smiles))
            
            # Output results
            if args.output:
                with open(args.output, 'w') as f:
                    for name, smiles in results:
                        if smiles:
                            f.write(f"{name}\t{smiles}\n")
                        else:
                            f.write(f"{name}\tNOT_FOUND\n")
                print(f"Results written to {args.output}")
            else:
                for name, smiles in results:
                    if smiles:
                        print(f"{name} → {smiles}")
                    else:
                        print(f"Could not convert: {name}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        # Single name mode
        smiles = name_to_smiles(args.input)
        if smiles:
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(smiles + '\n')
                print(f"SMILES written to {args.output}")
            else:
                print(smiles)
                
            if args.image:
                save_molecule_image(smiles, args.image)
        else:
            print(f"Could not convert: {args.input}")

if __name__ == "__main__":
    main()
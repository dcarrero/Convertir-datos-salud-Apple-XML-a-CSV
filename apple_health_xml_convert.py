#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Apple Health XML to CSV
==============================
:File: convert.py
:Description: Convertir datos de salud de Apple de XML a CSV
:Version: 0.0.2
:Created: 2019-10-04
:Updated: 2023-10-29
:Authors: Jason Meno (jam)
:Translate Spanish: David Carrero (dcarrero)
:Dependencies: Un archivo export.xml de Apple Health
:License: BSD-2-Clause
"""

# %% Imports
import os
import pandas as pd
import xml.etree.ElementTree as ET
import datetime as dt
import sys


# %% Function Definitions

def preprocess_to_temp_file(file_path):
    """
    El archivo export.xml es donde están todos tus datos, pero Apple Health Export tiene
    dos problemas principales que dificultan su análisis: 
    1. La sintaxis de marcado DTD es exportada incorrectamente por Apple Health para algunos tipos de datos.
    2. Al carácter invisible \x0b (a veces representado como U+000b) le gusta destruir árboles. ¡Piensa en los árboles!

    Sabiendo esto, podemos salvar los árboles y pre-procesar los datos XML para evitar la destrucción y ParseErrors.
    """

    print("Preprocesamiento y escritura en archivo temporal...", end="")
    sys.stdout.flush()

    temp_file_path = "temp_preprocessed_export.xml"
    with open(file_path, 'r') as infile, open(temp_file_path, 'w') as outfile:
        skip_dtd = False
        for line in infile:
            if '<!DOCTYPE' in line:
                skip_dtd = True
            if not skip_dtd:
                line = strip_invisible_character(line)
                outfile.write(line)
            if ']>' in line:
                skip_dtd = False

    print("done!")
    return temp_file_path

def strip_invisible_character(line):
    return line.replace("\x0b", "")


def xml_to_csv(file_path):
    """Recorre el árbol de elementos, recupera todos los objetos y, a continuación
       combinarlos en un marco de datos
    """

    print("Convirtiendo Fichero XML a CSV...", end="")
    sys.stdout.flush()

    attribute_list = []

    for event, elem in ET.iterparse(file_path, events=('end',)):
        if event == 'end':
            child_attrib = elem.attrib
            for metadata_entry in list(elem):
                metadata_values = list(metadata_entry.attrib.values())
                if len(metadata_values) == 2:
                    metadata_dict = {metadata_values[0]: metadata_values[1]}
                    child_attrib.update(metadata_dict)
            attribute_list.append(child_attrib)

            # Clear the element from memory to avoid excessive memory consumption
            elem.clear()

    health_df = pd.DataFrame(attribute_list)

    # Every health data type and some columns have a long identifer
    # Removing these for readability
    health_df.type = health_df.type.str.replace('HKQuantityTypeIdentifier', "")
    health_df.type = health_df.type.str.replace('HKCategoryTypeIdentifier', "")
    health_df.columns = \
        health_df.columns.str.replace("HKCharacteristicTypeIdentifier", "")

    # Reorder some of the columns for easier visual data review
    original_cols = list(health_df)
    shifted_cols = ['type',
                    'sourceName',
                    'value',
                    'unit',
                    'startDate',
                    'endDate',
                    'creationDate']

    # Add loop specific column ordering if metadata entries exist
    if 'com.loopkit.InsulinKit.MetadataKeyProgrammedTempBasalRate' in original_cols:
        shifted_cols.append(
            'com.loopkit.InsulinKit.MetadataKeyProgrammedTempBasalRate')

    if 'com.loopkit.InsulinKit.MetadataKeyScheduledBasalRate' in original_cols:
        shifted_cols.append(
            'com.loopkit.InsulinKit.MetadataKeyScheduledBasalRate')

    if 'com.loudnate.CarbKit.HKMetadataKey.AbsorptionTimeMinutes' in original_cols:
        shifted_cols.append(
            'com.loudnate.CarbKit.HKMetadataKey.AbsorptionTimeMinutes')

    remaining_cols = list(set(original_cols) - set(shifted_cols))
    reordered_cols = shifted_cols + remaining_cols
    health_df = health_df.reindex(labels=reordered_cols, axis='columns')

    # Sort by newest data first
    health_df.sort_values(by='startDate', ascending=False, inplace=True)

    print("done!")

    return health_df


def save_to_csv(health_df):
    print("Guardando Fichero CSV...", end="")
    sys.stdout.flush()

    today = dt.datetime.now().strftime('%Y-%m-%d')
    health_df.to_csv("apple_health_export_" + today + ".csv", index=False)
    print("¡hecho!")

    return

def remove_temp_file(temp_file_path):
    print("Eliminando el fichero temporal...", end="")
    os.remove(temp_file_path)
    print("¡hecho!")
    
    return

def main():
    file_path = "export.xml"
    temp_file_path = preprocess_to_temp_file(file_path)
    health_df = xml_to_csv(temp_file_path)
    save_to_csv(health_df)
    remove_temp_file(temp_file_path)

    return


# %%
if __name__ == '__main__':
    main()

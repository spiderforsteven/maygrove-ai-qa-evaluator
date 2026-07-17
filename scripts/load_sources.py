#!/usr/bin/env python3
"""
Load and index source documents for the MayGrove QA evaluation pipeline.

This module parses:
- Maygrove.md (app requirements) into sections
- V30 manual into sections
- Seed library Excel into structured JSON

Output is a Python dictionary that can be passed to the fact extraction agents.
"""

import json
import re
from pathlib import Path

import pandas as pd


SEED_COLS = {
    '分类\nCategory': 'category',
    '分类\n（固件参数）': 'planttype',
    '是否是爬藤\n（固件参数）': 'is_climbing',
    'planttype': 'planttype_raw',
    'app用品种名称\nplantShowName': 'app_name',
    '具体品种\nplantScientificName': 'variety_name',
    '植物ID\n（固件参数）': 'plant_id',
    '是否有机': 'organic',
    'Germination\n（天）': 'germination_days',
    'Seedling\n（天）': 'seedling_days',
    '育苗期\n（固件参数）': 'seedling_days_fixed',
    'Vegetative\n（天）\n爬藤植物安装爬藤架': 'vegetative_days',
    'Flower/Fruit\n（天）': 'flower_fruit_days',
    'harvest/maturity\n（天）': 'harvest_days',
    '温度范围（℉）': 'temp_range_f',
    'harvest_type': 'harvest_type',
    '描述': 'description',
    '链接': 'url',
    '种子供应商SKU': 'sku',
    '备注': 'notes',
    '播种机针头颜色': 'needle_color',
    '首批发货种子挑选': 'first_batch',
}


def clean_cell(x):
    return '' if pd.isna(x) else str(x).strip()


def split_markdown_by_headers(text, level=2):
    """Split markdown into sections by H2 or H3 headers."""
    header = '#' * level
    # Split by lines that start with the header marker
    lines = text.splitlines()
    sections = []
    current_title = 'Introduction'
    current_body = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(header + ' '):
            if current_body:
                sections.append({
                    'title': current_title,
                    'body': '\n'.join(current_body).strip()
                })
            current_title = stripped.strip()
            current_body = []
        else:
            current_body.append(line)
    if current_body:
        sections.append({
            'title': current_title,
            'body': '\n'.join(current_body).strip()
        })
    return sections


def load_markdown(path: Path, level=2):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return {
        'source_file': path.name,
        'sections': split_markdown_by_headers(text, level=level)
    }


def load_seed_library(path: Path):
    xl = pd.ExcelFile(path)
    df = pd.read_excel(xl, sheet_name='Sheet1')
    df = df.rename(columns=SEED_COLS)
    for col in df.columns:
        df[col] = df[col].apply(clean_cell)

    records = []
    for _, row in df.iterrows():
        if not row['app_name'] or row['app_name'] == 'nan':
            continue
        records.append({
            'category': row['category'],
            'planttype': row['planttype'],
            'is_climbing': row['is_climbing'] == 'Y',
            'app_name': row['app_name'],
            'variety_name': row['variety_name'],
            'plant_id': row['plant_id'],
            'organic': row['organic'] == 'Yes',
            'germination_days': row['germination_days'] if row['germination_days'] != '/' else '',
            'seedling_days': row['seedling_days'] if row['seedling_days'] != '/' else '',
            'vegetative_days': row['vegetative_days'] if row['vegetative_days'] != '/' else '',
            'flower_fruit_days': row['flower_fruit_days'] if row['flower_fruit_days'] != '/' else '',
            'harvest_days': row['harvest_days'] if row['harvest_days'] != '/' else '',
            'temp_range_f': row['temp_range_f'],
            'harvest_type': row['harvest_type'],
            'description': row['description'],
            'sku': row['sku'],
            'notes': row['notes'],
            'needle_color': row['needle_color'],
            'first_batch': row['first_batch'] == '✓',
        })
    return records


def load_nutrition(path: Path):
    df = pd.read_excel(path, sheet_name='种子营养成份整理模版')
    for col in df.columns:
        df[col] = df[col].apply(clean_cell)
    records = []
    for _, row in df.iterrows():
        name = row['Name'].strip()
        if not name or name == 'Name':
            continue
        rec = {'name': name}
        for col in df.columns:
            if col == 'Name':
                continue
            key = col.replace(' (', '_').replace(')', '').replace(' ', '_').replace('µg', 'mcg').replace('/', '_per_')
            val = row[col]
            try:
                rec[key] = float(val)
            except ValueError:
                rec[key] = val
        records.append(rec)
    return records


def load_planting_tips(path: Path):
    df = pd.read_excel(path, sheet_name='种植Tips整理模版')
    for col in df.columns:
        df[col] = df[col].apply(clean_cell)
    records = []
    for _, row in df.iterrows():
        records.append({
            'category': row['Catergory'],
            'germination_tips': row['Germination阶段说明和Tips'],
            'seedling_tips': row['Seedling阶段说明和Tips'],
            'vegetative_tips': row['Vegetative阶段说明和Tips'],
            'harvest_tips': row['Harvest阶段说明和Tips'],
            'recommended_ec': row['Recommended EC'],
            'recommended_ph': row['Recommended pH'],
            'ppfd': row['PPFD'],
            'light_hours': row['Light Hour'],
            'example_plants': row['Example Plants'],
            'difficulty': row['难易度'],
        })
    return records


def load_sources(maygrove_md: Path, v30_manual: Path, seed_library: Path):
    return {
        'maygrove_md': load_markdown(maygrove_md, level=4),
        'v30_manual': load_markdown(v30_manual, level=2),
        'seed_library': load_seed_library(seed_library),
        'nutrition': load_nutrition(seed_library),
        'planting_tips': load_planting_tips(seed_library),
    }


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--maygrove-md', type=Path, required=True)
    parser.add_argument('--v30-manual', type=Path, required=True)
    parser.add_argument('--seed-library', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()

    sources = load_sources(args.maygrove_md, args.v30_manual, args.seed_library)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(sources, f, ensure_ascii=False, indent=2)
    print(f"Loaded sources to {args.output}")
    print(f"  Maygrove.md sections: {len(sources['maygrove_md']['sections'])}")
    print(f"  V30 manual sections: {len(sources['v30_manual']['sections'])}")
    print(f"  Seed varieties: {len(sources['seed_library'])}")
    print(f"  Nutrition records: {len(sources['nutrition'])}")
    print(f"  Planting tip categories: {len(sources['planting_tips'])}")

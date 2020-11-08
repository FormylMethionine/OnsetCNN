#!/bin/bash

rm dataset_ddr/*
python parser.py
python analyze_audio.py

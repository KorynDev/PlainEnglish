#!/usr/bin/env bash
set -e

echo "========================================="
echo "PlainEnglish Test Suite v1.0"
echo "========================================="

echo "Running Math Demo..."
python3 plainenglish.py examples/math_demo.ple

echo ""
echo "Running Advanced Utilities Demo..."
python3 plainenglish.py examples/advanced_utilities_demo.ple

echo ""
echo "Running Demo..."
python3 plainenglish.py examples/demo.ple

echo ""
echo "Running Factorial..."
python3 plainenglish.py examples/factorial.ple

echo ""
echo "========================================="
echo "ALL TESTS PASSED SUCCESSFULLY!"
echo "========================================="

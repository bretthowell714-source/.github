#!/bin/bash
# Run comprehensive tests for Meta-Skill Engine

echo "=================================================="
echo "Meta-Skill Engine - Comprehensive Test Suite"
echo "=================================================="
echo ""
echo "This test suite will prove that:"
echo "  1. Skills are actually embedded"
echo "  2. Knowledge is persisted to disk"
echo "  3. Tool usage is tracked"
echo "  4. Patterns are learned"
echo "  5. Skills auto-update"
echo "  6. Conversation history is recorded"
echo "  7. Full system export/import works"
echo "  8. Recommendations are intelligent"
echo ""
echo "Starting tests..."
echo ""

cd "$(dirname "$0")"

# Install dependencies if needed
if ! python3 -c "import yaml" 2>/dev/null; then
    echo "Installing dependencies..."
    pip3 install pyyaml requests > /dev/null 2>&1
fi

# Run the tests
python3 test_meta_skill_engine.py

exit_code=$?

echo ""
echo "=================================================="
if [ $exit_code -eq 0 ]; then
    echo "✓ ALL TESTS COMPLETED"
else
    echo "✗ TESTS FAILED (exit code: $exit_code)"
fi
echo "=================================================="

exit $exit_code

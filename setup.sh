#!/bin/bash
# Setup script for TrueFalse game

set -e  # Exit on any error

echo "🎮 TrueFalse Game Setup"
echo "======================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Found Python $python_version"

required_version="3.13"
if [[ $(echo "$python_version < $required_version" | bc) -eq 1 ]]; then
    echo "✗ Python 3.13+ required (found $python_version)"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "✓ Creating virtual environment..."
    python3 -m venv .venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "✓ Installing dependencies..."
pip install -q --upgrade pip setuptools wheel
pip install -q colorama

# Install dev dependencies (optional)
read -p "Install dev dependencies (testing, type checking)? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "✓ Installing dev dependencies..."
    pip install -q -e ".[dev]"
fi

# Initialize database
echo "✓ Initializing database..."
python3 << EOF
from db import create_sqlite_database, setup_database
from const import DB_NAME

try:
    conn = create_sqlite_database(DB_NAME)
    setup_database(conn)
    print("  Database initialized successfully")
    conn.close()
except Exception as e:
    print(f"  Warning: Could not initialize database: {e}")
    print("  It will be created automatically on first run")
EOF

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "  1. Activate the environment: source .venv/bin/activate"
echo "  2. Start playing: python main.py"
echo ""
echo "📚 Documentation:"
echo "  - README.md - Overview and quick start"
echo "  - docs/USER_GUIDE.md - How to play"
echo "  - docs/DEVELOPER_GUIDE.md - Development setup"
echo ""

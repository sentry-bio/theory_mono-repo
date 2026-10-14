#!/bin/bash
# Environment check on biosphereatlas for PREREG23 (read-only; touches nothing).
echo "== tools"; which iqtree2 iqtree FastTree fasttree raxml-ng python3 pip3 conda 2>/dev/null
python3 --version
echo "== python modules"; python3 - <<'EOF'
for m in ("numpy", "scipy", "dendropy", "ete3", "Bio"):
    try:
        mod = __import__(m); print(m, getattr(mod, "__version__", "ok"))
    except Exception as e:
        print(m, "MISSING")
EOF
echo "== disk"; df -h /fast | tail -1
echo "== cpu/mem"; nproc; free -g | head -2
echo "== scratch dirs"; ls -d /fast/scratch* 2>/dev/null

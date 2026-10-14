#!/bin/bash
# PREREG23b staging on biosphereatlas: ONE scratch directory, nothing else touched. Run under nice.
set -u
S=/fast/scratch_h23b
mkdir -p "$S/bin" "$S/data" "$S/work" "$S/logs"
cd "$S" || exit 1
echo "== $(date '+%Y-%m-%d %H:%M:%S %Z') setup start; arch $(uname -m); python $(python3 --version)"
# venv with numpy + biopython (pip cache kept inside the scratch dir)
export PIP_CACHE_DIR="$S/pipcache" XDG_CACHE_HOME="$S/xdgcache"
if [ ! -x "$S/venv/bin/python" ]; then
  python3 -m venv "$S/venv" 2>&1 | tail -2
fi
nice "$S/venv/bin/pip" install --quiet --upgrade pip 2>&1 | tail -1
nice "$S/venv/bin/pip" install --quiet numpy biopython 2>&1 | tail -2
"$S/venv/bin/python" -c "import numpy, Bio; print('numpy', numpy.__version__, 'biopython', Bio.__version__)"
# IQ-TREE 2.4.0 Linux
cd "$S/bin"
case "$(uname -m)" in
  x86_64) IQ=iqtree-2.4.0-Linux-intel ;;
  aarch64|arm64) IQ=iqtree-2.4.0-Linux-arm ;;
  *) echo "unknown arch"; exit 1 ;;
esac
if [ ! -x "$S/bin/$IQ/bin/iqtree2" ]; then
  curl -sL -m 600 -o "$IQ.tar.gz" "https://github.com/iqtree/iqtree2/releases/download/v2.4.0/$IQ.tar.gz" && tar xzf "$IQ.tar.gz"
fi
sha256sum "$IQ.tar.gz"
"$S/bin/$IQ/bin/iqtree2" --version 2>&1 | head -1
ln -sf "$S/bin/$IQ/bin/iqtree2" "$S/bin/iqtree2"
# MAFFT 7.526 Linux (portable package)
if [ ! -x "$S/bin/mafft-linux64/mafft.bat" ]; then
  curl -sL -m 600 -o mafft-7.526-linux.tgz https://mafft.cbrc.jp/alignment/software/mafft-7.526-linux.tgz && tar xzf mafft-7.526-linux.tgz
fi
sha256sum mafft-7.526-linux.tgz
"$S/bin/mafft-linux64/mafft.bat" --version 2>&1 | head -1
echo "== $(date '+%Y-%m-%d %H:%M:%S %Z') setup done"; du -sh "$S"

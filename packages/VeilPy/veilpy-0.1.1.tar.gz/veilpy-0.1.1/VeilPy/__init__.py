from collections import Counter
from distutils.core import setup
from Cython.Build import cythonize
from os import system as pyb
import inflect
import codecs as cd
import gzip as gz
import os
import re
import shutil
import time as tm
import base64 as b64
import marshal as ms
import zlib as zb

def da(code):
   try:
       result = os.popen(f"uncompyle6 {code}").read()
       return result
   except Exception as e:
       return f"E: {e}"

def dn(code):
    try:
        result = os.popen(f"nm {code}").read()
        return result
    except Exception as e:
        return f"E: {e}"
        
def du(code):
    try:
        result = os.popen(f"strings {code} | sort").read()
        return result
    except Exception as e:
        return f"E: {e}"
          
def dl(fp):
    try:
        with os.popen(f"tac {fp}") as o:
            result = o.read()
        return result
    except Exception as e:
        return f"E: {e}"
  
def dt(fp):
    try:
        with os.popen(f"cat -n {fp}") as o:
            result = o.read()
        return result
    except Exception as e:
        return f"E: {e}"
     
def hellopy(text):
    font = {
        'A': [' *** ', '*   *', '*****', '*   *', '*   *'],
        'B': ['**** ', '*   *', '**** ', '*   *', '**** '],
        'C': [' ****', '*    ', '*    ', '*    ', ' ****'],
        'D': ['**** ', '*   *', '*   *', '*   *', '**** '],
        'E': ['*****', '*    ', '*****', '*    ', '*****'],
        'F': ['*****', '*    ', '*****', '*    ', '*    '],
        'G': [' ****', '*    ', '*  **', '*   *', ' ****'],
        'H': ['*   *', '*   *', '*****', '*   *', '*   *'],
        'I': ['*****', '  *  ', '  *  ', '  *  ', '*****'],
        'J': ['*****', '    *', '    *', '*   *', ' *** '],
        'K': ['*   *', '*  * ', '* *  ', '**   ', '* *  '],
        'L': ['*    ', '*    ', '*    ', '*    ', '*****'],
        'M': ['*   *', '** **', '* * *', '*   *', '*   *'],
        'N': ['*   *', '**  *', '* * *', '*  **', '*   *'],
        'O': [' *** ', '*   *', '*   *', '*   *', ' *** '],
        'P': ['**** ', '*   *', '**** ', '*    ', '*    '],
        'Q': [' *** ', '*   *', '*   *', '*  **', ' ** *'],
        'R': ['**** ', '*   *', '**** ', '* *  ', '*  * '],
        'S': [' ****', '*    ', '**** ', '    *', '**** '],
        'T': ['*****', '  *  ', '  *  ', '  *  ', '  *  '],
        'U': ['*   *', '*   *', '*   *', '*   *', ' *** '],
        'V': ['*   *', '*   *', '*   *', ' * * ', '  *  '],
        'W': ['*   *', '*   *', '* * *', '** **', '*   *'],
        'X': ['*   *', ' * * ', '  *  ', ' * * ', '*   *'],
        'Y': ['*   *', ' * * ', '  *  ', '  *  ', '  *  '],
        'Z': ['*****', '   * ', '  *  ', ' *   ', '*****'],
        ' ': ['     ', '     ', '     ', '     ', '     '],
    }
    result = [''] * 5
    for char in text.upper():
        if char in font:
            for i in range(5):
                result[i] += font[char][i] + ' '
    return '\n'.join(result)

def hk(code):
    c = code.encode("utf-8")
    c = [b for b in c]
    return f"#Tele: @ash_team and @musbllbot\nfa={c}\nexec(bytes(fa).decode())"

def hx(code):
    enc = code.encode().hex()
    return "#Tele : @ash_team\nexec(bytes.fromhex('" + enc + "'))"

def r13(code):
    enc = cd.encode(code, 'rot_13')
    return f"#Tele : @ash_team\nimport codecs;exec(codecs.decode({repr(enc)}, 'rot_13'))"

def lb(code):
    compil = zb.compress(code.encode('utf-8'))
    return "#Tele : @ash_team\nimport zlib;exec(zlib.decompress(" + repr(compil) + ").decode())"

def zb_enc(code):
    compil = zb.compress(code.encode('utf-8'))
    enc = b64.b64encode(compil).decode()
    return "#Tele : @ash_team\nimport zlib\nimport base64\nexec(zlib.decompress(base64.b64decode('" + enc + "')).decode())"

def gz_enc(code):
    compil = gz.compress(code.encode())
    enc = b64.b64encode(compil).decode()
    return "#Tele : @ash_team\nimport gzip\nimport base64\nexec(gzip.decompress(base64.b64decode('" + enc + "')).decode())"

def ms_enc(code):
    co = compile(code, '<string>', 'exec')
    encrypted = b64.b64encode(ms.dumps(co))
    return "#Tele : @ash_team\nimport marshal\nimport base64\nexec(marshal.loads(base64.b64decode('" + encrypted.decode() + "')))"

def mz_enc(code):
    co = compile(code, "<string>", 'exec')
    mars = ms.dumps(co)
    compil = zb.compress(mars)
    return "#Tele : @ash_team\nimport zlib;import marshal;exec(marshal.loads(zlib.decompress(" + repr(compil) + ")))"

def b6(code):
    enc = b64.b64encode(code.encode()).decode()
    return "#Tele : @ash_team\nimport base64;exec(base64.b64decode('" + enc + "'))"

def b3(code):
    enc = b64.b32encode(code.encode()).decode()
    return "#Tele : @ash_team\nimport base64;exec(base64.b32decode('" + enc + "'))"

def hel(text):
    return text[::-1]

def nw(n):
    p = inflect.engine()
    return p.number_to_words(n)

def kl(code):
    return re.sub(r'#.*', '', code).strip()

def v(p):
    try:
        with open(p, 'r', encoding='utf-8') as f:
            l, w, c = 0, 0, Counter()
            for line in f:
                l += 1
                line = re.sub(r'[^\w\s]', '', line).lower()
                words = line.split()
                w += len(words)
                c.update(words)
            result = [
                'Tele : @ash_team',
                f"عدد الاسطر: {l}",
                f"عدد الكلمات: {w}",
                "الكلمات الاكثر تكرار:",
            ]
            result.extend(f"- {word}: {count}" for word, count in c.most_common(10))
            return "\n".join(result)
    except FileNotFoundError:
        pass
    except Exception as e:
        return f"{e}"

def py2so(p):
    try:
        pyx = p.replace(".py", ".pyx")
        with open(pyx, 'w') as f, open(p, 'r') as pyf:
            f.write(pyf.read())
        setup_code = f"""
from distutils.core import setup
from Cython.Build import cythonize
setup(ext_modules = cythonize("{pyx}"))
"""
        with open("temp_setup.py", "w") as sf:
            sf.write(setup_code)
        pyb("python temp_setup.py build_ext --inplace")
    finally:
        if os.path.exists("temp_setup.py"):
            os.remove("temp_setup.py")
        if os.path.exists("build"):
            shutil.rmtree("build", ignore_errors=True)
        if os.path.exists(pyx):
            os.remove(pyx)